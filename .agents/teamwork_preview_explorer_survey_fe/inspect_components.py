import json
import re
from pathlib import Path

REPO_ROOT = Path(r"c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2")
FRONTEND_SRC = REPO_ROOT / "frontend" / "src"

with open(REPO_ROOT / ".agents" / "teamwork_preview_explorer_survey_fe" / "audit_summary.json", "r", encoding="utf-8") as f:
    summary = json.load(f)

# Let's inspect each directory under components/
component_dirs = sorted(list(set(c.split('/')[1] for c in summary["components"].keys() if '/' in c)))

def inspect_component_details():
    res = {}
    for c_path, c_info in summary["components"].items():
        full_path = FRONTEND_SRC / c_path
        with open(full_path, "r", encoding="utf-8") as f:
            code = f.read()

        # Find which components this component imports
        imports = []
        for line in code.splitlines():
            m = re.search(r'from\s+[\'"]([^\'"]+)[\'"]', line)
            if m:
                imports.append(m.group(1))

        # Find props interface or type
        props_def = re.findall(r'(?:interface|type)\s+([A-Za-z0-9_]*Props[A-Za-z0-9_]*)\s*(?:=\s*)?\{([^}]*)\}', code, re.DOTALL)
        
        # Check exported components
        exports = []
        for m in re.finditer(r'export\s+(?:default\s+)?(?:function|const|class)\s+([A-Za-z0-9_]+)', code):
            exports.append(m.group(1))

        # Check state, API calls, hooks
        apis_used = re.findall(r'\b(api\.[A-Za-z0-9_]+|seasonApi\.[A-Za-z0-9_]+|medicalApi\.[A-Za-z0-9_]+|trainingApi\.[A-Za-z0-9_]+|tradeApi\.[A-Za-z0-9_]+|traitsApi\.[A-Za-z0-9_]+|scoutingApi\.[A-Za-z0-9_]+|abilitiesApi\.[A-Za-z0-9_]+)', code)
        
        res[c_path] = {
            "is_reachable": c_info["reachable"],
            "imported_by": c_info["imported_by"],
            "exports": exports,
            "props_def": props_def,
            "apis_used": list(set(apis_used)),
            "mock_hits": c_info["mock_hits"]
        }
    return res

if __name__ == "__main__":
    details = inspect_component_details()
    with open(REPO_ROOT / ".agents" / "teamwork_preview_explorer_survey_fe" / "component_details.json", "w", encoding="utf-8") as f:
        json.dump(details, f, indent=2)
    print(f"Details dumped for {len(details)} components.")
