import json
from pathlib import Path

REPO_ROOT = Path(r"c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2")
FRONTEND_SRC = REPO_ROOT / "frontend" / "src"

with open(REPO_ROOT / ".agents" / "teamwork_preview_explorer_survey_fe" / "deep_file_analysis.json", "r", encoding="utf-8") as f:
    deep = json.load(f)

with open(REPO_ROOT / ".agents" / "teamwork_preview_explorer_survey_fe" / "audit_summary.json", "r", encoding="utf-8") as f:
    summary = json.load(f)

print("=== MOCK / FALLBACK / PLACEHOLDER FINDINGS BY FILE ===")
for file_rel, fdata in sorted(deep.items()):
    mocks = fdata.get("mock_findings", [])
    mock_objs = fdata.get("mock_obj_summaries", [])
    if mocks or mock_objs:
        is_unmounted = file_rel in summary["unreachable_files"]
        print(f"\nFILE: {file_rel} {'[UNMOUNTED]' if is_unmounted else '[MOUNTED]'}")
        for mo in mock_objs:
            print(f"  * Object: {mo['variable']} -> {mo['preview']}")
        for m in mocks:
            print(f"  - Line {m['line']}: {m['content']}")
