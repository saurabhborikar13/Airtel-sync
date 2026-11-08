# Airtel SYNC Hackathon 2026 · Track A: Project Udyam Digital
## Making Small Businesses Go Digital in One Sitting
# watch demo video  : https://drive.google.com/file/d/1TwcPl2c8KbH7sJIPwkrbOD9QJjv4vQ7D/view?usp=drive_link
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask 3.0](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/ML-RandomForest-orange.svg)](https://scikit-learn.org/)
[![DPDP Act 2023](https://img.shields.io/badge/Compliance-DPDP_Act_2023-red.svg)](https://www.meity.gov.in/)

> **Project Udyam Digital** is an end-to-end, digital-first customer acquisition, intelligent bundling, instant KYC, and self-service onboarding platform engineered for India's 6 Crore+ Micro, Small, and Medium Enterprises (MSMEs).

---

## 🏆 Key Achievements & Impact Metrics

| Metric | Legacy Field Sales Process | Project Udyam Digital | Business Impact |
| :--- | :--- | :--- | :--- |
| **Customer Acquisition Cost (CAC)** | ₹15,000 / customer | **₹2,450 / customer** | **-83.7% CAC Reduction** |
| **Lead-to-Activation Time** | 17.6 Days | **< 24 Hours** | **95% Faster Time-to-Market** |
| **Funnel Conversion Rate** | 7.36% (368 / 5,000) | **28.0%** | **3.8x Conversion Surge** |
| **Customer Follow-Up Chases** | 3.0 Calls / customer | **0 Calls** | **100% Elimination via Live Hub** |
| **Customer 6-Month Churn** | 11.2% | **< 4.0%** | **Consolidated SLA Billing** |

---

## 🚀 Complete Step-by-Step Guide: Running in VS Code From Scratch

### 1. Prerequisites
Ensure you have Python installed (Python 3.10, 3.11, 3.12, 3.13, or 3.14):
```bash
python --version
```

### 2. Open Project in VS Code
1. Launch **Visual Studio Code**.
2. Go to **File ➔ Open Folder...** and select `d:\Airtel_prj` (or wherever you extracted the project ZIP).
3. Open the integrated terminal in VS Code using <kbd>Ctrl</kbd> + <kbd>`</kbd> (backtick) or **Terminal ➔ New Terminal**.

### 3. Install Dependencies
In the VS Code terminal, run:
```bash
pip install -r requirements.txt
```

### 4. Run the Project (1-Click Start)
Run the automated startup runner:
```bash
python run.py
```
* The script automatically validates data files, spins up the local server, and launches your default web browser to:
  👉 **`http://localhost:5000`**

*(Alternatively, you can run `python app.py` and open `http://localhost:5000` in any web browser).*

---

## 🧭 Multi-Page Platform Architecture

The web application is structured into dedicated, production-grade pages:

| Page | URL Route | Core Functionality |
| :--- | :--- | :--- |
| **Executive Dashboard** | `/` | Platform KPI stats, onboarding timeline, DPDP compliance summary |
| **AI Business Advisor** | `/advisor` | Conversational vernacular advisor (EN / HI / TA), voice input (Web Speech API), business archetype selector |
| **Quote Builder** | `/quote` | Catalog of 25 products across 5 categories, real-time GST pricing, custom bundle creator |
| **Smart KYC Engine** | `/kyc` | 12 specimen automated validator (K01–K12), Mod-36 checksum, GSTIN & Udyam registry lookups |
| **Order Tracker** | `/tracker` | 5-stage live dispatch & installation tracker with simulated WhatsApp / SMS notifications |
| **Partner CRM** | `/crm` | 5,000 lead database, Random Forest ML propensity scoring, conversion funnel analytics |
| **Deliverables & Downloads** | `/deliverables` | 1-click download of Business Case Presentation (PPTX), full source code ZIP, and architecture docs |

---

## 🧭 Platform Capabilities & Feature Tour

### 1. GenAI Conversational Business Advisor (`#advisor`)
* **Vernacular & Multilingual:** Toggle between **English**, **हिंदी (Hindi)**, **Hinglish**, and **தமிழ் (Tamil)**.
* **Archetype Quick Presets:** Pre-configured profiles for:
  * 🛒 *Micro Retail & Services (55% of MSMEs)*: Kiranas, pharmacies, salons (UPI zero-drop, Cloud POS).
  * 🩺 *Professional Offices (25% of MSMEs)*: Clinics, CA firms, coaching centres (300 Mbps, Static IP, Cloud Backup).
  * 🏢 *Small Multi-Site (15% of MSMEs)*: 3–10 branch restaurants (SD-WAN, 4G/5G Failover, Cloud CCTV).
  * ⚙️ *Small Manufacturers (5% of MSMEs)*: Auto-parts, fabrication units (Dedicated Leased Line 1:1, IoT machine monitoring).
* **Conversational Natural Language Chat:** Ask queries naturally via text or the **Voice Interaction** simulation.
* **Plain Language Rationale:** Explains *why* each product is recommended in plain business language without confusing tech jargon.

### 2. Transparent Interactive Quote & Checkout (`#quote`)
* **Consolidated Billing:** Replaces multiple bills with a single, clear monthly invoice combining connectivity, cloud, and security.
* **Interactive Add-On Matrix:** Toggle Static IP, 4G/5G Wireless Backup, WhatsApp API, Cloud CCTV, and Endpoint Antivirus in real time with technical dependency checking.
* **Contract Commitment Toggles:** Choose 12, 24, or 36 months to unlock up to 20% commitment discounts and waived setup fees.

### 3. Smart KYC & DPDP Act 2023 Verification Engine (`#kyc`)
* **Statutory DPDP Compliance Notice:** Clear, affirmative, unbundled consent with purpose limitation, data minimisation, and automated 30-day document purge notice.
* **Specimen Tester Pack (K01–K12):** Test the platform against the 12 hackathon synthetic test cases:
  * **K03 (Ganesh Woodcraft)** & **K12 (Star Electronics)**: 100% Clean & Valid — Instant Green Approval!
  * **K01**: Correctly catches **Cancelled GSTIN status** and missing Udyam number.
  * **K02**: Detects **skewed image rotation** and **invalid mod-36 GSTIN checksum** (digit 0 vs letter O).
  * **K04**: Detects **severe blur** via 2D Laplacian variance convolution.
  * **K05**: Flags **missing mandatory Udyam certificate**.
  * **K06**: Catches **tampered GSTIN** that differs from the official registry.
  * **K07**: Flags **trade name vs legal name divergence** (Shri Physio vs Neelgiri Physio).
  * **K08**: Catches **character checksum mismatch** in GSTIN.
  * **K09 & K10**: Flags **unauthorized signatory designation** (Admin for Proprietorship, Owner for LLP).
  * **K11**: Catches **expired address proof** (utility bill > 90 days old relative to reference date 2026-07-15).
* **Fast-Track Registry Lookup:** Direct API query against 3,534 GST records and 2,723 Udyam records.
* **Dynamic PII Masking:** Masks PAN, GSTIN, Aadhaar, and phone numbers across all screens.

### 4. Real-Time Order Tracker & Self-Service Hub (`#tracker`)
* **5-Stage Visual Stepper:** Order Confirmed ➔ Smart KYC Approved ➔ Dispatched ➔ Site Installation Scheduled ➔ Activated.
* **Dynamic SLA Countdown:** Dynamically calculates guaranteed activation date based on product `typical_install_days`.
* **Proactive WhatsApp & SMS Simulation:** Feeds live milestone notifications to customer's mobile view, completely eliminating the 3+ chase calls.

### 5. Partner & Sales Back-Office CRM + ML Propensity AI (`#crm`)
* **Funnel Analytics Dashboard:** Live diagnostics on all 5,000 synthetic SMB leads.
* **Machine Learning Propensity Model:** Random Forest classifier trained on `smb_leads.csv` predicting customer conversion likelihood (High / Medium / Low).
* **Next-Best-Action Engine:** Prescribes tactical scripts for field agents tailored to the lead's historical drop reason.
* **Assisted Field Onboarding:** Field reps can guide walk-in customers through the same 5-minute digital journey.

---

## 📁 Project Directory Structure

```
d:\Airtel_prj\
├── app.py                             # Main Flask Backend API server & web app router
├── run.py                             # 1-Click launcher with auto-browser opening
├── requirements.txt                   # Production Python package dependencies
├── generate_artifacts.py              # Script to build presentation deck and submission ZIP
├── Business_Case_Presentation.pptx    # 10-Slide Airtel SYNC Business Case Presentation Deck
├── Project_Udyam_Digital_Airtel_SYNC.zip # Complete packaged project archive for submission
│
├── data/                              # Fictional Hackathon Datasets
│   ├── product_catalogue.csv          # 25 enterprise products with eligibility & dependencies
│   ├── smb_leads.csv                  # 5,000 SMB lead records with funnel stages & drop reasons
│   ├── mock_gstin_registry.csv        # 3,534 GST records (Active / Cancelled)
│   ├── mock_udyam_registry.csv        # 2,723 MSME Udyam registration records
│   └── kyc_documents/                 # 47 specimen KYC PNG images (K01 to K12)
│
├── models/                            # Machine Learning Models
│   ├── propensity_model.pkl           # Trained Random Forest Lead Propensity Classifier
│   └── train_propensity_model.py      # Training script for scikit-learn ML pipeline
│
├── services/                          # Core Domain Logic Microservices
│   ├── advisor_engine.py              # Conversational AI & product bundling rules engine
│   ├── kyc_validator.py               # Smart KYC computer vision, checksum, & registry validator
│   ├── crm_service.py                 # Leads querying, funnel metrics & ML propensity scoring
│   └── presentation_gen.py            # Automated 10-slide PowerPoint presentation generator
│
├── static/                            # Frontend Static Assets
│   ├── css/style.css                  # Airtel Business design system stylesheet
│   └── js/app.js                      # Frontend application logic, state, and speech synthesis
│
├── templates/
│   └── index.html                     # Responsive single-page application container
│
└── docs/                              # Technical & Compliance Documentation
    ├── Solution_Architecture.md       # Full architecture specification with Mermaid diagrams
    ├── DPDP_Privacy_and_Security_Note.md # 1-page DPDP Act 2023 compliance whitepaper
    └── RUN_GUIDE.md                   # Quick reference run guide
```

---

## 📋 Hackathon Deliverables Checklist

- [x] **Working Prototype:** Fully functional, responsive, multilingual web application (`http://localhost:5000`).
- [x] **Solution Architecture Document:** Complete data flow and component topology in `docs/Solution_Architecture.md`.
- [x] **10-Slide Business Case Presentation:** Professional `.pptx` deck saved at `Business_Case_Presentation.pptx` (and downloadable from web UI).
- [x] **DPDP Act 2023 1-Page Privacy Note:** Comprehensive compliance architecture documented in `docs/DPDP_Privacy_and_Security_Note.md`.
- [x] **Packaged Submission ZIP:** Complete 7.5 MB archive ready for direct submission at `Project_Udyam_Digital_Airtel_SYNC.zip`.

---

## 👥 Credits
Built for the **Airtel SYNC Hackathon 2026** (Enterprise Track A: Project Udyam Digital).
All datasets, business names, identifiers, and documents are synthetic and generated for this challenge.
