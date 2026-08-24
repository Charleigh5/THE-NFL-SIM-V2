import json
from pathlib import Path

REPO_ROOT = Path(r"c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2")

with open(REPO_ROOT / ".agents" / "teamwork_preview_explorer_survey_fe" / "mounted_details.json", "r", encoding="utf-8") as f:
    mounted = json.load(f)

with open(REPO_ROOT / ".agents" / "teamwork_preview_explorer_survey_fe" / "unmounted_details.json", "r", encoding="utf-8") as f:
    unmounted = json.load(f)

with open(REPO_ROOT / ".agents" / "teamwork_preview_explorer_survey_fe" / "jsx_calls.json", "r", encoding="utf-8") as f:
    jsx_calls = json.load(f)

with open(REPO_ROOT / ".agents" / "teamwork_preview_explorer_survey_fe" / "page_analysis.json", "r", encoding="utf-8") as f:
    page_analysis = json.load(f)

catalog = []

# Process mounted components
for c_path, data in sorted(mounted.items()):
    cname = data["component_name"]
    calls = jsx_calls.get(cname, [])
    callers = list(set(c["caller_file"] for c in calls))
    
    expected_props = []
    if data["props_def"]:
        for pdef in data["props_def"]:
            expected_props.extend(pdef[1])
            
    passed_props_summary = []
    for call in calls:
        passed_props_summary.append({
            "caller": call["caller_file"],
            "passed_attrs": call["attrs"]
        })

    catalog.append({
        "component_name": cname,
        "file_path": data["file_path"],
        "status": "MOUNTED",
        "mounted_on": data["mounted_on"],
        "callers": callers,
        "expected_props": expected_props,
        "passed_props_samples": passed_props_summary[:3],
        "mock_hits": data["mock_hits"],
        "states": data["states"],
    })

# Process unmounted components
for c_path, data in sorted(unmounted.items()):
    cname = data["component_name"]
    calls = jsx_calls.get(cname, [])
    callers = list(set(c["caller_file"] for c in calls))
    
    expected_props = []
    if data["props_def"]:
        for pdef in data["props_def"]:
            expected_props.extend(pdef[1])

    catalog.append({
        "component_name": cname,
        "file_path": data["file_path"],
        "status": "UNMOUNTED / ORPHANED",
        "mounted_on": [],
        "callers": callers,
        "expected_props": expected_props,
        "passed_props_samples": [],
        "mock_hits": data["mock_hits"],
        "states": data["states"],
    })

with open(REPO_ROOT / ".agents" / "teamwork_preview_explorer_survey_fe" / "full_catalog.json", "w", encoding="utf-8") as out:
    json.dump(catalog, out, indent=2, ensure_ascii=False)

print(f"Catalog contains {len(catalog)} components.")
