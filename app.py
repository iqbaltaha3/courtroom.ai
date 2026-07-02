import streamlit as st
from graph.graph import court_graph
from datetime import datetime
import io
import textwrap
import time
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from evaluation.evaluator import SystemEvaluator
from auth import authenticate, submit_access_request

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="MyPeshkar - Never Miss a Tareekh.",
    page_icon="⚖",
    layout="wide"
)

# ============================================
# PROFESSIONAL CSS (Black, Gold & Pure White Theme)
# ============================================
st.markdown("""
<style>
    /* -------------------- MAIN BACKGROUND -------------------- */
    .stApp {
        background-color: #f5f7fa;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    }

    /* -------------------- SCROLLBAR -------------------- */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #eaedf2; }
    ::-webkit-scrollbar-thumb { background: #704214; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #4A2C1A; }

    /* -------------------- HEADER -------------------- */
    .court-header {
        background: linear-gradient(135deg, #704214 0%, #4A2C1A 100%);
        padding: 2.5rem 2.5rem;
        border-radius: 8px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 16px rgba(107, 83, 68, 0.25);
    }
    .court-header h1 {
        font-size: 56px;
        font-weight: 300;
        font-family: 'Brush Script MT', 'Lucida Handwriting', cursive;
        letter-spacing: 2px;
        color: #ffffff;
        margin: 0;
        transform: skewX(-10deg);
    }
    .court-header h1 span {
        color: #ffffff;
        font-weight: 700;
    }
    .court-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 14px;
        letter-spacing: 1px;
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }

    /* -------------------- TOP ROW: CASE MANAGER + LEGAL RESEARCH -------------------- */
    .top-card {
        background: linear-gradient(135deg, #FFFBF5 0%, #F5E6D3 100%);
        border: 2px solid #D4A574;
        padding: 1.5rem;
        border-radius: 8px;
        height: 100%;
        border-left: 6px solid #704214;
        min-height: 140px;
        box-shadow: 0 4px 12px rgba(70, 42, 26, 0.15), inset 0 1px 0 rgba(212, 165, 116, 0.3);
        transition: box-shadow 0.2s ease;
    }
    .top-card:hover {
        box-shadow: 0 6px 20px rgba(70, 42, 26, 0.2), inset 0 1px 0 rgba(212, 165, 116, 0.4);
    }
    .top-card h4 {
        color: #704214;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin: 0 0 1rem 0;
        font-weight: 700;
    }
    .top-card .item {
        color: #2c3e50;
        font-size: 14px;
        padding: 6px 0;
        border-bottom: 1px solid #f0f3f7;
    }
    .top-card .item:last-child {
        border-bottom: none;
    }
    .top-card .item strong {
        color: #2c3e50;
        font-weight: 600;
        margin-right: 6px;
    }
    .top-card .item .value {
        color: #34495e;
        white-space: pre-wrap;
        word-wrap: break-word;
        line-height: 1.6;
    }
    .top-card .empty {
        color: #95a5a6;
        font-size: 14px;
        font-style: italic;
    }
    .top-card.consultant-panel {
        background: #ffffff;
        border-left: 4px solid #27ae60;
    }
    .top-card.consultant-panel h4 {
        color: #27ae60;
    }
    .top-card .sublabel {
        color: #704214;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin: 1rem 0 0.5rem 0;
        font-weight: 700;
    }
    .top-card ul.bullet-list {
        margin: 0;
        padding-left: 1.2rem;
        color: #2c3e50;
        font-size: 14px;
        line-height: 1.7;
    }
    .top-card ul.bullet-list li {
        margin-bottom: 4px;
    }
    .top-card ul.bullet-list.missing li {
        color: #e74c3c;
    }

    /* -------------------- LEGAL RESEARCH CARD ITEMS -------------------- */
    .law-card {
        background: linear-gradient(135deg, #FFFBF5 0%, #F5E6D3 100%);
        border-left: 6px solid #704214;
        padding: 1rem;
        margin-bottom: 1rem;
        font-size: 14px;
        color: #2c3e50;
        border-radius: 4px;
    }
    .law-card .title {
        font-weight: 700;
        color: #4A2C1A;
        margin-bottom: 4px;
    }
    .law-card .meta {
        color: #7f8c8d;
        font-size: 12px;
        margin-bottom: 6px;
    }
    .law-card .relevance {
        color: #34495e;
        line-height: 1.6;
    }

    /* -------------------- JUDGE & VERDICT -------------------- */
    .judge-container {
        background: linear-gradient(135deg, #FFFBF5 0%, #F5E6D3 100%);
        border: 2px solid #D4A574;
        border-left: 6px solid #704214;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        text-align: center;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(70, 42, 26, 0.15), inset 0 1px 0 rgba(212, 165, 116, 0.3);
    }
    .judge-container .label {
        color: #7f8c8d;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 700;
    }
    .judge-container .verdict-text {
        font-size: 28px;
        font-weight: 700;
        letter-spacing: 1px;
        margin: 0.5rem 0;
    }
    .judge-container .verdict-green { color: #27ae60; }
    .judge-container .verdict-red { color: #e74c3c; }
    .judge-container .verdict-amber { color: #f39c12; }
    .judge-container .confidence {
        background: rgba(212, 165, 116, 0.1);
        padding: 6px 18px;
        border-radius: 20px;
        color: #704214;
        font-size: 13px;
        font-weight: 700;
        border: 2px solid #D4A574;
        display: inline-block;
        margin-top: 0.5rem;
    }

    /* Full Verdict Reasoning Box */
    .verdict-reasoning {
        background: linear-gradient(135deg, #FFFBF5 0%, #F5E6D3 100%);
        border: 2px solid #D4A574;
        border-left: 6px solid #704214;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border-radius: 8px;
        text-align: left;
        box-shadow: 0 4px 12px rgba(70, 42, 26, 0.15), inset 0 1px 0 rgba(212, 165, 116, 0.3);
    }
    .verdict-reasoning .label {
        color: #704214;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 1rem;
        display: block;
        font-weight: 700;
    }
    .verdict-reasoning .content {
        color: #2c3e50;
        font-size: 15px;
        line-height: 1.8;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    .verdict-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .verdict-field {
        background: linear-gradient(135deg, #FFFBF5 0%, #F5E6D3 100%);
        border: 2px solid #D4A574;
        border-left: 6px solid #704214;
        padding: 1.2rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(70, 42, 26, 0.15), inset 0 1px 0 rgba(212, 165, 116, 0.3);
    }
    .verdict-field .label {
        color: #704214;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 0.6rem;
        display: block;
        font-weight: 700;
    }
    .verdict-field .content {
        color: #2c3e50;
        font-size: 14px;
        line-height: 1.7;
    }
    .sections-pill-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
    }
    .sections-pill {
        background: rgba(212, 165, 116, 0.15);
        border: 2px solid #704214;
        color: #704214;
        font-size: 12px;
        font-weight: 600;
        padding: 6px 14px;
        border-radius: 20px;
    }

    /* -------------------- DEBATE COLUMNS -------------------- */
    .debate-column {
        background: linear-gradient(135deg, #FFFBF5 0%, #F5E6D3 100%);
        border: 2px solid #D4A574;
        padding: 1.5rem;
        height: 100%;
        min-height: 250px;
        border-left: 6px solid #704214;
        overflow-y: auto;
        max-height: 500px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(70, 42, 26, 0.15), inset 0 1px 0 rgba(212, 165, 116, 0.3);
    }
    .debate-column .col-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        border-bottom: 2px solid #f0f3f7;
        padding-bottom: 1rem;
        margin-bottom: 1rem;
        position: sticky;
        top: 0;
        background: #ffffff;
        z-index: 2;
    }
    .debate-column .col-header .icon { font-size: 24px; }
    .debate-column .col-header h3 {
        margin: 0;
        color: #2c3e50;
        font-size: 18px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .debate-column .col-header .sub {
        color: #95a5a6;
        font-size: 12px;
        font-weight: 400;
        margin-left: auto;
    }
    .debate-column .empty-state {
        color: #bdc3c7;
        font-size: 14px;
        font-style: italic;
        padding: 1.5rem 0;
        text-align: center;
    }
    .argument-block {
        background: linear-gradient(135deg, #FFFBF5 0%, #F5E6D3 100%);
        border-left: 6px solid #704214;
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 4px;
        color: #2c3e50;
        font-size: 14px;
        line-height: 1.8;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    .argument-block .round-tag {
        font-size: 11px;
        text-transform: uppercase;
        color: #704214;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 6px;
        display: block;
    }
    .argument-block.prosecution { border-left-color: #e74c3c; }
    .argument-block.defense { border-left-color: #27ae60; }

    /* -------------------- COURT REPORTER (BOTTOM) -------------------- */
    .reporter-card {
        background: linear-gradient(135deg, #FFFBF5 0%, #F5E6D3 100%);
        border: 2px solid #D4A574;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 6px solid #704214;
        margin-top: 1.5rem;
        box-shadow: 0 4px 12px rgba(70, 42, 26, 0.15), inset 0 1px 0 rgba(212, 165, 116, 0.3);
    }
    .reporter-card h4 {
        color: #704214;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin: 0 0 1rem 0;
        font-weight: 700;
    }
    .reporter-card .headline {
        color: #2c3e50;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 1rem;
        border-left: 6px solid #704214;
        padding-left: 1rem;
    }
    .reporter-card .report {
        color: #2c3e50;
        font-size: 15px;
        line-height: 1.8;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    .reporter-card .empty {
        color: #95a5a6;
        font-size: 14px;
        font-style: italic;
    }

    /* -------------------- INPUT & BUTTONS -------------------- */
    .stTextArea textarea {
        background: #ffffff !important;
        color: #2c3e50 !important;
        border: 1px solid #e1e8ed !important;
        border-radius: 6px !important;
        font-size: 14px !important;
        line-height: 1.6 !important;
    }
    .stTextArea textarea:focus {
        border-color: #0066cc !important;
        box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1) !important;
    }
    .stButton button {
        background: linear-gradient(135deg, #704214 0%, #5A3410 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.7rem 2rem !important;
        letter-spacing: 0.5px;
        font-size: 14px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 12px rgba(70, 42, 26, 0.3), inset 0 1px 0 rgba(212, 165, 116, 0.3);
        width: 100%;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #5A3410 0%, #4A2C1A 100%) !important;
        box-shadow: 0 6px 20px rgba(70, 42, 26, 0.4), inset 0 1px 0 rgba(212, 165, 116, 0.4) !important;
    }
    .stButton button:disabled {
        opacity: 0.5;
        pointer-events: none;
    }

    /* -------------------- DIVIDERS -------------------- */
    .gold-divider {
        height: 1px;
        background: #e1e8ed;
        margin: 1.5rem 0;
    }

    /* -------------------- STATUS -------------------- */
    .status-text {
        color: #7f8c8d;
        font-size: 13px;
        text-align: center;
        padding: 0.5rem 0;
        letter-spacing: 0.5px;
    }
    .status-text .gold { color: #704214; }

    /* -------------------- IDLE STATE -------------------- */
    .idle-state {
        text-align: center;
        padding: 4rem 1rem;
        color: #95a5a6;
    }
    .idle-state .icon {
        font-size: 64px;
        margin-bottom: 1rem;
        opacity: 0.6;
    }
    .idle-state h2 {
        color: #704214;
        font-weight: 600;
        letter-spacing: 1px;
        font-size: 26px;
    }
    .idle-state p {
        color: #7f8c8d;
        font-size: 15px;
    }

    /* -------------------- COMPLAINT DISPLAY -------------------- */
    .complaint-box {
        background: linear-gradient(135deg, #FFFBF5 0%, #F5E6D3 100%);
        border-left: 6px solid #704214;
        padding: 1.2rem;
        margin-bottom: 1rem;
        border-radius: 4px;
    }
    .complaint-box .label {
        color: #704214;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin: 0 0 0.5rem 0;
        font-weight: 700;
    }
    .complaint-box .text {
        color: #2c3e50;
        font-size: 14px;
        line-height: 1.6;
        margin: 0;
        white-space: pre-wrap;
    }

    /* -------------------- CHARACTER COUNTER & FILE FEEDBACK -------------------- */
    .char-counter {
        font-size: 12px;
        color: #7f8c8d;
        text-align: right;
        margin-top: 0.3rem;
    }
    .char-counter.good { color: #27ae60; font-weight: 600; }
    .char-counter.warning { color: #f39c12; font-weight: 600; }
    
    .upload-feedback {
        background: #f0f8f0;
        border-left: 4px solid #27ae60;
        padding: 0.8rem;
        border-radius: 4px;
        margin: 1rem 0;
        font-size: 13px;
        color: #27ae60;
    }
    .upload-feedback .filename {
        font-weight: 600;
    }

    /* -------------------- RESPONSIVE -------------------- */
    @media (max-width: 768px) {
        .judge-container { flex-direction: column; gap: 0.5rem; text-align: center; }
        .debate-column { min-height: auto; max-height: none; }
        .top-card { min-height: auto; }
        .verdict-grid { grid-template-columns: 1fr; }
        .court-header { padding: 2rem 1.5rem; }
        .court-header h1 { font-size: 24px; }
    }
</style>
""", unsafe_allow_html=True)


