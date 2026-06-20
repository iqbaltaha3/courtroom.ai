import streamlit as st
from graph.graph import court_graph
from datetime import datetime

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Courtroom AI - Legal Simulation",
    page_icon="⚖️",
    layout="wide"
)

# ============================================
# PROFESSIONAL CSS (Black, Gold & Pure White Theme)
# ============================================
st.markdown("""
<style>
    /* -------------------- MAIN BACKGROUND -------------------- */
    .stApp {
        background-color: #0a0a0f;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* -------------------- SCROLLBAR -------------------- */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #1a1a1a; }
    ::-webkit-scrollbar-thumb { background: #c9a84c; border-radius: 4px; }

    /* -------------------- HEADER -------------------- */
    .court-header {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a1a1a 100%);
        padding: 1.8rem 2.5rem;
        border-radius: 0;
        border-bottom: 3px solid #c9a84c;
        margin-bottom: 2rem;
        text-align: center;
    }
    .court-header h1 {
        font-size: 32px;
        font-weight: 700;
        letter-spacing: 2px;
        color: #ffffff;
        margin: 0;
    }
    .court-header h1 span {
        color: #c9a84c;
    }
    .court-header p {
        color: #a0a0a0;
        font-size: 14px;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin: 6px 0 0 0;
        font-weight: 300;
    }

    /* -------------------- TOP ROW: CASE MANAGER + LEGAL RESEARCH -------------------- */
    .top-card {
        background: #0f0f14;
        border: 1px solid #1e1e24;
        padding: 1.2rem 1.5rem;
        border-radius: 0;
        height: 100%;
        border-top: 3px solid #c9a84c;
        min-height: 140px;
    }
    .top-card h4 {
        color: #c9a84c;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 0 0 0.8rem 0;
        font-weight: 600;
    }
    .top-card .item {
        color: #ffffff;
        font-size: 14px;
        padding: 4px 0;
        border-bottom: 1px solid #1a1a1a;
    }
    .top-card .item strong {
        color: #ffffff;
        font-weight: 600;
        margin-right: 6px;
    }
    .top-card .item .value {
        color: #ffffff;
        white-space: pre-wrap;
        word-wrap: break-word;
        line-height: 1.6;
    }
    .top-card .empty {
        color: #cccccc;
        font-size: 14px;
        font-style: italic;
    }

    /* -------------------- JUDGE & VERDICT -------------------- */
    .judge-container {
        background: #141418;
        border: 1px solid #2a2a2a;
        border-left: 6px solid #c9a84c;
        padding: 1.2rem 2rem;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .judge-container .label {
        color: #888888;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .judge-container .verdict-text {
        font-size: 26px;
        font-weight: 700;
        letter-spacing: 1px;
    }
    .judge-container .verdict-green { color: #4ade80; }
    .judge-container .verdict-red { color: #f87171; }
    .judge-container .confidence {
        background: #1e1e24;
        padding: 4px 16px;
        border-radius: 20px;
        color: #c9a84c;
        font-size: 13px;
        font-weight: 600;
        border: 1px solid #2a2a2a;
    }

    /* Full Verdict Reasoning Box */
    .verdict-reasoning {
        background: #141418;
        border: 1px solid #2a2a2a;
        border-left: 4px solid #c9a84c;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        border-radius: 0;
        text-align: left;
    }
    .verdict-reasoning .label {
        color: #c9a84c;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 0.75rem;
        display: block;
    }
    .verdict-reasoning .content {
        color: #ffffff;
        font-size: 15px;
        line-height: 1.8;
        white-space: pre-wrap;
        word-wrap: break-word;
    }

    /* -------------------- DEBATE COLUMNS -------------------- */
    .debate-column {
        background: #0f0f14;
        border: 1px solid #1e1e24;
        padding: 1.5rem 1.8rem;
        height: 100%;
        min-height: 250px;
        border-top: 4px solid #c9a84c;
        overflow-y: auto;
        max-height: 500px;
    }
    .debate-column .col-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        border-bottom: 1px solid #1e1e24;
        padding-bottom: 0.75rem;
        margin-bottom: 1rem;
        position: sticky;
        top: 0;
        background: #0f0f14;
        z-index: 2;
    }
    .debate-column .col-header .icon { font-size: 22px; }
    .debate-column .col-header h3 {
        margin: 0;
        color: #ffffff;
        font-size: 18px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .debate-column .col-header .sub {
        color: #888888;
        font-size: 12px;
        font-weight: 300;
        margin-left: auto;
    }
    .debate-column .empty-state {
        color: #666666;
        font-size: 14px;
        font-style: italic;
        padding: 1.2rem 0;
        text-align: center;
    }
    .argument-block {
        background: #141418;
        border-left: 4px solid #c9a84c;
        padding: 1rem 1.2rem;
        margin-bottom: 1rem;
        border-radius: 0;
        color: #ffffff;
        font-size: 14px;
        line-height: 1.8;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    .argument-block .round-tag {
        font-size: 11px;
        text-transform: uppercase;
        color: #c9a84c;
        font-weight: 600;
        letter-spacing: 1px;
        margin-bottom: 4px;
        display: block;
    }
    .argument-block.prosecution { border-left-color: #fbbf24; }
    .argument-block.defense { border-left-color: #94a3b8; }

    /* -------------------- COURT REPORTER (BOTTOM) -------------------- */
    .reporter-card {
        background: #0f0f14;
        border: 1px solid #1e1e24;
        padding: 1.2rem 2rem;
        border-radius: 0;
        border-top: 3px solid #c9a84c;
        margin-top: 1.5rem;
    }
    .reporter-card h4 {
        color: #c9a84c;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 0 0 0.8rem 0;
        font-weight: 600;
    }
    .reporter-card .headline {
        color: #ffffff;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 0.75rem;
        border-left: 3px solid #c9a84c;
        padding-left: 1rem;
    }
    .reporter-card .report {
        color: #ffffff;
        font-size: 15px;
        line-height: 1.8;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    .reporter-card .empty {
        color: #cccccc;
        font-size: 14px;
        font-style: italic;
    }

    /* -------------------- INPUT & BUTTONS -------------------- */
    .stTextArea textarea {
        background: #141418 !important;
        color: #ffffff !important;
        border: 1px solid #2a2a2a !important;
        border-radius: 0 !important;
        font-size: 14px !important;
        line-height: 1.6 !important;
        font-family: 'Inter', sans-serif !important;
    }
    .stTextArea textarea:focus {
        border-color: #c9a84c !important;
        box-shadow: none !important;
    }
    .stButton button {
        background: #c9a84c !important;
        color: #0a0a0f !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 0 !important;
        padding: 0.6rem 2.5rem !important;
        letter-spacing: 1px;
        text-transform: uppercase;
        font-size: 14px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 0 20px rgba(201, 168, 76, 0.15);
        width: 100%;
    }
    .stButton button:hover {
        background: #d4af37 !important;
        box-shadow: 0 0 30px rgba(201, 168, 76, 0.3) !important;
        transform: translateY(-1px);
    }
    .stButton button:disabled {
        opacity: 0.4;
        pointer-events: none;
    }

    /* -------------------- DIVIDERS -------------------- */
    .gold-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #c9a84c, transparent);
        margin: 1rem 0 1.5rem 0;
        opacity: 0.4;
    }

    /* -------------------- STATUS -------------------- */
    .status-text {
        color: #888888;
        font-size: 13px;
        text-align: center;
        padding: 0.5rem 0;
        letter-spacing: 1px;
    }
    .status-text .gold { color: #c9a84c; }

    /* -------------------- IDLE STATE -------------------- */
    .idle-state {
        text-align: center;
        padding: 4rem 1rem;
        color: #555555;
    }
    .idle-state .icon {
        font-size: 64px;
        margin-bottom: 1rem;
        opacity: 0.6;
    }
    .idle-state h2 {
        color: #c9a84c;
        font-weight: 400;
        letter-spacing: 2px;
        font-size: 26px;
    }
    .idle-state p {
        color: #666666;
        font-size: 15px;
    }

    /* -------------------- COMPLAINT DISPLAY -------------------- */
    .complaint-box {
        background: #141418;
        border-left: 4px solid #c9a84c;
        padding: 1rem 1.5rem;
        margin-bottom: 1rem;
        border-radius: 0;
    }
    .complaint-box .label {
        color: #c9a84c;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 0 0 0.3rem 0;
    }
    .complaint-box .text {
        color: #ffffff;
        font-size: 15px;
        line-height: 1.6;
        margin: 0;
        white-space: pre-wrap;
    }

    /* -------------------- RESPONSIVE -------------------- */
    @media (max-width: 768px) {
        .judge-container { flex-direction: column; gap: 0.5rem; text-align: center; }
        .debate-column { min-height: auto; max-height: none; }
        .top-card { min-height: auto; }
    }
</style>
""", unsafe_allow_html=True)


