#!/usr/bin/env python3
"""Quick test to verify all imports and functions work."""

import sys

try:
    print("Testing imports...")
    from agents import call_claude, call_structured
    print("✅ agents/__init__.py imports work")
    
    from agents.case_manager import run_case_manager
    print("✅ case_manager imports work")
    
    from agents.legal_research import run_legal_research
    print("✅ legal_research imports work")
    
    from agents.top_consultant import run_top_consultant
    print("✅ top_consultant imports work")
    
    from agents.consultant import run_consultant
    print("✅ consultant imports work")
    
    from graph.graph import court_graph
    print("✅ graph imports work")
    
    print("\n✅ All imports successful!")
    print("✅ App should be ready to run")
    
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}")
    print(f"Details: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
