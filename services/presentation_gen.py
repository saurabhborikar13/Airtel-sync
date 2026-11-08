"""
Airtel SYNC Hackathon 2026 — Track A: Project Udyam Digital
Official 7-Slide Submission Presentation & PDF Generator
Team: CountDown_VNIT
Members: Saurabh Borikar, Anupam Ayush (VNIT Nagpur)
"""

import os
import sys
import subprocess
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO_PATH = os.path.join(BASE_DIR, "static", "images", "airtel_logo.png")
VIDEO_LINK = "https://drive.google.com/file/d/1TwcPl2c8KbH7sJIPwkrbOD9QJjv4vQ7D/view?usp=drive_link"
GITHUB_LINK = "https://github.com/saurabhborikar13/Airtel-sync"

# ── High-Contrast Executive Brand Palette ───────────────────────────────────────
RED          = RGBColor(0xE4, 0x00, 0x00)   # Official Airtel Red
RED_DARK     = RGBColor(0x99, 0x00, 0x00)   # Deep Vibrant Crimson (High-contrast)
RED_LIGHT    = RGBColor(0xFE, 0xF2, 0xF2)   # Soft Red Tint
NAVY_DEEP    = RGBColor(0x0A, 0x0F, 0x1D)   # Obsidian Navy
NAVY_CARD    = RGBColor(0x13, 0x1D, 0x31)   # Slate 850 Elevated Card
NAVY_LIGHT   = RGBColor(0x27, 0x36, 0x4E)   # Slate 700 Accent
GOLD         = RGBColor(0xFB, 0xBF, 0x24)   # Bright Amber Gold (Vibrant)
GOLD_DARK    = RGBColor(0xD9, 0x77, 0x06)   # Deep Gold
GOLD_LIGHT   = RGBColor(0xFF, 0xFB, 0xEB)   # Soft Amber Tint
GREEN        = RGBColor(0x05, 0x96, 0x69)   # Emerald Green
GREEN_LIGHT  = RGBColor(0xEC, 0xFD, 0xF5)   # Mint Light
BLUE         = RGBColor(0x25, 0x63, 0xEB)   # Electric Royal Blue
BLUE_CARD    = RGBColor(0x0C, 0x24, 0x48)   # Deep Sapphire Blue (High-contrast)
BLUE_LIGHT   = RGBColor(0xEF, 0xF6, 0xFF)   # Soft Sky Blue
WHITE        = RGBColor(0xFF, 0xFF, 0xFF)   # Pure White
PAGE_BG      = RGBColor(0xF8, 0xFA, 0xFC)   # Ultra Clean Background (Slate 50)
BORDER_LIGHT = RGBColor(0xE2, 0xE8, 0xF0)   # Clean Border (Slate 200)
TEXT_MAIN    = RGBColor(0x0F, 0x17, 0x2A)   # Heading Charcoal
TEXT_BODY    = RGBColor(0x33, 0x41, 0x55)   # Readable Body Slate
TEXT_MUTED   = RGBColor(0x64, 0x74, 0x8B)   # Secondary Gray
CYAN_ACCENT  = RGBColor(0x38, 0xBD, 0xF8)   # Tech Cyan Accent (Glowing)

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


def add_rounded_card(slide, x, y, w, h, fill_color, border_color=None, border_width=Pt(1.5)):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = border_width
    else:
        shape.line.fill.background()
    return shape


def add_logo(slide, x, y, w, h):
    if os.path.exists(LOGO_PATH):
        slide.shapes.add_picture(LOGO_PATH, x, y, width=w, height=h)


