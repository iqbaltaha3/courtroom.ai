#!/usr/bin/env python3
"""
End-to-end pipeline test for the Courtroom AI system.
Tests all agents: case manager → legal research → consultant → 
prosecutor → defense → judge → reporter → top consultant
"""

import os
import sys
from dotenv import load_dotenv
from graph.graph import court_graph

# Load environment variables
load_dotenv()

# Verify API keys are set
if not os.getenv("GROQ_API_KEY"):
    print("❌ ERROR: GROQ_API_KEY not set in .env")
    sys.exit(1)

if not os.getenv("TAVILY_API_KEY"):
    print("❌ ERROR: TAVILY_API_KEY not set in .env")
    sys.exit(1)

print("✅ API keys loaded successfully\n")

# A relevant legal case for testing
TEST_COMPLAINT = """
I, Rajesh Kumar (age 35), residing at 123 MG Road, Bangalore, lodge this complaint against 
Vikram Singh (age 32, shopkeeper at convenience store), residing at 456 Commercial Street.

On 15th June 2024, at approximately 8:30 PM, I went to Vikram's convenience store to purchase milk 
and groceries. I paid him ₹500 in cash for items totaling approximately ₹450. 

Vikram deliberately handed me incorrect change of ₹20 instead of ₹50. When I pointed this out immediately, 
Vikram rudely refused to correct it, using abusive language and physically pushing me out of the store. 
I fell and sustained minor injuries on my arm.

Two customers present in the store witnessed this incident. I believe Vikram acted with criminal intent 
to wrongfully gain ₹30 through dishonest means and caused me hurt through deliberate physical violence.

I request the court to take necessary action against Vikram for theft and intentional hurt.
"""

print("=" * 80)
print("COURTROOM AI - FULL PIPELINE TEST")
print("=" * 80)
print("\n📋 COMPLAINT FILED:")
print("-" * 80)
print(TEST_COMPLAINT)
print("-" * 80)

print("\n🔄 STARTING PIPELINE EXECUTION...\n")

try:
    # Initialize state with complaint
    initial_state = {
        "complaint": TEST_COMPLAINT,
        # These will be filled by case_manager
        "entities": None,
        "accused": None,
        "offence": None,
        "victim": None,
        "facts": None,
        "case_intake": None,
        # Legal research
        "laws": None,
        "sections_applied": None,
        "precedents": None,
        "legal_research": None,
        # Consultant
        "consultant": None,
        # Round 1
        "pros_r1": None,
        "def_r1": None,
        # Round 2
        "pros_r2": None,
        "def_r2": None,
        # Judge & Reporter
        "verdict": None,
        "verdict_short": None,
        "confidence": None,
        "reasoning": None,
        "probable_punishment": None,
        "judge_verdict": None,
        "headline": None,
        "report": None,
        # Top consultant
        "top_consultant": None,
    }
    
    # Run the pipeline with streaming
    for i, update in enumerate(court_graph.stream(initial_state, stream_mode="updates"), 1):
        if not isinstance(update, dict):
            continue
        
        node_name = list(update.keys())[0]
        updates = update[node_name]
        print(f"\n{'='*80}")
        print(f"[{i}] NODE: {node_name.upper()}")
        print(f"{'='*80}")
        
        # Display relevant outputs based on node
        if node_name == "case_manager":
            print(f"✓ Case Intake: {updates.get('case_intake', 'Pending')}")
            if updates.get('accused'):
                print(f"  Accused: {updates['accused']}")
            if updates.get('victim'):
                print(f"  Victim: {updates['victim']}")
            if updates.get('offence'):
                print(f"  Alleged Offence: {updates['offence']}")
        
        elif node_name == "legal_research":
            print(f"✓ Legal Research Complete")
            if updates.get('sections_applied'):
                print(f"  Sections Applied: {updates['sections_applied']}")
            if updates.get('precedents'):
                print(f"  Precedents Found: {updates['precedents']}")
            print(f"\n📚 Full Legal Research:\n{updates.get('laws', 'N/A')[:500]}...")
        
        elif node_name == "consultant":
            print(f"✓ Internal Consultant Assessment:\n{updates.get('consultant', 'N/A')[:400]}...")
        
        elif node_name == "prosecutor_r1":
            print(f"✓ Prosecutor Round 1 Arguments:\n{updates.get('pros_r1', 'N/A')[:400]}...")
        
        elif node_name == "defense_r1":
            print(f"✓ Defense Round 1 Arguments:\n{updates.get('def_r1', 'N/A')[:400]}...")
        
        elif node_name == "prosecutor_r2":
            print(f"✓ Prosecutor Round 2 Rebuttal:\n{updates.get('pros_r2', 'N/A')[:400]}...")
        
        elif node_name == "defense_r2":
            print(f"✓ Defense Round 2 Rebuttal:\n{updates.get('def_r2', 'N/A')[:400]}...")
        
        elif node_name == "judge":
            print(f"✓ Judge Verdict:")
            if updates.get('verdict_short'):
                print(f"  Decision: {updates['verdict_short']}")
            if updates.get('confidence'):
                print(f"  Confidence: {updates['confidence']}")
            if updates.get('probable_punishment'):
                print(f"  Probable Punishment: {updates['probable_punishment']}")
        
        elif node_name == "reporter":
            print(f"✓ Court Reporter Summary:")
            print(f"  Headline: {updates.get('headline', 'N/A')}")
            print(f"\n📰 Report:\n{updates.get('report', 'N/A')[:500]}...")
        
        elif node_name == "top_consultant":
            print(f"✓ Executive Consultant Analysis:\n{updates.get('top_consultant', 'N/A')[:500]}...")
    
    print(f"\n{'='*80}")
    print("✅ PIPELINE EXECUTION COMPLETED SUCCESSFULLY")
    print(f"{'='*80}\n")

except Exception as e:
    print(f"\n❌ ERROR DURING PIPELINE EXECUTION:")
    print(f"{type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
