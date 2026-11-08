"""
Airtel SYNC Hackathon 2026 — Track A: Project Udyam Digital
Official 7-Slide Submission Presentation & PDF Generator
Fully compliant with Hackathon Portal requirements:
- Exactly 7 slides
- Under 20 MB size limit
- Official Airtel branding & logo on all slides
- Embedded clickable Video Demo & Solution links
"""

import os
import subprocess
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO_PATH = os.path.join(BASE_DIR, "static", "images", "airtel_logo.png")
VIDEO_LINK = "https://drive.google.com/file/d/1TwcPl2c8KbH7sJIPwkrbOD9QJjv4vQ7D/view?usp=drive_link"

# Brand Palette
RED       = RGBColor(0xE4, 0x00, 0x00)   # Official Airtel Red
NAVY      = RGBColor(0x11, 0x18, 0x27)   # Deep Executive Navy
DARK_CARD = RGBColor(0x1F, 0x29, 0x37)   # Dark Gray Card
GOLD      = RGBColor(0xF5, 0x9E, 0x0B)   # Amber Gold
GREEN     = RGBColor(0x10, 0xB9, 0x81)   # Emerald Success
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)   # Pure White
LGRAY     = RGBColor(0xF9, 0xFA, 0xFB)   # Subtle Page Gray
CARD_BG   = RGBColor(0xFF, 0xFF, 0xFF)   # Card White
BORDER_C  = RGBColor(0xE5, 0xE7, 0xEB)   # Card Border Gray
TEXT_DARK = RGBColor(0x1F, 0x29, 0x37)   # Charcoal Text
TEXT_MUTED= RGBColor(0x6B, 0x72, 0x80)   # Secondary Text
BLUE      = RGBColor(0x25, 0x63, 0xEB)   # Accent Blue

SW = Inches(13.333)   # 16:9 Widescreen
SH = Inches(7.5)


def add_shape_rect(slide, x, y, w, h, fill_color, border_color=None, border_width=Pt(1)):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = border_width
    else:
        shape.line.fill.background()
    return shape


def add_rounded_card(slide, x, y, w, h, fill_color, border_color=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)
    else:
        shape.line.fill.background()
    return shape


def add_logo(slide, x, y, w, h):
    if os.path.exists(LOGO_PATH):
        slide.shapes.add_picture(LOGO_PATH, x, y, width=w, height=h)


def add_header(slide, title_text, slide_num_str):
    # Top navigation banner
    add_shape_rect(slide, Inches(0), Inches(0), SW, Inches(0.85), NAVY)
    add_shape_rect(slide, Inches(0), Inches(0.82), SW, Inches(0.04), RED)

    # Logo left
    add_logo(slide, Inches(0.35), Inches(0.08), Inches(1.3), Inches(0.68))

    # Hackathon and title tag
    txb = slide.shapes.add_textbox(Inches(1.85), Inches(0.12), Inches(8.5), Inches(0.62))
    tf = txb.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    r1 = p1.add_run()
    r1.text = "AIRTEL SYNC HACKATHON 2026 · TRACK A  |  "
    r1.font.size = Pt(10)
    r1.font.bold = True
    r1.font.color.rgb = GOLD
    r1.font.name = "Arial"

    r2 = p1.add_run()
    r2.text = title_text
    r2.font.size = Pt(16)
    r2.font.bold = True
    r2.font.color.rgb = WHITE
    r2.font.name = "Arial"

    # Slide Counter Right
    cnt = slide.shapes.add_textbox(Inches(10.8), Inches(0.18), Inches(2.1), Inches(0.5))
    ctf = cnt.text_frame
    cp = ctf.paragraphs[0]
    cp.alignment = PP_ALIGN.RIGHT
    cpr = cp.add_run()
    cpr.text = slide_num_str
    cpr.font.size = Pt(11)
    cpr.font.bold = True
    cpr.font.color.rgb = WHITE

    # Footer
    add_shape_rect(slide, Inches(0), Inches(7.02), SW, Inches(0.48), NAVY)
    ftx = slide.shapes.add_textbox(Inches(0.4), Inches(7.05), Inches(7.0), Inches(0.4))
    fp = ftx.text_frame.paragraphs[0]
    fpr = fp.add_run()
    fpr.text = "Project Udyam Digital — Bharti Airtel Ltd. · Confidential Submission"
    fpr.font.size = Pt(9)
    fpr.font.color.rgb = RGBColor(0x9C, 0xA3, 0xAF)

    # Video link button in footer on every slide
    flnk = slide.shapes.add_textbox(Inches(7.8), Inches(7.05), Inches(5.1), Inches(0.4))
    flnk.click_action.hyperlink.address = VIDEO_LINK
    flp = flnk.text_frame.paragraphs[0]
    flp.alignment = PP_ALIGN.RIGHT
    flpr = flp.add_run()
    flpr.text = "🎥 Click to Watch Demo Video (Google Drive)"
    flpr.font.size = Pt(9.5)
    flpr.font.bold = True
    flpr.font.color.rgb = GOLD
    flpr.hyperlink.address = VIDEO_LINK