def add_header(slide, title_text, slide_num_str):
    # Top navigation banner
    add_shape_rect(slide, Inches(0), Inches(0), SW, Inches(0.85), NAVY_DEEP)
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
    cnt = slide.shapes.add_textbox(Inches(11.0), Inches(0.18), Inches(1.9), Inches(0.5))
    ctf = cnt.text_frame
    cp = ctf.paragraphs[0]
    cp.alignment = PP_ALIGN.RIGHT
    cpr = cp.add_run()
    cpr.text = slide_num_str
    cpr.font.size = Pt(11)
    cpr.font.bold = True
    cpr.font.color.rgb = WHITE

    # Footer Banner
    add_shape_rect(slide, Inches(0), Inches(6.96), SW, Inches(0.54), NAVY_DEEP)
    add_shape_rect(slide, Inches(0), Inches(6.96), SW, Inches(0.02), RED)

    # Left footer label: Team Name & Members clearly listed!
    ftx = slide.shapes.add_textbox(Inches(0.4), Inches(7.01), Inches(6.0), Inches(0.45))
    fp = ftx.text_frame.paragraphs[0]
    fpr = fp.add_run()
    fpr.text = "Team: CountDown_VNIT | Saurabh Borikar, Anupam Ayush · VNIT Nagpur"
    fpr.font.size = Pt(9.5)
    fpr.font.bold = True
    fpr.font.color.rgb = RGBColor(0xCB, 0xD5, 0xE1)

    # Right footer: DUAL PROMINENT ACTION BUTTONS (High-contrast, impossible to miss)
    # 1. Video Button
    btn_v = add_rounded_card(slide, Inches(6.6), Inches(7.01), Inches(3.1), Inches(0.44), RED_DARK, GOLD, Pt(1.5))
    btn_v.click_action.hyperlink.address = VIDEO_LINK
    v_tx = slide.shapes.add_textbox(Inches(6.6), Inches(7.02), Inches(3.1), Inches(0.42))
    v_tx.click_action.hyperlink.address = VIDEO_LINK
    vp = v_tx.text_frame.paragraphs[0]
    vp.alignment = PP_ALIGN.CENTER
    vr = vp.add_run()
    vr.text = "🎥 WATCH VIDEO DEMO"
    vr.font.size = Pt(9.5)
    vr.font.bold = True
    vr.font.color.rgb = WHITE
    vr.hyperlink.address = VIDEO_LINK

    # 2. GitHub Button
    btn_g = add_rounded_card(slide, Inches(9.9), Inches(7.01), Inches(3.1), Inches(0.44), BLUE_CARD, CYAN_ACCENT, Pt(1.5))
    btn_g.click_action.hyperlink.address = GITHUB_LINK
    g_tx = slide.shapes.add_textbox(Inches(9.9), Inches(7.02), Inches(3.1), Inches(0.42))
    g_tx.click_action.hyperlink.address = GITHUB_LINK
    gp = g_tx.text_frame.paragraphs[0]
    gp.alignment = PP_ALIGN.CENTER
    gr = gp.add_run()
    gr.text = "💻 VIEW GITHUB CODE"
    gr.font.size = Pt(9.5)
    gr.font.bold = True
    gr.font.color.rgb = CYAN_ACCENT
    gr.hyperlink.address = GITHUB_LINK


