import os
import re
import json
from pathlib import Path

REPO_ROOT = Path(r"c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2")
FRONTEND_SRC = REPO_ROOT / "frontend" / "src"

def analyze_all_files_deep():
    files = list(FRONTEND_SRC.rglob("*.tsx")) + list(FRONTEND_SRC.rglob("*.ts"))
    
    # Load mount graph
    with open(REPO_ROOT / ".agents" / "teamwork_preview_explorer_survey_fe" / "audit_summary.json", "r", encoding="utf-8") as f:
        summary = json.load(f)

    detailed_report = {}

    for fpath in files:
        rel = fpath.relative_to(FRONTEND_SRC).as_posix()
        try:
            with open(fpath, "r", encoding="utf-8") as fh:
                code = fh.read()
        except Exception as e:
            continue

        # Extract component names exported or declared
        comp_names = []
        for m in re.finditer(r'(?:export\s+(?:default\s+)?(?:function|const|class)|function|const)\s+([A-Z][A-Za-z0-9_]*)', code):
            comp_names.append(m.group(1))

        # Extract props interface/type
        props_defs = []
        for m in re.finditer(r'(?:export\s+)?(?:interface|type)\s+([A-Za-z0-9_]*Props[A-Za-z0-9_]*)\s*(?:=\s*)?\{([^}]*)\}', code, re.DOTALL):
            props_defs.append({
                "name": m.group(1),
                "fields": [line.strip() for line in m.group(2).strip().splitlines() if line.strip() and not line.strip().startswith("//")]
            })

        # Direct component function prop signatures (e.g. const Foo: React.FC<Props> = ({ a, b }) => ...)
        prop_destructuring = []
        for m in re.finditer(r'(?:function\s+([A-Z][A-Za-z0-9_]*)|const\s+([A-Z][A-Za-z0-9_]*)\s*:\s*React\.FC(?:<[^>]+>)?\s*=\s*|\bconst\s+([A-Z][A-Za-z0-9_]*)\s*=\s*)\s*\(\s*\{([^}]+)\}', code):
            cname = m.group(1) or m.group(2) or m.group(3)
            fields = [x.strip().split('=')[0].split(':')[0].strip() for x in m.group(4).split(',') if x.strip()]
            prop_destructuring.append({"component": cname, "props": fields})

        # Look for hardcoded mock data patterns:
        # 1. const MOCK_... / const mock... / DUMMY_...
        # 2. Hardcoded arrays with player names / dummy stats / mock scores / etc.
        # 3. Fallbacks || [ { id: 1, ... } ] or useState([ ... ])
        # 4. Comments with TODO, FIXME, Mock, Placeholder
        mock_findings = []
        for line_no, line in enumerate(code.splitlines(), 1):
            stripped = line.strip()
            # Const mock variables
            if re.search(r'\b(?:const|let|var)\s+(?:mock|dummy|sample|fake|placeholder|defaultMock)[A-Za-z0-9_]*\s*=', stripped, re.IGNORECASE):
                mock_findings.append({"line": line_no, "type": "MOCK_VAR_DECLARATION", "content": stripped})
            elif re.search(r'\bMOCK_[A-Z0-9_]+\b', stripped):
                mock_findings.append({"line": line_no, "type": "MOCK_CONSTANT_USAGE", "content": stripped})
            elif 'TODO:' in stripped or 'FIXME:' in stripped or 'TODO ' in stripped:
                mock_findings.append({"line": line_no, "type": "TODO_COMMENT", "content": stripped})
            elif re.search(r'//.*mock', stripped, re.IGNORECASE) or re.search(r'/\*.*mock', stripped, re.IGNORECASE):
                mock_findings.append({"line": line_no, "type": "MOCK_COMMENT", "content": stripped})
            elif re.search(r'//.*placeholder', stripped, re.IGNORECASE):
                mock_findings.append({"line": line_no, "type": "PLACEHOLDER_COMMENT", "content": stripped})
            elif re.search(r'//.*dummy', stripped, re.IGNORECASE):
                mock_findings.append({"line": line_no, "type": "DUMMY_COMMENT", "content": stripped})

        # Check for hardcoded mock data arrays (like array of objects with name, rating, etc.)
        mock_objects = re.findall(r'const\s+([A-Za-z0-9_]*(?:Mock|mock|Dummy|dummy|Sample|sample)[A-Za-z0-9_]*)\s*(?::\s*[^=]+)?=\s*(\[[\s\S]*?\]|\{[\s\S]*?\});', code)
        mock_obj_summaries = []
        for var_name, body in mock_objects:
            mock_obj_summaries.append({
                "variable": var_name,
                "length_chars": len(body),
                "preview": body[:120].replace('\n', ' ') + ('...' if len(body) > 120 else '')
            })

        detailed_report[rel] = {
            "component_names": list(set(comp_names)),
            "props_defs": props_defs,
            "prop_destructuring": prop_destructuring,
            "mock_findings": mock_findings,
            "mock_obj_summaries": mock_obj_summaries,
            "is_reachable": rel in summary.get("unreachable_files", []) or rel in summary.get("pages", {}) or rel in summary.get("components", {})
        }

    with open(REPO_ROOT / ".agents" / "teamwork_preview_explorer_survey_fe" / "deep_file_analysis.json", "w", encoding="utf-8") as out:
        json.dump(detailed_report, out, indent=2)

    print("Deep analysis written.")

if __name__ == "__main__":
    analyze_all_files_deep()
