import json
from pathlib import Path

REPO_ROOT = Path(r"c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2")
FRONTEND_SRC = REPO_ROOT / "frontend" / "src"

with open(REPO_ROOT / ".agents" / "teamwork_preview_explorer_survey_fe" / "audit_summary.json", "r", encoding="utf-8") as f:
    summary = json.load(f)

with open(REPO_ROOT / ".agents" / "teamwork_preview_explorer_survey_fe" / "deep_file_analysis.json", "r", encoding="utf-8") as f:
    deep = json.load(f)

print("=== ALL PAGES & SUBTREE BREAKDOWN ===")
for page_path, pdata in sorted(summary["pages"].items()):
    print(f"\nPAGE: {page_path}")
    print(f"  Reachable in router: {pdata['reachable']}")
    
    # Check what this page imports directly
    # Check mock findings in this page
    p_deep = deep.get(page_path, {})
    mocks = p_deep.get("mock_findings", [])
    if mocks:
        print(f"  Mock / Todo count in page: {len(mocks)}")
        for m in mocks[:5]:
            print(f"    - Line {m['line']} ({m['type']}): {m['content']}")
    else:
        print("  Mock / Todo count in page: 0")

    mock_objs = p_deep.get("mock_obj_summaries", [])
    if mock_objs:
        for mo in mock_objs:
            print(f"    * Mock Obj: {mo['variable']} -> {mo['preview']}")
