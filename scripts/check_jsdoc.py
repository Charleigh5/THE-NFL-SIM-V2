import os
import re

def find_jsdoc_issues(root_dir):
    issues = []
    # Regex to find exported functions/classes
    # Simplified: looks for 'export const', 'export function', 'export class'
    # Then checks if the preceding lines contain '/**'
    export_pattern = re.compile(r'export\s+(const|function|class|interface|type)\s+(\w+)')

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.ts') or file.endswith('.tsx'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lines = f.readlines()

                    for i, line in enumerate(lines):
                        match = export_pattern.search(line)
                        if match:
                            # Check previous lines for JSDoc
                            has_jsdoc = False
                            # Look back up to 5 lines for a comment end '*/'
                            for j in range(1, 6):
                                if i - j >= 0:
                                    prev_line = lines[i-j].strip()
                                    if '*/' in prev_line:
                                        has_jsdoc = True
                                        break
                                    if prev_line and not prev_line.startswith('//') and not prev_line.startswith('*'):
                                         # If we hit code or empty line that isn't comment related, stop
                                         pass

                            if not has_jsdoc:
                                issues.append(f"{filepath}:{i+1}: Missing JSDoc for exported {match.group(1)} '{match.group(2)}'")
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")
    return issues

if __name__ == "__main__":
    issues = find_jsdoc_issues('frontend/src')
    for issue in issues:
        print(issue)