# ============================================
# HTML ESCAPE HELPER
# ============================================
import html as _html_module

def esc(text) -> str:
    """Escape text before interpolating into raw HTML blocks."""
    if text is None:
        return ""
    return _html_module.escape(str(text))


def _build_report_content(state: dict) -> str:
    report_lines = []
    report_lines.append("# ⚖️ MyPeshkar Case Analysis Report")
    report_lines.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")
    
    # TOP CONSULTANT - MOVED TO THE TOP
    report_lines.append("## 🏛️ Top Consultant")
    report_lines.append(state.get('top_consultant', 'Not available.') or 'Not available.')
    report_lines.append("")

    # SIMULATION SECTION - DEBATE ROUNDS AND JUDGE VERDICT
    report_lines.append("## ⚔️ Prosecution Round 1")
    report_lines.append(state.get('pros_r1', 'Not available.') or 'Not available.')
    report_lines.append("")

    report_lines.append("## 🛡️ Defense Round 1")
    report_lines.append(state.get('def_r1', 'Not available.') or 'Not available.')
    report_lines.append("")

    report_lines.append("## ⚔️ Prosecution Round 2")
    report_lines.append(state.get('pros_r2', 'Not available.') or 'Not available.')
    report_lines.append("")

    report_lines.append("## 🛡️ Defense Round 2")
    report_lines.append(state.get('def_r2', 'Not available.') or 'Not available.')
    report_lines.append("")

    report_lines.append("## 👨‍⚖️ Judge")
    jv = state.get("judge_verdict")
    if jv:
        report_lines.append(f"- **Verdict:** {jv.get('verdict', 'Unknown')}")
        report_lines.append(f"- **Confidence:** {jv.get('confidence', 'N/A')}%")
        report_lines.append(f"- **Findings:** {jv.get('findings', '')}")
        report_lines.append(f"- **Prosecution Assessment:** {jv.get('prosecution_assessment', '')}")
        report_lines.append(f"- **Defense Assessment:** {jv.get('defense_assessment', '')}")
        report_lines.append(f"- **Reasoning:** {jv.get('reasoning', '')}")
        sections_applied_list = jv.get("sections_applied") or []
        report_lines.append(f"- **Sections Applied:** {', '.join(sections_applied_list)}")
        report_lines.append(f"- **Probable Punishment:** {jv.get('probable_punishment', '')}")
    else:
        report_lines.append(f"- **Verdict Short:** {state.get('verdict_short', 'Unknown')}")
        report_lines.append(f"- **Confidence:** {state.get('confidence', 'N/A')}%")
        report_lines.append(f"- **Full Verdict:**\n{state.get('verdict', 'Not available.')}")
    report_lines.append("")

    # REPORTER - FINAL SECTION
    report_lines.append("## 📰 Reporter")
    report_lines.append(f"- **Headline:** {state.get('headline', 'No headline.')}")
    report_lines.append(f"- **Report:**\n{state.get('report', 'Not available.')}")
    report_lines.append("")

    report_lines.append("## 📂 Case Manager")
    ci = state.get("case_intake")
    if ci:
        report_lines.append(f"- **Accused:** {ci.get('accused', 'Unknown')}")
        report_lines.append(f"- **Victim:** {ci.get('victim', 'Unknown')}")
        report_lines.append(f"- **Offences:** {ci.get('offences', 'Unknown')}")
        report_lines.append(f"- **Allegation:** {ci.get('allegation', 'Unknown')}")
        report_lines.append(f"- **Jurisdiction:** {ci.get('jurisdiction', 'Unknown')}")
        facts_list = ci.get("facts") or []
        if facts_list:
            report_lines.append("- **Facts:**")
            for f in facts_list:
                report_lines.append(f"  - {f}")
        missing_list = ci.get("missing_information") or []
        if missing_list:
            report_lines.append("- **Missing Information:**")
            for m in missing_list:
                report_lines.append(f"  - {m}")
    else:
        report_lines.append(f"- **Accused:** {state.get('accused', 'Unknown')}")
        report_lines.append(f"- **Victim:** {state.get('victim', 'Unknown')}")
        report_lines.append(f"- **Offence:** {state.get('offence', 'Unknown')}")
        report_lines.append(f"- **Facts:** {state.get('facts', 'Unknown')}")
    report_lines.append("")

    report_lines.append("## 📚 Legal Research")
    lr = state.get("legal_research")
    if lr:
        sections = lr.get("applicable_sections") or []
        for sec in sections:
            report_lines.append(f"- **{sec.get('section')} | {sec.get('act')}** — {sec.get('relevance')}")
        precedents = lr.get("precedents") or []
        if precedents:
            report_lines.append("- **Precedents:**")
            for p in precedents:
                report_lines.append(f"  - {p.get('case_name')} ({p.get('court')}, {p.get('year')}) — {p.get('relevance')}")
        evidentiary_notes = lr.get("evidentiary_notes") or []
        if evidentiary_notes:
            report_lines.append("- **Evidentiary Notes:**")
            for n in evidentiary_notes:
                report_lines.append(f"  - {n}")
    else:
        report_lines.append(f"- **Laws:** {state.get('laws', 'Not specified')}")
        report_lines.append(f"- **Sections Applied:** {state.get('sections_applied', 'Not specified')}")
        report_lines.append(f"- **Precedents:** {state.get('precedents', 'Not specified')}")
    report_lines.append("")

    report_lines.append("## 🧭 Internal Consultant")
    report_lines.append(state.get('consultant', 'Not available.') or 'Not available.')
    report_lines.append("")

    return "\n".join(report_lines)


