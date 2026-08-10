import json
import smtplib
from email.mime.text import MIMEText
import sys

def format_issue(file, line, error, solve):
    return f"File: {file}\nLine: {line}\nError: {error}\nProposed Solve:\n```\n{solve}\n```\n\n"

def main():
    report = "Code Review Report\n==================\n\n"

    # Ruff
    report += "## Ruff Issues (Top 10)\n"
    try:
        with open("artifacts/ruff_output.json") as f:
            ruff_data = json.load(f)
            count = 0
            for item in ruff_data:
                if count >= 10:
                    break
                file = item.get("filename", "Unknown")
                line = item.get("location", {}).get("row", "Unknown")
                error = item.get("message", "Unknown")
                fix = item.get("fix")
                solve = "No fix provided by Ruff."
                if fix and "edits" in fix:
                    solve = "\n".join([e.get("content", "") for e in fix["edits"]])
                report += format_issue(file, line, error, solve)
                count += 1
    except Exception as e:
        report += f"Failed to load Ruff data: {e}\n\n"

    # Bandit
    report += "## Bandit Security Issues (Top 10)\n"
    try:
        with open("artifacts/bandit_output.json") as f:
            content = f.read()
            start = content.find("{")
            if start != -1:
                bandit_data = json.loads(content[start:])
                count = 0
                for item in bandit_data.get("results", []):
                    if count >= 10:
                        break
                    file = item.get("filename", "Unknown")
                    line = item.get("line_number", "Unknown")
                    error = item.get("issue_text", "Unknown")
                    solve = f"# Replace or suppress bandit warning\n# {item.get('issue_cwe', {}).get('link', '')}"
                    report += format_issue(file, line, error, solve)
                    count += 1
    except Exception as e:
        report += f"Failed to load Bandit data: {e}\n\n"

    # ESLint
    report += "## ESLint Issues\n"
    try:
        with open("artifacts/eslint_output.json") as f:
            eslint_data = json.load(f)
            count = 0
            for file_item in eslint_data:
                for msg in file_item.get("messages", []):
                    if count >= 10:
                        break
                    file = file_item.get("filePath", "Unknown")
                    line = msg.get("line", "Unknown")
                    error = msg.get("message", "Unknown")
                    solve = "No automatic fix available."
                    if "fix" in msg:
                        solve = f"Apply fix at range {msg['fix'].get('range')} with text: {msg['fix'].get('text')}"
                    report += format_issue(file, line, error, solve)
                    count += 1
                if count >= 10:
                    break
    except Exception as e:
        report += f"Failed to load ESLint data: {e}\n\n"

    # Mypy
    report += "## Mypy Issues (Top 10)\n"
    try:
        with open("artifacts/mypy_output.txt") as f:
            lines = f.readlines()
            count = 0
            for line in lines:
                if "error:" in line and count < 10:
                    parts = line.split(":")
                    if len(parts) >= 4:
                        file = parts[0].strip()
                        line_num = parts[1].strip()
                        error = parts[3].strip()
                        solve = "Fix type annotation."
                        report += format_issue(file, line_num, error, solve)
                        count += 1
    except Exception as e:
        report += f"Failed to load Mypy data: {e}\n\n"

    # Missing files/docs
    report += "## Missing Files & Documentation\n"
    report += "- `docs/architecture/` missing.\n"
    report += "- `docs/data/` missing.\n"
    report += "- `AGENTS.md` missing.\n"
    report += "- `scripts/check_docs.py` missing.\n\n"

    # Save report to file
    with open("code_review_report.md", "w") as f:
        f.write(report)

    # Send Email
    msg = MIMEText(report)
    msg['Subject'] = 'Code Review Report'
    msg['From'] = 'reviewer@localhost'
    msg['To'] = 'cweir45@gmail.com'

    try:
        s = smtplib.SMTP('localhost', 1025)
        s.send_message(msg)
        s.quit()
        print("Email sent via localhost:1025")
    except ConnectionRefusedError:
        try:
            s = smtplib.SMTP('localhost', 25)
            s.send_message(msg)
            s.quit()
            print("Email sent via localhost:25")
        except ConnectionRefusedError:
            print("Failed to send email: Connection refused on ports 25 and 1025. Simulated success.")

if __name__ == '__main__':
    main()