# ==============================================================================
# SLIDE 1: Title & Executive Overview + Live Submission Links
# ==============================================================================
def make_slide_1(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = NAVY_DEEP

    # Left vertical red accent bar
    add_shape_rect(slide, Inches(0), Inches(0), Inches(0.2), SH, RED)

    # Official Airtel Logo Top Left
    add_logo(slide, Inches(0.75), Inches(0.35), Inches(2.1), Inches(1.1))

    # Header category badge
    add_rounded_card(slide, Inches(3.0), Inches(0.42), Inches(4.3), Inches(0.42), RED)
    tx = slide.shapes.add_textbox(Inches(3.0), Inches(0.43), Inches(4.3), Inches(0.4))
    p = tx.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "AIRTEL SYNC HACKATHON 2026 · TRACK A"
    r.font.size = Pt(10.5)
    r.font.bold = True
    r.font.color.rgb = WHITE

    # 🏆 PROMINENT TEAM BADGE TOP RIGHT (CountDown_VNIT)
    t_card = add_rounded_card(slide, Inches(7.5), Inches(0.35), Inches(5.1), Inches(1.15), NAVY_CARD, GOLD, Pt(2))
    t_box = slide.shapes.add_textbox(Inches(7.65), Inches(0.4), Inches(4.8), Inches(1.05))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    
    tp1 = tf_t.paragraphs[0]
    tr1 = tp1.add_run()
    tr1.text = "🏆 TEAM: CountDown_VNIT\n"
    tr1.font.size = Pt(13)
    tr1.font.bold = True
    tr1.font.color.rgb = GOLD

    tp2 = tf_t.add_paragraph()
    tr2 = tp2.add_run()
    tr2.text = "👥 Saurabh Borikar  |  Anupam Ayush\n"
    tr2.font.size = Pt(11)
    tr2.font.bold = True
    tr2.font.color.rgb = WHITE

    tp3 = tf_t.add_paragraph()
    tr3 = tp3.add_run()
    tr3.text = "Visvesvaraya National Institute of Technology (VNIT Nagpur)"
    tr3.font.size = Pt(9)
    tr3.font.color.rgb = CYAN_ACCENT

    # Main Project Title
    tbox = slide.shapes.add_textbox(Inches(0.75), Inches(1.62), Inches(11.8), Inches(1.05))
    tp = tbox.text_frame.paragraphs[0]
    tr = tp.add_run()
    tr.text = "PROJECT UDYAM DIGITAL"
    tr.font.size = Pt(44)
    tr.font.bold = True
    tr.font.color.rgb = WHITE

    # Subtitle
    tp2 = tbox.text_frame.add_paragraph()
    tr2 = tp2.add_run()
    tr2.text = "Making Small Businesses Go Digital in One Sitting (< 24 Hours) — Connectivity, Cloud SaaS & Smart KYC"
    tr2.font.size = Pt(15.5)
    tr2.font.color.rgb = RGBColor(0xCB, 0xD5, 0xE1)

    # 4 Key Performance Metrics Cards
    kpis = [
        ("₹2,450", "Target CAC", "-83.7% from ₹15,000", RED),
        ("< 24 Hours", "Activation Latency", "-95% from 17.6 days", GREEN),
        ("28.0%", "Funnel Conversion", "3.8x uplift from 7.36%", GOLD),
        ("0 Calls", "Status Chases", "100% self-serve tracking", BLUE),
    ]
    card_w = Inches(2.7)
    card_h = Inches(1.4)
    start_x = Inches(0.75)
    card_y = Inches(2.85)

    for i, (val, title, note, color) in enumerate(kpis):
        cx = start_x + i * Inches(2.95)
        add_rounded_card(slide, cx, card_y, card_w, card_h, NAVY_CARD, color, Pt(1.5))
        
        tx = slide.shapes.add_textbox(cx, card_y + Inches(0.08), card_w, Inches(0.55))
        p = tx.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = val
        r.font.size = Pt(25)
        r.font.bold = True
        r.font.color.rgb = color

        tx2 = slide.shapes.add_textbox(cx, card_y + Inches(0.65), card_w, Inches(0.35))
        p2 = tx2.text_frame.paragraphs[0]
        p2.alignment = PP_ALIGN.CENTER
        r2 = p2.add_run()
        r2.text = title
        r2.font.size = Pt(11.5)
        r2.font.bold = True
        r2.font.color.rgb = WHITE

        tx3 = slide.shapes.add_textbox(cx, card_y + Inches(0.98), card_w, Inches(0.35))
        p3 = tx3.text_frame.paragraphs[0]
        p3.alignment = PP_ALIGN.CENTER
        r3 = p3.add_run()
        r3.text = note
        r3.font.size = Pt(9.5)
        r3.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)

    # ── HIGH-VISIBILITY HERO LINKS CONTAINER (Seen at First Glance) ─────────────
    hero_y = Inches(4.45)
    add_rounded_card(slide, Inches(0.75), hero_y, Inches(11.85), Inches(2.45), NAVY_CARD, RED, Pt(2.5))

    # Header label for deliverables
    h_label = slide.shapes.add_textbox(Inches(0.95), hero_y + Inches(0.08), Inches(11.4), Inches(0.38))
    hlp = h_label.text_frame.paragraphs[0]
    hlr = hlp.add_run()
    hlr.text = "⚡ SUBMISSION DELIVERABLES — LIVE INTERACTIVE LINKS (CLICK AT FIRST GLANCE)"
    hlr.font.size = Pt(12)
    hlr.font.bold = True
    hlr.font.color.rgb = GOLD

    # Button 1: VIDEO DEMO (Crimson Card with Gold Border & White/Gold Text)
    vbox = add_rounded_card(slide, Inches(0.95), hero_y + Inches(0.5), Inches(5.65), Inches(1.8), RED_DARK, GOLD, Pt(3))
    vbox.click_action.hyperlink.address = VIDEO_LINK
    vtx = slide.shapes.add_textbox(Inches(1.1), hero_y + Inches(0.58), Inches(5.35), Inches(1.65))
    vtx.click_action.hyperlink.address = VIDEO_LINK
    
    vp1 = vtx.text_frame.paragraphs[0]
    vr1 = vp1.add_run()
    vr1.text = "🎥 PRODUCT DEMONSTRATION VIDEO\n"
    vr1.font.size = Pt(14)
    vr1.font.bold = True
    vr1.font.color.rgb = GOLD

    vp2 = vtx.text_frame.add_paragraph()
    vr2 = vp2.add_run()
    vr2.text = "▶ CLICK HERE TO WATCH ON GOOGLE DRIVE\n"
    vr2.font.size = Pt(11.5)
    vr2.font.bold = True
    vr2.font.color.rgb = WHITE
    vr2.font.underline = True
    vr2.hyperlink.address = VIDEO_LINK

    vp3 = vtx.text_frame.add_paragraph()
    vr3 = vp3.add_run()
    vr3.text = "End-to-end walkthrough: Multilingual AI Advisor, 12 Smart KYC specs & CRM"
    vr3.font.size = Pt(9.5)
    vr3.font.color.rgb = RGBColor(0xFE, 0xF0, 0x8A)

    # Button 2: GITHUB REPO (Deep Sapphire Card with Cyan Border & White/Cyan Text)
    gbox = add_rounded_card(slide, Inches(6.8), hero_y + Inches(0.5), Inches(5.65), Inches(1.8), BLUE_CARD, CYAN_ACCENT, Pt(3))
    gbox.click_action.hyperlink.address = GITHUB_LINK
    gtx = slide.shapes.add_textbox(Inches(6.95), hero_y + Inches(0.58), Inches(5.35), Inches(1.65))
    gtx.click_action.hyperlink.address = GITHUB_LINK
    
    gp1 = gtx.text_frame.paragraphs[0]
    gr1 = gp1.add_run()
    gr1.text = "💻 GITHUB SOURCE CODE REPOSITORY\n"
    gr1.font.size = Pt(14)
    gr1.font.bold = True
    gr1.font.color.rgb = CYAN_ACCENT

    gp2 = gtx.text_frame.add_paragraph()
    gr2 = gp2.add_run()
    gr2.text = "▶ CLICK HERE: github.com/saurabhborikar13/Airtel-sync\n"
    gr2.font.size = Pt(11)
    gr2.font.bold = True
    gr2.font.color.rgb = WHITE
    gr2.font.underline = True
    gr2.hyperlink.address = GITHUB_LINK

    gp3 = gtx.text_frame.add_paragraph()
    gr3 = gp3.add_run()
    gr3.text = "Full Flask codebase, trained Random Forest ML model (AUC 0.645) & DPDP docs"
    gr3.font.size = Pt(9.5)
    gr3.font.color.rgb = RGBColor(0xBA, 0xE6, 0xFD)

    # Footer note
    ft = slide.shapes.add_textbox(Inches(0.75), Inches(7.02), Inches(11.85), Inches(0.35))
    ftp = ft.text_frame.paragraphs[0]
    ftp.alignment = PP_ALIGN.RIGHT
    ftpr = ftp.add_run()
    ftpr.text = "Team CountDown_VNIT (Saurabh Borikar & Anupam Ayush) · Bharti Airtel Ltd. · Track A"
    ftpr.font.size = Pt(9.5)
    ftpr.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)


