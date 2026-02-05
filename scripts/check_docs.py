import ast
import os
import sys

def check_docstrings(directory):
    missing_docs = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        node = ast.parse(f.read())

                    # Check module docstring
                    if not ast.get_docstring(node):
                         missing_docs.append(f"{filepath}:1: Missing module docstring")

                    for item in ast.walk(node):
                        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                            if not ast.get_docstring(item):
                                missing_docs.append(f"{filepath}:{item.lineno}: Missing docstring for {item.name}")
                except Exception as e:
                    print(f"Error parsing {filepath}: {e}")
    return missing_docs

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_docs.py <directory>")
        sys.exit(1)

    issues = check_docstrings(sys.argv[1])
    for issue in issues:
        print(issue)
