"""
Proof of concept — run the full graph with a sample complaint.
No server needed. Just:

    python tests/test_graph.py

Prints each agent's output as it completes.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from graph.graph import court_graph

SAMPLE_COMPLAINT = ("""Here is a full structured summary of the 2019 Supreme Court judgment in the Ram Janmabhoomi–Babri Masjid case (M. Siddiq v. Mahant Suresh Das & Ors., 2019) in a single cohesive paragraph:

The Supreme Court of India, in its unanimous 5-judge Constitution Bench judgment delivered on 9 November 2019, resolved the long-standing Ram Janmabhoomi–Babri Masjid title dispute by awarding the entire 2.77-acre disputed land in Ayodhya to the deity Ram Lalla Virajman for the construction of a Hindu temple, while directing the Union Government to allot an alternative 5-acre plot to the Sunni Waqf Board for the construction of a mosque. The Court held that the archaeological evidence presented by the Archaeological Survey of India (ASI) suggested the existence of a large non-Islamic structure beneath the demolished Babri Masjid, though it did not conclusively prove the destruction of a Hindu temple for mosque construction. It further found that while Muslims had offered prayers in the mosque for a long period, this alone did not establish exclusive legal title through adverse possession. The Court strongly condemned the 1992 demolition of the Babri Masjid as a violation of the rule of law and observed that such an act could not confer legal rights to the perpetrators. However, in crafting the remedy, the Court relied on its powers under Article 142 of the Constitution to do “complete justice,” concluding that the balance of equities, historical claims, and evidence favored granting the site for the construction of a temple while simultaneously ensuring that the Muslim community was not left without an alternative place of worship. The judgment effectively brought the decades-long litigation to a close while attempting to balance competing historical, religious, and legal claims within a constitutional framework."""
)

NODE_OUTPUT_KEY = {
    "case_manager":   "entities",
    "legal_research": "laws",
    "consultant":     "consultant",
    "prosecutor_r1":  "pros_r1",
    "defense_r1":     "def_r1",
    "prosecutor_r2":  "pros_r2",
    "defense_r2":     "def_r2",
    "judge":          "verdict",
    "reporter":       "report",
}

DIVIDERS = {
    "prosecutor_r1": "── ROUND 1 ──────────────────────────────",
    "prosecutor_r2": "── ROUND 2 ──────────────────────────────",
    "judge":         "── JUDGMENT ─────────────────────────────",
    "reporter":      "── COURT REPORT ─────────────────────────",
}

def main():
    print("\n⚖  COURTROOM AI — PROOF OF CONCEPT\n")
    print(f"COMPLAINT:\n{SAMPLE_COMPLAINT}\n")
    print("=" * 50)

    initial_state = {
        "complaint": SAMPLE_COMPLAINT,
        "entities": None, "accused": None, "offence": None,
        "laws": None,
        "consultant": None,
        "pros_r1": None, "def_r1": None,
        "pros_r2": None, "def_r2": None,
        "verdict": None, "verdict_short": None,
        "confidence": None, "sections_applied": None,
        "headline": None, "report": None,
    }

    for event in court_graph.stream(
        initial_state,
        stream_mode="updates"
    ):
        for node_name, partial in event.items():

            if node_name in DIVIDERS:
                print(f"\n{DIVIDERS[node_name]}\n")

            key = NODE_OUTPUT_KEY.get(node_name, "")

            if isinstance(partial, dict):
                content = partial.get(key, partial)
            else:
                content = partial

            label = node_name.replace("_", " ").upper()

            print(f"[{label}]")
            print(content)
            print()

    print("=" * 50)
    print("✓  Simulation complete.\n")


if __name__ == "__main__":
    main()