# ==============================================================================
# SLIDE 1: Title & Executive Overview + Live Submission Links
# ==============================================================================
def make_slide_1(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = NAVY

    # Left vertical red accent bar
    add_shape_rect(slide, Inches(0), Inches(0), Inches(0.2), SH, RED)

    # Logo Top Left
    add_logo(slide, Inches(0.8), Inches(0.55), Inches(2.2), Inches(1.15))

    # Header category pill
    add_rounded_card(slide, Inches(3.3), Inches(0.65), Inches(4.8), Inches(0.42), RED)
    tx = slide.shapes.add_textbox(Inches(3.3), Inches(0.66), Inches(4.8), Inches(0.4))
    p = tx.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "AIRTEL SYNC HACKATHON 2026 · TRACK A SUBMISSION"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = WHITE

    # Main Title
    tbox = slide.shapes.add_textbox(Inches(0.8), Inches(1.85), Inches(11.8), Inches(1.2))
    tp = tbox.text_frame.paragraphs[0]
    tr = tp.add_run()
    tr.text = "PROJECT UDYAM DIGITAL"
    tr.font.size = Pt(44)
    tr.font.bold = True
    tr.font.color.rgb = WHITE

    # Subtitle
    tp2 = tbox.text_frame.add_paragraph()
    tr2 = tp2.add_run()
    tr2.text = "Accelerating India's 63M+ MSMEs from Inquiry to Active Fibre & Cloud in One Sitting (<24 Hours)"
    tr2.font.size = Pt(17)
    tr2.font.color.rgb = RGBColor(0xD1, 0xD5, 0xDB)

    # 3 High-Impact KPI Blocks
    kpis = [
        ("₹2,450", "Target CAC", "-83.7% from ₹15,000 baseline", RED),
        ("< 24 Hours", "Lead-to-Active", "-95% reduction from 17.6 days", GREEN),
        ("28.0%", "Conversion Rate", "3.8x uplift from 7.36% baseline", GOLD),
        ("0 Calls", "Status Chases", "100% self-serve order visibility", BLUE),
    ]
    card_w = Inches(2.7)
    card_h = Inches(1.5)
    start_x = Inches(0.8)
    card_y = Inches(3.2)

    for i, (val, title, note, color) in enumerate(kpis):
        cx = start_x + i * Inches(2.95)
        add_rounded_card(slide, cx, card_y, card_w, card_h, DARK_CARD, color)
        
        tx = slide.shapes.add_textbox(cx, card_y + Inches(0.12), card_w, Inches(0.6))
        p = tx.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = val
        r.font.size = Pt(26)
        r.font.bold = True
        r.font.color.rgb = color

        tx2 = slide.shapes.add_textbox(cx, card_y + Inches(0.72), card_w, Inches(0.4))
        p2 = tx2.text_frame.paragraphs[0]
        p2.alignment = PP_ALIGN.CENTER
        r2 = p2.add_run()
        r2.text = title
        r2.font.size = Pt(12)
        r2.font.bold = True
        r2.font.color.rgb = WHITE

        tx3 = slide.shapes.add_textbox(cx, card_y + Inches(1.05), card_w, Inches(0.35))
        p3 = tx3.text_frame.paragraphs[0]
        p3.alignment = PP_ALIGN.CENTER
        r3 = p3.add_run()
        r3.text = note
        r3.font.size = Pt(9.5)
        r3.font.color.rgb = RGBColor(0x9C, 0xA3, 0xAF)

    # Interactive Links Card (Crucial for Reviewers)
    link_card_y = Inches(4.95)
    add_rounded_card(slide, Inches(0.8), link_card_y, Inches(11.55), Inches(1.85), DARK_CARD, RED)

    ltit = slide.shapes.add_textbox(Inches(1.0), link_card_y + Inches(0.1), Inches(11.1), Inches(0.4))
    lp = ltit.text_frame.paragraphs[0]
    lr = lp.add_run()
    lr.text = "🔗 SUBMISSION DELIVERABLES & INTERACTIVE LINKS"
    lr.font.size = Pt(12)
    lr.font.bold = True
    lr.font.color.rgb = GOLD

    # Video Button Card
    vbox = add_rounded_card(slide, Inches(1.0), link_card_y + Inches(0.55), Inches(5.4), Inches(1.1), NAVY, GOLD)
    vbox.click_action.hyperlink.address = VIDEO_LINK
    vtx = slide.shapes.add_textbox(Inches(1.15), link_card_y + Inches(0.62), Inches(5.1), Inches(0.95))
    vtx.click_action.hyperlink.address = VIDEO_LINK
    vp = vtx.text_frame.paragraphs[0]
    vr1 = vp.add_run()
    vr1.text = "🎥 Product Walkthrough Video (Google Drive)"
    vr1.font.size = Pt(12)
    vr1.font.bold = True
    vr1.font.color.rgb = WHITE
    vp2 = vtx.text_frame.add_paragraph()
    vr2 = vp2.add_run()
    vr2.text = "▶ Click here to view the end-to-end video demonstration"
    vr2.font.size = Pt(10)
    vr2.font.color.rgb = GOLD
    vr2.font.underline = True
    vr2.hyperlink.address = VIDEO_LINK

    # Codebase & Architecture Card
    cbox = add_rounded_card(slide, Inches(6.7), link_card_y + Inches(0.55), Inches(5.4), Inches(1.1), NAVY, BLUE)
    ctx = slide.shapes.add_textbox(Inches(6.85), link_card_y + Inches(0.65), Inches(5.1), Inches(0.9))
    cp = ctx.text_frame.paragraphs[0]
    cr1 = cp.add_run()
    cr1.text = "💻 Working Full-Stack Web Application\n"
    cr1.font.size = Pt(12)
    cr1.font.bold = True
    cr1.font.color.rgb = WHITE
    cr2 = cp.add_run()
    cr2.text = "Built on Flask, Multi-Lingual Web Speech Voice, 12-Specimen Smart KYC, RF ML CRM"
    cr2.font.size = Pt(10)
    cr2.font.color.rgb = RGBColor(0x93, 0xC5, 0xFD)

    # Footer note
    ft = slide.shapes.add_textbox(Inches(0.8), Inches(6.9), Inches(11.55), Inches(0.4))
    ftp = ft.text_frame.paragraphs[0]
    ftp.alignment = PP_ALIGN.RIGHT
    ftpr = ftp.add_run()
    ftpr.text = "Bharti Airtel Ltd. · Track A: Digitising SMB Onboarding · November 2026"
    ftpr.font.size = Pt(9.5)
    ftpr.font.color.rgb = RGBColor(0x9C, 0xA3, 0xAF)


# ==============================================================================
# SLIDE 2: Problem Statement & MSME Market Opportunity
# ==============================================================================
def make_slide_2(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = LGRAY
    add_header(slide, "Market Opportunity & The SMB Friction Problem", "Slide 2 of 7")

    # Left: Market Opportunity Card
    add_rounded_card(slide, Inches(0.5), Inches(1.1), Inches(5.8), Inches(5.85), CARD_BG, BORDER_C)
    add_shape_rect(slide, Inches(0.5), Inches(1.1), Inches(5.8), Inches(0.45), RED)
    th1 = slide.shapes.add_textbox(Inches(0.7), Inches(1.12), Inches(5.4), Inches(0.4))
    r = th1.text_frame.paragraphs[0].add_run()
    r.text = "🇮🇳 The MSME Market Opportunity"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = WHITE

    points1 = [
        ("63M+ Micro, Small & Medium Enterprises", "Backbone of Indian GDP (30%) and employment (110M+ workers). Only ~15% currently possess managed enterprise digital infrastructure."),
        ("₹2.5 Lakh Crore Connectivity & SaaS TAM", "Rapidly shifting from unorganized consumer broadband to bundled B2B connectivity, cyber safety, cloud storage, and POS systems."),
        ("Airtel's Strategic Advantage", "Unmatched nationwide fibre footprint, 5G standalone edge, trusted enterprise relationship, and comprehensive business product ecosystem (25+ B2B products)."),
        ("The Growth Bottleneck", "Massive top-funnel demand is throttled by complex paper onboarding, multi-visit document chases, and non-transparent pricing."),
    ]
    y_off = Inches(1.7)
    for title, desc in points1:
        tx = slide.shapes.add_textbox(Inches(0.7), y_off, Inches(5.4), Inches(1.15))
        tf = tx.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        r1 = p1.add_run()
        r1.text = "• " + title + "\n"
        r1.font.size = Pt(11)
        r1.font.bold = True
        r1.font.color.rgb = TEXT_DARK
        r2 = p1.add_run()
        r2.text = desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = TEXT_MUTED
        y_off += Inches(1.22)

    # Right: The Baseline Friction & Funnel Breakdown
    add_rounded_card(slide, Inches(6.6), Inches(1.1), Inches(6.2), Inches(5.85), CARD_BG, BORDER_C)
    add_shape_rect(slide, Inches(6.6), Inches(1.1), Inches(6.2), Inches(0.45), NAVY)
    th2 = slide.shapes.add_textbox(Inches(6.8), Inches(1.12), Inches(5.8), Inches(0.4))
    r = th2.text_frame.paragraphs[0].add_run()
    r.text = "⚠️ Current Funnel Reality (smb_leads.csv Baseline)"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = WHITE

    # Funnel Drop-off bars
    stages = [
        ("Total Inquiries / Leads", 5000, "100%", NAVY),
        ("Contacted by Sales", 3406, "68.1%", RGBColor(0x37, 0x41, 0x51)),
        ("Interested in Demo", 1974, "39.5%", BLUE),
        ("Docs Submitted", 861, "17.2%", GOLD),
        ("KYC Approved", 588, "11.8%", RGBColor(0xF9, 0x73, 0x16)),
        ("Activated & Billing", 368, "7.36%", RED),
    ]
    fy = Inches(1.68)
    for name, count, pct, col in stages:
        bar_w = Inches(3.2 * (count / 5000.0))
        # Name
        tx = slide.shapes.add_textbox(Inches(6.75), fy - Inches(0.05), Inches(2.2), Inches(0.4))
        p = tx.text_frame.paragraphs[0]
        pr = p.add_run()
        pr.text = name
        pr.font.size = Pt(9.5)
        pr.font.bold = True
        pr.font.color.rgb = TEXT_DARK
        # Bar
        add_shape_rect(slide, Inches(9.0), fy, bar_w, Inches(0.24), col)
        # Value
        tx2 = slide.shapes.add_textbox(Inches(9.1) + bar_w, fy - Inches(0.07), Inches(1.6), Inches(0.35))
        p2 = tx2.text_frame.paragraphs[0]
        pr2 = p2.add_run()
        pr2.text = f"{count:,} ({pct})"
        pr2.font.size = Pt(9)
        pr2.font.bold = True
        pr2.font.color.rgb = col
        fy += Inches(0.42)

    # 4 Pain point badges below funnel
    pains = [
        ("17.6 Days Latency", "Physical form submissions & manual back-office verifications"),
        ("₹15,000 High CAC", "Multiple field RM visits, paper courier, high churn leakage"),
        ("3.0 Status Chases", "Frustrated SMB owners calling reps repeatedly for updates"),
        ("11.2% Early Churn", "Missed SLA expectations, fragmented multi-vendor setups"),
    ]
    py = Inches(4.35)
    for title, sub in pains:
        card = add_rounded_card(slide, Inches(6.8), py, Inches(5.8), Inches(0.58), RGBColor(0xFE, 0xF2, 0xF2), RED)
        tx = slide.shapes.add_textbox(Inches(6.9), py + Inches(0.04), Inches(5.6), Inches(0.5))
        tf = tx.text_frame
        p = tf.paragraphs[0]
        r1 = p.add_run()
        r1.text = "• " + title + ": "
        r1.font.size = Pt(9.5)
        r1.font.bold = True
        r1.font.color.rgb = RED
        r2 = p.add_run()
        r2.text = sub
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = TEXT_DARK
        py += Inches(0.64)


# ==============================================================================
# SLIDE 3: 4 MSME Archetypes & Bundled Solutions
# ==============================================================================
def make_slide_3(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = LGRAY
    add_header(slide, "Target Segments & 4 Pre-Configured Value Bundles", "Slide 3 of 7")

    bundles = [
        {
            "segment": "Micro Retail",
            "share": "55% of Leads",
            "icon": "🏪",
            "profile": "Kiranas, apparel shops, local pharmacies, food joints",
            "bundle": "Smart Retail Bundle",
            "price": "₹1,998 / mo",
            "discount": "10% Bundle Discount",
            "products": [
                "Airtel Biz Fibre 100 Mbps (Unlimited)",
                "Smart Cloud POS & Soundbox",
                "Secure Airtel Guest Wi-Fi Portal",
                "Digital Payment Settlement Integration"
            ],
            "value_prop": "Fast checkout, customer Wi-Fi marketing, zero downtime for UPI payments.",
            "color": RED,
            "badge_bg": RGBColor(0xFE, 0xF2, 0xF2)
        },
        {
            "segment": "Professional Offices",
            "share": "25% of Leads",
            "icon": "💼",
            "profile": "Chartered Accountants, law firms, doctors, consultants",
            "bundle": "Secure Office Bundle",
            "price": "₹2,698 / mo",
            "discount": "12% Bundle Discount",
            "products": [
                "Airtel Biz Fibre 300 Mbps High Speed",
                "Static IP Address (for ERP & Tally)",
                "Airtel Cloud Backup (1 TB Encrypted)",
                "DNS Cyber Threat Protection Shield"
            ],
            "value_prop": "Remote client data access, compliant automated daily backups, secure audits.",
            "color": BLUE,
            "badge_bg": RGBColor(0xEF, 0xF6, 0xFF)
        },
        {
            "segment": "Small Multi-Site",
            "share": "15% of Leads",
            "icon": "🏬",
            "profile": "Retail chains, diagnostic labs, boutique gym branches",
            "bundle": "Connected Multi-Site",
            "price": "₹3,798 / mo",
            "discount": "15% Bundle Discount",
            "products": [
                "Airtel Biz Fibre 300 Mbps Primary",
                "Automated 4G/5G Wireless Failover SIM",
                "Airtel Cloud CCTV (8-Channel, 30d retention)",
                "Centralized SD-WAN Hub Management"
            ],
            "value_prop": "100% operational uptime, centralized surveillance, unified multisite billing.",
            "color": GREEN,
            "badge_bg": RGBColor(0xEC, 0xFD, 0xF5)
        },
        {
            "segment": "Small Manufacturers",
            "share": "5% of Leads",
            "icon": "🏭",
            "profile": "Auto-component workshops, fabrication, food packaging",
            "bundle": "Industrial Power Bundle",
            "price": "₹6,900 / mo",
            "discount": "18% Bundle Discount",
            "products": [
                "1:1 Dedicated Internet Leased Line (10 Mbps)",
                "Industrial IoT Machine Telemetry Gateway",
                "Next-Gen Hardware Firewall (NGFW)",
                "Priority 24/7 Enterprise Mission SLA"
            ],
            "value_prop": "Guaranteed low latency, machine telemetry logging, perimeter cyber security.",
            "color": GOLD,
            "badge_bg": RGBColor(0xFF, 0xFB, 0xEB)
        },
    ]

    card_w = Inches(2.85)
    card_h = Inches(5.8)
    y_top = Inches(1.1)

    for i, b in enumerate(bundles):
        x_left = Inches(0.5) + i * Inches(3.15)
        card = add_rounded_card(slide, x_left, y_top, card_w, card_h, CARD_BG, BORDER_C)

        # Segment Banner
        add_shape_rect(slide, x_left, y_top, card_w, Inches(0.68), b["color"])
        th = slide.shapes.add_textbox(x_left, y_top + Inches(0.04), card_w, Inches(0.6))
        p = th.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r1 = p.add_run()
        r1.text = f"{b['icon']} {b['segment']}\n"
        r1.font.size = Pt(11.5)
        r1.font.bold = True
        r1.font.color.rgb = WHITE
        r2 = p.add_run()
        r2.text = b["share"]
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = RGBColor(0xFE, 0xF3, 0xC7)

        # Price Box
        pbox = add_rounded_card(slide, x_left + Inches(0.15), y_top + Inches(0.8), card_w - Inches(0.3), Inches(0.72), b["badge_bg"], b["color"])
        ptx = slide.shapes.add_textbox(x_left + Inches(0.15), y_top + Inches(0.82), card_w - Inches(0.3), Inches(0.7))
        pp = ptx.text_frame.paragraphs[0]
        pp.alignment = PP_ALIGN.CENTER
        pr1 = pp.add_run()
        pr1.text = b["price"] + "\n"
        pr1.font.size = Pt(13)
        pr1.font.bold = True
        pr1.font.color.rgb = b["color"]
        pr2 = pp.add_run()
        pr2.text = b["discount"]
        pr2.font.size = Pt(8.5)
        pr2.font.bold = True
        pr2.font.color.rgb = TEXT_MUTED

        # Profile
        tx_prof = slide.shapes.add_textbox(x_left + Inches(0.15), y_top + Inches(1.58), card_w - Inches(0.3), Inches(0.65))
        tx_prof.text_frame.word_wrap = True
        ppr = tx_prof.text_frame.paragraphs[0]
        ppr_r = ppr.add_run()
        ppr_r.text = "Target Persona: " + b["profile"]
        ppr_r.font.size = Pt(8.5)
        ppr_r.font.color.rgb = TEXT_MUTED

        # Products Header
        tx_ph = slide.shapes.add_textbox(x_left + Inches(0.15), y_top + Inches(2.25), card_w - Inches(0.3), Inches(0.3))
        prh = tx_ph.text_frame.paragraphs[0].add_run()
        prh.text = "📦 Included Solutions:"
        prh.font.size = Pt(9)
        prh.font.bold = True
        prh.font.color.rgb = TEXT_DARK

        # Product list
        py = y_top + Inches(2.55)
        for prod in b["products"]:
            ptx = slide.shapes.add_textbox(x_left + Inches(0.15), py, card_w - Inches(0.3), Inches(0.48))
            ptx.text_frame.word_wrap = True
            pp_run = ptx.text_frame.paragraphs[0].add_run()
            pp_run.text = "✓ " + prod
            pp_run.font.size = Pt(8.5)
            pp_run.font.color.rgb = TEXT_DARK
            py += Inches(0.48)

        # Value Proposition Box
        val_box = add_rounded_card(slide, x_left + Inches(0.12), y_top + Inches(4.7), card_w - Inches(0.24), Inches(0.95), LGRAY, BORDER_C)
        vtx = slide.shapes.add_textbox(x_left + Inches(0.16), y_top + Inches(4.74), card_w - Inches(0.32), Inches(0.85))
        vtx.text_frame.word_wrap = True
        vp = vtx.text_frame.paragraphs[0]
        vr1 = vp.add_run()
        vr1.text = "💡 Business Impact:\n"
        vr1.font.size = Pt(8.5)
        vr1.font.bold = True
        vr1.font.color.rgb = b["color"]
        vr2 = vp.add_run()
        vr2.text = b["value_prop"]
        vr2.font.size = Pt(8)
        vr2.font.color.rgb = TEXT_MUTED


# ==============================================================================
# SLIDE 4: End-to-End Solution Architecture & User Journey
# ==============================================================================
def make_slide_4(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = LGRAY
    add_header(slide, "Solution Architecture & One-Sitting User Journey", "Slide 4 of 7")

    # Left: 4-Tier Enterprise Architecture
    add_rounded_card(slide, Inches(0.5), Inches(1.1), Inches(6.0), Inches(5.85), CARD_BG, BORDER_C)
    add_shape_rect(slide, Inches(0.5), Inches(1.1), Inches(6.0), Inches(0.45), NAVY)
    th1 = slide.shapes.add_textbox(Inches(0.7), Inches(1.12), Inches(5.6), Inches(0.4))
    r = th1.text_frame.paragraphs[0].add_run()
    r.text = "🏗️ 4-Tier Scalable Solution Architecture"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = WHITE

    tiers = [
        ("Presentation Layer", "Responsive HTML5/JS Web App, Airtel Theme, Web Speech API (Multilingual Voice in EN/HI/TA)", RED),
        ("Application & API Gateway", "Modular Flask REST Framework, Advisor Engine, KYC Verification Service, Order Lifecycle Tracker", NAVY),
        ("Intelligence & Decision Layer", "GenAI Rule Engine, Random Forest Propensity Classifier (AUC 0.645, 12 features), 12-Check KYC Engine", BLUE),
        ("Data & Compliance Vault", "Mock GSTIN & Udyam Registries (6,200+ records), DPDP Act 2023 Consent Audit Logs, AES-256 Storage", GREEN),
    ]
    ty = Inches(1.7)
    for title, desc, color in tiers:
        tbox = add_rounded_card(slide, Inches(0.7), ty, Inches(5.6), Inches(1.08), LGRAY, color)
        tx = slide.shapes.add_textbox(Inches(0.85), ty + Inches(0.08), Inches(5.3), Inches(0.95))
        tf = tx.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        r1 = p1.add_run()
        r1.text = "⚡ " + title + "\n"
        r1.font.size = Pt(10.5)
        r1.font.bold = True
        r1.font.color.rgb = color
        r2 = p1.add_run()
        r2.text = desc
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = TEXT_DARK
        ty += Inches(1.28)

    # Right: The 5-Step Rapid Onboarding Flow
    add_rounded_card(slide, Inches(6.8), Inches(1.1), Inches(6.0), Inches(5.85), CARD_BG, BORDER_C)
    add_shape_rect(slide, Inches(6.8), Inches(1.1), Inches(6.0), Inches(0.45), RED)
    th2 = slide.shapes.add_textbox(Inches(7.0), Inches(1.12), Inches(5.6), Inches(0.4))
    r = th2.text_frame.paragraphs[0].add_run()
    r.text = "🚀 One-Sitting Customer Journey (< 10 Minutes)"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = WHITE

    steps = [
        ("Step 1: Voice / Text Needs Discovery", "SMB owner speaks in Hindi, Tamil, or English; AI matches archetype & formulates customized proposal in <7 seconds."),
        ("Step 2: Instant Transparent Quote", "Auto-applies bundle discounts (10–18%), computes 18% GST itemization, and outputs branded PDF summary & WhatsApp quote."),
        ("Step 3: Instant Registry Pre-fill", "Live lookup against GSTIN & Udyam registries pre-fills enterprise name, constitution, and authorized signatories without manual entry."),
        ("Step 4: Smart Specimen KYC Verification", "Rule-based document validation checks blur, skew, 90-day recency, Mod-36 checksum, and signatory authority in seconds."),
        ("Step 5: Order Dispatch & Real-Time Tracking", "Generates Order ID, dispatches hardware, allocates field installation engineer, and provides customer self-serve tracker."),
    ]
    sy = Inches(1.68)
    for title, desc in steps:
        sbox = add_rounded_card(slide, Inches(7.0), sy, Inches(5.6), Inches(0.92), RGBColor(0xFE, 0xF2, 0xF2), RED)
        tx = slide.shapes.add_textbox(Inches(7.15), sy + Inches(0.06), Inches(5.3), Inches(0.8))
        tf = tx.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        r1 = p1.add_run()
        r1.text = title + "\n"
        r1.font.size = Pt(10)
        r1.font.bold = True
        r1.font.color.rgb = RED
        r2 = p1.add_run()
        r2.text = desc
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = TEXT_DARK
        sy += Inches(1.02)


# ==============================================================================
# SLIDE 5: GenAI Multilingual Advisor & Smart KYC (DPDP Compliant)
# ==============================================================================
def make_slide_5(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = LGRAY
    add_header(slide, "Core Innovations: GenAI Advisor & Smart KYC Engine", "Slide 5 of 7")

    # Left: GenAI Multilingual Advisor
    add_rounded_card(slide, Inches(0.5), Inches(1.1), Inches(6.0), Inches(5.85), CARD_BG, BORDER_C)
    add_shape_rect(slide, Inches(0.5), Inches(1.1), Inches(6.0), Inches(0.45), RED)
    th1 = slide.shapes.add_textbox(Inches(0.7), Inches(1.12), Inches(5.6), Inches(0.4))
    r = th1.text_frame.paragraphs[0].add_run()
    r.text = "🎙️ GenAI Multilingual Advisor"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = WHITE

    adv_features = [
        ("Voice-First Consultation (Web Speech API)", "Micro-entrepreneurs often prefer speaking over typing. Supports real-time speech-to-text in English, Hindi, and Tamil."),
        ("Archetype-Driven Semantic Engine", "Maps informal prompts (e.g., 'mujhe payment machine aur fast internet chahiye') into structured B2B SKUs in <7 seconds."),
        ("Multi-Lingual Business Rationales", "Generates personalized, non-technical value rationales explaining expected ROI in the customer's native tongue."),
        ("One-Click Bundle Hand-Off", "Recommended bundle instantly populates Quote Builder with exact SKUs, contract tenure, and promotional pricing."),
    ]
    ay = Inches(1.7)
    for title, desc in adv_features:
        add_rounded_card(slide, Inches(0.7), ay, Inches(5.6), Inches(1.1), LGRAY, RED)
        tx = slide.shapes.add_textbox(Inches(0.85), ay + Inches(0.08), Inches(5.3), Inches(0.95))
        tf = tx.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        r1 = p1.add_run()
        r1.text = "✓ " + title + "\n"
        r1.font.size = Pt(10)
        r1.font.bold = True
        r1.font.color.rgb = RED
        r2 = p1.add_run()
        r2.text = desc
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = TEXT_MUTED
        ay += Inches(1.25)

    # Right: Smart KYC & DPDP Compliance
    add_rounded_card(slide, Inches(6.8), Inches(1.1), Inches(6.0), Inches(5.85), CARD_BG, BORDER_C)
    add_shape_rect(slide, Inches(6.8), Inches(1.1), Inches(6.0), Inches(0.45), NAVY)
    th2 = slide.shapes.add_textbox(Inches(7.0), Inches(1.12), Inches(5.6), Inches(0.4))
    r = th2.text_frame.paragraphs[0].add_run()
    r.text = "🛡️ Smart KYC Pipeline & DPDP Compliance"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = WHITE

    # Specimen Summary Pill
    add_rounded_card(slide, Inches(7.0), Inches(1.68), Inches(5.6), Inches(0.75), RGBColor(0xEC, 0xFD, 0xF5), GREEN)
    tx_spec = slide.shapes.add_textbox(Inches(7.1), Inches(1.72), Inches(5.4), Inches(0.7))
    tsp = tx_spec.text_frame.paragraphs[0]
    tspr1 = tsp.add_run()
    tspr1.text = "Verified Against All 12 Hackathon KYC Specimen Files (K01–K12):\n"
    tspr1.font.size = Pt(9.5)
    tspr1.font.bold = True
    tspr1.font.color.rgb = GREEN
    tspr2 = tsp.add_run()
    tspr2.text = "• K03 (Pvt Ltd) & K12 (NE Proprietorship) APPROVED (94% & 91% Trust Score)\n• K01, K02, K04–K11 accurately flagged & REJECTED with specific compliance causes"
    tspr2.font.size = Pt(8.5)
    tspr2.font.color.rgb = TEXT_DARK

    kyc_checks = [
        ("Algorithmic Verification", "Mod-36 GSTIN checksum validation, PAN entity code checking, Laplacien variance blur detection, Hough skew detection."),
        ("Registry Cross-Verification", "Real-time automated reconciliation against mock GSTIN (3,534 records) & Udyam (2,723 records) registries."),
        ("Signatory Governance", "Validates board resolutions, MOA signatory authority, partner consents, and power-of-attorney documentation."),
        ("DPDP Act 2023 Compliance", "AES-256 encryption at rest, TLS 1.3 in transit, explicit consent capture, purpose limitation, and full audit trails."),
    ]
    ky = Inches(2.55)
    for title, desc in kyc_checks:
        add_rounded_card(slide, Inches(7.0), ky, Inches(5.6), Inches(0.95), LGRAY, BLUE)
        tx = slide.shapes.add_textbox(Inches(7.15), ky + Inches(0.06), Inches(5.3), Inches(0.85))
        tf = tx.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        r1 = p1.add_run()
        r1.text = "🔒 " + title + "\n"
        r1.font.size = Pt(9.5)
        r1.font.bold = True
        r1.font.color.rgb = BLUE
        r2 = p1.add_run()
        r2.text = desc
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = TEXT_MUTED
        ky += Inches(1.05)


# ==============================================================================
# SLIDE 6: Partner CRM, ML Propensity Engine & Transparent Quote Builder
# ==============================================================================
def make_slide_6(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = LGRAY
    add_header(slide, "Partner CRM, ML Propensity & Transparent Quote Builder", "Slide 6 of 7")

    # Left: Partner CRM & ML Propensity Engine
    add_rounded_card(slide, Inches(0.5), Inches(1.1), Inches(6.0), Inches(5.85), CARD_BG, BORDER_C)
    add_shape_rect(slide, Inches(0.5), Inches(1.1), Inches(6.0), Inches(0.45), NAVY)
    th1 = slide.shapes.add_textbox(Inches(0.7), Inches(1.12), Inches(5.6), Inches(0.4))
    r = th1.text_frame.paragraphs[0].add_run()
    r.text = "🎯 Partner CRM & ML Propensity Engine"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = WHITE

    crm_details = [
        ("Trained Random Forest Classifier (AUC 0.645)", "Trained on smb_leads.csv (5,000 leads) utilizing 12 engineered features: business sector, employee size, inquiry channel, engagement velocity, and city circle."),
        ("3-Tier Propensity Scoring", "Categorizes every incoming inquiry into High, Medium, or Low Propensity with estimated probability of activation within 30 days."),
        ("Automated Next-Best-Action (NBA) Prescriptions", "High Propensity: Priority RM phone call within 2 hours with bundled discount.\nMedium Propensity: Automated WhatsApp catalog & customer case study.\nLow Propensity: Nurture email sequence with educational video guides."),
        ("Sales Channel Enablement", "Provides field channel partners with real-time conversion insights, pending document alerts, and commission visibility."),
    ]
    cy = Inches(1.7)
    for title, desc in crm_details:
        add_rounded_card(slide, Inches(0.7), cy, Inches(5.6), Inches(1.12), LGRAY, NAVY)
        tx = slide.shapes.add_textbox(Inches(0.85), cy + Inches(0.06), Inches(5.3), Inches(1.0))
        tf = tx.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        r1 = p1.add_run()
        r1.text = "⚡ " + title + "\n"
        r1.font.size = Pt(9.5)
        r1.font.bold = True
        r1.font.color.rgb = NAVY
        r2 = p1.add_run()
        r2.text = desc
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = TEXT_MUTED
        cy += Inches(1.24)

    # Right: Transparent Quote Builder & Order Tracker
    add_rounded_card(slide, Inches(6.8), Inches(1.1), Inches(6.0), Inches(5.85), CARD_BG, BORDER_C)
    add_shape_rect(slide, Inches(6.8), Inches(1.1), Inches(6.0), Inches(0.45), RED)
    th2 = slide.shapes.add_textbox(Inches(7.0), Inches(1.12), Inches(5.6), Inches(0.4))
    r = th2.text_frame.paragraphs[0].add_run()
    r.text = "🧾 Quote Builder & Real-Time Order Tracker"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = WHITE

    quote_details = [
        ("Full 25-Product Enterprise Catalog", "Connectivity, Cloud SaaS, Cyber Security, IoT, and Collaboration SKUs clearly priced with no hidden charges."),
        ("Automated GST & Bundle Discount Engine", "Instant calculation of 18% GST (CGST + SGST / IGST) and applied volume savings so the customer sees the exact out-of-pocket figure."),
        ("Instant Digital Contract Generation", "Creates tamper-evident contract agreement with digital e-sign option, eliminating paper couriers and physical signature delays."),
        ("Zero-Chase Real-Time Order Tracking", "Customer receives SMS/WhatsApp order link with 5 live milestones (Order Placed → Feasibility → KYC → Hardware Dispatch → Line Live) and SLA alerts."),
    ]
    qy = Inches(1.7)
    for title, desc in quote_details:
        add_rounded_card(slide, Inches(7.0), qy, Inches(5.6), Inches(1.12), LGRAY, RED)
        tx = slide.shapes.add_textbox(Inches(7.15), qy + Inches(0.06), Inches(5.3), Inches(1.0))
        tf = tx.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        r1 = p1.add_run()
        r1.text = "✓ " + title + "\n"
        r1.font.size = Pt(9.5)
        r1.font.bold = True
        r1.font.color.rgb = RED
        r2 = p1.add_run()
        r2.text = desc
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = TEXT_MUTED
        qy += Inches(1.24)


# ==============================================================================
# SLIDE 7: Business Impact, Unit Economics & 90-Day Pan-India Roadmap
# ==============================================================================
def make_slide_7(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = LGRAY
    add_header(slide, "Business Impact, Unit Economics & 90-Day Execution Roadmap", "Slide 7 of 7")

    # Left: Impact & Unit Economics Table
    add_rounded_card(slide, Inches(0.5), Inches(1.1), Inches(6.0), Inches(5.85), CARD_BG, BORDER_C)
    add_shape_rect(slide, Inches(0.5), Inches(1.1), Inches(6.0), Inches(0.45), NAVY)
    th1 = slide.shapes.add_textbox(Inches(0.7), Inches(1.12), Inches(5.6), Inches(0.4))
    r = th1.text_frame.paragraphs[0].add_run()
    r.text = "📈 Measurable Business Impact & ROI"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = WHITE

    metrics = [
        ("Customer Acquisition Cost", "₹15,000", "₹2,450", "-83.7%", GREEN),
        ("Lead-to-Activation Latency", "17.6 Days", "< 24 Hours", "-95.0%", GREEN),
        ("Funnel Conversion Rate", "7.36%", "28.0%", "+3.8x", RED),
        ("Status Inquiries per Deal", "3.0 Calls", "0 Calls (Self-Serve)", "-100%", GREEN),
        ("6-Month Post-Sale Churn", "11.2%", "< 4.0%", "-64.3%", GREEN),
        ("Activated SMBs / 5k Cohort", "368 MSMEs", "1,400 MSMEs", "+1,032 MSMEs", RED),
    ]

    # Table Header
    my = Inches(1.68)
    add_shape_rect(slide, Inches(0.7), my, Inches(5.6), Inches(0.32), DARK_CARD)
    tx_th = slide.shapes.add_textbox(Inches(0.7), my, Inches(5.6), Inches(0.32))
    p_th = tx_th.text_frame.paragraphs[0]
    p_th.add_run().text = "Metric                          Baseline       Target       Delta"
    p_th.runs[0].font.size = Pt(9)
    p_th.runs[0].font.bold = True
    p_th.runs[0].font.color.rgb = WHITE

    my += Inches(0.35)
    for idx, (name, base, target, delta, col) in enumerate(metrics):
        row_bg = LGRAY if (idx % 2 == 0) else CARD_BG
        add_shape_rect(slide, Inches(0.7), my, Inches(5.6), Inches(0.46), row_bg)
        tx = slide.shapes.add_textbox(Inches(0.8), my + Inches(0.04), Inches(5.4), Inches(0.4))
        p = tx.text_frame.paragraphs[0]
        r1 = p.add_run()
        r1.text = f"{name:<24} {base:<12} {target:<12} "
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = TEXT_DARK
        r2 = p.add_run()
        r2.text = delta
        r2.font.size = Pt(8.5)
        r2.font.bold = True
        r2.font.color.rgb = col
        my += Inches(0.48)

    # ROI Summary Block
    add_rounded_card(slide, Inches(0.7), Inches(4.9), Inches(5.6), Inches(1.85), NAVY, GOLD)
    tx_roi = slide.shapes.add_textbox(Inches(0.85), Inches(4.98), Inches(5.3), Inches(1.7))
    tf_roi = tx_roi.text_frame
    tf_roi.word_wrap = True
    p_roi = tf_roi.paragraphs[0]
    rr1 = p_roi.add_run()
    rr1.text = "💰 Annualized Value Creation for Airtel:\n"
    rr1.font.size = Pt(11)
    rr1.font.bold = True
    rr1.font.color.rgb = GOLD
    rr2 = p_roi.add_run()
    rr2.text = "• CAC Savings: (₹15,000 - ₹2,450) × 1,400 activations = ₹1.75 Cr per 5,000 leads.\n" \
               "• Recurring ARR Boost: +1,032 incremental SMBs @ ₹2,500/mo avg = ₹3.10 Cr ARR.\n" \
               "• Scaled to 100,000 Annual Leads: ₹35+ Cr CAC reduction + ₹62+ Cr added ARR."
    rr2.font.size = Pt(8.5)
    rr2.font.color.rgb = WHITE

    # Right: 90-Day Execution Roadmap & Final Links
    add_rounded_card(slide, Inches(6.8), Inches(1.1), Inches(6.0), Inches(5.85), CARD_BG, BORDER_C)
    add_shape_rect(slide, Inches(6.8), Inches(1.1), Inches(6.0), Inches(0.45), RED)
    th2 = slide.shapes.add_textbox(Inches(7.0), Inches(1.12), Inches(5.6), Inches(0.4))
    r = th2.text_frame.paragraphs[0].add_run()
    r.text = "🗓️ 90-Day Execution Roadmap & Rollout"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = WHITE

    phases = [
        ("Days 1–30: Pilot in 5 Metro Circles", "Deploy in Mumbai, Delhi-NCR, Bengaluru, Hyderabad, and Chennai. Train 150 Airtel Partner RMs; onboard first 1,000 SMBs; refine OCR models.", RED),
        ("Days 31–60: Tier-2 Circle Expansion", "Scale across 25 Tier-2 cities (Pune, Ahmedabad, Jaipur, Lucknow, Kochi, etc.). Integrate with Airtel BSS billing engine and CRM API.", BLUE),
        ("Days 61–90: Pan-India General Rollout", "Activate across all 22 Airtel telecom circles. Launch customer self-onboarding web portal alongside partner assisted channel.", GREEN),
    ]
    ry = Inches(1.68)
    for title, desc, col in phases:
        add_rounded_card(slide, Inches(7.0), ry, Inches(5.6), Inches(0.96), LGRAY, col)
        tx = slide.shapes.add_textbox(Inches(7.15), ry + Inches(0.06), Inches(5.3), Inches(0.85))
        tf = tx.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        r1 = p1.add_run()
        r1.text = "🚩 " + title + "\n"
        r1.font.size = Pt(9.5)
        r1.font.bold = True
        r1.font.color.rgb = col
        r2 = p1.add_run()
        r2.text = desc
        r2.font.size = Pt(8)
        r2.font.color.rgb = TEXT_DARK
        ry += Inches(1.08)

    # Submission Action Card with Video Link
    cta_box = add_rounded_card(slide, Inches(7.0), Inches(5.05), Inches(5.6), Inches(1.7), DARK_CARD, GOLD)
    cta_box.click_action.hyperlink.address = VIDEO_LINK
    tx_cta = slide.shapes.add_textbox(Inches(7.15), Inches(5.12), Inches(5.3), Inches(1.55))
    tx_cta.click_action.hyperlink.address = VIDEO_LINK
    tf_cta = tx_cta.text_frame
    tf_cta.word_wrap = True
    p_cta = tf_cta.paragraphs[0]
    cr1 = p_cta.add_run()
    cr1.text = "🎥 REVIEWER ACTION: WATCH PRODUCT DEMONSTRATION\n"
    cr1.font.size = Pt(10.5)
    cr1.font.bold = True
    cr1.font.color.rgb = GOLD
    cr2 = p_cta.add_run()
    cr2.text = "▶ Click here to view the official Google Drive Video Demonstration\n"
    cr2.font.size = Pt(9.5)
    cr2.font.bold = True
    cr2.font.color.rgb = WHITE
    cr2.font.underline = True
    cr2.hyperlink.address = VIDEO_LINK
    cr3 = p_cta.add_run()
    cr3.text = "\nZero paper. Zero manual delays. Making MSMEs go digital in one sitting."
    cr3.font.size = Pt(8.5)
    cr3.font.italic = True
    cr3.font.color.rgb = RGBColor(0x9C, 0xA3, 0xAF)


# ==============================================================================
# MAIN EXPORT LOGIC (Generates both PPTX and PDF)
# ==============================================================================
def generate_7_slide_deck():
    prs = Presentation()
    prs.slide_width = SW
    prs.slide_height = SH

    make_slide_1(prs)
    make_slide_2(prs)
    make_slide_3(prs)
    make_slide_4(prs)
    make_slide_5(prs)
    make_slide_6(prs)
    make_slide_7(prs)

    pptx_path_main = os.path.join(BASE_DIR, "Business_Case_Presentation.pptx")
    pptx_path_7slide = os.path.join(BASE_DIR, "Project_Udyam_Digital_7_Slides.pptx")

    prs.save(pptx_path_main)
    prs.save(pptx_path_7slide)
    print(f"[OK] Saved PPTX to: {pptx_path_main} ({os.path.getsize(pptx_path_main):,} bytes)")
    print(f"[OK] Saved PPTX to: {pptx_path_7slide} ({os.path.getsize(pptx_path_7slide):,} bytes)")

    # Convert to PDF using PowerPoint automation
    pdf_path_main = os.path.join(BASE_DIR, "Business_Case_Presentation.pdf")
    pdf_path_7slide = os.path.join(BASE_DIR, "Project_Udyam_Digital_7_Slides.pdf")

    # PowerShell converter script
    ps_script = f"""
$pptxPath = "{pptx_path_7slide}"
$pdfPath = "{pdf_path_7slide}"
$pdfPathMain = "{pdf_path_main}"

try {{
    $ppt = New-Object -ComObject PowerPoint.Application
    $pres = $ppt.Presentations.Open($pptxPath, [Microsoft.Office.Core.MsoTriState]::msoTrue, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse)
    # ppSaveAsPDF = 32
    $pres.SaveAs($pdfPath, 32)
    $pres.SaveAs($pdfPathMain, 32)
    $pres.Close()
    $ppt.Quit()
    Write-Host "[OK] PDF Conversion completed successfully!"
}} catch {{
    Write-Host "[WARN] COM Conversion failed: $_"
}}
"""
    ps_file = os.path.join(BASE_DIR, "convert_pptx_to_pdf.ps1")
    with open(ps_file, "w", encoding="utf-8") as f:
        f.write(ps_script)

    try:
        res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", ps_file], capture_output=True, text=True, timeout=30)
        print("PowerShell Output:", res.stdout)
    except Exception as e:
        print("Conversion exception:", e)

    if os.path.exists(ps_file):
        try:
            os.remove(ps_file)
        except Exception:
            pass

    return pptx_path_7slide, pdf_path_7slide


def create_business_case_deck(output_path=None):
    generate_7_slide_deck()
    return os.path.join(BASE_DIR, "Business_Case_Presentation.pptx")


def generate_presentation(output_path=None):
    generate_7_slide_deck()
    return os.path.join(BASE_DIR, "Business_Case_Presentation.pptx")


if __name__ == "__main__":
    generate_7_slide_deck()
