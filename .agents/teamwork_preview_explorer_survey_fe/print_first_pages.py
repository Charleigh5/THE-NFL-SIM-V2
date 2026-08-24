import json
from pathlib import Path

REPO_ROOT = Path(r"c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2")
with open(REPO_ROOT / ".agents" / "teamwork_preview_explorer_survey_fe" / "page_analysis.json", "r", encoding="utf-8") as f:
    page_data = json.load(f)

first_pages = ["Dashboard.tsx", "DepthChart.tsx", "DraftLegacy.tsx", "DraftRoom.tsx", "FrontOffice.tsx", "FrontOffice_Baseline.tsx", "LiveSim.tsx", "MedicalCenter.tsx", "OffseasonDashboard.tsx"]

for p in first_pages:
    data = page_data.get(p, {})
    print(f"=== PAGE: {p} ({data.get('lines', 0)} lines) ===")
    print(f"  Imports: {data.get('imported_comps', [])}")
    print(f"  JSX Tags: {data.get('jsx_tags', [])}")
    print(f"  APIs: {data.get('apis', [])}")
    print(f"  Stores/Hooks: {data.get('stores', [])}")
    print(f"  States: {[s[0] for s in data.get('states', [])]}")
    print()