def _build_pdf_bytes(report_text: str) -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    left = 50
    top = height - 50
    line_height = 12

    def draw_wrapped(text: str, x: int, y: int, font_name: str = "Helvetica", font_size: int = 10):
        nonlocal top
        c.setFont(font_name, font_size)
        text = text.replace("**", "")
        for raw_line in text.split("\n"):
            if y < 50:
                c.showPage()
                c.setFont(font_name, font_size)
                y = height - 50
            if not raw_line.strip():
                y -= line_height
                continue
            wrapped = textwrap.wrap(raw_line, width=110)
            for chunk in wrapped:
                if y < 50:
                    c.showPage()
                    c.setFont(font_name, font_size)
                    y = height - 50
                c.drawString(x, y, chunk)
                y -= line_height
        return y

    y = top
    for line in report_text.splitlines():
        if y < 50:
            c.showPage()
            y = height - 50
        if line.startswith("# "):
            y = draw_wrapped(line[2:], left, y, font_name="Helvetica-Bold", font_size=16)
            y -= 6
        elif line.startswith("## "):
            y = draw_wrapped(line[3:], left, y, font_name="Helvetica-Bold", font_size=12)
            y -= 4
        elif line.startswith("- **"):
            y = draw_wrapped(line[2:].replace("- **", "").replace("**", ""), left + 6, y)
        elif line.startswith("  - "):
            y = draw_wrapped(line[4:], left + 18, y)
        elif line.startswith("- "):
            y = draw_wrapped(line[2:], left + 6, y)
        else:
            y = draw_wrapped(line, left, y)
    c.save()
    return buffer.getvalue()


