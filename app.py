import os
import sys
import json
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template, send_file, send_from_directory
from flask_cors import CORS

from services.advisor_engine import AdvisorEngine
from services.kyc_validator import SmartKYCValidator, SPECIMEN_METADATA
from services.crm_service import CRMService
from services.presentation_gen import create_business_case_deck

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_PATH = os.path.join(BASE_DIR, "models", "propensity_model.pkl")

advisor = AdvisorEngine(DATA_DIR)
kyc_validator = SmartKYCValidator(DATA_DIR)
crm = CRMService(DATA_DIR, MODEL_PATH)

# In-memory orders store for tracking
ORDERS_DB = {}

@app.route("/")
def index():
    return render_template("index.html")

# ==========================================
# ADVISOR APIS
# ==========================================
@app.route("/api/advisor/chat", methods=["POST"])
def advisor_chat():
    data = request.json or {}
    message = data.get("message", "")
    context = data.get("context", {})
    result = advisor.chat_response(message, context)
    # Normalize: frontend expects "response" key, advisor returns "reply"
    if "reply" in result and "response" not in result:
        result["response"] = result.pop("reply")
    # Also surface bundle data at top-level for the frontend
    if "recommendation" in result:
        rec = result["recommendation"]
        pb = rec.get("primary_bundle", {})
        result["bundle"] = {
            "bundle_title": rec.get("bundle_title", ""),
            "total_monthly_with_gst": pb.get("total_monthly_with_gst", 0),
            "products": [{"name": p["name"], "product_name": p["name"]} for p in pb.get("products", [])],
            "setup_fee_inr": pb.get("setup_fee_inr", 0),
        }
    return jsonify(result)

@app.route("/api/advisor/recommend", methods=["POST"])
def advisor_recommend():
    profile = request.json or {}
    bundle = advisor.recommend_bundle(profile)
    return jsonify(bundle)

@app.route("/api/products", methods=["GET"])
def get_products():
    products = advisor.get_all_products()
    clean_products = []
    for raw_p in products:
        p = dict(raw_p)
        p["product_code"] = str(p.get("product_id", ""))
        p["name"] = str(p.get("product_name", ""))
        try:
            p["monthly_inr"] = int(p.get("price_min_inr_per_month", 0))
        except (ValueError, TypeError):
            p["monthly_inr"] = 0
        try:
            p["setup_fee_inr"] = int(p.get("one_time_setup_inr", 0))
        except (ValueError, TypeError):
            p["setup_fee_inr"] = 0
        for k, v in list(p.items()):
            if isinstance(v, float) and (v != v):
                p[k] = ""
            elif v is None:
                p[k] = ""
        clean_products.append(p)
    return jsonify(clean_products)

# ==========================================
# SMART KYC APIS
# ==========================================
@app.route("/api/kyc/specimens", methods=["GET"])
def get_specimens():
    result = []
    for code, meta in SPECIMEN_METADATA.items():
        result.append({
            "code": code,
            "business_name": meta["business_name"],
            "legal_name": meta["legal_name"],
            "constitution": meta["constitution"],
            "known_issues_count": len(meta["issues"]),
            "is_clean": len(meta["issues"]) == 0
        })
    return jsonify(result)

@app.route("/api/kyc/lookup-gstin", methods=["POST"])
def lookup_gstin():
    data = request.json or {}
    gstin = data.get("gstin", "")
    res = kyc_validator.lookup_gstin(gstin)
    return jsonify(res)

@app.route("/api/kyc/lookup-udyam", methods=["POST"])
def lookup_udyam():
    data = request.json or {}
    udyam = data.get("udyam", "")
    res = kyc_validator.lookup_udyam(udyam)
    return jsonify(res)

@app.route("/api/kyc/verify-specimen", methods=["POST"])
def verify_specimen():
    data = request.json or {}
    applicant_code = data.get("applicant_code", "K03")
    result = kyc_validator.verify_specimen(applicant_code)
    return jsonify(result)

