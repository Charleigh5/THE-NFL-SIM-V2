import json
from pathlib import Path

REPO_ROOT = Path(r"c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2")
with open(REPO_ROOT / ".agents" / "teamwork_preview_explorer_survey_fe" / "page_analysis.json", "r", encoding="utf-8") as f:
    page_data = json.load(f)

for p, data in sorted(page_data.items()):
    print(f"=== PAGE: {p} ({data['lines']} lines) ===")
    print(f"  Imports: {data['imported_comps']}")
    print(f"  JSX Tags: {data['jsx_tags']}")
    print(f"  APIs: {data['apis']}")
    print(f"  Stores/Hooks: {data['stores']}")
    print(f"  States: {[s[0] for s in data['states']]}")
    print()