# ============================================
# SESSION STATE INITIALIZATION
# ============================================
if "case_state" not in st.session_state:
    st.session_state.case_state = {
        "complaint": "",
        "entities": None,
        "accused": None,
        "victim": None,
        "offence": None,
        "facts": None,
        "laws": None,
        "sections_applied": None,
        "precedents": None,
        "pros_r1": None,
        "def_r1": None,
        "pros_r2": None,
        "def_r2": None,
        "verdict": None,
        "verdict_short": None,
        "confidence": None,
        "headline": None,
        "report": None,
        "is_running": False,
    }

if "simulation_complete" not in st.session_state:
    st.session_state.simulation_complete = False

if "stream_iter" not in st.session_state:
    st.session_state.stream_iter = None


# ============================================
# HEADER
# ============================================
st.markdown("""
<div class="court-header">
    <h1>⚖️ <span>COURTROOM</span> AI</h1>
    <p>Indian Law · Multi-Agent Adversarial Simulation</p>
</div>
""", unsafe_allow_html=True)


# ============================================
# INPUT SECTION
# ============================================
with st.container():
    col_input1, col_input2 = st.columns([3, 1])
    with col_input1:
        complaint = st.text_area(
            "Complaint",
            height=100,
            placeholder="Enter the case brief / complaint details here...",
            key="complaint_input",
            disabled=st.session_state.case_state["is_running"],
            label_visibility="collapsed"
        )
    with col_input2:
        st.write("")
        st.write("")
        if st.button("⚖️ Begin Simulation", type="primary", use_container_width=True):
            if not complaint.strip():
                st.warning("Please enter a complaint.")
                st.stop()

            # Reset state
            st.session_state.case_state = {
                "complaint": complaint,
                "entities": None,
                "accused": None,
                "victim": None,
                "offence": None,
                "facts": None,
                "laws": None,
                "sections_applied": None,
                "precedents": None,
                "pros_r1": None,
                "def_r1": None,
                "pros_r2": None,
                "def_r2": None,
                "verdict": None,
                "verdict_short": None,
                "confidence": None,
                "headline": None,
                "report": None,
                "is_running": True,
            }
            st.session_state.simulation_complete = False
            st.session_state.stream_iter = None
            st.rerun()