# ==========================================
# ORDERS & TRACKER APIS
# ==========================================
@app.route("/api/orders/create", methods=["POST"])
def create_order():
    data = request.json or {}
    order_id = f"AIRTEL-UDYAM-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    install_days = int(data.get("estimated_install_days", 3))
    est_activation = (datetime.now() + timedelta(days=install_days)).strftime("%d %b %Y")

    order_record = {
        "order_id": order_id,
        "business_name": data.get("business_name", "Small Business Enterprise"),
        "contact_phone": SmartKYCValidator.mask_pii(data.get("contact_phone", "9876543210"), "phone"),
        "city": data.get("city", "Bengaluru"),
        "bundle_title": data.get("bundle_title", "Udyam Digital Starter"),
        "monthly_inr": data.get("total_monthly_with_gst", 2227),
        "setup_inr": data.get("setup_fee_inr", 0),
        "contract_months": data.get("contract_months", 12),
        "status": "KYC Verified & Equipment Dispatched",
        "progress_step": 3,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "estimated_activation_date": est_activation,
        "install_days": install_days,
        "milestones": [
            {"step": 1, "title": "Order Placed & Confirmed", "status": "Completed", "time": "Just now", "detail": "Digital bundle configured with zero paper contract"},
            {"step": 2, "title": "Smart KYC & DPDP Verification", "status": "Completed", "time": "Just now", "detail": "Mod-36 checksum, Udyam, & address proof verified"},
            {"step": 3, "title": "SIM & CPE Equipment Dispatched", "status": "In Progress", "time": "Today", "detail": f"Tracking ID: AW-AIRTEL-{order_id[-6:]}"},
            {"step": 4, "title": "Field Engineer Site Installation", "status": "Pending", "time": f"Within {install_days} days", "detail": "Prior appointment scheduled via SMS"},
            {"step": 5, "title": "Service Live & Active", "status": "Pending", "time": est_activation, "detail": "High-speed broadband + billing active"}
        ],
        "notifications": [
            {
                "channel": "WhatsApp",
                "time": "Just now",
                "message": f"🎉 Namaste {data.get('business_name', 'Customer')}! Your Airtel Udyam bundle is booked (Order #{order_id}). Expected activation: {est_activation}. Track live: airtel.in/track/{order_id}"
            },
            {
                "channel": "SMS",
                "time": "Just now",
                "message": f"Airtel Business: Order {order_id} confirmed. KYC verification successful. Technician visit slot scheduled."
            }
        ]
    }
    ORDERS_DB[order_id] = order_record
    return jsonify(order_record)

@app.route("/api/orders/<order_id>", methods=["GET"])
def get_order(order_id):
    order = ORDERS_DB.get(order_id)
    if not order:
        # Generate on-demand default
        order = {
            "order_id": order_id,
            "business_name": "Ganesh Woodcraft",
            "contact_phone": "+91 98XXXXXX89",
            "city": "Nagpur",
            "bundle_title": "Professional Practice Cloud Suite",
            "monthly_inr": 3184,
            "setup_inr": 0,
            "contract_months": 12,
            "status": "Field Engineer Site Visit Scheduled",
            "progress_step": 4,
            "created_at": "Today, 10:30 AM",
            "estimated_activation_date": "Within 48 Hours",
            "install_days": 2,
            "milestones": [
                {"step": 1, "title": "Order Placed & Confirmed", "status": "Completed", "time": "Yesterday", "detail": "Digital bundle selected"},
                {"step": 2, "title": "Smart KYC & DPDP Verification", "status": "Completed", "time": "Yesterday", "detail": "GSTIN & Udyam Verified"},
                {"step": 3, "title": "SIM & CPE Equipment Dispatched", "status": "Completed", "time": "Today, 08:00 AM", "detail": "Out for delivery"},
                {"step": 4, "title": "Field Engineer Site Installation", "status": "In Progress", "time": "Today, 03:00 PM", "detail": "Technician assigned: Ramesh K. (+91 94XXXXXX12)"},
                {"step": 5, "title": "Service Live & Active", "status": "Pending", "time": "Tonight", "detail": "Activation confirmation via WhatsApp"}
            ],
            "notifications": [
                {"channel": "WhatsApp", "time": "08:15 AM", "message": "Your fiber router CPE has been dispatched from Nagpur warehouse."},
                {"channel": "SMS", "time": "10:00 AM", "message": "Engineer Ramesh K. is assigned for site installation today at 3:00 PM."}
            ]
        }
    return jsonify(order)

