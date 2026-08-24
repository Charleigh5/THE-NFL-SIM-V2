import os
import re
import json
from pathlib import Path
from collections import defaultdict, deque

REPO_ROOT = Path(r"c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2")
FRONTEND_SRC = REPO_ROOT / "frontend" / "src"

def resolve_import(source_file: Path, import_path: str):
    if import_path.startswith('.'):
        target = (source_file.parent / import_path).resolve()
        for ext in ['', '.tsx', '.ts', '/index.tsx', '/index.ts', '.d.ts', '.css', '.module.css']:
            test_path = Path(str(target) + ext)
            if test_path.exists() and test_path.is_file():
                try:
                    return test_path.relative_to(FRONTEND_SRC).as_posix()
                except ValueError:
                    return None
    elif not import_path.startswith('@') and not import_path.startswith('react') and not import_path.startswith('lucide') and not import_path.startswith('framer') and not import_path.startswith('clsx'):
        target = (FRONTEND_SRC / import_path).resolve()
        for ext in ['', '.tsx', '.ts', '/index.tsx', '/index.ts']:
            test_path = Path(str(target) + ext)
            if test_path.exists() and test_path.is_file():
                try:
                    return test_path.relative_to(FRONTEND_SRC).as_posix()
                except ValueError:
                    return None
    return None

def main():
    all_tsx = list(FRONTEND_SRC.rglob("*.tsx"))
    all_ts = list(FRONTEND_SRC.rglob("*.ts"))
    all_files = all_tsx + all_ts

    file_contents = {}
    for f in all_files:
        rel = f.relative_to(FRONTEND_SRC).as_posix()
        try:
            with open(f, 'r', encoding='utf-8') as fh:
                file_contents[rel] = fh.read()
        except Exception as e:
            file_contents[rel] = f"ERROR: {e}"

    # Map file -> imported files (resolved)
    import_graph = {rel: set() for rel in file_contents}
    # Map file -> imported by
    imported_by = {rel: set() for rel in file_contents}

    for rel, content in file_contents.items():
        filepath = FRONTEND_SRC / rel
        import_matches = re.finditer(r'from\s+[\'"]([^\'"]+)[\'"]|import\s+[\'"]([^\'"]+)[\'"]', content)
        for m in import_matches:
            imp_path = m.group(1) or m.group(2)
            resolved = resolve_import(filepath, imp_path)
            if resolved and resolved in file_contents:
                import_graph[rel].add(resolved)
                imported_by[resolved].add(rel)

    # Detect exports per file
    exports_map = {}
    for rel, content in file_contents.items():
        exported = []
        for m in re.finditer(r'export\s+default\s+(?:function|class|const|let|var)?\s*([A-Za-z0-9_]+)?', content):
            name = m.group(1) or "default"
            exported.append(f"default({name})")
        for m in re.finditer(r'export\s+(?:const|function|class|type|interface|enum)\s+([A-Za-z0-9_]+)', content):
            exported.append(m.group(1))
        exports_map[rel] = exported

    # Identify entry point and reachable files
    # Roots: App.tsx, main.tsx, router.tsx, layouts/MainLayout.tsx
    # Let's find all files reachable from App.tsx / main.tsx / router.tsx
    reachable = set()
    queue = deque(["main.tsx", "App.tsx", "router.tsx", "layouts/MainLayout.tsx"])
    for q in list(queue):
        if q in file_contents:
            reachable.add(q)
    
    while queue:
        curr = queue.popleft()
        for neighbor in import_graph.get(curr, []):
            if neighbor not in reachable:
                reachable.add(neighbor)
                queue.append(neighbor)

    # Route mappings from router.tsx
    router_content = file_contents.get("router.tsx", "")
    routes = []
    # Pattern to capture path, element, loader, errorElement
    route_blocks = re.findall(r'\{\s*(?:index:\s*true|path:\s*[\'"]([^\'"]+)[\'"])[^}]*element:\s*<([A-Za-z0-9_]+)[^/]*/>(?:[^}]*loader:\s*([A-Za-z0-9_]+))?[^}]*\}', router_content, re.DOTALL)
    for path, elem, loader in route_blocks:
        routes.append({
            "path": path or "/",
            "element": elem,
            "loader": loader or None
        })

    # Catalog every page in pages/
    pages_catalog = {}
    for rel in sorted(file_contents.keys()):
        if rel.startswith("pages/") and rel.endswith(".tsx"):
            is_reachable = rel in reachable
            parents = sorted(list(imported_by[rel]))
            pages_catalog[rel] = {
                "reachable": is_reachable,
                "imported_by": parents,
                "exports": exports_map.get(rel, [])
            }

    # Catalog every component in components/
    components_catalog = {}
    for rel in sorted(file_contents.keys()):
        if rel.startswith("components/") and (rel.endswith(".tsx") or rel.endswith(".ts")):
            is_reachable = rel in reachable
            parents = sorted(list(imported_by[rel]))
            
            # Check mock data indicators
            content = file_contents[rel]
            mock_hits = []
            for i, line in enumerate(content.splitlines(), 1):
                low = line.lower()
                if any(w in low for w in ["mock", "dummy", "fake", "hardcoded", "placeholder", "sample_data", "stub", "todo", "fixme"]):
                    # filter out html input placeholder="..." unless it looks like mock
                    if 'placeholder="' in low or "placeholder='" in low:
                        if not any(w in low for w in ["mock", "dummy", "fake", "todo", "stub"]):
                            continue
                    mock_hits.append((i, line.strip()))
            
            # Extract Props definition
            props_match = re.findall(r'(?:interface|type)\s+([A-Za-z0-9_]*Props[A-Za-z0-9_]*)\s*(?:=\s*)?\{([^}]*)\}', content, re.DOTALL)
            
            components_catalog[rel] = {
                "reachable": is_reachable,
                "imported_by": parents,
                "exports": exports_map.get(rel, []),
                "props": [(p[0], p[1].strip()) for p in props_match],
                "mock_hits": mock_hits
            }

    output = {
        "routes": routes,
        "reachable_count": len(reachable),
        "total_files": len(file_contents),
        "unreachable_files": sorted(list(set(file_contents.keys()) - reachable)),
        "pages": pages_catalog,
        "components": components_catalog
    }

    with open(REPO_ROOT / ".agents" / "teamwork_preview_explorer_survey_fe" / "audit_summary.json", "w", encoding="utf-8") as out:
        json.dump(output, out, indent=2)

    print(f"Summary generated: {len(pages_catalog)} pages, {len(components_catalog)} components.")
    print(f"Reachable files: {len(reachable)} / {len(file_contents)}. Unreachable: {len(output['unreachable_files'])}")

if __name__ == "__main__":
    main()
