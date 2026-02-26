import os
import re

def parse_ruff_output(filepath):
    issues = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines or lines that don't start with a path (heuristic)
                # Ruff output typically starts with path/to/file.py:line:col:
                if not line or ':' not in line:
                    continue

                parts = line.split(':', 3)
                if len(parts) >= 4:
                    file_path = parts[0].strip()
                    # Check if file_path looks like a valid path (contains '/')
                    if '/' not in file_path and not file_path.endswith('.py'):
                         continue

                    line_num = parts[1].strip()
                    if not line_num.isdigit():
                        continue

                    error_desc = parts[3].strip()
                    issues.append({
                        'file': file_path,
                        'line': line_num,
                        'error': error_desc,
                        'solve': f"Fix Ruff issue: {error_desc}. Run `ruff check --fix {file_path}` or manually correct."
                    })
    except FileNotFoundError:
        pass
    return issues

def parse_mypy_output(filepath):
    issues = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                # Format: path/to/file.py:line: error: message [code]
                parts = line.split(':', 2)
                if len(parts) >= 3 and 'error:' in parts[2]:
                    file_path = parts[0].strip()
                    line_num = parts[1].strip()
                    error_desc = parts[2].strip()
                    issues.append({
                        'file': file_path,
                        'line': line_num,
                        'error': error_desc,
                        'solve': f"Fix Mypy type error: {error_desc}. Add type hints or ignore with `# type: ignore` if necessary."
                    })
    except FileNotFoundError:
        pass
    return issues

def parse_eslint_output(filepath):
    issues = []
    current_file = None
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                # Heuristic: file paths often start with '/' or contain extensions
                if (line.startswith('/') or line.endswith('.ts') or line.endswith('.tsx')) and ':' not in line:
                    current_file = line
                elif current_file and not line.startswith('✖') and not line.startswith('warning') and not line.startswith('error'):
                    # Trying to catch lines like "  27:21  warning  Unexpected console statement  no-console"
                    # But ESLint output format can be tricky. Let's look for line:col pattern at start
                    parts = line.split(maxsplit=3)
                    if len(parts) >= 3:
                        line_col = parts[0]
                        if ':' in line_col and line_col.replace(':', '').isdigit():
                            line_num = line_col.split(':')[0]
                            severity = parts[1] # error/warning
                            message = parts[2]
                            rule = parts[3] if len(parts) > 3 else "unknown"
                            issues.append({
                                'file': current_file,
                                'line': line_num,
                                'error': f"{severity}: {message} ({rule})",
                                'solve': f"Fix ESLint issue: {message}. Run `npm run lint -- --fix` or manually correct."
                            })
    except FileNotFoundError:
        pass
    return issues

def parse_tsc_output(filepath):
    issues = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                # Format: path/to/file.ts(line,col): error TSxxxx: message
                match = re.search(r'([^(]+)\((\d+),\d+\): error (TS\d+): (.+)', line)
                if match:
                    issues.append({
                        'file': match.group(1).strip(),
                        'line': match.group(2).strip(),
                        'error': f"{match.group(3)}: {match.group(4).strip()}",
                        'solve': f"Fix TypeScript error: {match.group(4).strip()}. check types."
                    })
    except FileNotFoundError:
        pass
    return issues

def parse_grep_output(filepath, error_type, solve_template):
    issues = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                parts = line.split(':', 2)
                if len(parts) >= 3:
                    file_path = parts[0].strip()
                    line_num = parts[1].strip()
                    content = parts[2].strip()
                    issues.append({
                        'file': file_path,
                        'line': line_num,
                        'error': f"{error_type}: {content}",
                        'solve': solve_template
                    })
    except FileNotFoundError:
        pass
    return issues

def parse_jsdoc_output(filepath):
    issues = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                parts = line.split(':', 2)
                if len(parts) >= 3:
                    file_path = parts[0].strip()
                    line_num = parts[1].strip()
                    error_desc = parts[2].strip()
                    issues.append({
                        'file': file_path,
                        'line': line_num,
                        'error': error_desc,
                        'solve': "Add JSDoc comment block describing the function parameters and return type."
                    })
    except FileNotFoundError:
        pass
    return issues

def main():
    all_issues = []

    all_issues.extend(parse_ruff_output('ruff_output.txt'))
    # all_issues.extend(parse_ruff_output('docstring_issues.txt')) # Same format
    all_issues.extend(parse_mypy_output('mypy_output.txt'))
    all_issues.extend(parse_eslint_output('eslint_output.txt'))
    all_issues.extend(parse_tsc_output('tsc_output.txt'))

    all_issues.extend(parse_grep_output('security_issues.txt', 'Security Risk', 'Replace weak hashing algorithm (md5) with a stronger one like sha256.'))
    all_issues.extend(parse_grep_output('frontend_alerts.txt', 'Production Alert', 'Remove `alert()` call used for debugging.'))
    all_issues.extend(parse_grep_output('frontend_logs.txt', 'Production Console Log', 'Remove `console.log()` call used for debugging.'))

    all_issues.extend(parse_jsdoc_output('jsdoc_issues.txt'))

    with open('REVIEW_REPORT.md', 'w') as f:
        f.write("# Code Review Report\n\n")
        f.write("**To:** cweir45@gmail.com\n\n")
        f.write("## Findings\n\n")

        if not all_issues:
            f.write("No issues found.\n")
        else:
            # Sort by file then line
            all_issues.sort(key=lambda x: (x['file'], int(x['line']) if x['line'].isdigit() else 0))

            for issue in all_issues:
                f.write(f"### {issue['file']}\n")
                f.write(f"- **Line:** {issue['line']}\n")
                f.write(f"- **Error:** {issue['error']}\n")
                f.write(f"- **Proposed Solve:**\n")
                f.write(f"  ```\n  {issue['solve']}\n  ```\n\n")

if __name__ == "__main__":
    main()
