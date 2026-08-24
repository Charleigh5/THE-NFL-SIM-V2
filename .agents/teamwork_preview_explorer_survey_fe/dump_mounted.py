import json
import re
from pathlib import Path

REPO_ROOT = Path(r"c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2")
FRONTEND_SRC = REPO_ROOT / "frontend" / "src"

with open(REPO_ROOT / ".agents" / "teamwork_preview_explorer_survey_fe" / "audit_summary.json", "r", encoding="utf-8") as f:
    summary = json.load(f)

mounted_comps = [c for c, inf in summary["components"].items() if inf["reachable"]]

mounted_details = {}
for c_path in sorted(mounted_comps):
    fpath = FRONTEND_SRC / c_path
    with open(fpath, "r", encoding="utf-8") as fh:
        code = fh.read()
    
    props_match = re.findall(r'(?:interface|type)\s+([A-Za-z0-9_]*Props[A-Za-z0-9_]*)\s*(?:=\s*)?\{([^}]*)\}', code, re.DOTALL)
    
    exports = []
    for m in re.finditer(r'export\s+(?:default\s+)?(?:function|const|class)\s+([A-Za-z0-9_]+)', code):
        exports.append(m.group(1))
        
    states = re.findall(r'const\s+\[([A-Za-z0-9_]+),\s*set[A-Za-z0-9_]+\]\s*=\s*useState(?:<[^>]+>)?\(([^)]*)\)', code)
    
    imported = []
    for line in code.splitlines():
        m = re.search(r'from\s+[\'"]([^\'"]+)[\'"]', line)
        if m:
            imported.append(m.group(1))

    mocks = []
    for idx, line in enumerate(code.splitlines(), 1):
        low = line.lower()
        if any(w in low for w in ["mock", "dummy", "fake", "sample", "stub", "placeholder"]):
            # ignore html input placeholder="..." unless also has dummy/mock/stub
            if 'placeholder="' in low or "placeholder='" in low:
                if not any(w in low for w in ["mock", "dummy", "fake", "todo", "stub"]):
                    continue
            mocks.append((idx, line.strip()))

    imported_by = summary["components"][c_path]["imported_by"]

    mounted_details[c_path] = {
        "component_name": exports[0] if exports else c_path.split('/')[-1].replace('.tsx', '').replace('.ts', ''),
        "file_path": f"frontend/src/{c_path}",
        "lines": len(code.splitlines()),
        "exports": exports,
        "mounted_on": imported_by,
        "props_def": [(p[0], [line.strip() for line in p[1].strip().splitlines() if line.strip()]) for p in props_match],
        "states": [s[0] for s in states],
        "imports": imported,
        "mock_hits": mocks,
    }

with open(REPO_ROOT / ".agents" / "teamwork_preview_explorer_survey_fe" / "mounted_details.json", "w", encoding="utf-8") as out:
    json.dump(mounted_details, out, indent=2, ensure_ascii=False)

print(f"Dumped {len(mounted_details)} mounted component details.")
