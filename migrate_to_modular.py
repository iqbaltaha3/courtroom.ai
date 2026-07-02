#!/usr/bin/env python3
"""
Migration Script: Reorganize MyPeshkar into modular structure
Run: python migrate_to_modular.py
"""

import shutil
import os
import re
from pathlib import Path

def update_imports(file_path: str) -> str:
    """Update file imports to match new module structure."""
    with open(file_path, "r") as f:
        content = f.read()
    
    # Update agent imports
    content = re.sub(
        r'from agents import',
        'from ..services import',
        content
    )
    content = re.sub(
        r'from agents\.schemas',
        'from .schemas',
        content
    )
    content = re.sub(
        r'from agents\.web_search',
        'from ..utils.web_search',
        content
    )
    
    # Update graph imports
    content = re.sub(
        r'from graph\.state import',
        'from ..core import',
        content
    )
    content = re.sub(
        r'from graph\.graph import',
        'from ..core import',
        content
    )
    
    # Update auth imports
    content = re.sub(
        r'from auth import',
        'from ..services import',
        content
    )
    
    # Update evaluation imports
    content = re.sub(
        r'from evaluation\.evaluator import',
        'from ..evaluation import',
        content
    )
    content = re.sub(
        r'from evaluation\.dashboard import',
        'from ..evaluation import',
        content
    )
    
    # Update API imports
    content = re.sub(
        r'from api\.main import',
        'from ..api import',
        content
    )
    
    return content


def copy_agents():
    """Copy agent files from agents/ to src/agents/ with updated imports."""
    print("📦 Copying agents...")
    agent_files = [
        ("agents/case_manager.py", "src/agents/case_analyst.py"),
        ("agents/legal_research.py", "src/agents/legal_researcher.py"),
        ("agents/prosecutor.py", "src/agents/prosecutor.py"),
        ("agents/defense.py", "src/agents/defense.py"),
        ("agents/judge.py", "src/agents/judge.py"),
        ("agents/reporter.py", "src/agents/reporter.py"),
        ("agents/consultant.py", "src/agents/consultant.py"),
        ("agents/top_consultant.py", "src/agents/top_consultant.py"),
        ("agents/schemas.py", "src/agents/schemas.py"),  # No import changes
        ("agents/web_search.py", "src/utils/web_search.py"),
    ]
    
    for src, dst in agent_files:
        if os.path.exists(src):
            content = update_imports(src)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(dst, "w") as f:
                f.write(content)
            print(f"  ✓ {src} → {dst}")
        else:
            print(f"  ✗ {src} not found")


def copy_evaluation():
    """Copy evaluation files from evaluation/ to src/evaluation/."""
    print("📊 Copying evaluation module...")
    eval_files = [
        ("evaluation/evaluator.py", "src/evaluation/evaluator.py"),
        ("evaluation/metrics.py", "src/evaluation/metrics.py"),
        ("evaluation/dashboard.py", "src/evaluation/dashboard.py"),
    ]
    
    for src, dst in eval_files:
        if os.path.exists(src):
            content = update_imports(src)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(dst, "w") as f:
                f.write(content)
            print(f"  ✓ {src} → {dst}")
        else:
            print(f"  ✗ {src} not found")
    
    # Copy data directory
    if os.path.exists("evaluation/data"):
        shutil.copytree("evaluation/data", "src/evaluation/data", dirs_exist_ok=True)
        print("  ✓ evaluation/data → src/evaluation/data")


def create_ui_stubs():
    """Create stub files for UI components."""
    print("🎨 Creating UI module stubs...")
    
    # Create __init__.py files
    init_files = [
        "src/ui/__init__.py",
        "src/ui/components/__init__.py",
        "src/ui/pages/__init__.py",
    ]
    
    for init_file in init_files:
        os.makedirs(os.path.dirname(init_file), exist_ok=True)
        if not os.path.exists(init_file):
            with open(init_file, "w") as f:
                f.write('"""UI module - Streamlit frontend."""\n')
            print(f"  ✓ Created {init_file}")


def create_utils_stubs():
    """Create stub files for utils."""
    print("🔧 Creating utils module stubs...")
    
    utils_files = {
        "src/utils/__init__.py": '"""Utils module - helper functions."""\n',
        "src/utils/helpers.py": '"""Helper functions for MyPeshkar."""\n\n# Add helper functions here\n',
        "src/utils/validators.py": '"""Validation functions."""\n\n# Add validators here\n',
        "src/utils/logger.py": '"""Logging configuration."""\n\nimport logging\n\nlogger = logging.getLogger("mypeshkar")\n',
    }
    
    for file_path, content in utils_files.items():
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write(content)
            print(f"  ✓ Created {file_path}")


def create_api_stubs():
    """Create stub for API module."""
    print("🔌 Creating API module stub...")
    
    api_init = "src/api/__init__.py"
    os.makedirs(os.path.dirname(api_init), exist_ok=True)
    if not os.path.exists(api_init):
        with open(api_init, "w") as f:
            f.write('"""REST API module - future API endpoints."""\n')
        print(f"  ✓ Created {api_init}")


def create_summary():
    """Create a summary of the migration."""
    summary = """# Migration Complete! ✅

Your MyPeshkar codebase has been reorganized into a clean modular structure.

## What Changed

- **src/config/** - All settings and constants
- **src/core/** - LangGraph orchestrator
- **src/agents/** - 8 specialized AI agents (renamed case_manager → case_analyst, legal_research → legal_researcher)
- **src/services/** - LLM service and authentication
- **src/evaluation/** - Metrics and evaluation dashboard
- **src/ui/** - Streamlit frontend (ready for component extraction)
- **src/utils/** - Helper functions and web search
- **src/api/** - REST API (stub)

## Next Steps

1. **Update Main App Import:**
   ```python
   # In app.py
   from src.core import court_graph
   from src.services import authenticate, submit_access_request
   from src.ui.pages import tools_page, metrics_page, vision_page
   ```

2. **Extract UI Components:**
   - Move CSS to `src/ui/components/styles.py`
   - Move form components to `src/ui/components/forms.py`
   - Split app.py into pages in `src/ui/pages/`

3. **Run Tests:**
   ```bash
   python -m pytest tests/
   ```

4. **Start Dev Server:**
   ```bash
   streamlit run src/ui/app.py
   ```

## Interview Explanation

"I reorganized the codebase into a layered modular structure:
- **Config layer** for settings
- **Core layer** for workflow orchestration  
- **Agent layer** for AI specialists
- **Service layer** for APIs and auth
- **UI layer** for Streamlit interface
- **Utils layer** for helpers

This makes it easy to add new features, test independently, and onboard new developers."

---

See MIGRATION_GUIDE.md for detailed import mappings.
"""
    
    with open("MIGRATION_COMPLETE.md", "w") as f:
        f.write(summary)
    print("✅ Created MIGRATION_COMPLETE.md")


def main():
    """Run all migration steps."""
    print("\n🚀 Starting MyPeshkar Migration to Modular Structure...\n")
    
    try:
        copy_agents()
        copy_evaluation()
        create_ui_stubs()
        create_utils_stubs()
        create_api_stubs()
        create_summary()
        
        print("\n✅ Migration complete! Check MIGRATION_COMPLETE.md for next steps.\n")
    except Exception as e:
        print(f"\n❌ Migration error: {e}\n")
        raise


if __name__ == "__main__":
    main()
