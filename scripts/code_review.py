import os
import ast
import sys

def check_file(filepath):
    issues = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        tree = ast.parse(content)

        has_docstring_module = ast.get_docstring(tree) is not None
        if not has_docstring_module:
            # issues.append((filepath, 1, "Missing module docstring", "Add a module-level docstring."))
            pass # Skipping module docstrings for noise reduction

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Check function docstring
                if ast.get_docstring(node) is None and node.name != "__init__":
                     issues.append((filepath, node.lineno, f"Missing docstring for function '{node.name}'", f"Add a docstring explaining '{node.name}'."))

                # Check return type hint (ignoring __init__)
                if node.returns is None and node.name != "__init__":
                    issues.append((filepath, node.lineno, f"Missing return type hint for function '{node.name}'", f"Add '-> type' annotation."))

                # Check argument type hints
                for arg in node.args.args:
                    if arg.annotation is None and arg.arg not in ['self', 'cls']:
                         issues.append((filepath, node.lineno, f"Missing type hint for argument '{arg.arg}' in '{node.name}'", f"Add ': type' annotation."))

    except Exception as e:
        issues.append((filepath, 1, f"Error parsing file: {e}", "Fix syntax errors."))

    return issues

def check_directory(directory):
    all_issues = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                all_issues.extend(check_file(filepath))
    return all_issues

def check_apts_structure():
    issues = []
    apts_root = "apts"
    if not os.path.isdir(apts_root):
        return []

    for root, dirs, files in os.walk(apts_root):
        if "__init__.py" not in files:
             issues.append((root, 0, f"Missing __init__.py in {root}", "Create an empty __init__.py file."))
    return issues

def main():
    issues = []
    issues.extend(check_directory("backend/app"))
    issues.extend(check_directory("apts"))
    issues.extend(check_apts_structure())

    # Sort by filepath
    issues.sort(key=lambda x: x[0])

    print("FILE|LINE|ERROR|SOLVE")
    for issue in issues:
        print(f"{issue[0]}|{issue[1]}|{issue[2]}|{issue[3]}")

if __name__ == "__main__":
    main()
