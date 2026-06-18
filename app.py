import streamlit as st
from graph.graph import court_graph
print(court_graph)

st.set_page_config(
    page_title="Courtroom AI",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ Courtroom AI")
st.caption("Indian Law Multi-Agent Court Simulation")

complaint = st.text_area(
    "Complaint",
    height=150,
    placeholder="Describe the complaint..."
)

if st.button("Begin Simulation"):

    if not complaint.strip():
        st.warning("Enter a complaint first.")
        st.stop()

    initial_state = {
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
    }

    NODE_NAMES = {
        "case_manager": "📂 Case Manager",
        "legal_research": "📚 Legal Research",
        "prosecutor_r1": "⚔️ Prosecutor Round 1",
        "defense_r1": "🛡️ Defense Round 1",
        "prosecutor_r2": "⚔️ Prosecutor Round 2",
        "defense_r2": "🛡️ Defense Round 2",
        "judge": "👨‍⚖️ Judge",
        "reporter": "📰 Reporter",
    }

    with st.spinner("Running simulation..."):

        for event in court_graph.stream(
            initial_state,
            stream_mode="updates"
        ):

            for node_name, partial in event.items():

                st.subheader(
                    NODE_NAMES.get(node_name, node_name)
                )

                st.write(partial)

    st.success("Simulation complete.")