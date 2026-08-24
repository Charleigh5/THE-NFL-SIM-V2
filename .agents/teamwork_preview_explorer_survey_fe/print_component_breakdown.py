import json
from pathlib import Path
from collections import defaultdict

REPO_ROOT = Path(r"c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2")
FRONTEND_SRC = REPO_ROOT / "frontend" / "src"

with open(REPO_ROOT / ".agents" / "teamwork_preview_explorer_survey_fe" / "component_details.json", "r", encoding="utf-8") as f:
    details = json.load(f)

# Group by directory
by_dir = defaultdict(dict)
for c_path, c_info in sorted(details.items()):
    parts = c_path.split('/')
    if len(parts) == 2:
        d = "root_components"
    else:
        d = parts[1]
    by_dir[d][c_path] = c_info

for d_name, comps in sorted(by_dir.items()):
    print(f"\n=======================================================")
    print(f"DIRECTORY: components/{d_name} (Total: {len(comps)})")
    print(f"=======================================================")
    for c_path, c_info in sorted(comps.items()):
        status = "MOUNTED" if c_info["is_reachable"] else "UNMOUNTED / ORPHANED"
        imported_by = ", ".join(c_info["imported_by"]) if c_info["imported_by"] else "NONE"
        exports = ", ".join(c_info["exports"]) if c_info["exports"] else "NONE"
        props_str = ""
        if c_info["props_def"]:
            props_str = "; ".join([f"{p[0]}: {p[1][:40]}..." for p in c_info["props_def"]])
        apis = ", ".join(c_info["apis_used"]) if c_info["apis_used"] else "None"
        mocks = len(c_info["mock_hits"])

        print(f"\n* File: {c_path}")
        print(f"  Status: [{status}]")
        print(f"  Exports: {exports}")
        print(f"  Imported By: {imported_by}")
        print(f"  Props: {props_str if props_str else 'No Props Interface'}")
        print(f"  APIs: {apis}")
        print(f"  Mock Hits: {mocks}")
        if mocks > 0:
            for mh in c_info["mock_hits"][:3]:
                print(f"    - L{mh[0]}: {mh[1]}")