# ==============================================================================
# SLIDE 2: Problem Statement & MSME Market Opportunity
# ==============================================================================
def make_slide_2(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = PAGE_BG
    add_header(slide, "Market Opportunity & The SMB Friction Problem", "Slide 2 of 7")

    # Left: Market Opportunity Card
    add_rounded_card(slide, Inches(0.5), Inches(1.05), Inches(5.8), Inches(5.75), WHITE, BORDER_LIGHT)
    add_shape_rect(slide, Inches(0.5), Inches(1.05), Inches(5.8), Inches(0.45), RED)
    th1 = slide.shapes.add_textbox(Inches(0.7), Inches(1.07), Inches(5.4), Inches(0.4))
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
    y_off = Inches(1.65)
    for title, desc in points1:
        tx = slide.shapes.add_textbox(Inches(0.7), y_off, Inches(5.4), Inches(1.15))
        tf = tx.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        r1 = p1.add_run()
        r1.text = "• " + title + "\n"
        r1.font.size = Pt(11)
        r1.font.bold = True
        r1.font.color.rgb = TEXT_MAIN
        r2 = p1.add_run()
        r2.text = desc
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = TEXT_BODY
        y_off += Inches(1.2)

    # Right: The Baseline Friction & Funnel Breakdown
    add_rounded_card(slide, Inches(6.6), Inches(1.05), Inches(6.2), Inches(5.75), WHITE, BORDER_LIGHT)
    add_shape_rect(slide, Inches(6.6), Inches(1.05), Inches(6.2), Inches(0.45), NAVY_DEEP)
    th2 = slide.shapes.add_textbox(Inches(6.8), Inches(1.07), Inches(5.8), Inches(0.4))
    r = th2.text_frame.paragraphs[0].add_run()
    r.text = "⚠️ Current Funnel Reality (smb_leads.csv Baseline)"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = WHITE

    # Funnel Drop-off bars
    stages = [
        ("Total Inquiries / Leads", 5000, "100%", NAVY_DEEP),
        ("Contacted by Sales", 3406, "68.1%", NAVY_LIGHT),
        ("Interested in Demo", 1974, "39.5%", BLUE),
        ("Docs Submitted", 861, "17.2%", GOLD_DARK),
        ("KYC Approved", 588, "11.8%", RGBColor(0xEA, 0x58, 0x0C)),
        ("Activated & Billing", 368, "7.36%", RED),
    ]
    fy = Inches(1.65)
    for name, count, pct, col in stages:
        bar_w = Inches(3.2 * (count / 5000.0))
        # Name
        tx = slide.shapes.add_textbox(Inches(6.75), fy - Inches(0.05), Inches(2.2), Inches(0.4))
        p = tx.text_frame.paragraphs[0]
        pr = p.add_run()
        pr.text = name
        pr.font.size = Pt(9.5)
        pr.font.bold = True
        pr.font.color.rgb = TEXT_MAIN
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
    py = Inches(4.3)
    for title, sub in pains:
        add_rounded_card(slide, Inches(6.8), py, Inches(5.8), Inches(0.56), RED_LIGHT, RED, Pt(1))
        tx = slide.shapes.add_textbox(Inches(6.9), py + Inches(0.03), Inches(5.6), Inches(0.5))
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
        r2.font.color.rgb = TEXT_MAIN
        py += Inches(0.62)


# ==============================================================================
# SLIDE 3: 4 MSME Archetypes & Bundled Solutions
# ==============================================================================
def make_slide_3(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = PAGE_BG
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
            "badge_bg": RED_LIGHT
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
            "badge_bg": BLUE_LIGHT
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
            "badge_bg": GREEN_LIGHT
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
            "color": GOLD_DARK,
            "badge_bg": GOLD_LIGHT
        },
    ]

    card_w = Inches(2.85)
    card_h = Inches(5.75)
    y_top = Inches(1.05)

    for i, b in enumerate(bundles):
        x_left = Inches(0.5) + i * Inches(3.15)
        add_rounded_card(slide, x_left, y_top, card_w, card_h, WHITE, BORDER_LIGHT)

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
        add_rounded_card(slide, x_left + Inches(0.15), y_top + Inches(0.8), card_w - Inches(0.3), Inches(0.72), b["badge_bg"], b["color"], Pt(1))
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
        prh.font.color.rgb = TEXT_MAIN

        # Product list
        py = y_top + Inches(2.55)
        for prod in b["products"]:
            ptx = slide.shapes.add_textbox(x_left + Inches(0.15), py, card_w - Inches(0.3), Inches(0.48))
            ptx.text_frame.word_wrap = True
            pp_run = ptx.text_frame.paragraphs[0].add_run()
            pp_run.text = "✓ " + prod
            pp_run.font.size = Pt(8.5)
            pp_run.font.color.rgb = TEXT_BODY
            py += Inches(0.48)

        # Value Proposition Box
        add_rounded_card(slide, x_left + Inches(0.12), y_top + Inches(4.7), card_w - Inches(0.24), Inches(0.92), PAGE_BG, BORDER_LIGHT, Pt(1))
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
    slide.background.fill.fore_color.rgb = PAGE_BG
    add_header(slide, "Solution Architecture & One-Sitting User Journey", "Slide 4 of 7")

    # Left: 4-Tier Enterprise Architecture
    add_rounded_card(slide, Inches(0.5), Inches(1.05), Inches(6.0), Inches(5.75), WHITE, BORDER_LIGHT)
    add_shape_rect(slide, Inches(0.5), Inches(1.05), Inches(6.0), Inches(0.45), NAVY_DEEP)
    th1 = slide.shapes.add_textbox(Inches(0.7), Inches(1.07), Inches(5.6), Inches(0.4))
    r = th1.text_frame.paragraphs[0].add_run()
    r.text = "🏗️ 4-Tier Scalable Solution Architecture"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = WHITE

    tiers = [
        ("Presentation Layer", "Responsive HTML5/JS Web App, Airtel Theme, Web Speech API (Multilingual Voice in EN/HI/TA)", RED),
        ("Application & API Gateway", "Modular Flask REST Framework, Advisor Engine, KYC Verification Service, Order Lifecycle Tracker", NAVY_DEEP),
        ("Intelligence & Decision Layer", "GenAI Rule Engine, Random Forest Propensity Classifier (AUC 0.645, 12 features), 12-Check KYC Engine", BLUE),
        ("Data & Compliance Vault", "Mock GSTIN & Udyam Registries (6,200+ records), DPDP Act 2023 Consent Audit Logs, AES-256 Storage", GREEN),
    ]
    ty = Inches(1.65)
    for title, desc, color in tiers:
        add_rounded_card(slide, Inches(0.7), ty, Inches(5.6), Inches(1.08), PAGE_BG, color, Pt(1))
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
        r2.font.color.rgb = TEXT_BODY
        ty += Inches(1.26)

    # Right: The 5-Step Rapid Onboarding Flow
    add_rounded_card(slide, Inches(6.8), Inches(1.05), Inches(6.0), Inches(5.75), WHITE, BORDER_LIGHT)
    add_shape_rect(slide, Inches(6.8), Inches(1.05), Inches(6.0), Inches(0.45), RED)
    th2 = slide.shapes.add_textbox(Inches(7.0), Inches(1.07), Inches(5.6), Inches(0.4))
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
    sy = Inches(1.65)
    for title, desc in steps:
        add_rounded_card(slide, Inches(7.0), sy, Inches(5.6), Inches(0.92), RED_LIGHT, RED, Pt(1))
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
        r2.font.color.rgb = TEXT_MAIN
        sy += Inches(1.02)


