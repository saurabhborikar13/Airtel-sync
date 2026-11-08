import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_business_case_deck(output_path: str):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color Palette (Airtel Brand & Professional Dark/Light)
    COLOR_RED = RGBColor(228, 0, 0)         # Airtel Primary Red
    COLOR_DARK = RGBColor(26, 26, 36)       # Rich Charcoal Navy
    COLOR_WHITE = RGBColor(255, 255, 255)
    COLOR_LIGHT_GRAY = RGBColor(245, 246, 250)
    COLOR_TEXT_MUTED = RGBColor(110, 115, 130)
    COLOR_TEXT_MAIN = RGBColor(30, 35, 45)
    COLOR_ACCENT_GREEN = RGBColor(16, 185, 129)
    COLOR_CARD_BORDER = RGBColor(225, 230, 240)

    blank_layout = prs.slide_layouts[6]
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static", "images", "airtel_logo.png")

    def add_header(slide, title_text, category_text="AIRTEL SYNC HACKATHON 2026 · TRACK A"):
        # Category Banner
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(10.5), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_RED

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(10.5), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_DARK

        # Top right logo
        if os.path.exists(logo_path):
            slide.shapes.add_picture(logo_path, Inches(11.8), Inches(0.45), width=Inches(0.75), height=Inches(0.75))

        # Top red accent bar
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(0.04))
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_RED
        line.line.color.rgb = COLOR_RED

    def add_card(slide, left, top, width, height, bg_color=COLOR_LIGHT_GRAY, border_color=COLOR_CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        return card

    # ==========================================
    # SLIDE 1: Title & Executive Summary
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_DARK
    bg1.line.fill.background()

    # Red decorative bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(1.8), Inches(0.2), Inches(4.0))
    bar.fill.solid()
    bar.fill.fore_color.rgb = COLOR_RED
    bar.line.fill.background()

    # Title slide logo
    if os.path.exists(logo_path):
        s1.shapes.add_picture(logo_path, Inches(10.5), Inches(1.8), width=Inches(1.8), height=Inches(1.8))

    tb1 = s1.shapes.add_textbox(Inches(1.5), Inches(1.7), Inches(8.8), Inches(4.5))
    tf1 = tb1.text_frame
    p0 = tf1.paragraphs[0]
    p0.text = "AIRTEL SYNC HACKATHON 2026 · TRACK A"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_RED

    p1 = tf1.add_paragraph()
    p1.text = "Project Udyam Digital"
    p1.font.size = Pt(40)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE
    p1.space_before = Pt(12)

    p2 = tf1.add_paragraph()
    p2.text = "Making Small Businesses Go Digital in One Sitting"
    p2.font.size = Pt(20)
    p2.font.color.rgb = RGBColor(200, 210, 230)
    p2.space_before = Pt(8)

    p3 = tf1.add_paragraph()
    p3.text = "An end-to-end AI-powered acquisition, instant KYC, transparent pricing, and self-service onboarding engine designed for India's 6 Crore+ MSMEs."
    p3.font.size = Pt(14)
    p3.font.color.rgb = RGBColor(180, 190, 205)
    p3.space_before = Pt(24)

    p4 = tf1.add_paragraph()
    p4.text = "Key Results: Customer Acquisition Cost slashed from ₹15,000 to < ₹2,500 (-83%) · Onboarding time collapsed from 17.6 days to < 24 hours · Status follow-up calls reduced from 3.0 to 0."
    p4.font.size = Pt(12)
    p4.font.bold = True
    p4.font.color.rgb = COLOR_ACCENT_GREEN
    p4.space_before = Pt(16)

    # ==========================================
    # SLIDE 2: Market Opportunity & Ground Reality
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Market Opportunity & The Current Funnel Leakage")

    # Card 1: The Opportunity
    add_card(s2, 0.8, 1.8, 5.7, 5.0)
    tb = s2.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.5))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "The 6 Crore+ MSME Reality"
    p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = COLOR_DARK
    
    bullets = [
        "Massive Unserved Base: India has over 6.3 crore MSMEs contributing ~30% of GDP. Most currently rely on consumer mobile hotspots and unorganized local ISPs.",
        "Rapid Digitization Needs: Retailers and clinics now need fixed high-speed broadband for UPI soundboxes/POS, cloud billing, CCTV surveillance, and WhatsApp customer reach.",
        "Vendor Fragmentation: Owners currently deal with 4-5 fragmented vendors with separate bills, no SLA, and zero customer support."
    ]
    for b in bullets:
        p = tf.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(13); p.font.color.rgb = COLOR_TEXT_MAIN; p.space_before = Pt(10)

    # Card 2: Funnel Diagnostic
    add_card(s2, 6.8, 1.8, 5.7, 5.0)
    tb = s2.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.5))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "Current Acquisition Bottlenecks (Synthetic Baseline)"
    p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = COLOR_DARK

    metrics = [
        "93% Funnel Dropout: 5,000 leads generate only 368 activations (7.36% overall conversion).",
        "Steepest Drop at Quote: 56% of leads drop between Needs Assessed and Quote Accepted due to complex PDF quotes and pushy sales reps.",
        "Crippling Acquisition Cost: Blended CAC is ~₹15,000 per activated customer, severely depressing customer lifetime value (LTV:CAC ~1.8x).",
        "Sluggish 17.6-Day Cycle: Manual physical KYC and repeated follow-up calls (3x per customer) cause severe customer frustration."
    ]
    for m in metrics:
        p = tf.add_paragraph()
        p.text = "• " + m
        p.font.size = Pt(13); p.font.color.rgb = COLOR_TEXT_MAIN; p.space_before = Pt(8)

    # ==========================================
    # SLIDE 3: Customer Segment Prioritization
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "MSME Segment Prioritization & Tailored Value Propositions")

    segs = [
        ("Micro Retail & Services", "55% Base", "High Priority #1", "Kiranas, salons, pharmacies. Highly price-sensitive. Needs: Uninterrupted UPI transactions, Cloud POS, and verified WhatsApp customer alerts.", "Bundle: Biz Fibre 100 + Cloud POS + Guest Wi-Fi (₹1,500 - ₹2,500/mo)"),
        ("Professional Offices", "25% Base", "High Priority #2", "Clinics, CA firms, coaching centres, legal practices. Needs: 99.9% uptime, Static IP, Cloud Email, and 1 TB automated backup.", "Bundle: Biz Fibre 300 + Static IP + Cloud Email + Backup (₹2,500 - ₹4,500/mo)"),
        ("Multi-Site Businesses", "15% Base", "Strategic Growth", "Restaurant chains, 3-10 store retail branches. Needs: Single consolidated bill, SD-WAN interconnect, 4G/5G failover, and Cloud CCTV.", "Bundle: Biz Fibre + SD-WAN + Failover + Cloud CCTV (₹6,000 - ₹12,000/mo)"),
        ("Small Manufacturers", "5% Base", "High ARPU", "Auto-parts units, textile fabrication, processing units. Needs: 1:1 dedicated Leased Lines with SLA, Machine IoT sensors, and Managed Firewall.", "Bundle: Leased Line 20 + Managed Firewall + IoT (₹12,000 - ₹25,000/mo)")
    ]

    for idx, (title, share, tag, desc, bundle) in enumerate(segs):
        col_left = 0.8 + idx * 2.95
        add_card(s3, col_left, 1.8, 2.8, 5.0)
        tb = s3.shapes.add_textbox(Inches(col_left + 0.15), Inches(1.95), Inches(2.5), Inches(4.7))
        tf = tb.text_frame
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = COLOR_DARK
        
        p = tf.add_paragraph()
        p.text = f"{share} · {tag}"
        p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = COLOR_RED; p.space_before = Pt(4)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(11); p.font.color.rgb = COLOR_TEXT_MAIN; p.space_before = Pt(8)

        p = tf.add_paragraph()
        p.text = "Recommended Solution:"
        p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = COLOR_DARK; p.space_before = Pt(12)

        p = tf.add_paragraph()
        p.text = bundle
        p.font.size = Pt(11); p.font.color.rgb = COLOR_RED; p.space_before = Pt(4)

    # ==========================================
    # SLIDE 4: Digital-First Customer Journey
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Project Udyam Digital: 4-Step Self-Serve Customer Journey")

    steps = [
        ("Step 1: AI Advisor", "Conversational Discovery", "Replaces physical sales visits. Engages owner in their preferred regional language (Hindi, Tamil, Hinglish). Discovers business size and needs in under 90 seconds without jargon."),
        ("Step 2: 1-Click Quote", "Transparent Pricing", "Instantly presents a single consolidated monthly bill with 18% GST and setup fees clearly broken down. Interactive toggles let owners adjust bandwidth and add-ons in real time."),
        ("Step 3: Smart KYC", "Instant Verification", "Dual-mode KYC via instant GSTIN & Udyam API lookup or document upload. AI detects blur, orientation, checks mod-36 checksum, and masks PII in full compliance with DPDP Act 2023."),
        ("Step 4: Live Tracker", "Zero Chase Calls", "Visual milestone tracker displaying order confirmation, equipment dispatch, and technician installation slot. Automated WhatsApp alerts eliminate the 3 customer chase calls completely.")
    ]

    for idx, (title, subtitle, detail) in enumerate(steps):
        col_left = 0.8 + idx * 2.95
        add_card(s4, col_left, 1.8, 2.8, 5.0)
        tb = s4.shapes.add_textbox(Inches(col_left + 0.15), Inches(1.95), Inches(2.5), Inches(4.7))
        tf = tb.text_frame
        
        p = tf.paragraphs[0]
        p.text = f"0{idx+1}"
        p.font.size = Pt(24); p.font.bold = True; p.font.color.rgb = COLOR_RED

        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = COLOR_DARK; p.space_before = Pt(4)

        p = tf.add_paragraph()
        p.text = subtitle
        p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = COLOR_TEXT_MUTED; p.space_before = Pt(2)

        p = tf.add_paragraph()
        p.text = detail
        p.font.size = Pt(12); p.font.color.rgb = COLOR_TEXT_MAIN; p.space_before = Pt(10)

    # ==========================================
    # SLIDE 5: Product Bundling & Pricing Architecture
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Product Bundling Strategy & Transparent Pricing Architecture")

    add_card(s5, 0.8, 1.8, 5.7, 5.0)
    tb = s5.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.5))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "The 'Single Bill' Architectural Advantage"
    p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = COLOR_DARK

    bullets = [
        "Consolidated Billing Engine: Packages connectivity, cloud productivity, cybersecurity, and communication into one unified invoice.",
        "Rigorous Dependency Validation: Enforces technical prerequisites automatically (e.g. 4G/5G Failover requires Biz Fibre; Managed Firewall requires Leased Line/Fibre).",
        "GSTIN-Aware Eligibility: System smartly hides or adapts enterprise products requiring active GSTIN (e.g. ILL, SD-WAN, Cloud Telephony) for non-GST micro businesses.",
        "Commitment Incentives: Transparent 12, 24, and 36-month term toggles providing up to 15% annual savings and zero upfront setup fees."
    ]
    for b in bullets:
        p = tf.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(13); p.font.color.rgb = COLOR_TEXT_MAIN; p.space_before = Pt(10)

    add_card(s5, 6.8, 1.8, 5.7, 5.0)
    tb = s5.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.5))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "Representative Bundle Blueprints"
    p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = COLOR_DARK

    packs = [
        ("Udyam Starter (Kirana / Retail)", "₹1,887 / mo", "Biz Fibre 100 (P01) + Cloud POS (P19) + Guest Wi-Fi (P22)"),
        ("Practice Cloud Suite (Clinic / CA)", "₹3,184 / mo", "Biz Fibre 300 (P02) + Static IP (P11) + Cloud Email (P16) + 1TB Backup (P17)"),
        ("Multi-Branch Interconnect", "₹6,838 / mo", "Biz Fibre 300 (P02) + 4G/5G Failover (P09) + SD-WAN (P10) + Cloud CCTV (P23)"),
        ("Smart Plant & IoT (Manufacturing)", "₹13,499 / mo", "Internet Leased Line 20 (P05) + Firewall (P21) + Machine IoT (P24)")
    ]
    for name, price, comps in packs:
        p = tf.add_paragraph()
        p.text = f"{name} — {price}"
        p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = COLOR_RED; p.space_before = Pt(8)
        p = tf.add_paragraph()
        p.text = comps
        p.font.size = Pt(11); p.font.color.rgb = COLOR_TEXT_MAIN

    # ==========================================
    # SLIDE 6: Unit Economics Transformation
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Transforming Unit Economics & Customer Lifetime Value")

    metrics_comp = [
        ("Customer Acquisition Cost (CAC)", "₹15,000", "< ₹2,500", "-83% CAC Reduction via automated self-serve discovery & partner app"),
        ("Time to Activation", "17.6 Days", "< 24 Hours", "95% faster onboarding with instant digital KYC and pre-provisioned inventory"),
        ("Overall Funnel Conversion", "7.36%", "28.0%", "3.8x conversion surge by removing physical sales friction and opaque PDF quotes"),
        ("Customer Follow-Up Calls", "3.0 Calls", "0 Calls", "Self-service tracking and proactive WhatsApp milestones eliminate chasing"),
        ("6-Month Customer Churn", "11.2%", "< 4.0%", "Right-sized bundles with proactive SLA monitoring and consolidated billing")
    ]

    add_card(s6, 0.8, 1.8, 11.733, 5.0)
    tb = s6.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.3), Inches(4.5))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "Operational & Financial Benchmark Comparison"
    p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = COLOR_DARK

    for metric, before, after, impact in metrics_comp:
        p = tf.add_paragraph()
        p.text = f"• {metric}: Legacy {before}  ➔  Project Udyam {after}  |  Impact: {impact}"
        p.font.size = Pt(13); p.font.color.rgb = COLOR_TEXT_MAIN; p.space_before = Pt(10)

    # ==========================================
    # SLIDE 7: Field Force & Partner Synergy
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Partner Synergy: Empowering Field Sales & Local Resellers")

    add_card(s7, 0.8, 1.8, 5.7, 5.0)
    tb = s7.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.5))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "Empowering, Not Replacing, Local Partners"
    p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = COLOR_DARK

    points = [
        "Partner Co-Pilot Mode: Local retail distributors and field executives use the exact same AI Advisor as an on-ground consultation tool on their smartphones.",
        "Zero Channel Conflict: Leads originating from partner QR codes or partner referral IDs are permanently mapped, guaranteeing recurring commission payouts.",
        "On-Site Instant Onboarding: Field reps complete customer needs discovery, quote generation, and camera KYC on the spot in 5 minutes flat.",
        "High-Value Account Focus: Field sales force pivots from pitching low-margin single SIMs to advisory selling for high-ARPU Multi-Site and Manufacturing clients."
    ]
    for pt in points:
        p = tf.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(13); p.font.color.rgb = COLOR_TEXT_MAIN; p.space_before = Pt(10)

    add_card(s7, 6.8, 1.8, 5.7, 5.0)
    tb = s7.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.5))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "ML Lead Propensity & Partner CRM"
    p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = COLOR_DARK

    points2 = [
        "AI Propensity Scoring: Random Forest classifier dynamically scores all 5,000 leads to identify high-probability prospects (High / Medium / Low).",
        "Next-Best-Action Engine: Automatically prescribes the exact intervention based on past drop reason (e.g. price hesitation ➔ trigger 15% discount; time constraint ➔ WhatsApp link).",
        "Pipeline Visibility: Real-time partner dashboard monitors leads stalled at Needs Assessed or Quote Accepted for prioritized dispatch."
    ]
    for pt in points2:
        p = tf.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(13); p.font.color.rgb = COLOR_TEXT_MAIN; p.space_before = Pt(10)

    # ==========================================
    # SLIDE 8: Key Success Metrics & Targets
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Success Metrics Scorecard & Target KPIs")

    kpis = [
        ("Conversion Rate", "7.36%", "28.0%", "3.8x increase in overall lead-to-activation rate through frictionless UX"),
        ("Cycle Time", "17.6 Days", "< 24 Hours", "Instant digital KYC + same-day fiber dispatch model"),
        ("Blended CAC", "₹15,000", "< ₹2,500", "83% reduction in sales cost per acquired MSME customer"),
        ("Chase Calls", "3.0 Calls", "0.0 Calls", "100% elimination of manual status follow-ups via live order hub")
    ]

    for idx, (metric, current, target, note) in enumerate(kpis):
        col_left = 0.8 + idx * 2.95
        add_card(s8, col_left, 1.8, 2.8, 5.0)
        tb = s8.shapes.add_textbox(Inches(col_left + 0.15), Inches(1.95), Inches(2.5), Inches(4.7))
        tf = tb.text_frame

        p = tf.paragraphs[0]
        p.text = metric
        p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = COLOR_DARK

        p = tf.add_paragraph()
        p.text = f"Baseline: {current}"
        p.font.size = Pt(12); p.font.color.rgb = COLOR_TEXT_MUTED; p.space_before = Pt(8)

        p = tf.add_paragraph()
        p.text = f"Target: {target}"
        p.font.size = Pt(20); p.font.bold = True; p.font.color.rgb = COLOR_RED; p.space_before = Pt(4)

        p = tf.add_paragraph()
        p.text = note
        p.font.size = Pt(11); p.font.color.rgb = COLOR_TEXT_MAIN; p.space_before = Pt(10)

    # ==========================================
    # SLIDE 9: Data Privacy & DPDP Act 2023 Compliance
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Data Privacy & Security Architecture (DPDP Act, 2023)")

    add_card(s9, 0.8, 1.8, 5.7, 5.0)
    tb = s9.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.5))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "DPDP Act 2023 Compliance Principles"
    p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = COLOR_DARK

    dpdp = [
        "Granular Consent Architecture: Unambiguous, affirmative consent notice provided in customer's preferred language prior to document collection.",
        "Purpose Limitation: Data collected during KYC is cryptographically bound strictly to telecommunications onboarding and legal DOT verification.",
        "Data Minimisation: Collection restricted strictly to statutory KYC necessities (GSTIN, Udyam, 90-day address proof, Signatory ID).",
        "Storage Limitation & Automated Purge: Raw unencrypted document images auto-purged within 30 days post-activation, retaining only tamper-proof cryptographic audit hashes."
    ]
    for d in dpdp:
        p = tf.add_paragraph()
        p.text = "• " + d
        p.font.size = Pt(13); p.font.color.rgb = COLOR_TEXT_MAIN; p.space_before = Pt(10)

    add_card(s9, 6.8, 1.8, 5.7, 5.0)
    tb = s9.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.5))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "Security Engineering & Masking Controls"
    p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = COLOR_DARK

    sec = [
        "Zero-Trust PII Masking: GSTIN, PAN, and identity numbers are dynamically masked across all user interfaces, partner CRM views, and system log streams.",
        "Encryption Standards: AES-256 GCM encryption at rest in isolated vaults, with TLS 1.3 enforced for all API transactions in transit.",
        "Role-Based Access Control (RBAC): Strict least-privilege access partitions sensitive business applicant dossiers from field sales reps.",
        "Tamper-Proof Audit Trail: Every verification step records immutable cryptographic event signatures for regulatory DOT compliance."
    ]
    for s in sec:
        p = tf.add_paragraph()
        p.text = "• " + s
        p.font.size = Pt(13); p.font.color.rgb = COLOR_TEXT_MAIN; p.space_before = Pt(10)

    # ==========================================
    # SLIDE 10: Rollout Roadmap & Risk Mitigation
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "18-Month Phased Rollout Roadmap & Risk Mitigation")

    add_card(s10, 0.8, 1.8, 5.7, 5.0)
    tb = s10.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.5))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "Phased Execution Roadmap"
    p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = COLOR_DARK

    phases = [
        "Phase 1 (Months 1–3) — Pilot Launch: Deploy AI Advisor and Smart KYC across top 5 Tier-1 cities (Delhi, Mumbai, Bengaluru, Chennai, Hyderabad). Target: 10,000 onboardings.",
        "Phase 2 (Months 4–8) — Partner Network Scale: Roll out Partner Co-Pilot app to 5,000 local channel partners and expand coverage across 30 Tier-2 commercial hubs.",
        "Phase 3 (Months 9–14) — Vernacular & WhatsApp Native: Launch full conversational WhatsApp flow in 8 regional languages with voice-guided onboarding.",
        "Phase 4 (Months 15–18) — Autonomous Self-Provisioning: Zero-touch network activation with pre-configured plug-and-play 5G AirFiber CPEs."
    ]
    for ph in phases:
        p = tf.add_paragraph()
        p.text = "• " + ph
        p.font.size = Pt(12); p.font.color.rgb = COLOR_TEXT_MAIN; p.space_before = Pt(8)

    add_card(s10, 6.8, 1.8, 5.7, 5.0)
    tb = s10.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.5))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "Risk Matrix & Mitigation Strategies"
    p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = COLOR_DARK

    risks = [
        ("Risk: Partner channel pushback or boycotts", "Mitigation: Lifetime revenue-sharing commission model and co-pilot tool that makes partners close deals 3x faster."),
        ("Risk: Low digital literacy in Tier-2/3 kiranas", "Mitigation: Vernacular voice interface (Hindi/regional) and assisted partner onboarding."),
        ("Risk: Incomplete or forged KYC paperwork", "Mitigation: Automated blur detection, mod-36 checksum, and instant direct API verification against official GST/Udyam registries."),
        ("Risk: Regulatory scrutiny under DPDP Act 2023", "Mitigation: Privacy-by-design architecture, automated document purge schedules, and end-to-end PII masking.")
    ]
    for r_title, r_mit in risks:
        p = tf.add_paragraph()
        p.text = r_title
        p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = COLOR_RED; p.space_before = Pt(8)
        p = tf.add_paragraph()
        p.text = r_mit
        p.font.size = Pt(11); p.font.color.rgb = COLOR_TEXT_MAIN

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    prs.save(output_path)
    print(f"Presentation saved successfully to {output_path}")

if __name__ == "__main__":
    create_business_case_deck(r"d:\Airtel_prj\Business_Case_Presentation.pptx")
