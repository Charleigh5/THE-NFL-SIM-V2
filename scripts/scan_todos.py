import os
import sys

def scan_todos(directory):
    todos = []
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            # Skip binary files or lock files
            if file.endswith(('.pyc', '.lock', '.png', '.jpg', '.jpeg', '.gif', '.ico')):
                continue

            try:
                with open(filepath, "r", encoding="utf-8", errors='ignore') as f:
                    for i, line in enumerate(f, 1):
                        if "TODO" in line or "FIXME" in line:
                            todos.append(f"{filepath}:{i}: {line.strip()}")
            except Exception as e:
                print(f"Error reading {filepath}: {e}")
    return todos

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scan_todos.py <directory>")
        sys.exit(1)

    issues = scan_todos(sys.argv[1])
    for issue in issues:
        print(issue)
