import json
import re
from pathlib import Path

REPO_ROOT = Path(r"c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2")
FRONTEND_SRC = REPO_ROOT / "frontend" / "src"

with open(REPO_ROOT / ".agents" / "teamwork_preview_explorer_survey_fe" / "mounted_details.json", "r", encoding="utf-8") as f:
    mounted = json.load(f)

with open(REPO_ROOT / ".agents" / "teamwork_preview_explorer_survey_fe" / "audit_summary.json", "r", encoding="utf-8") as f:
    summary = json.load(f)

# Find all JSX calls in all files
all_files = list(FRONTEND_SRC.rglob("*.tsx"))
jsx_calls = {}

for f in all_files:
    rel = f.relative_to(FRONTEND_SRC).as_posix()
    with open(f, "r", encoding="utf-8") as fh:
        code = fh.read()
    
    # Find all JSX tags <ComponentName prop1={...} prop2="..." ...>
    # Note: Regex for JSX self-closing or opening tags
    matches = re.finditer(r'<([A-Z][A-Za-z0-9_]*)\s*([^>]*?)(?:/?>)', code)
    for m in matches:
        tag_name = m.group(1)
        attr_str = m.group(2)
        
        # Extract attribute names
        # prop="..." or prop={...} or boolean prop
        attrs = re.findall(r'\b([a-zA-Z0-9_\-]+)(?:=|\s|/>|$)', attr_str)
        # Filter standard JSX/HTML attributes if needed or keep all
        if tag_name not in jsx_calls:
            jsx_calls[tag_name] = []
        jsx_calls[tag_name].append({
            "caller_file": rel,
            "attrs": [a for a in attrs if a not in ["key", "className", "style", "id", "ref", "children"]]
        })

print(f"Captured JSX calls for {len(jsx_calls)} tags.")

with open(REPO_ROOT / ".agents" / "teamwork_preview_explorer_survey_fe" / "jsx_calls.json", "w", encoding="utf-8") as out:
    json.dump(jsx_calls, out, indent=2)
