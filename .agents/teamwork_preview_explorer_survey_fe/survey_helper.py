import os
import re
import json
from pathlib import Path

REPO_ROOT = Path(r"c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2")
FRONTEND_SRC = REPO_ROOT / "frontend" / "src"

def analyze_codebase():
    components_dir = FRONTEND_SRC / "components"
    pages_dir = FRONTEND_SRC / "pages"
    
    # 1. Collect all ts/tsx files
    all_files = list(FRONTEND_SRC.rglob("*.tsx")) + list(FRONTEND_SRC.rglob("*.ts"))
    
    # Map file relative path -> content
    file_contents = {}
    for f in all_files:
        rel = f.relative_to(FRONTEND_SRC).as_posix()
        try:
            with open(f, "r", encoding="utf-8") as fh:
                file_contents[rel] = fh.read()
        except Exception as e:
            file_contents[rel] = f"ERROR READING: {e}"

    # 2. Extract imports and exports per file
    file_info = {}
    for rel, content in file_contents.items():
        # find imports
        # match: import ... from '...'
        imports = []
        for line in content.splitlines():
            m = re.search(r'import\s+(?:(?:\*\s+as\s+\w+)|(?:\{[^}]+\})|(?:[\w\s,]+))\s+from\s+[\'"]([^\'"]+)[\'"]', line)
            if m:
                imports.append(m.group(1))
            else:
                m2 = re.search(r'import\s+[\'"]([^\'"]+)[\'"]', line)
                if m2:
                    imports.append(m2.group(1))
        
        # find exported names (default or named)
        exports = []
        # export default function/const/class/etc Name
        for m in re.finditer(r'export\s+default\s+(?:function|class|const|let|var)?\s*([A-Za-z0-9_]+)?', content):
            name = m.group(1) or "default"
            exports.append(f"default:{name}")
        # export const/function/class Name
        for m in re.finditer(r'export\s+(?:const|function|class|type|interface|enum)\s+([A-Za-z0-9_]+)', content):
            exports.append(m.group(1))
        # export { A, B }
        for m in re.finditer(r'export\s+\{([^}]+)\}', content):
            for item in m.group(1).split(','):
                item = item.strip().split(' as ')[-1].strip()
                if item:
                    exports.append(item)

        # find component props interface/type
        props_defs = re.findall(r'(?:interface|type)\s+([A-Za-z0-9_]*Props[A-Za-z0-9_]*)\s*(?:=\s*)?\{([^}]*)\}', content, re.DOTALL)
        
        # find mock / dummy / placeholder indicators
        mock_indicators = []
        for line_no, line in enumerate(content.splitlines(), 1):
            low = line.lower()
            if any(k in low for k in ['mock', 'dummy', 'placeholder', 'todo', 'fixme', 'sample_data', 'fake', 'stub']):
                # Ignore common CSS classes or standard react placeholder attribute if innocuous
                if 'placeholder=' in low and not any(k in low for k in ['mock', 'dummy', 'todo', 'fake', 'stub']):
                    continue
                mock_indicators.append((line_no, line.strip()))

        file_info[rel] = {
            "path": rel,
            "imports": imports,
            "exports": exports,
            "props_defs": props_defs,
            "mock_indicators": mock_indicators,
            "is_page": rel.startswith("pages/"),
            "is_component": rel.startswith("components/"),
        }

    return file_info, file_contents

if __name__ == "__main__":
    info, contents = analyze_codebase()
    with open(REPO_ROOT / ".agents" / "teamwork_preview_explorer_survey_fe" / "file_analysis.json", "w", encoding="utf-8") as out:
        json.dump(info, out, indent=2)
    print(f"Analyzed {len(info)} files.")
