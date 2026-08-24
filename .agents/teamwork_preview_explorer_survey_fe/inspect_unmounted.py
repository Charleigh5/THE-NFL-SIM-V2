import json
from pathlib import Path

REPO_ROOT = Path(r"c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2")
FRONTEND_SRC = REPO_ROOT / "frontend" / "src"

with open(REPO_ROOT / ".agents" / "teamwork_preview_explorer_survey_fe" / "audit_summary.json", "r", encoding="utf-8") as f:
    summary = json.load(f)

unmounted = [c for c, inf in summary["components"].items() if not inf["reachable"]]

print(f"=== UNMOUNTED COMPONENTS DEEP INSPECTION ({len(unmounted)}) ===")
for c_path in sorted(unmounted):
    fpath = FRONTEND_SRC / c_path
    with open(fpath, "r", encoding="utf-8") as fh:
        lines = fh.readlines()
    
    # first 15 lines of content
    preview = "".join(lines[:15])
    print(f"\nFILE: {c_path} ({len(lines)} lines)")
    print(f"--- PREVIEW ---")
    print(preview.strip())