# ==========================================
# PARTNER CRM & PROPENSITY APIS
# ==========================================
@app.route("/api/crm/funnel", methods=["GET"])
def crm_funnel():
    summary = crm.get_funnel_summary()
    # Normalize for frontend: add "stages", "activated", "kyc_complete", "segments" keys
    funnel_list = summary.get("funnel", [])
    stages_out = [{"stage": f["stage"], "count": f["count"]} for f in funnel_list]
    activated = next((f["count"] for f in funnel_list if f["stage"] == "Activated"), summary.get("activated_count", 0))
    kyc_complete = next((f["count"] for f in funnel_list if f["stage"] == "KYC complete"), 0)
    # Segment distribution from leads
    seg_counts = {}
    try:
        seg_counts = crm.leads_df["segment"].value_counts().head(5).to_dict()
    except Exception:
        pass
    summary["stages"] = stages_out
    summary["activated"] = activated
    summary["kyc_complete"] = kyc_complete
    summary["segments"] = seg_counts
    return jsonify(summary)

@app.route("/api/crm/leads", methods=["GET"])
def crm_leads():
    stage = request.args.get("stage")
    segment = request.args.get("segment")
    search = request.args.get("search")
    limit = int(request.args.get("limit", 100))
    leads = crm.get_leads(stage=stage, segment=segment, search=search, limit=limit)
    # Normalize field names for frontend
    for lead in leads:
        lead["stage"] = lead.pop("stage_reached", lead.get("stage", ""))
        lead["propensity_label"] = lead.pop("propensity_level", lead.get("propensity_label", "Medium"))
        if "industry" not in lead:
            lead["industry"] = lead.get("business_type", "—")
        if "contact_person" not in lead:
            lead["contact_person"] = ""
        if "next_action" not in lead:
            lead["next_action"] = "Follow up"
    return jsonify(leads)

@app.route("/api/crm/predict", methods=["POST"])
def crm_predict():
    lead_dict = request.json or {}
    pred = crm.predict_lead_propensity(lead_dict)
    action = crm.recommend_next_action(lead_dict)
    return jsonify({"propensity": pred, "recommended_action": action})

# ==========================================
# DOWNLOAD & EXPORT APIS
# ==========================================
@app.route("/api/download/presentation", methods=["GET"])
def download_presentation():
    pptx_path = os.path.join(BASE_DIR, "Business_Case_Presentation.pptx")
    if not os.path.exists(pptx_path):
        create_business_case_deck(pptx_path)
    return send_file(pptx_path, as_attachment=True, download_name="Airtel_SYNC_Project_Udyam_Presentation.pptx")

@app.route("/api/docs/<path:filename>", methods=["GET"])
def serve_doc(filename):
    docs_dir = os.path.join(BASE_DIR, "docs")
    try:
        return send_from_directory(docs_dir, filename, mimetype="text/plain")
    except Exception:
        return jsonify({"error": "Document not found"}), 404

@app.route("/api/products/all", methods=["GET"])
def get_products_all():
    return jsonify(advisor.get_all_products())

@app.route("/api/download/zip", methods=["GET"])
def download_zip():
    zip_path = os.path.join(BASE_DIR, "Project_Udyam_Digital_Airtel_SYNC.zip")
    if not os.path.exists(zip_path):
        import zipfile
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for root, dirs, files in os.walk(BASE_DIR):
                if any(x in root for x in ["__pycache__", ".git", "extracted_input"]):
                    continue
                for f in files:
                    if f.endswith(".zip"):
                        continue
                    full_p = os.path.join(root, f)
                    rel_p = os.path.relpath(full_p, BASE_DIR)
                    z.write(full_p, rel_p)
    return send_file(zip_path, as_attachment=True, download_name="Project_Udyam_Digital_Airtel_SYNC.zip")

@app.route("/advisor")
def advisor_page():
    return render_template("advisor.html")

@app.route("/quote")
def quote_page():
    return render_template("quote.html")

@app.route("/kyc")
def kyc_page():
    return render_template("kyc.html")

@app.route("/tracker")
def tracker_page():
    return render_template("tracker.html")

@app.route("/crm")
def crm_page():
    return render_template("crm.html")

@app.route("/deliverables")
def deliverables_page():
    return render_template("deliverables.html")

if __name__ == "__main__":
    print("Starting Airtel Project Udyam Digital Web Server on http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
