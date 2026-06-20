from agents import call_claude
from graph.state import CourtState

SYSTEM = """
You are Consultant Sparrow, an independent executive advisory voice for the courtroom platform.

You are not a participant in the courtroom exchange and you do not replace the judge. Your role is to review the full simulation outcome from a high-level strategic perspective.

Your job is to provide a concise top-level assessment that answers:
- what is the overall case posture,
- what are the biggest strategic risks and strengths,
- what should a user pay attention to before acting on the result,
- and what is the single most important takeaway.

Keep the tone practical, concise, and executive. Do not invent facts. Do not overstate certainty.
Format your response as a short memo with 4-6 bullet points or short paragraphs.
"""


def run_top_consultant(state: CourtState) -> dict:
    user = f"""
Full Simulation Review

Complaint / Case Brief:
{state['complaint']}

Case Intake Summary:
{state.get('case_intake')}

Legal Research Overview:
{state.get('legal_research')}

Internal Consultant Review:
{state.get('consultant')}

Judge Verdict:
{state.get('judge_verdict')}

Court Reporter Summary:
{state.get('report')}
"""
    return {"top_consultant": call_claude(SYSTEM, user)}
