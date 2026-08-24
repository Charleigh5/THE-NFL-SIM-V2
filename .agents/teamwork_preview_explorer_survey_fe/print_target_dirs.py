import json
from pathlib import Path
from collections import defaultdict

REPO_ROOT = Path(r"c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2")
with open(REPO_ROOT / ".agents" / "teamwork_preview_explorer_survey_fe" / "component_details.json", "r", encoding="utf-8") as f:
    details = json.load(f)

by_dir = defaultdict(dict)
for c_path, c_info in sorted(details.items()):
    parts = c_path.split('/')
    if len(parts) == 2:
        d = "root_components"
    else:
        d = parts[1]
    by_dir[d][c_path] = c_info

target_dirs = ["root_components", "3d", "audio", "coaching", "common", "debug", "dev", "draft", "game", "history", "immersive", "medical", "news", "offseason", "playbook", "player"]

for d_name in target_dirs:
    comps = by_dir.get(d_name, {})
    mounted = [c for c, inf in comps.items() if inf["is_reachable"]]
    unmounted = [c for c, inf in comps.items() if not inf["is_reachable"]]
    print(f"=== {d_name.upper()} (Total: {len(comps)} | Mounted: {len(mounted)} | Unmounted: {len(unmounted)}) ===")
    for c, inf in sorted(comps.items()):
        st = "MOUNTED" if inf["is_reachable"] else "UNMOUNTED"
        exp = ", ".join(inf["exports"]) if inf["exports"] else "NONE"
        imp = ", ".join(inf["imported_by"]) if inf["imported_by"] else "NONE"
        apis = ", ".join(inf["apis_used"]) if inf["apis_used"] else "None"
        props = [p[0] for p in inf["props_def"]]
        print(f"  [{st}] {c.split('/')[-1]} | Exp: {exp} | ImpBy: {imp} | Props: {props} | APIs: {apis}")
    print()
