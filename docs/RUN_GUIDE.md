# Quick Start Run Guide for VS Code

Follow these 4 simple steps to run **Project Udyam Digital** on Visual Studio Code:

### Step 1: Open Folder in VS Code
Open VS Code, press `Ctrl + K, Ctrl + O` (or **File > Open Folder...**), and select this project directory:
```
d:\Airtel_prj
```

### Step 2: Open Terminal
Open a new integrated terminal in VS Code using the shortcut `Ctrl + \`` (backtick) or click **Terminal > New Terminal**.

### Step 3: Install Required Packages
Run the following command:
```bash
pip install -r requirements.txt
```

### Step 4: Start the Server
Run the startup script:
```bash
python run.py
```

### Step 5: Open Web Application
The runner will automatically open your web browser, or you can manually navigate to:
👉 **http://localhost:5000**

---

### Key Live Demo Steps for Evaluators / Judges:
1. **AI Advisor:**
   - Click any archetype button (e.g. *Micro Retail 55%* or *Professional Offices 25%*).
   - Change language dropdown to **हिंदी (Hindi)** or **தமிழ் (Tamil)** to see instant multilingual recommendations.
   - Click the **Voice** button in the chat card to simulate voice discovery.
2. **Transparent Quote:**
   - Scroll to Step 2.
   - Toggle contract commitment buttons (12 Months, 24 Months, 36 Months) to see live discount updates.
   - Toggle add-ons (Static IP, 4G/5G failover, Cloud CCTV) with real-time recalculation.
3. **Smart KYC Live Test:**
   - Scroll to Step 3.
   - Under *Specimen Judge Pack (K01–K12)*, select any applicant from the dropdown:
     - Select **K03 (Ganesh Woodcraft)** or **K12 (Star Electronics)** to demonstrate a clean **Instant Pass**.
     - Select **K01** to show detection of **Cancelled GSTIN status** and missing Udyam number.
     - Select **K02** to show detection of **Skewed/Rotated Document** and **Mod-36 Checksum Failure**.
     - Select **K04** to demonstrate **Blur Detection** (Laplacian variance < 100).
     - Select **K11** to demonstrate **Expired Address Proof** (>90 days old from reference date 2026-07-15).
4. **Live Order Tracker:**
   - Click *Confirm Order & Generate Live Tracker*.
   - Watch the 5-stage visual milestone stepper and live WhatsApp notification feed.
5. **Partner CRM & ML Propensity:**
   - Scroll to Step 5 to view funnel diagnostics and the 5,000 SMB leads.
   - Filter by stage (*Needs assessed*) to see the machine learning propensity score (High/Medium/Low) and prescribed *Next-Best-Action* scripts.
6. **Download Deliverables:**
   - Click the top navigation buttons to download the 10-slide PowerPoint presentation (`.pptx`) or the complete submission ZIP (`.zip`).