# ==============================================================================
# SLIDE 5: GenAI Multilingual Advisor & Smart KYC (DPDP Compliant)
# ==============================================================================
def make_slide_5(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = PAGE_BG
    add_header(slide, "Core Innovations: GenAI Advisor & Smart KYC Engine", "Slide 5 of 7")

    # Left: GenAI Multilingual Advisor
    add_rounded_card(slide, Inches(0.5), Inches(1.05), Inches(6.0), Inches(5.75), WHITE, BORDER_LIGHT)
    add_shape_rect(slide, Inches(0.5), Inches(1.05), Inches(6.0), Inches(0.45), RED)
    th1 = slide.shapes.add_textbox(Inches(0.7), Inches(1.07), Inches(5.6), Inches(0.4))
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
    ay = Inches(1.65)
    for title, desc in adv_features:
        add_rounded_card(slide, Inches(0.7), ay, Inches(5.6), Inches(1.1), PAGE_BG, RED, Pt(1))
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
        ay += Inches(1.24)

    # Right: Smart KYC & DPDP Compliance
    add_rounded_card(slide, Inches(6.8), Inches(1.05), Inches(6.0), Inches(5.75), WHITE, BORDER_LIGHT)
    add_shape_rect(slide, Inches(6.8), Inches(1.05), Inches(6.0), Inches(0.45), NAVY_DEEP)
    th2 = slide.shapes.add_textbox(Inches(7.0), Inches(1.07), Inches(5.6), Inches(0.4))
    r = th2.text_frame.paragraphs[0].add_run()
    r.text = "🛡️ Smart KYC Pipeline & DPDP Compliance"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = WHITE

    # Specimen Summary Pill
    add_rounded_card(slide, Inches(7.0), Inches(1.65), Inches(5.6), Inches(0.75), GREEN_LIGHT, GREEN, Pt(1))
    tx_spec = slide.shapes.add_textbox(Inches(7.1), Inches(1.68), Inches(5.4), Inches(0.7))
    tsp = tx_spec.text_frame.paragraphs[0]
    tspr1 = tsp.add_run()
    tspr1.text = "Verified Against All 12 Hackathon KYC Specimen Files (K01–K12):\n"
    tspr1.font.size = Pt(9.5)
    tspr1.font.bold = True
    tspr1.font.color.rgb = GREEN
    tspr2 = tsp.add_run()
    tspr2.text = "• K03 (Pvt Ltd) & K12 (NE Proprietorship) APPROVED (94% & 91% Trust Score)\n• K01, K02, K04–K11 accurately flagged & REJECTED with specific compliance causes"
    tspr2.font.size = Pt(8.5)
    tspr2.font.color.rgb = TEXT_MAIN

    kyc_checks = [
        ("Algorithmic Verification", "Mod-36 GSTIN checksum validation, PAN entity code checking, Laplacian variance blur detection, Hough skew detection."),
        ("Registry Cross-Verification", "Real-time automated reconciliation against mock GSTIN (3,534 records) & Udyam (2,723 records) registries."),
        ("Signatory Governance", "Validates board resolutions, MOA signatory authority, partner consents, and power-of-attorney documentation."),
        ("DPDP Act 2023 Compliance", "AES-256 encryption at rest, TLS 1.3 in transit, explicit consent capture, purpose limitation, and full audit trails."),
    ]
    ky = Inches(2.52)
    for title, desc in kyc_checks:
        add_rounded_card(slide, Inches(7.0), ky, Inches(5.6), Inches(0.95), PAGE_BG, BLUE, Pt(1))
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
    slide.background.fill.fore_color.rgb = PAGE_BG
    add_header(slide, "Partner CRM, ML Propensity & Transparent Quote Builder", "Slide 6 of 7")

    # Left: Partner CRM & ML Propensity Engine
    add_rounded_card(slide, Inches(0.5), Inches(1.05), Inches(6.0), Inches(5.75), WHITE, BORDER_LIGHT)
    add_shape_rect(slide, Inches(0.5), Inches(1.05), Inches(6.0), Inches(0.45), NAVY_DEEP)
    th1 = slide.shapes.add_textbox(Inches(0.7), Inches(1.07), Inches(5.6), Inches(0.4))
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
    cy = Inches(1.65)
    for title, desc in crm_details:
        add_rounded_card(slide, Inches(0.7), cy, Inches(5.6), Inches(1.12), PAGE_BG, NAVY_DEEP, Pt(1))
        tx = slide.shapes.add_textbox(Inches(0.85), cy + Inches(0.06), Inches(5.3), Inches(1.0))
        tf = tx.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        r1 = p1.add_run()
        r1.text = "⚡ " + title + "\n"
        r1.font.size = Pt(9.5)
        r1.font.bold = True
        r1.font.color.rgb = NAVY_DEEP
        r2 = p1.add_run()
        r2.text = desc
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = TEXT_MUTED
        cy += Inches(1.24)

    # Right: Transparent Quote Builder & Order Tracker
    add_rounded_card(slide, Inches(6.8), Inches(1.05), Inches(6.0), Inches(5.75), WHITE, BORDER_LIGHT)
    add_shape_rect(slide, Inches(6.8), Inches(1.05), Inches(6.0), Inches(0.45), RED)
    th2 = slide.shapes.add_textbox(Inches(7.0), Inches(1.07), Inches(5.6), Inches(0.4))
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
    qy = Inches(1.65)
    for title, desc in quote_details:
        add_rounded_card(slide, Inches(7.0), qy, Inches(5.6), Inches(1.12), PAGE_BG, RED, Pt(1))
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
    slide.background.fill.fore_color.rgb = PAGE_BG
    add_header(slide, "Business Impact, Unit Economics & 90-Day Execution Roadmap", "Slide 7 of 7")

    # Left: Impact & Unit Economics Table
    add_rounded_card(slide, Inches(0.5), Inches(1.05), Inches(6.0), Inches(5.75), WHITE, BORDER_LIGHT)
    add_shape_rect(slide, Inches(0.5), Inches(1.05), Inches(6.0), Inches(0.45), NAVY_DEEP)
    th1 = slide.shapes.add_textbox(Inches(0.7), Inches(1.07), Inches(5.6), Inches(0.4))
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
    my = Inches(1.62)
    add_shape_rect(slide, Inches(0.7), my, Inches(5.6), Inches(0.32), NAVY_DEEP)
    tx_th = slide.shapes.add_textbox(Inches(0.7), my, Inches(5.6), Inches(0.32))
    p_th = tx_th.text_frame.paragraphs[0]
    p_th.add_run().text = "Metric                          Baseline       Target       Delta"
    p_th.runs[0].font.size = Pt(9)
    p_th.runs[0].font.bold = True
    p_th.runs[0].font.color.rgb = WHITE

    my += Inches(0.35)
    for idx, (name, base, target, delta, col) in enumerate(metrics):
        row_bg = PAGE_BG if (idx % 2 == 0) else WHITE
        add_shape_rect(slide, Inches(0.7), my, Inches(5.6), Inches(0.45), row_bg)
        tx = slide.shapes.add_textbox(Inches(0.8), my + Inches(0.04), Inches(5.4), Inches(0.4))
        p = tx.text_frame.paragraphs[0]
        r1 = p.add_run()
        r1.text = f"{name:<24} {base:<12} {target:<12} "
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = TEXT_MAIN
        r2 = p.add_run()
        r2.text = delta
        r2.font.size = Pt(8.5)
        r2.font.bold = True
        r2.font.color.rgb = col
        my += Inches(0.47)

    # ROI Summary Block
    add_rounded_card(slide, Inches(0.7), Inches(4.82), Inches(5.6), Inches(1.82), NAVY_DEEP, GOLD, Pt(1.5))
    tx_roi = slide.shapes.add_textbox(Inches(0.85), Inches(4.88), Inches(5.3), Inches(1.7))
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

    # Right: 90-Day Execution Roadmap & DUAL FINAL ACTION BUTTONS
    add_rounded_card(slide, Inches(6.8), Inches(1.05), Inches(6.0), Inches(5.75), WHITE, BORDER_LIGHT)
    add_shape_rect(slide, Inches(6.8), Inches(1.05), Inches(6.0), Inches(0.45), RED)
    th2 = slide.shapes.add_textbox(Inches(7.0), Inches(1.07), Inches(5.6), Inches(0.4))
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
    ry = Inches(1.62)
    for title, desc, col in phases:
        add_rounded_card(slide, Inches(7.0), ry, Inches(5.6), Inches(0.92), PAGE_BG, col, Pt(1))
        tx = slide.shapes.add_textbox(Inches(7.15), ry + Inches(0.05), Inches(5.3), Inches(0.82))
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
        r2.font.color.rgb = TEXT_MAIN
        ry += Inches(1.02)

    # ── FINAL JURY ACTION CONTAINER (Team CountDown_VNIT) ─────────────
    jury_y = Inches(4.78)
    add_rounded_card(slide, Inches(7.0), jury_y, Inches(5.6), Inches(1.86), NAVY_DEEP, GOLD, Pt(2))
    
    j_tx = slide.shapes.add_textbox(Inches(7.15), jury_y + Inches(0.05), Inches(5.3), Inches(0.35))
    jp = j_tx.text_frame.paragraphs[0]
    jr = jp.add_run()
    jr.text = "⭐ EVALUATION JURY ACTION — TEAM: CountDown_VNIT"
    jr.font.size = Pt(10)
    jr.font.bold = True
    jr.font.color.rgb = GOLD

    # Sub-card 1: Video Button
    cta_v = add_rounded_card(slide, Inches(7.15), jury_y + Inches(0.4), Inches(5.3), Inches(0.65), RED_DARK, GOLD, Pt(1.5))
    cta_v.click_action.hyperlink.address = VIDEO_LINK
    tv = slide.shapes.add_textbox(Inches(7.25), jury_y + Inches(0.42), Inches(5.1), Inches(0.6))
    tv.click_action.hyperlink.address = VIDEO_LINK
    tvp = tv.text_frame.paragraphs[0]
    tvr = tvp.add_run()
    tvr.text = "🎥 Watch Demo Video Walkthrough (Google Drive)\n"
    tvr.font.size = Pt(9.5)
    tvr.font.bold = True
    tvr.font.color.rgb = GOLD
    tvr2 = tvp.add_run()
    tvr2.text = "▶ Click here: drive.google.com/.../view"
    tvr2.font.size = Pt(8.5)
    tvr2.font.color.rgb = WHITE
    tvr2.font.underline = True
    tvr2.hyperlink.address = VIDEO_LINK

    # Sub-card 2: GitHub Button
    cta_g = add_rounded_card(slide, Inches(7.15), jury_y + Inches(1.1), Inches(5.3), Inches(0.65), BLUE_CARD, CYAN_ACCENT, Pt(1.5))
    cta_g.click_action.hyperlink.address = GITHUB_LINK
    tg = slide.shapes.add_textbox(Inches(7.25), jury_y + Inches(1.12), Inches(5.1), Inches(0.6))
    tg.click_action.hyperlink.address = GITHUB_LINK
    tgp = tg.text_frame.paragraphs[0]
    tgr = tgp.add_run()
    tgr.text = "💻 View Source Code & Architecture (GitHub)\n"
    tgr.font.size = Pt(9.5)
    tgr.font.bold = True
    tgr.font.color.rgb = CYAN_ACCENT
    tgr2 = tgp.add_run()
    tgr2.text = "▶ Click here: github.com/saurabhborikar13/Airtel-sync"
    tgr2.font.size = Pt(8.5)
    tgr2.font.color.rgb = WHITE
    tgr2.font.underline = True
    tgr2.hyperlink.address = GITHUB_LINK


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
    pptx_path_team = os.path.join(BASE_DIR, "Project_Udyam_Digital_CountDown_VNIT_7_Slides.pptx")

    # Safe save
    prs.save(pptx_path_main)
    prs.save(pptx_path_team)
    print(f"[OK] Saved PPTX to: {pptx_path_main} ({os.path.getsize(pptx_path_main):,} bytes)")
    print(f"[OK] Saved PPTX to: {pptx_path_team} ({os.path.getsize(pptx_path_team):,} bytes)")

    try:
        prs.save(pptx_path_7slide)
        print(f"[OK] Saved PPTX to: {pptx_path_7slide} ({os.path.getsize(pptx_path_7slide):,} bytes)")
    except PermissionError:
        print(f"[INFO] {pptx_path_7slide} is currently in use/viewed; updated {pptx_path_team} & {pptx_path_main}")

    # Convert to PDF using PowerPoint automation
    pdf_path_main = os.path.join(BASE_DIR, "Business_Case_Presentation.pdf")
    pdf_path_7slide = os.path.join(BASE_DIR, "Project_Udyam_Digital_7_Slides.pdf")
    pdf_path_team = os.path.join(BASE_DIR, "Project_Udyam_Digital_CountDown_VNIT_7_Slides.pdf")

    # Clean COM automation script using pptx_path_main (unlocked) as source
    ps_script = f"""
$pptxPath = "{pptx_path_main}"
$pdfPath = "{pdf_path_7slide}"
$pdfPathMain = "{pdf_path_main}"
$pdfPathTeam = "{pdf_path_team}"

try {{
    $ppt = New-Object -ComObject PowerPoint.Application
    $pres = $ppt.Presentations.Open($pptxPath, [Microsoft.Office.Core.MsoTriState]::msoTrue, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse)
    # ppSaveAsPDF = 32
    $pres.SaveAs($pdfPath, 32)
    $pres.SaveAs($pdfPathMain, 32)
    $pres.SaveAs($pdfPathTeam, 32)
    $pres.Close()
    $ppt.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($pres) | Out-Null
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($ppt) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
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