# ============================================
# SESSION STATE INITIALIZATION
# ============================================
EMPTY_CASE_STATE = {
    "complaint": "",
    "entities": None,
    "accused": None,
    "victim": None,
    "offence": None,
    "facts": None,
    "case_intake": None,
    "laws": None,
    "sections_applied": None,
    "precedents": None,
    "legal_research": None,
    "consultant": None,
    "top_consultant": None,
    "pros_r1": None,
    "def_r1": None,
    "pros_r2": None,
    "def_r2": None,
    "verdict": None,
    "verdict_short": None,
    "confidence": None,
    "reasoning": None,
    "probable_punishment": None,
    "judge_verdict": None,
    "headline": None,
    "report": None,
    "is_running": False,
    "execution_times": {},
}

if "case_state" not in st.session_state:
    st.session_state.case_state = dict(EMPTY_CASE_STATE)

if "simulation_complete" not in st.session_state:
    st.session_state.simulation_complete = False

if "stream_iter" not in st.session_state:
    st.session_state.stream_iter = None

if "node_times" not in st.session_state:
    st.session_state.node_times = {}

if "evaluator" not in st.session_state:
    st.session_state.evaluator = SystemEvaluator()

if "complaint_input" not in st.session_state:
    st.session_state.complaint_input = ""

if "uploaded_complaint" not in st.session_state:
    st.session_state.uploaded_complaint = ""


# ============================================
# HEADER (MOVED TO TOP)
# ============================================
st.markdown("""
<div class="court-header">
    <h1>MyPeshkar</h1>
    <p>Never Miss a Tareekh.</p>
</div>
""", unsafe_allow_html=True)


# ============================================
# AUTHENTICATION LAYER
# ============================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None