# ============================================
# STATUS INDICATOR
# ============================================
if st.session_state.case_state["is_running"]:
    st.markdown('<div class="status-text"><span class="gold">⚖️</span> Court is in session... Arguments are being exchanged.</div>', unsafe_allow_html=True)
elif st.session_state.simulation_complete:
    st.markdown('<div class="status-text"><span class="gold">✅</span> The Hon\'ble Judge has delivered the final verdict.</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="status-text">🏛️ Enter a case brief and begin the simulation.</div>', unsafe_allow_html=True)


# ============================================
# COMPLAINT DISPLAY (if submitted)
# ============================================
if st.session_state.case_state.get("complaint"):
    st.markdown(f"""
    <div class="complaint-box">
        <div class="label">📋 Case Brief</div>
        <div class="text">{st.session_state.case_state.get("complaint")}</div>
    </div>
    """, unsafe_allow_html=True)


st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)


# ============================================
# ROW 1: CASE MANAGER | LEGAL RESEARCH
# ============================================
col_cm, col_lr = st.columns(2, gap="large")

# ---------- CASE MANAGER ----------
with col_cm:
    st.markdown("""
    <div class="top-card">
        <h4>📂 Case Manager</h4>
    """, unsafe_allow_html=True)

    accused = st.session_state.case_state.get("accused")
    victim = st.session_state.case_state.get("victim")
    offence = st.session_state.case_state.get("offence")
    facts = st.session_state.case_state.get("facts")

    if accused or victim or offence:
        if accused:
            st.markdown(f'<div class="item"><strong>Accused:</strong> <span class="value">{accused}</span></div>', unsafe_allow_html=True)
        if victim:
            st.markdown(f'<div class="item"><strong>Victim:</strong> <span class="value">{victim}</span></div>', unsafe_allow_html=True)
        if offence:
            st.markdown(f'<div class="item"><strong>Offence:</strong> <span class="value">{offence}</span></div>', unsafe_allow_html=True)
        if facts:
            st.markdown(f'<div class="item"><strong>Facts:</strong> <span class="value">{facts}</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="empty">Awaiting case analysis...</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- LEGAL RESEARCH ----------
with col_lr:
    st.markdown("""
    <div class="top-card">
        <h4>📚 Legal Research</h4>
    """, unsafe_allow_html=True)

    laws = st.session_state.case_state.get("laws")
    sections = st.session_state.case_state.get("sections_applied")
    precedents = st.session_state.case_state.get("precedents")

    if laws or sections or precedents:
        if laws and laws != "Not specified":
            st.markdown(f'<div class="item"><strong>Laws:</strong> <span class="value">{laws}</span></div>', unsafe_allow_html=True)
        if sections and sections != "Not specified":
            st.markdown(f'<div class="item"><strong>Sections:</strong> <span class="value">{sections}</span></div>', unsafe_allow_html=True)
        if precedents and precedents != "Not specified":
            st.markdown(f'<div class="item"><strong>Precedents:</strong> <span class="value">{precedents}</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="empty">Researching applicable laws...</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ============================================
# ROW 2: JUDGE (Full Width)
# ============================================
verdict_short = st.session_state.case_state.get("verdict_short")
confidence = st.session_state.case_state.get("confidence")
full_reasoning = st.session_state.case_state.get("verdict", "")

# --- Judge Header ---
if not verdict_short:
    st.markdown("""
    <div class="judge-container">
        <span class="label">👨‍⚖️ The Hon'ble Judge</span><br>
        <span style="color: #666666; font-size: 18px;">Deliberating on the case...</span>
    </div>
    """, unsafe_allow_html=True)
else:
    if "guilty" in str(verdict_short).lower():
        verdict_color = "verdict-red"
        status_text = "GUILTY"
    else:
        verdict_color = "verdict-green"
        status_text = "NOT GUILTY"

    st.markdown(f"""
    <div class="judge-container">
        <span class="label">👨‍⚖️ The Hon'ble Judge</span><br>
        <span class="verdict-text {verdict_color}">{status_text}</span><br>
        <span style="color: #aaaaaa; font-size: 16px;">{verdict_short}</span><br>
        <span class="confidence">Confidence {confidence}%</span>
    </div>
    """, unsafe_allow_html=True)

# --- Full Reasoning (always show if available) ---
if full_reasoning and "Error" not in full_reasoning:
    st.markdown(f"""
    <div class="verdict-reasoning">
        <span class="label">📜 Full Verdict &amp; Reasoning</span>
        <div class="content">{full_reasoning}</div>
    </div>
    """, unsafe_allow_html=True)
elif verdict_short:
    # Fallback to short verdict if full reasoning missing
    st.markdown(f"""
    <div class="verdict-reasoning">
        <span class="label">📜 Verdict Summary</span>
        <div class="content">{verdict_short}</div>
    </div>
    """, unsafe_allow_html=True)


# ============================================
# ROW 3: PROSECUTOR R1 | DEFENSE R1
# ============================================
col_pros_r1, col_def_r1 = st.columns(2, gap="large")

# ---------- PROSECUTOR R1 ----------
with col_pros_r1:
    st.markdown("""
    <div class="debate-column">
        <div class="col-header">
            <span class="icon">⚔️</span>
            <h3>Prosecution</h3>
            <span class="sub">Round 1 — Opening</span>
        </div>
    """, unsafe_allow_html=True)

    r1 = st.session_state.case_state.get("pros_r1")
    if r1:
        st.markdown(f'<div class="argument-block prosecution">{r1}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="empty-state">⏳ Awaiting opening argument...</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- DEFENSE R1 ----------
with col_def_r1:
    st.markdown("""
    <div class="debate-column">
        <div class="col-header">
            <span class="icon">🛡️</span>
            <h3>Defense</h3>
            <span class="sub">Round 1 — Opening</span>
        </div>
    """, unsafe_allow_html=True)

    r1 = st.session_state.case_state.get("def_r1")
    if r1:
        st.markdown(f'<div class="argument-block defense">{r1}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="empty-state">⏳ Awaiting opening argument...</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================
# ROW 4: PROSECUTOR R2 | DEFENSE R2
# ============================================
col_pros_r2, col_def_r2 = st.columns(2, gap="large")

# ---------- PROSECUTOR R2 ----------
with col_pros_r2:
    st.markdown("""
    <div class="debate-column">
        <div class="col-header">
            <span class="icon">⚔️</span>
            <h3>Prosecution</h3>
            <span class="sub">Round 2 — Closing</span>
        </div>
    """, unsafe_allow_html=True)

    r2 = st.session_state.case_state.get("pros_r2")
    if r2:
        st.markdown(f'<div class="argument-block prosecution">{r2}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="empty-state">⏳ Awaiting closing argument...</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- DEFENSE R2 ----------
with col_def_r2:
    st.markdown("""
    <div class="debate-column">
        <div class="col-header">
            <span class="icon">🛡️</span>
            <h3>Defense</h3>
            <span class="sub">Round 2 — Closing</span>
        </div>
    """, unsafe_allow_html=True)

    r2 = st.session_state.case_state.get("def_r2")
    if r2:
        st.markdown(f'<div class="argument-block defense">{r2}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="empty-state">⏳ Awaiting closing argument...</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================
# ROW 5: COURT REPORTER (Full Width)
# ============================================
headline = st.session_state.case_state.get("headline")
report = st.session_state.case_state.get("report")

st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

if headline or report:
    st.markdown("""
    <div class="reporter-card">
        <h4>📰 Court Reporter</h4>
    """, unsafe_allow_html=True)
    if headline:
        st.markdown(f'<div class="headline">📌 {headline}</div>', unsafe_allow_html=True)
    if report:
        st.markdown(f'<div class="report">{report}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="reporter-card">
        <h4>📰 Court Reporter</h4>
        <div class="empty">⏳ Preparing the case summary...</div>
    </div>
    """, unsafe_allow_html=True)


# ============================================
# STREAMING ENGINE (INCREMENTAL UPDATES)
# ============================================
if st.session_state.case_state.get("is_running") and not st.session_state.simulation_complete:

    # If stream iterator is None, create it with the initial state
    if st.session_state.stream_iter is None:
        initial_state = {
            "complaint": st.session_state.case_state["complaint"],
            "entities": None,
            "accused": None,
            "victim": None,
            "offence": None,
            "facts": None,
            "laws": None,
            "sections_applied": None,
            "precedents": None,
            "pros_r1": None,
            "def_r1": None,
            "pros_r2": None,
            "def_r2": None,
            "verdict": None,
            "verdict_short": None,
            "confidence": None,
            "headline": None,
            "report": None,
        }
        st.session_state.stream_iter = court_graph.stream(
            initial_state,
            stream_mode="updates"
        )

    # Get the next update from the stream
    try:
        event = next(st.session_state.stream_iter)
        # event is a dict: {node_name: partial_state}
        for node_name, partial in event.items():
            # Update session state with all keys from this partial
            for key, value in partial.items():
                if value is not None:
                    st.session_state.case_state[key] = value
        # Rerun to reflect the new state in the UI
        st.rerun()
    except StopIteration:
        # Stream finished
        st.session_state.simulation_complete = True
        st.session_state.case_state["is_running"] = False
        st.session_state.stream_iter = None
        st.rerun()
    except Exception as e:
        st.error(f"Simulation error: {e}")
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

    # ---- DOWNLOAD REPORT ----
    # Build a formatted Markdown report from the state
    s = st.session_state.case_state
    report_lines = []
    report_lines.append("# ⚖️ Courtroom AI Simulation Report")
    report_lines.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")
    report_lines.append("## 📋 Case Brief")
    report_lines.append(s.get("complaint", "Not provided."))
    report_lines.append("")

    report_lines.append("## 📂 Case Manager")
    report_lines.append(f"- **Accused:** {s.get('accused', 'Unknown')}")
    report_lines.append(f"- **Victim:** {s.get('victim', 'Unknown')}")
    report_lines.append(f"- **Offence:** {s.get('offence', 'Unknown')}")
    report_lines.append(f"- **Facts:** {s.get('facts', 'Unknown')}")
    if s.get("entities"):
        report_lines.append(f"- **Full Analysis:**\n{s.get('entities')}")
    report_lines.append("")

    report_lines.append("## 📚 Legal Research")
    report_lines.append(f"- **Laws:** {s.get('laws', 'Not specified')}")
    report_lines.append(f"- **Sections Applied:** {s.get('sections_applied', 'Not specified')}")
    report_lines.append(f"- **Precedents:** {s.get('precedents', 'Not specified')}")
    report_lines.append("")

    report_lines.append("## ⚔️ Prosecution Round 1")
    report_lines.append(s.get('pros_r1', 'Not available.') or 'Not available.')
    report_lines.append("")

    report_lines.append("## 🛡️ Defense Round 1")
    report_lines.append(s.get('def_r1', 'Not available.') or 'Not available.')
    report_lines.append("")

    report_lines.append("## ⚔️ Prosecution Round 2")
    report_lines.append(s.get('pros_r2', 'Not available.') or 'Not available.')
    report_lines.append("")

    report_lines.append("## 🛡️ Defense Round 2")
    report_lines.append(s.get('def_r2', 'Not available.') or 'Not available.')
    report_lines.append("")

    report_lines.append("## 👨‍⚖️ Judge")
    report_lines.append(f"- **Verdict Short:** {s.get('verdict_short', 'Unknown')}")
    report_lines.append(f"- **Confidence:** {s.get('confidence', 'N/A')}%")
    report_lines.append(f"- **Full Verdict:**\n{s.get('verdict', 'Not available.')}")
    report_lines.append("")

    report_lines.append("## 📰 Reporter")
    report_lines.append(f"- **Headline:** {s.get('headline', 'No headline.')}")
    report_lines.append(f"- **Report:**\n{s.get('report', 'Not available.')}")
    report_lines.append("")

    report_content = "\n".join(report_lines)

    # ---- Buttons ----
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        st.download_button(
            label="📥 Download Report (Markdown)",
            data=report_content,
            file_name="courtroom_report.md",
            mime="text/markdown",
            use_container_width=True,
        )
    with col_btn2:
        if st.button("🔄 Start New Case", use_container_width=True):
            st.session_state.case_state = {
                "complaint": "",
                "entities": None,
                "accused": None,
                "victim": None,
                "offence": None,
                "facts": None,
                "laws": None,
                "sections_applied": None,
                "precedents": None,
                "pros_r1": None,
                "def_r1": None,
                "pros_r2": None,
                "def_r2": None,
                "verdict": None,
                "verdict_short": None,
                "confidence": None,
                "headline": None,
                "report": None,
                "is_running": False,
            }
            st.session_state.simulation_complete = False
            st.session_state.stream_iter = None
            st.rerun()