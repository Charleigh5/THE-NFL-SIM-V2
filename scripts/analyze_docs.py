import os
import ast
import re

def analyze_python_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            content = f.read()
            tree = ast.parse(content)
        except Exception as e:
            return [], [], [], [f"Error parsing {filepath}: {e}"]

    missing_docs = []
    todos = []

    # Check for TODOs
    for i, line in enumerate(content.splitlines(), 1):
        if "TODO" in line or "FIXME" in line:
            todos.append((i, line.strip()))

    # Check docstrings
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not ast.get_docstring(node):
                missing_docs.append((node.lineno, node.name, type(node).__name__))

    return missing_docs, todos

def analyze_ts_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    missing_docs = []
    todos = []

    lines = content.splitlines()
    for i, line in enumerate(lines, 1):
        if "TODO" in line or "FIXME" in line:
            todos.append((i, line.strip()))

        # Heuristic for exported functions/classes missing JSDoc
        # Look for 'export function' or 'export class' or 'export const X = () =>'
        # Then check if the previous lines contain '/**'
        if re.search(r'export\s+(function|class|const|interface|type)\s+([a-zA-Z0-9_]+)', line):
            # Check previous lines for JSDoc end '*/'
            has_doc = False
            for offset in range(1, 10): # Check up to 10 lines back
                if i - offset < 0: break
                prev_line = lines[i - 1 - offset].strip()
                if '*/' in prev_line:
                    has_doc = True
                    break
                if prev_line and not prev_line.startswith('//') and not prev_line.startswith('*'):
                    # Hit code or empty line, stop looking
                    break

            if not has_doc:
                match = re.search(r'export\s+(function|class|const|interface|type)\s+([a-zA-Z0-9_]+)', line)
                name = match.group(2) if match else "unknown"
                missing_docs.append((i, name, "Export"))

    return missing_docs, todos

def main():
    report_file = "doc_analysis.log"
    with open(report_file, 'w') as log:
        log.write("Documentation and Technical Debt Analysis\n")
        log.write("=========================================\n\n")

        for root, dirs, files in os.walk("."):
            if "node_modules" in root or "__pycache__" in root or ".git" in root or "venv" in root:
                continue

            for file in files:
                filepath = os.path.join(root, file)

                if file.endswith(".py"):
                    missing, todos = analyze_python_file(filepath)
                    if missing or todos:
                        log.write(f"File: {filepath}\n")
                        for line, name, type_ in missing:
                            log.write(f"  Line {line}: Missing docstring for {type_} '{name}'\n")
                        for line, content in todos:
                            log.write(f"  Line {line}: {content}\n")
                        log.write("\n")

                elif file.endswith(".ts") or file.endswith(".tsx"):
                    missing, todos = analyze_ts_file(filepath)
                    if missing or todos:
                        log.write(f"File: {filepath}\n")
                        for line, name, type_ in missing:
                            log.write(f"  Line {line}: Missing JSDoc for exported '{name}'\n")
                        for line, content in todos:
                            log.write(f"  Line {line}: {content}\n")
                        log.write("\n")

if __name__ == "__main__":
    main()
