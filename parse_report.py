import json
import re

def write_report():
    report = []

    report.append("Code Review Report")
    report.append("==================\n")

    # Process Ruff
    try:
        with open('artifacts/ruff_output.txt', 'r') as f:
            content = f.read()
            blocks = re.split(r'--> (.*?):(\d+):(\d+)', content)

            for i in range(1, len(blocks), 4):
                if i + 3 < len(blocks):
                    current_file = blocks[i]
                    line_num = blocks[i+1]

                    prev_block = blocks[i-1]
                    error_match = re.search(r'([A-Z0-9]{4,5}) (\[\*?\] )?(.*)', prev_block.strip().split('\n')[-1])
                    if error_match:
                        error_code = error_match.group(1)
                        error_desc = error_match.group(3)

                        report.append(f"File: {current_file}")
                        report.append(f"Line: {line_num}")
                        report.append(f"Error: {error_code} - {error_desc}")
                        report.append(f"Solve: Apply formatting/fixing according to {error_code}")

                        next_block = blocks[i+3]
                        code_match = re.search(r'^\s*\|\s*(.*)$', next_block, re.MULTILINE)
                        if code_match:
                            report.append("Proposed Code Solve:")
                            report.append("```python\n" + code_match.group(1) + "\n```\n")
                        else:
                            report.append("Proposed Code Solve:")
                            report.append("```python\n# Fix code accordingly\n```\n")
    except Exception as e:
        print(f"Error parsing ruff: {e}")

    # Process Mypy
    try:
        with open('artifacts/mypy_output.txt', 'r') as f:
            for line in f:
                parts = line.split(":")
                if len(parts) >= 4 and "error" in line:
                    file_path = parts[0]
                    line_num = parts[1]
                    error_msg = ":".join(parts[3:]).strip()

                    report.append(f"File: {file_path}")
                    report.append(f"Line: {line_num}")
                    report.append(f"Error: Mypy - {error_msg}")
                    report.append("Solve: Add or correct type hints.")
                    report.append("Proposed Code Solve:")
                    report.append("```python\n# Add specific type hint corresponding to the error\n```\n")
    except Exception as e:
        print(f"Error parsing mypy: {e}")

    # Process ESLint
    try:
        with open('artifacts/eslint_output.json', 'r') as f:
            data = json.load(f)
            for file_data in data:
                file_path = file_data.get('filePath', '')
                for msg in file_data.get('messages', []):
                    line_num = msg.get('line', 'Unknown')
                    error_msg = msg.get('message', 'Unknown error')
                    rule_id = msg.get('ruleId', 'Unknown rule')
                    source = msg.get('source', '')

                    if '/app/frontend/' in file_path:
                        file_path = file_path.split('/app/frontend/')[1]

                    report.append(f"File: frontend/{file_path}")
                    report.append(f"Line: {line_num}")
                    report.append(f"Error: ESLint [{rule_id}] - {error_msg}")
                    report.append(f"Solve: Apply fixes according to {rule_id}.")
                    report.append("Proposed Code Solve:")

                    if source:
                        report.append("```typescript\n" + source.strip() + " // Apply linter suggested fix\n```\n")
                    else:
                        report.append("```typescript\n// Apply linter suggested fix\n```\n")
    except Exception as e:
        print(f"Error parsing eslint: {e}")

    # Process Bandit
    try:
        with open('artifacts/bandit_output.txt', 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if line.startswith(">> Issue:"):
                    issue = line.strip().split(">> Issue: ")[1]
                    file_line = ""
                    for j in range(i+1, min(i+10, len(lines))):
                        if lines[j].startswith("   Location:"):
                            file_line = lines[j].strip().split("Location: ")[1]
                            break
                    if file_line:
                        parts = file_line.split(":")
                        file_path = parts[0]
                        line_num = parts[1] if len(parts) > 1 else "Unknown"

                        report.append(f"File: {file_path}")
                        report.append(f"Line: {line_num}")
                        report.append(f"Error: Bandit Security Issue - {issue}")
                        report.append("Solve: Address the security vulnerability (e.g., use more secure functions/configurations).")
                        report.append("Proposed Code Solve:")
                        report.append("```python\n# Apply security fix\n```\n")
    except Exception as e:
        print(f"Error parsing bandit: {e}")

    # Process Missing Files
    missing_files = []
    import os
    if not os.path.exists('docs/architecture'): missing_files.append('docs/architecture/')
    if not os.path.exists('docs/data'): missing_files.append('docs/data/')
    if not os.path.exists('AGENTS.md'): missing_files.append('AGENTS.md')
    if not os.path.exists('scripts/check_docs.py'): missing_files.append('scripts/check_docs.py')

    if missing_files:
        for missing in missing_files:
            report.append(f"File: {missing}")
            report.append(f"Line: N/A")
            report.append(f"Error: Missing File")
            report.append(f"Solve: Create the missing file or directory.")
            report.append("Proposed Code Solve:")
            report.append(f"```bash\nmkdir -p {os.path.dirname(missing)} && touch {missing}\n```\n")

    # Save report
    with open('REVIEW_REPORT.md', 'w') as f:
        f.write("\n".join(report))

if __name__ == "__main__":
    write_report()
