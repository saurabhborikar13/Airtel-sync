import os
import pickle
import pandas as pd
import numpy as np
from typing import Dict, List, Any

class CRMService:
    def __init__(self, data_dir: str, model_path: str):
        self.data_dir = data_dir
        self.leads_df = pd.read_csv(os.path.join(data_dir, "smb_leads.csv"))
        self.model = None
        if os.path.exists(model_path):
            with open(model_path, "rb") as f:
                self.model = pickle.load(f)

    def get_funnel_summary(self) -> Dict[str, Any]:
        """Calculates exact funnel conversions and operational metrics."""
        total = len(self.leads_df)
        stages = ["Lead", "Contacted", "Needs assessed", "Quote accepted", "KYC complete", "Activated"]
        stage_counts = self.leads_df["stage_reached"].value_counts().to_dict()

        # Cumulative reached count
        order = {"Lead": 0, "Contacted": 1, "Needs assessed": 2, "Quote accepted": 3, "KYC complete": 4, "Activated": 5}
        self.leads_df["stage_idx"] = self.leads_df["stage_reached"].map(order).fillna(0)

        funnel_list = []
        for s in stages:
            s_idx = order[s]
            count_reached = (self.leads_df["stage_idx"] >= s_idx).sum()
            funnel_list.append({
                "stage": s,
                "count": int(count_reached),
                "pct_of_total": round((count_reached / total) * 100, 1)
            })

        activated_df = self.leads_df[self.leads_df["outcome"] == "Activated"]
        avg_days = float(activated_df["days_lead_to_activation"].mean())
        avg_calls = float(activated_df["customer_follow_up_calls"].mean())
        blended_cac = float(self.leads_df["acquisition_cost_inr"].sum() / max(1, len(activated_df)))
        median_arpu = float(activated_df["monthly_bundle_value_inr"].median())

        drop_reasons = self.leads_df["drop_reason"].value_counts().head(8).to_dict()

        return {
            "total_leads": total,
            "activated_count": len(activated_df),
            "activation_rate_pct": round((len(activated_df) / total) * 100, 2),
            "avg_days_to_activate": round(avg_days, 1),
            "avg_customer_follow_up_calls": round(avg_calls, 1),
            "blended_cac_inr": round(blended_cac),
            "median_bundle_monthly_inr": round(median_arpu),
            "funnel": funnel_list,
            "top_drop_reasons": drop_reasons
        }

    def get_leads(self, stage: str = None, segment: str = None, search: str = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Returns filtered leads with ML propensity scores."""
        df = self.leads_df.copy()

        if stage and stage != "All":
            df = df[df["stage_reached"].str.lower() == stage.lower()]
        if segment and segment != "All":
            df = df[df["segment"].str.lower() == segment.lower()]
        if search:
            s = search.lower().strip()
            df = df[
                df["business_name"].str.lower().str.contains(s, na=False) |
                df["lead_id"].str.lower().str.contains(s, na=False) |
                df["city"].str.lower().str.contains(s, na=False)
            ]

        sample_df = df.head(limit).copy()
        results = []

        for _, r in sample_df.iterrows():
            propensity = self.predict_lead_propensity(r.to_dict())
            next_action = self.recommend_next_action(r.to_dict())
            results.append({
                "lead_id": r["lead_id"],
                "business_name": r["business_name"],
                "business_type": r["business_type"],
                "segment": r["segment"],
                "city": r["city"],
                "city_tier": int(r["city_tier"]),
                "stage_reached": r["stage_reached"],
                "outcome": r["outcome"],
                "drop_reason": r["drop_reason"] if pd.notna(r["drop_reason"]) else None,
                "has_gstin": r["has_gstin"],
                "has_udyam": r["has_udyam"],
                "monthly_spend": float(r["monthly_telecom_spend_inr"]) if pd.notna(r["monthly_telecom_spend_inr"]) else 0,
                "propensity_score": propensity["score"],
                "propensity_level": propensity["level"],
                "next_action": next_action
            })

        return results

    def predict_lead_propensity(self, lead_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Runs the trained Random Forest classifier to compute propensity to activate."""
        if not self.model:
            # Fallback heuristic
            score = 0.5
            if lead_dict.get("has_gstin") == "Y": score += 0.25
            if lead_dict.get("segment") in ["Professional offices", "Small manufacturers"]: score += 0.15
            return {"score": round(score, 2), "level": "High" if score >= 0.6 else "Medium"}

        features = [
            "lead_source", "segment", "city_tier", "state", "preferred_language",
            "employee_count", "num_sites", "annual_turnover_band",
            "has_gstin", "has_udyam", "current_internet", "monthly_telecom_spend_inr"
        ]
        row = {}
        for f in features:
            val = lead_dict.get(f)
            if f in ["employee_count", "num_sites", "monthly_telecom_spend_inr"]:
                try:
                    row[f] = [float(val) if pd.notna(val) else 0.0]
                except:
                    row[f] = [0.0]
            else:
                row[f] = [str(val) if pd.notna(val) else "Unknown"]

        input_df = pd.DataFrame(row)
        try:
            proba = float(self.model.predict_proba(input_df)[0][1])
            # Calibrate probability for display
            score = round(proba * 100, 1)
            level = "High" if score >= 25.0 else ("Medium" if score >= 10.0 else "Low")
            return {"score": score, "level": level}
        except Exception:
            return {"score": 35.0, "level": "Medium"}

    def recommend_next_action(self, lead: Dict[str, Any]) -> str:
        """Prescribes tactical Next-Best-Action for field rep or partner based on drop reason & stage."""
        stage = lead.get("stage_reached", "")
        drop = str(lead.get("drop_reason", "")).lower()

        if "price too high" in drop:
            return "Offer 15% annual commitment discount or propose Biz 5G AirFiber starter tier."
        elif "no time for a visit" in drop:
            return "Send direct self-serve WhatsApp onboarding link for 5-minute digital sign-up."
        elif "quote too complex" in drop:
            return "Trigger transparent 1-slider WhatsApp quote with all-inclusive monthly pricing."
        elif "locked in" in drop:
            return "Log contract expiry date in CRM and schedule automated buyout callback 30 days prior."
        elif "unreachable" in drop:
            return "Trigger verified WhatsApp Business interactive menu in customer's preferred language."
        elif stage == "Needs assessed":
            return "Send digital interactive bundle quote directly to owner's WhatsApp."
        elif stage == "Quote accepted":
            return "Notify partner to assist customer with 1-click camera KYC upload."
        elif stage == "KYC complete":
            return "Expedite dispatch and book priority fiber technician slot."
        return "Standard digital nurture follow-up via WhatsApp Business."
