import os
import pandas as pd
from typing import Dict, List, Any

class AdvisorEngine:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.catalog_df = pd.read_csv(os.path.join(data_dir, "product_catalogue.csv")).fillna("")
        self.products_by_id = {r["product_id"]: r.to_dict() for _, r in self.catalog_df.iterrows()}

    def get_all_products(self) -> List[Dict[str, Any]]:
        clean_df = self.catalog_df.fillna("")
        return clean_df.to_dict(orient="records")

    def recommend_bundle(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recommends tailored product bundles based on MSME profile:
        - business_type (kirana, clinic, ca_office, coaching, restaurant, manufacturer, etc.)
        - segment (micro, prof, multi, mfg)
        - employees (int)
        - sites (int)
        - city_tier (1 or 2)
        - has_gstin (bool / 'Y' / 'N')
        - monthly_budget (int)
        - priority_needs (list of strings: upi, cctv, whatsapp, backup, email, security, iot, pos, etc.)
        - language ('en', 'hi', 'hinglish', 'ta')
        """
        segment = user_profile.get("segment", "micro").lower()
        employees = int(user_profile.get("employees", 5))
        sites = int(user_profile.get("sites", 1))
        city_tier = int(user_profile.get("city_tier", 1))
        has_gstin = str(user_profile.get("has_gstin", "Y")).upper() in ["Y", "TRUE", "YES", "1"]
        priorities = [p.lower() for p in user_profile.get("priority_needs", [])]
        lang = user_profile.get("language", "en").lower()

        # Archetype mapping if business_type given
        btype = user_profile.get("business_type", "").lower()
        if any(k in btype for k in ["kirana", "retail", "shop", "salon", "pharmacy", "store"]):
            segment = "micro"
        elif any(k in btype for k in ["clinic", "hospital", "doctor", "ca", "law", "consult", "coaching", "school"]):
            segment = "prof"
        elif any(k in btype for k in ["restaurant", "chain", "outlet", "hotel", "branch"]):
            segment = "multi" if sites > 1 else "micro"
        elif any(k in btype for k in ["factory", "manufacturing", "textile", "auto", "plant", "unit"]):
            segment = "mfg"

        primary_bundle_ids = []
        alt_bundle_ids = []
        rationales = {}

        # 1. Base Connectivity
        if segment == "micro":
            # For micro: Biz 5G AirFiber 100 or Biz Fibre 100
            primary_bundle_ids.append("P01")  # Biz Fibre 100
            alt_bundle_ids.append("P04")      # Biz 5G AirFiber 100
            rationales["P01"] = {
                "en": "Guaranteed 100 Mbps fiber speed ensures instant UPI soundbox and POS transactions without payment drops.",
                "hi": "100 Mbps फ़ाइबर इंटरनेट यह सुनिश्चित करता है कि UPI साउंडबॉक्स और POS पेमेंट कभी भी नेटवर्क की वजह से न अटकें।",
                "hinglish": "100 Mbps fiber speed se UPI payment aur POS transactions bilkul instantly clear hote hain.",
                "ta": "100 Mbps அதிவேக ஃபைபர் மூலம் UPI மற்றும் POS பேமெண்ட்டுகள் தடையின்றி நடக்கும்."
            }
            rationales["P04"] = {
                "en": "Plug-and-play 5G AirFiber gets you online in under 48 hours without trenching cables.",
                "hi": "5G एयरफ़ाइबर 48 घंटे के भीतर बिना किसी वायर या केबल खुदाई के चालू हो जाता है।",
                "hinglish": "48 hours ke andar bina kisi wire jhanjhat ke fast 5G broadband setup.",
                "ta": "வயரிங் எதுவும் இன்றி 48 மணி நேரத்தில் செயல்படும் 5G ஏர்ஃபைபர்."
            }
        elif segment == "prof":
            # Professional: Biz Fibre 300
            primary_bundle_ids.append("P02")  # Biz Fibre 300
            alt_bundle_ids.append("P01")      # Biz Fibre 100
            rationales["P02"] = {
                "en": "300 Mbps symmetrical fiber provides high bandwidth for multi-doctor video consults and large CAD/tax file uploads.",
                "hi": "300 Mbps की हाई-स्पीड वीडियो कंसल्टेशन और भारी टैक्स व अकाउंटिंग फ़ाइलों को तुरंत अपलोड करने के लिए आदर्श है।",
                "hinglish": "300 Mbps symmetrical fiber video calls aur heavy client documents ke liye smooth connection deta hai.",
                "ta": "300 Mbps ஃபைபர் மூலம் பெரிய டாகுமெண்ட்கள் மற்றும் வீடியோ கால்கள் எளிதாகச் செயல்படும்."
            }
            # Add Static IP
            primary_bundle_ids.append("P11")
            rationales["P11"] = {
                "en": "Static IP allows secure remote access to on-premise billing software, tally servers, and CCTV.",
                "hi": "स्टैटिक आईपी आपके टैली सर्वर, क्लिनिक सॉफ्टवेयर और सीसीटीवी को कहीं से भी सुरक्षित एक्सेस करने की सुविधा देता है।",
                "hinglish": "Static IP se Tally server aur clinic billing system ko ghar baithe securely access kar sakte hain.",
                "ta": "ஸ்டேடிக் IP மூலம் டேலி சர்வர் மற்றும் சிசிடிவி-யை எங்கிருந்தும் அணுகலாம்."
            }
        elif segment == "multi":
            # Multi-site: Biz Fibre 300 + Managed SD-WAN + 4G/5G Failover
            primary_bundle_ids.append("P02")
            primary_bundle_ids.append("P09")  # Backup 4G/5G Failover
            if has_gstin:
                primary_bundle_ids.append("P10")  # Managed SD-WAN
            alt_bundle_ids.extend(["P01", "P09"])
            rationales["P02"] = {
                "en": "Reliable 300 Mbps connectivity for real-time inventory synchronization across all branch outlets.",
                "hi": "सभी शाखाओं और दुकानों के बीच लाइव इन्वेंट्री और बिलिंग सिंक के लिए 300 Mbps कनेक्शन।",
                "hinglish": "Sabhi outlets me live billing aur inventory sync ke liye ultra-reliable 300 Mbps line.",
                "ta": "அனைத்து கிளைகளிலும் பில்லிங் ஒரே நேரத்தில் சீராக இயங்க 300 Mbps இணைப்பு."
            }
            rationales["P09"] = {
                "en": "Automatic 4G/5G failover keeps billing alive even if the primary fiber cable is accidentally cut.",
                "hi": "अगर मुख्य केबल कट भी जाए, तो 4G/5G बैकअप तुरंत चालू होकर बिलिंग को रुकने नहीं देता।",
                "hinglish": "Agar main wire kat bhi jaaye to 4G/5G auto-switch billing ko rukne nahi dega.",
                "ta": "முக்கிய ஃபைபர் பாதிக்கப்பட்டாலும் 4G/5G ஆட்டோ-பேக்கப் மூலம் பில்லிங் நிற்காது."
            }
            if has_gstin:
                rationales["P10"] = {
                    "en": "Centralized SD-WAN connects all stores into a single secure virtual network under one single bill.",
                    "hi": "एसडी-वैन आपकी सभी दुकानों को एक ही बिल और एक ही सुरक्षित नेटवर्क में जोड़ता है।",
                    "hinglish": "SD-WAN se sabhi stores ek central secure network aur single consolidated bill par aate hain.",
                    "ta": "அனைத்து கிளைகளையும் ஒரே பாதுகாப்பான நெட்வொர்க்கில் இணைக்கும் SD-WAN."
                }
        else:  # mfg
            if has_gstin:
                primary_bundle_ids.append("P05")  # Internet Leased Line 20
                alt_bundle_ids.append("P03")      # Biz Fibre 1G
                rationales["P05"] = {
                    "en": "1:1 unshared Leased Line with 99.9% uptime SLA for mission-critical ERP systems and industrial machinery.",
                    "hi": "99.9% अपटाइम SLA वाली 1:1 अनशेयर्ड लीज्ड लाइन जो फ़ैक्टरी के ERP और मशीनों को 24x7 कनेक्ट रखती है।",
                    "hinglish": "Dedicated 1:1 leased line with 99.9% SLA taaki factory ERP kabhi down na ho.",
                    "ta": "தொழிற்சாலைகளுக்கான 99.9% SLA கொண்ட பிரத்யேக லீஸ்டு லைன்."
                }
                primary_bundle_ids.append("P21")  # Managed Firewall
                rationales["P21"] = {
                    "en": "Enterprise-grade perimeter firewall guards plant networks against ransomware and unauthorized intrusions.",
                    "hi": "एंटरप्राइज़ फ़ायरवॉल आपके फ़ैक्टरी नेटवर्क को साइबर हमलों और रैनसमवेयर से बचाता है।",
                    "hinglish": "Managed Firewall plant machines ko cyber attacks aur malware se protect karta hai.",
                    "ta": "தொழிற்சாலை கணினிகளை வைரஸ் தாக்குதலிலிருந்து காக்கும் ஃபயர்வால்."
                }
            else:
                primary_bundle_ids.append("P03")  # Biz Fibre 1G
                alt_bundle_ids.append("P02")

        # 2. Add-ons based on business priorities & segment
        if segment == "micro":
            primary_bundle_ids.append("P19")  # Cloud POS & Billing
            rationales["P19"] = {
                "en": "Cloud POS streamlines daily billing, digital invoices, and GST compliant receipts on any phone or tablet.",
                "hi": "क्लाउड पीओएस किसी भी मोबाइल या टैबलेट पर तुरंत जीएसटी बिलिंग और डिजिटल रसीदें जारी करता है।",
                "hinglish": "Mobile pe hi daily billing aur digital receipts banane ke liye Cloud POS.",
                "ta": "மொபைல் மூலமே டிஜிட்டல் பில்லிங் செய்ய கிளவுட் POS."
            }
            if has_gstin:
                primary_bundle_ids.append("P15")  # WhatsApp Business API
                rationales["P15"] = {
                    "en": "Official WhatsApp Business API sends automated delivery alerts, offers, and payment links with your verified green tick.",
                    "hi": "व्हाट्सएप बिज़नेस एपीआई से ग्राहकों को ऑटोमैटिक बिल, डिलीवरी अपडेट और ऑफ़र भेजें।",
                    "hinglish": "Customers ko WhatsApp par automated bill, tracking updates aur discount offers bhejein.",
                    "ta": "வாட்ஸ்அப் மூலம் வாடிக்கையாளர்களுக்கு பில் மற்றும் சலுகை தகவல்களை அனுப்பலாம்."
                }
            primary_bundle_ids.append("P22")  # Secure Wi-Fi with Guest Network
            rationales["P22"] = {
                "en": "Separates customer guest Wi-Fi from your internal billing terminal for complete payment cybersecurity.",
                "hi": "ग्राहकों के वाई-फ़ाई को आपकी बिलिंग मशीन से अलग रखता है ताकि आपका पेमेंट डाटा पूरी तरह सुरक्षित रहे।",
                "hinglish": "Customer Wi-Fi ko billing terminal se alag rakh kar fraud se bachata hai.",
                "ta": "வாடிக்கையாளர் வைஃபையை பில்லிங் சாதனத்திலிருந்து பிரித்து பாதுகாப்பு அளிக்கிறது."
            }
        elif segment == "prof":
            primary_bundle_ids.append("P16")  # Cloud Email & Office Suite
            primary_bundle_ids.append("P17")  # Cloud Backup 1 TB
            primary_bundle_ids.append("P20")  # Endpoint Security
            rationales["P16"] = {
                "en": "Professional business email (you@yourfirm.com) builds instant trust with high-value clients.",
                "hi": "प्रोफेशनल ईमेल (you@yourfirm.com) क्लाइंट्स में आपके ब्रांड का भरोसा बढ़ाता है।",
                "hinglish": "Professional domain email (doctor@clinic.com) se clients ka trust badhta hai.",
                "ta": "தொழில்முறை ஈமெயில் முகவரி வாடிக்கையாளர்களிடையே நன்மதிப்பை உருவாக்கும்."
            }
            rationales["P17"] = {
                "en": "Automated cloud backup protects client records, audit files, and medical histories against hardware crashes.",
                "hi": "ऑटोमैटिक क्लाउड बैकअप आपके महत्वपूर्ण ऑडिट, क्लाइंट व मेडिकल रिकॉर्ड्स को सुरक्षित रखता है।",
                "hinglish": "1 TB cloud backup se system kharab hone par bhi zaroori data safe rehta hai.",
                "ta": "1 TB கிளவுட் பேக்கப் மூலம் முக்கிய தரவுகள் பாதுகாக்கப்படும்."
            }
            rationales["P20"] = {
                "en": "Endpoint antivirus & anti-phishing defense shields office PCs from malware and data leaks.",
                "hi": "एंटीवायरस और फ़िशिंग सुरक्षा आपके सभी ऑफिस कंप्यूटरों को सुरक्षित रखती है।",
                "hinglish": "Endpoint security office laptops aur PCs ko cyber threats se safe rakhti hai.",
                "ta": "கணினிகளை மால்வேர் மற்றும் சைபர் அச்சுறுத்தல்களிலிருந்து பாதுகாக்கும்."
            }
        elif segment == "multi":
            primary_bundle_ids.append("P23")  # Cloud CCTV
            primary_bundle_ids.append("P19")  # Cloud POS
            rationales["P23"] = {
                "en": "Live cloud CCTV feeds from all store branches viewable in a single mobile dashboard without local DVR costs.",
                "hi": "बिना महंगे डीवीआर के, सभी दुकानों की लाइव सीसीटीवी रिकॉर्डिंग अपने फोन पर देखें।",
                "hinglish": "Ek hi phone screen par sabhi branches ke live CCTV cameras bina DVR ke dekhein.",
                "ta": "அனைத்து கிளைகளின் சிசிடிவி காட்சிகளையும் மொபைலில் நேரடியாகக் காணலாம்."
            }
        elif segment == "mfg":
            if has_gstin:
                primary_bundle_ids.append("P24")  # Machine Monitoring IoT
                rationales["P24"] = {
                    "en": "IoT machine sensors track operational hours, vibration anomalies, and power draw to prevent line breakdowns.",
                    "hi": "आईओटी सेंसर मशीनों के चलने के घंटे और बिजली खपत पर नजर रखकर अचानक खराबी से बचाते हैं।",
                    "hinglish": "Machine IoT sensors breakdown se pehle alert bhej kar production loss rokte hain.",
                    "ta": "மெஷின்களை கண்காணித்து பழுதுகளை முன்கூட்டியே தடுக்கும் IoT சென்சார்."
                }
            primary_bundle_ids.append("P17")  # Cloud Backup

        # Check dependencies (requires_one_of) and GST requirement
        def sanitize_bundle(b_ids):
            clean_ids = []
            for pid in b_ids:
                prod = self.products_by_id.get(pid)
                if not prod:
                    continue
                # GST check
                if prod.get("requires_gstin") == "Y" and not has_gstin:
                    continue
                clean_ids.append(pid)

            # Check requires_one_of
            final_ids = []
            for pid in clean_ids:
                prod = self.products_by_id[pid]
                req = str(prod.get("requires_one_of", "")).strip()
                if req and req != "nan":
                    options = req.split("|")
                    if not any(opt in clean_ids for opt in options):
                        # Dependency not satisfied, skip
                        continue
                final_ids.append(pid)
            return list(dict.fromkeys(final_ids))

        primary_bundle_ids = sanitize_bundle(primary_bundle_ids)
        alt_bundle_ids = sanitize_bundle(alt_bundle_ids)
        if not alt_bundle_ids:
            alt_bundle_ids = ["P01", "P07"]

        def calculate_bundle_pricing(pids):
            monthly_min = 0
            monthly_max = 0
            setup_fee = 0
            max_install_days = 1
            items = []
            for pid in pids:
                p = self.products_by_id[pid]
                monthly_min += p["price_min_inr_per_month"]
                monthly_max += p["price_max_inr_per_month"]
                setup_fee += p["one_time_setup_inr"]
                max_install_days = max(max_install_days, int(p["typical_install_days"]))
                
                # Language specific rationale
                rat = rationales.get(pid, {})
                explanation = rat.get(lang, rat.get("en", p["description"]))

                items.append({
                    "product_id": pid,
                    "name": p["product_name"],
                    "category": p["category"],
                    "description": p["description"],
                    "price_min": p["price_min_inr_per_month"],
                    "price_max": p["price_max_inr_per_month"],
                    "setup_fee": p["one_time_setup_inr"],
                    "install_days": p["typical_install_days"],
                    "rationale": explanation
                })

            # Bundle discount (10% off for bundle of 3+ products)
            discount_pct = 10 if len(pids) >= 3 else 5
            monthly_discounted = round(monthly_min * (1 - discount_pct / 100))
            gst_amount = round(monthly_discounted * 0.18)
            total_with_gst = monthly_discounted + gst_amount

            return {
                "products": items,
                "base_monthly_inr": monthly_min,
                "discount_pct": discount_pct,
                "discounted_monthly_inr": monthly_discounted,
                "gst_18_pct": gst_amount,
                "total_monthly_with_gst": total_with_gst,
                "setup_fee_inr": setup_fee,
                "estimated_install_days": max_install_days
            }

        primary_quote = calculate_bundle_pricing(primary_bundle_ids)
        alt_quote = calculate_bundle_pricing(alt_bundle_ids)

        # Overview rationale
        bundle_titles = {
            "micro": {
                "en": "Udyam Smart Digital Starter",
                "hi": "उद्यम डिजिटल स्टार्टर बंडल",
                "ta": "உத்யம் ஸ்மார்ட் டிஜிட்டல் பேக்"
            },
            "prof": {
                "en": "Professional Practice Cloud Suite",
                "hi": "प्रोफेशनल ऑफिस क्लाउड सुइट",
                "ta": "தொழில்முறை கிளவுட் சூட்"
            },
            "multi": {
                "en": "Multi-Store Unified Enterprise Bundle",
                "hi": "मल्टी-स्टोर यूनिफाइड एंटरप्राइज बंडल",
                "ta": "மல்டி-ஸ்டோர் என்டர்பிரைஸ் பேக்"
            },
            "mfg": {
                "en": "Smart Manufacturing & IoT Bundle",
                "hi": "स्मार्ट मैन्युफैक्चरिंग एवं आईओटी बंडल",
                "ta": "ஸ்மார்ட் உற்பத்தி மற்றும் IoT பேக்"
            }
        }

        return {
            "segment": segment,
            "bundle_title": bundle_titles.get(segment, {}).get(lang, "Udyam Digital Business Bundle"),
            "primary_bundle": primary_quote,
            "alternative_bundle": alt_quote,
            "user_profile": user_profile
        }

    def chat_response(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Provides human-like conversational responses for the Advisor chatbot in English/Hindi/Hinglish/Tamil."""
        msg = message.lower().strip()
        lang = context.get("language", "en")

        # Intent detection
        if any(w in msg for w in ["kirana", "dukan", "shop", "salon", "medical", "pharmacy"]):
            context["segment"] = "micro"
            rec = self.recommend_bundle(context)
            if lang == "hi":
                reply = "शानदार! आपकी दुकान के लिए 'उद्यम डिजिटल स्टार्टर' एकदम सही रहेगा। इसमें 100 Mbps फ़ाइबर इंटरनेट, क्लाउड पीओएस बिलिंग और ग्राहकों के लिए सेफ वाई-फ़ाई शामिल है। इससे आपके UPI पेमेंट कभी नहीं अटकेंगे। क्या आप इसका तुरंत कोटेशन देखना चाहेंगे?"
            elif lang == "ta":
                reply = "சிறப்பு! உங்கள் கடைக்கு 'உத்யம் டிஜிட்டல் பேக்' மிகவும் பொருத்தமானது. இதில் 100 Mbps ஃபைபர், கிளவுட் POS மற்றும் பாதுகாப்பான வைஃபை கிடைக்கும். கொட்டேஷனை பார்க்கலாமா?"
            elif lang == "hinglish":
                reply = "Perfect! Aapki shop ke liye 'Udyam Digital Starter' best rahega. Isme 100 Mbps high-speed fiber, Cloud POS billing aur customer safe Wi-Fi included hai taaki UPI payments smoothly chalein. Kya aap quote dekhna chahenge?"
            else:
                reply = "Great! For your retail business, the 'Udyam Smart Digital Starter' is the ideal choice. It includes Biz Fibre 100 for zero-fail UPI payments, Cloud POS billing, and Secure Guest Wi-Fi. Would you like to review the transparent monthly quote?"
            return {"reply": reply, "context": context, "recommendation": rec}

        elif any(w in msg for w in ["clinic", "doctor", "ca", "advocate", "law", "coaching", "school"]):
            context["segment"] = "prof"
            rec = self.recommend_bundle(context)
            if lang == "hi":
                reply = "बिल्कुल! आपके प्रोफेशन के लिए 300 Mbps फ़ाइबर, स्टैटिक आईपी और 1 TB क्लाउड बैकअप आवश्यक है ताकि आपके क्लाइंट्स और पेशेंट्स का रिकॉर्ड्स हमेशा सुरक्षित रहे। आइए इसका बंडल और प्राइस देखते हैं।"
            elif lang == "ta":
                reply = "உங்கள் தொழில்முறை அலுவலகத்திற்கு 300 Mbps ஃபைபர், ஸ்டேடிக் IP மற்றும் 1 TB கிளவுட் பேக்கப் மிகச் சிறந்தது. இதன் மூலம் கிளையண்ட் தகவல்கள் பாதுகாப்பாக இருக்கும்."
            elif lang == "hinglish":
                reply = "Samajh gaya! Aapke office/clinic ke liye 300 Mbps fiber, static IP aur 1 TB cloud backup zaroori hai jisse client records aur Tally data hamesha secure rahein."
            else:
                reply = "Understood! For professional practices, reliable uptime, cloud data backup, and endpoint security are essential. We recommend our 'Professional Practice Cloud Suite' with Biz Fibre 300, Static IP, Cloud Email, and 1 TB Secure Backup."
            return {"reply": reply, "context": context, "recommendation": rec}

        elif any(w in msg for w in ["restaurant", "branches", "outlets", "multi", "chain", "2 stores", "3 stores"]):
            context["segment"] = "multi"
            context["sites"] = 3
            rec = self.recommend_bundle(context)
            if lang == "hi":
                reply = "अति उत्तम! जब आपके पास कई शाखाएं हों, तो सभी स्टोर्स के लिए 4G/5G ऑटो-बैकअप और क्लाउड सीसीटीवी सबसे ज़रूरी है ताकि बिलिंग कभी न रुके और एक ही स्क्रीन पर सभी स्टोर्स दिखें।"
            else:
                reply = "Excellent! For multi-site businesses, seamless branch connectivity, automatic 4G/5G failover, and centralized Cloud CCTV are vital so you never lose a sale even during local cable outages."
            return {"reply": reply, "context": context, "recommendation": rec}

        elif any(w in msg for w in ["factory", "manufacturing", "textile", "plant", "unit", "industry"]):
            context["segment"] = "mfg"
            rec = self.recommend_bundle(context)
            if lang == "hi":
                reply = "फ़ैक्टरी संचालन के लिए 99.9% गारंटीड अपटाइम वाली 1:1 लीज्ड लाइन, मशीन मॉनिटरिंग आईओटी और एंटरप्राइज फ़ायरवॉल की आवश्यकता होती है।"
            else:
                reply = "For manufacturing plants, dedicated 1:1 leased lines with 99.9% uptime SLA, Machine Monitoring IoT sensors, and Managed Firewall protection guarantee uninterrupted production."
            return {"reply": reply, "context": context, "recommendation": rec}

        elif any(w in msg for w in ["price", "cost", "how much", "budget", "kitna", "rate"]):
            rec = self.recommend_bundle(context)
            monthly = rec["primary_bundle"]["total_monthly_with_gst"]
            return {
                "reply": f"Our transparent all-inclusive bundle starts at just ₹{monthly}/month (inclusive of 18% GST). There are zero hidden charges and you get a single consolidated monthly bill. You can customize add-ons anytime!",
                "context": context,
                "recommendation": rec
            }

        else:
            rec = self.recommend_bundle(context)
            return {
                "reply": "Welcome to Airtel Project Udyam Digital! Tell me briefly about your business (for example: 'I own a pharmacy in Jaipur with 4 staff' or 'We run a 3-outlet restaurant chain') and I will configure the exact high-speed digital bundle for you in seconds.",
                "context": context,
                "recommendation": rec
            }