if not st.session_state.authenticated:
    # LOGIN PAGE STYLING
    st.markdown("""
    <style>
        .login-container {
            max-width: 450px;
            margin: 3rem auto;
            padding: 0;
        }
        .login-section {
            background: linear-gradient(135deg, #FFFBF5 0%, #F5E6D3 100%);
            padding: 2.5rem;
            border-radius: 8px;
            border: 2px solid #D4A574;
            box-shadow: 0 4px 16px rgba(70, 42, 26, 0.15), inset 0 1px 0 rgba(212, 165, 116, 0.3);
            margin-bottom: 1.5rem;
        }
        .login-section h3 {
            color: #704214;
            font-size: 20px;
            font-weight: 700;
            margin-top: 0;
            margin-bottom: 1.5rem;
            border-bottom: 2px solid #D4A574;
            padding-bottom: 1rem;
            text-align: center;
        }
        .stTextInput > div > div > input {
            background: #f8f9fb !important;
            border: 1px solid #e1e8ed !important;
            color: #2c3e50 !important;
            border-radius: 6px !important;
            padding: 0.8rem 1rem !important;
            font-size: 14px !important;
        }
        .stTextInput > div > div > input:focus {
            border-color: #704214 !important;
            box-shadow: 0 0 0 3px rgba(112, 66, 20, 0.15) !important;
        }
        .stTextArea textarea {
            background: #f8f9fb !important;
            border: 1px solid #e1e8ed !important;
            color: #2c3e50 !important;
            border-radius: 6px !important;
            padding: 0.8rem 1rem !important;
            font-size: 14px !important;
        }
        .stTextArea textarea:focus {
            border-color: #704214 !important;
            box-shadow: 0 0 0 3px rgba(112, 66, 20, 0.15) !important;
        }
        .stFormSubmitButton {
            width: 100%;
        }
        .divider-text {
            text-align: center;
            color: #95a5a6;
            font-size: 13px;
            margin: 1.5rem 0;
            font-weight: 600;
            letter-spacing: 1px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # CENTERED LOGIN PAGE
    _, center_col, _ = st.columns([1, 1.2, 1])
    
    with center_col:
        # LOGIN FORM
        st.markdown('<div class="login-section">', unsafe_allow_html=True)
        st.markdown("### Sign In")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit_login = st.form_submit_button("Sign In", use_container_width=True)
        
        if submit_login:
            if username and password:
                if authenticate(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success("Sign in successful. Redirecting...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please try again.")
            else:
                st.warning("Please enter both username and password.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # DIVIDER
        st.markdown('<div class="divider-text">OR REQUEST ACCESS</div>', unsafe_allow_html=True)
        
        # REQUEST ACCESS FORM
        st.markdown('<div class="login-section">', unsafe_allow_html=True)
        st.markdown("### Request Access")
        
        with st.form("access_request_form"):
            email = st.text_input("Email address", placeholder="your.email@company.com")
            message = st.text_area(
                "How will you use this platform?",
                placeholder="Briefly describe your intended use case",
                height=80
            )
            submit_request = st.form_submit_button("Submit Request", use_container_width=True)
        
        if submit_request:
            if email and message:
                if submit_access_request(email, message):
                    st.success("Request submitted successfully.")
                    st.info("Check your email for updates.")
                else:
                    st.error("Error submitting request. Please try again.")
            else:
                st.warning("Please fill in all fields.")

else:
    # AUTHENTICATED USER - SHOW MAIN APP
    
    # Initialize selected tool in session state
    if "selected_tool" not in st.session_state:
        st.session_state.selected_tool = None
    
    # Logout button in sidebar
    with st.sidebar:
        if st.button("Sign Out", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.clear()
            st.success("Signed out successfully.")
            time.sleep(1)
            st.rerun()
        st.markdown(f"**Logged in as:** {st.session_state.username}")
        st.markdown("---")
    

    # ============================================
    # TABS & NAVIGATION
    # ============================================
    tab_tools, tab_metrics, tab_vision = st.tabs(["Tools", "Metrics", "Vision"])


    # ============================================
    # TAB 1: TOOLS
    # ============================================
    with tab_tools:
        if st.session_state.selected_tool is None:
            # Tools Dashboard Header
            st.markdown("""
            <div style="margin-bottom: 3rem;">
                <h2 style="margin: 0; color: #2c3e50; font-weight: 700; font-size: 36px;">Tools</h2>
                <p style="margin: 0.5rem 0 0 0; color: #7f8c8d; font-size: 15px;">Select a tool to get started</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2, gap="large")
            
            # Courtroom Debate Card
            with col1:
                st.markdown("""
                <div style="
                    background: linear-gradient(135deg, #FFFBF5 0%, #F5E6D3 100%);
                    border: 2px solid #704214;
                    box-shadow: 0 12px 32px rgba(70, 42, 26, 0.2), inset 0 1px 0 rgba(212, 165, 116, 0.3);
                    border-radius: 16px;
                    padding: 40px;
                    box-shadow: 0 12px 32px rgba(70, 42, 26, 0.2), inset 0 1px 0 rgba(212, 165, 116, 0.3);
                    cursor: pointer;
                    transition: all 0.3s ease;
                    min-height: 300px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                ">
                    <div style="text-align: center;">
                        <div style="font-size: 56px; margin-bottom: 24px;">⚖</div>
                        <h3 style="margin: 0 0 16px 0; color: #2c3e50; font-size: 28px; font-weight: 700;">Courtroom Debate</h3>
                        <p style="margin: 0; color: #666; font-size: 15px; line-height: 1.6; max-width: 280px; margin: 0 auto;">
                            Orchestrated adversarial debate with 8 specialized AI agents analyzing cases in depth
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Start Courtroom Debate", type="primary", use_container_width=True, key="btn_launch_debate"):
                    st.session_state.selected_tool = "courtroom_simulation"
                    st.rerun()
            
            # Coming Soon Card
            with col2:
                st.markdown("""
                <div style="
                    background: #f9f8f6;
                    border: 2px dashed #D4A574;
                    border-radius: 16px;
                    padding: 40px;
                    box-shadow: 0 4px 12px rgba(70, 42, 26, 0.12);
                    opacity: 0.7;
                    min-height: 300px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                ">
                    <div style="text-align: center;">
                        <div style="font-size: 56px; margin-bottom: 24px;">✨</div>
                        <h3 style="margin: 0 0 16px 0; color: #999; font-size: 28px; font-weight: 700;">More Coming Soon</h3>
                        <p style="margin: 0; color: #aaa; font-size: 15px; line-height: 1.6;">
                            Additional legal AI tools in development
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        elif st.session_state.selected_tool == "courtroom_simulation":
            # Show simulation tool
            col_back, col_title = st.columns([1, 10])
            with col_back:
                if st.button("← Back to Tools", key="btn_back_tools"):
                    st.session_state.selected_tool = None
                    st.rerun()
            
            st.markdown("---")
            
            # ============================================
            # INPUT SECTION (hidden during simulation)
            # ============================================
            if not st.session_state.case_state.get("is_running"):
                with st.container():
                    col_input1, col_input2 = st.columns([3, 1])
                    with col_input1:
                        # UPLOAD HANDLER FIRST (before text_area widget)
                        uploaded_file = st.file_uploader(
                            "Or upload a complaint file (.txt, .pdf)",
                            type=['txt', 'pdf'],
                            key="complaint_uploader",
                            disabled=False,
                            label_visibility="visible"
                        )

                        if uploaded_file is not None:
                            try:
                                file_type = uploaded_file.type
                                text = ""
                                if file_type == "text/plain":
                                    text = uploaded_file.getvalue().decode("utf-8")
                                elif file_type == "application/pdf":
                                    try:
                                        from pypdf import PdfReader
                                        reader = PdfReader(uploaded_file)
                                        for page in reader.pages:
                                            page_text = page.extract_text()
                                            if page_text:
                                                text += page_text + "\n"
                                    except ImportError:
                                        st.error("The 'pypdf' library is required for PDF uploads. Please install it with: pip install pypdf")
                                        text = ""
                            
                                if text:
                                    # Store in a separate variable, NOT in complaint_input
                                    st.session_state.uploaded_complaint = text
                                    # Show confirmation - don't display the full text
                                    st.success(f"✅ File uploaded successfully ({len(text)} characters)")
                            except Exception as e:
                                st.error(f"Error reading file: {e}")

                    # NOW CREATE TEXT_AREA (after session_state is populated)
                    # User can edit manually entered text
                    complaint = st.text_area(
                        "Complaint or case brief",
                        height=120,
                        placeholder="Include: who, what, when, where, why (200+ characters)",
                        key="complaint_input",
                        disabled=False,
                        label_visibility="visible",
                        help="Minimum 50 characters for analysis"
                    )
                    
                    # Show file feedback
                    if st.session_state.get("uploaded_complaint"):
                        file_chars = len(st.session_state.uploaded_complaint)
                        st.markdown(f'<div class="upload-feedback"><span class="filename">✓ File loaded</span> ({file_chars:,} characters)</div>', unsafe_allow_html=True)
                    
                    # Character counter
                    complaint_text = st.session_state.get("complaint_input", "")
                    char_count = len(complaint_text)
                    char_status = "good" if char_count >= 100 else ("warning" if char_count > 0 else "")
                    st.markdown(f'<div class="char-counter {char_status}">{char_count} characters</div>', unsafe_allow_html=True)

                with col_input2:
                    st.write("")
                    st.write("")
                    if st.button("Begin Simulation", type="primary", use_container_width=True):
                        # Use uploaded content if available, otherwise use manual input
                        current_complaint = st.session_state.get("uploaded_complaint") or st.session_state.get("complaint_input", "")
                        if not current_complaint.strip():
                            st.error("Please enter a complaint (minimum 50 characters) or upload a file.")
                            st.stop()
                        elif len(current_complaint) < 50:
                            st.error(f"Complaint too short ({len(current_complaint)}/50 characters). Please add more details.")
                            st.stop()

                        st.session_state.case_state = dict(EMPTY_CASE_STATE)
                        st.session_state.case_state["complaint"] = current_complaint
                        st.session_state.case_state["is_running"] = True
                        st.session_state.simulation_complete = False
                        st.session_state.stream_iter = None
                        st.rerun()

        # ============================================
        # STATUS INDICATOR WITH CONTEXTUAL MESSAGES
        # ============================================
        if st.session_state.case_state["is_running"]:
            # Determine current stage based on what's been completed
            if st.session_state.case_state.get("judge_verdict"):
                stage = "Finalizing report..."
            elif st.session_state.case_state.get("def_r2"):
                stage = "Judge deliberating..."
            elif st.session_state.case_state.get("pros_r2"):
                stage = "Defense responding..."
            elif st.session_state.case_state.get("def_r1"):
                stage = "Prosecution rebuttal..."
            elif st.session_state.case_state.get("pros_r1"):
                stage = "Defense presenting arguments..."
            elif st.session_state.case_state.get("legal_research"):
                stage = "Building case arguments..."
            elif st.session_state.case_state.get("case_intake"):
                stage = "Researching applicable laws..."
            else:
                stage = "Analyzing case facts..."
            st.markdown(f'<div class="status-text"><span class="gold">{stage}</span></div>', unsafe_allow_html=True)
        elif st.session_state.simulation_complete:
            st.markdown('<div class="status-text"><span class="gold">Simulation complete. Review results below.</span></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-text">Enter a case brief and click Begin Simulation to start.</div>', unsafe_allow_html=True)

        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

        # ============================================
        # COLLAPSIBLE AGENT SECTIONS
        # ============================================
        col_cm, col_lr, col_cons = st.columns(3, gap="large")

        with col_cm:
            with st.expander("Case Manager", expanded=True):
                case_intake = st.session_state.case_state.get("case_intake")

                if case_intake:
                    accused = case_intake.get("accused")
                    victim = case_intake.get("victim")
                    offences = case_intake.get("offences")
                    allegation = case_intake.get("allegation")
                    jurisdiction = case_intake.get("jurisdiction")
                    facts_list = case_intake.get("facts") or []
                    missing_list = case_intake.get("missing_information") or []

                    if accused:
                        st.markdown(f'<div class="item"><strong>Accused:</strong> <span class="value">{esc(accused)}</span></div>', unsafe_allow_html=True)
                    if victim:
                        st.markdown(f'<div class="item"><strong>Victim:</strong> <span class="value">{esc(victim)}</span></div>', unsafe_allow_html=True)
                    if offences:
                        st.markdown(f'<div class="item"><strong>Offences:</strong> <span class="value">{esc(offences)}</span></div>', unsafe_allow_html=True)
                    if allegation:
                        st.markdown(f'<div class="item"><strong>Allegation:</strong> <span class="value">{esc(allegation)}</span></div>', unsafe_allow_html=True)
                    if jurisdiction:
                        st.markdown(f'<div class="item"><strong>Jurisdiction:</strong> <span class="value">{esc(jurisdiction)}</span></div>', unsafe_allow_html=True)

                    if facts_list:
                        st.markdown('<div class="sublabel">Material Facts</div>', unsafe_allow_html=True)
                        items = "".join(f"<li>{esc(f)}</li>" for f in facts_list)
                        st.markdown(f'<ul class="bullet-list">{items}</ul>', unsafe_allow_html=True)

                    if missing_list:
                        st.markdown('<div class="sublabel">Missing Information</div>', unsafe_allow_html=True)
                        items = "".join(f"<li>{esc(m)}</li>" for m in missing_list)
                        st.markdown(f'<ul class="bullet-list missing">{items}</ul>', unsafe_allow_html=True)

                else:
                    st.info("Analyzing case details...")

        with col_lr:
            with st.expander("Legal Research", expanded=True):
                legal_research = st.session_state.case_state.get("legal_research")

                if legal_research:
                    sections = legal_research.get("applicable_sections") or []
                    precedents = legal_research.get("precedents") or []
                    evidentiary_notes = legal_research.get("evidentiary_notes") or []
                    unsettled = legal_research.get("unsettled_questions") or []

                    if sections:
                        st.markdown('<div class="sublabel">Applicable Sections</div>', unsafe_allow_html=True)
                        for s in sections:
                            st.markdown(f"""
                            <div class="law-card">
                                <div class="title">{esc(s.get('section'))} — {esc(s.get('act'))}</div>
                                <div class="relevance">{esc(s.get('relevance'))}</div>
                            </div>
                            """, unsafe_allow_html=True)

                    if precedents:
                        st.markdown('<div class="sublabel">Precedents</div>', unsafe_allow_html=True)
                        for p in precedents:
                            st.markdown(f"""
                            <div class="law-card">
                                <div class="title">{esc(p.get('case_name'))}</div>
                                <div class="meta">{esc(p.get('court'))} · {esc(p.get('year'))}</div>
                                <div class="relevance">{esc(p.get('relevance'))}</div>
                            </div>
                            """, unsafe_allow_html=True)

                    if evidentiary_notes:
                        st.markdown('<div class="sublabel">Evidentiary Notes</div>', unsafe_allow_html=True)
                        items = "".join(f"<li>{esc(n)}</li>" for n in evidentiary_notes)
                        st.markdown(f'<ul class="bullet-list">{items}</ul>', unsafe_allow_html=True)

                    if unsettled:
                        st.markdown('<div class="sublabel">Unsettled Questions</div>', unsafe_allow_html=True)
                        items = "".join(f"<li>{esc(q)}</li>" for q in unsettled)
                        st.markdown(f'<ul class="bullet-list">{items}</ul>', unsafe_allow_html=True)

                    if not (sections or precedents or evidentiary_notes or unsettled):
                        st.info("No applicable laws identified yet.")
                
                if not legal_research:
                    st.info("Researching applicable laws...")

        with col_cons:
            with st.expander("Internal Consultant", expanded=True):
                consultant = st.session_state.case_state.get("consultant")
                if consultant:
                    st.markdown(f'<div class="item"><span class="value">{esc(consultant)}</span></div>', unsafe_allow_html=True)
                else:
                    st.info("Analyzing case strategy...")

        # ============================================
        # ROW 2: JUDGE VERDICT (Collapsible)
        # ============================================
        judge_verdict = st.session_state.case_state.get("judge_verdict")
        verdict_short = st.session_state.case_state.get("verdict_short")
        confidence = st.session_state.case_state.get("confidence")

        with st.expander("Judge Verdict", expanded=True):
            if not verdict_short:
                st.markdown("""
                <div class="judge-container">
                    <span class="label">The Hon'ble Judge</span><br>
                    <span style="color: #666666; font-size: 18px;">Deliberating on the case...</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                v_lower = str(verdict_short).lower()
                if "not guilty" in v_lower:
                    verdict_color = "verdict-green"
                    status_text = "NOT GUILTY"
                elif "partially" in v_lower:
                    verdict_color = "verdict-amber"
                    status_text = "PARTIALLY LIABLE"
                elif "guilty" in v_lower:
                    verdict_color = "verdict-red"
                    status_text = "GUILTY"
                else:
                    verdict_color = "verdict-amber"
                    status_text = esc(verdict_short).upper()

                st.markdown(f"""
                <div class="judge-container">
                    <span class="label">The Hon'ble Judge</span><br>
                    <span class="verdict-text {verdict_color}">{status_text}</span><br>
                    <span style="color: #aaaaaa; font-size: 16px;">{esc(verdict_short)}</span><br>
                    <span class="confidence">Confidence {esc(confidence)}%</span>
                </div>
                """, unsafe_allow_html=True)

            if judge_verdict:
                findings = judge_verdict.get("findings")
                pros_assessment = judge_verdict.get("prosecution_assessment")
                def_assessment = judge_verdict.get("defense_assessment")
                reasoning = judge_verdict.get("reasoning")
                sections_applied_list = judge_verdict.get("sections_applied") or []
                probable_punishment = judge_verdict.get("probable_punishment")

                if findings or pros_assessment or def_assessment:
                    st.markdown('<div class="verdict-grid">', unsafe_allow_html=True)
                    if findings:
                        st.markdown(f"""
                        <div class="verdict-field">
                            <span class="label">Findings</span>
                            <div class="content">{esc(findings)}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    if pros_assessment:
                        st.markdown(f"""
                        <div class="verdict-field">
                            <span class="label">Prosecution Assessment</span>
                            <div class="content">{esc(pros_assessment)}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    if def_assessment:
                        st.markdown(f"""
                        <div class="verdict-field">
                            <span class="label">Defense Assessment</span>
                            <div class="content">{esc(def_assessment)}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    if probable_punishment:
                        st.markdown(f"""
                        <div class="verdict-field">
                            <span class="label">Probable Punishment</span>
                            <div class="content">{esc(probable_punishment)}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                if sections_applied_list:
                    pills = "".join(f'<span class="sections-pill">{esc(s)}</span>' for s in sections_applied_list)
                    st.markdown(f"""
                    <div class="verdict-reasoning">
                        <span class="label">Sections Applied</span>
                        <div class="sections-pill-row">{pills}</div>
                    </div>
                    """, unsafe_allow_html=True)

                if reasoning:
                    st.markdown(f"""
                    <div class="verdict-reasoning">
                        <span class="label">Reasoning</span>
                        <div class="content">{esc(reasoning)}</div>
                    </div>
                    """, unsafe_allow_html=True)

            else:
                full_reasoning = st.session_state.case_state.get("verdict", "")
                if full_reasoning and "Error" not in full_reasoning:
                    st.markdown(f"""
                    <div class="verdict-reasoning">
                        <span class="label">Full Verdict & Reasoning</span>
                        <div class="content">{esc(full_reasoning)}</div>
                    </div>
                    """, unsafe_allow_html=True)
                elif verdict_short:
                    st.markdown(f"""
                    <div class="verdict-reasoning">
                        <span class="label">Verdict Summary</span>
                        <div class="content">{esc(verdict_short)}</div>
                    </div>
                    """, unsafe_allow_html=True)

        # ============================================
        # PROSECUTION & DEFENSE ROUNDS (Collapsible)
        # ============================================
        with st.expander("Prosecution Round 1 - Opening", expanded=False):
            r1 = st.session_state.case_state.get("pros_r1")
            if r1:
                st.markdown(f'<div class="argument-block prosecution">{esc(r1)}</div>', unsafe_allow_html=True)
            else:
                st.info("Awaiting prosecution opening argument...")

        with st.expander("Defense Round 1 - Opening", expanded=False):
            r1 = st.session_state.case_state.get("def_r1")
            if r1:
                st.markdown(f'<div class="argument-block defense">{esc(r1)}</div>', unsafe_allow_html=True)
            else:
                st.info("Awaiting defense opening argument...")

        with st.expander("Prosecution Round 2 - Closing", expanded=False):
            r2 = st.session_state.case_state.get("pros_r2")
            if r2:
                st.markdown(f'<div class="argument-block prosecution">{esc(r2)}</div>', unsafe_allow_html=True)
            else:
                st.info("Awaiting prosecution closing argument...")

        with st.expander("Defense Round 2 - Closing", expanded=False):
            r2 = st.session_state.case_state.get("def_r2")
            if r2:
                st.markdown(f'<div class="argument-block defense">{esc(r2)}</div>', unsafe_allow_html=True)
            else:
                st.info("Awaiting defense closing argument...")

        # ============================================
        # COURT REPORTER (Collapsible - Journalistic Style)
        # ============================================
        headline = st.session_state.case_state.get("headline")
        report = st.session_state.case_state.get("report")

        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

        with st.expander("Court Reporter Summary", expanded=True):
            if headline or report:
                if headline:
                    st.markdown(f'<div style="font-size: 18px; font-weight: 700; margin-bottom: 1rem; color: #704214;">{esc(headline)}</div>', unsafe_allow_html=True)
                if report:
                    st.markdown(f'<div style="font-size: 15px; line-height: 1.8; color: #2c3e50; white-space: pre-wrap;">{esc(report)}</div>', unsafe_allow_html=True)
            else:
                st.info("Preparing the case summary...")

        # ---------- CONSULTANT SPARROW ----------
        show_consultant_panel = (
            st.session_state.case_state.get("top_consultant")
            or st.session_state.simulation_complete
            or st.session_state.case_state.get("report")
            or st.session_state.case_state.get("judge_verdict")
            or st.session_state.case_state.get("is_running")
        )
        if show_consultant_panel:
            consultant_sparrow = st.session_state.case_state.get("top_consultant")
            st.markdown("""
            <div class="top-card consultant-panel" style="margin-top: 1rem;">
                <h4>🏛️ Consultant Sparrow</h4>
            """, unsafe_allow_html=True)
            if consultant_sparrow and str(consultant_sparrow).strip():
                st.markdown(f'<div class="item"><span class="value">{esc(consultant_sparrow)}</span></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="empty">⏳ Consultant Sparrow is reviewing the full case...</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # ============================================
        # STREAMING ENGINE (INCREMENTAL UPDATES)
        # ============================================
        if st.session_state.case_state.get("is_running") and not st.session_state.simulation_complete:
            progress_placeholder = st.empty()
            progress_placeholder.info("🔄 Streaming simulation events...")
        
            if st.session_state.stream_iter is None:
                initial_state = dict(EMPTY_CASE_STATE)
                initial_state["complaint"] = st.session_state.case_state["complaint"]
                initial_state.pop("is_running", None)

                try:
                    progress_placeholder.info("📊 Initializing graph stream...")
                    print("[STREAM] Initializing graph.stream()")
                    st.session_state.stream_iter = court_graph.stream(
                        initial_state,
                        stream_mode="updates"
                    )
                    print("[STREAM] ✅ Stream initialized")
                except Exception as e:
                    progress_placeholder.error(f"❌ Error initializing stream: {e}")
                    import traceback
                    st.error(traceback.format_exc())
                    st.session_state.case_state["is_running"] = False
                    st.session_state.stream_iter = None
                    st.rerun()

            try:
                node_start_time = time.time()
                print("[STREAM] Calling next() on stream_iter...")
                event = next(st.session_state.stream_iter)
                print(f"[STREAM] Got event: {event}")
            
                # Log which node(s) are being processed
                node_names = list(event.keys())
                print(f"🔄 Processing node(s): {node_names}")
                progress_placeholder.info(f"🔄 Running: {', '.join(node_names)}")
            
                for node_name, partial in event.items():
                    node_elapsed = time.time() - node_start_time
                    st.session_state.node_times[node_name] = node_elapsed
                    print(f"  ✅ {node_name}: {node_elapsed:.2f}s - keys: {list(partial.keys())}")
            
                    # Safely update state
                    try:
                        for key, value in partial.items():
                            if value is not None:
                                st.session_state.case_state[key] = value
                    except Exception as e:
                        print(f"  ⚠️  Error updating state for {node_name}: {e}")
                        raise
            
                print("[STREAM] About to rerun after processing event")
                st.rerun()
            
            except StopIteration:
                print("✅ Stream completed successfully (StopIteration)")
                progress_placeholder.success("✅ Simulation completed!")
                st.session_state.simulation_complete = True
                st.session_state.case_state["is_running"] = False
                st.session_state.stream_iter = None
                st.rerun()
            
            except TimeoutError as e:
                print(f"⏱️  TIMEOUT: {e}")
                progress_placeholder.error(f"⏱️ Timeout: Node took too long")
                st.error(f"Node processing timed out: {e}")
                st.session_state.case_state["is_running"] = False
                st.session_state.stream_iter = None
                st.rerun()
            
            except Exception as e:
                print(f"❌ STREAMING ERROR: {e}")
                import traceback
                error_msg = traceback.format_exc()
                print(error_msg)
                progress_placeholder.error(f"❌ Error: {str(e)[:100]}")
                st.error(f"Error: {e}")
                with st.expander("📋 Full Error Details"):
                    st.code(error_msg)
                st.session_state.case_state["is_running"] = False
                st.session_state.stream_iter = None
                st.rerun()

        # ============================================
        # IDLE / RESET & DOWNLOAD REPORT
        # ============================================
        if not st.session_state.case_state.get("is_running") and not st.session_state.simulation_complete:
            if not st.session_state.case_state.get("complaint"):
                st.markdown("""
                <div class="idle-state">
                    <div class="icon">🏛️</div>
                    <h2>The Court Awaits</h2>
                    <p>Enter a case brief above to begin the adversarial simulation.</p>
                </div>
                """, unsafe_allow_html=True)

        if st.session_state.simulation_complete:
            st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

            if "metrics_recorded" not in st.session_state:
                st.session_state.metrics_recorded = False
    
            if not st.session_state.metrics_recorded:
                metrics = st.session_state.evaluator.evaluate_case(
                    st.session_state.case_state,
                    st.session_state.node_times
                )
                st.session_state.metrics_recorded = True
                st.success(f"✅ Case evaluated. Quality Score: {metrics.overall_quality_score:.1f}/100")
    
            s = st.session_state.case_state
            report_content = _build_report_content(s)

            col_btn1, col_btn2, col_btn3 = st.columns(3)
            with col_btn1:
                st.download_button(
                    label="📄 Download PDF",
                    data=_build_pdf_bytes(report_content),
                    file_name="courtroom_report.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            with col_btn2:
                st.download_button(
                    label="📥 Download Markdown",
                    data=report_content,
                    file_name="courtroom_report.md",
                    mime="text/markdown",
                    use_container_width=True,
                )
            with col_btn3:
                if st.button("Start New Case", use_container_width=True):
                    st.session_state.case_state = dict(EMPTY_CASE_STATE)
                    st.session_state.simulation_complete = False
                    st.session_state.stream_iter = None
                    st.session_state.node_times = {}
                    st.session_state.metrics_recorded = False
                    st.session_state.complaint_input = ""
                    st.session_state.uploaded_complaint = ""
                    st.rerun()

    # ============================================
    # TAB 2: METRICS
    # ============================================
    with tab_metrics:
        from evaluation.dashboard import show_evaluation_dashboard
        show_evaluation_dashboard()

    # ============================================
    # TAB 3: VISION
    # ============================================
    with tab_vision:
        st.markdown("""
        ## Our Vision

        *Every court has a Peshkar — managing files, tracking orders, keeping every hearing on schedule.*

        *Now every lawyer can have their own.*

        ### What is MyPeshkar?

        MyPeshkar organizes your cases, tracks your hearing dates, and prepares your research — so you walk into court ready, every single time.

        ### Not a Replacement

        MyPeshkar is not a replacement for your legal skill. It's your personal Peshkar, working for you.

        A Peshkar handles the administrative burden so the lawyer can focus on advocacy. MyPeshkar does exactly that:

        ✓ **Organize Cases** — All your case files, arguments, and research in one place  
        ✓ **Track Hearings** — Never miss a Tareekh (court date) again  
        ✓ **Prepare Research** — AI-powered legal research across Indian precedent and statutes  
        ✓ **Structure Arguments** — Turn scattered notes into coherent legal arguments  
        ✓ **Bilingual Support** — Work seamlessly in Hindi and English  

        ### Why It Matters

        India has over **1.5 million practicing advocates**. Most manage cases on paper, spreadsheets, and memory. 

        A Peshkar ensures nothing falls through the cracks. Your Peshkar—MyPeshkar—does the same.

        ---

        **MyPeshkar** — Your personal legal Peshkar. Never miss a Tareekh again.
        """)