import re
import json
from pathlib import Path

REPO_ROOT = Path(r"c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2")
FRONTEND_SRC = REPO_ROOT / "frontend" / "src"

pages_dir = FRONTEND_SRC / "pages"
page_files = sorted(list(pages_dir.glob("*.tsx")))

page_analysis = {}
for pf in page_files:
    pname = pf.name
    with open(pf, "r", encoding="utf-8") as fh:
        code = fh.read()

    # Find imported components
    imported_comps = []
    for line in code.splitlines():
        m = re.search(r'import\s+(?:\{([^}]+)\}|([A-Za-z0-9_]+))\s+from\s+[\'"]([^\'"]+)[\'"]', line)
        if m:
            cnames = m.group(1) or m.group(2)
            src = m.group(3)
            imported_comps.append((cnames.strip(), src.strip()))

    # Find JSX child elements rendered
    jsx_tags = set(re.findall(r'<([A-Z][A-Za-z0-9_]*)', code))

    # Find API / store hooks
    apis = list(set(re.findall(r'\b(api\.[A-Za-z0-9_]+|seasonApi\.[A-Za-z0-9_]+|medicalApi\.[A-Za-z0-9_]+|trainingApi\.[A-Za-z0-9_]+|tradeApi\.[A-Za-z0-9_]+|traitsApi\.[A-Za-z0-9_]+|scoutingApi\.[A-Za-z0-9_]+|abilitiesApi\.[A-Za-z0-9_]+)', code)))
    stores = list(set(re.findall(r'\b(use[A-Za-z0-9_]+Store|use[A-Za-z0-9_]+Context|useTheme|useAudio)\b', code)))

    # Find state variables
    states = re.findall(r'const\s+\[([A-Za-z0-9_]+),\s*set[A-Za-z0-9_]+\]\s*=\s*useState(?:<[^>]+>)?\(([^)]*)\)', code)

    page_analysis[pname] = {
        "imported_comps": imported_comps,
        "jsx_tags": sorted(list(jsx_tags)),
        "apis": apis,
        "stores": stores,
        "states": states,
        "lines": len(code.splitlines())
    }

with open(REPO_ROOT / ".agents" / "teamwork_preview_explorer_survey_fe" / "page_analysis.json", "w", encoding="utf-8") as f:
    json.dump(page_analysis, f, indent=2)

print("Page analysis complete.")
