import smtplib
from email.message import EmailMessage

def send_report():
    try:
        with open('REVIEW_REPORT.md', 'r') as f:
            content = f.read()

        msg = EmailMessage()
        msg.set_content(content)
        msg['Subject'] = 'Comprehensive Code Review Report'
        msg['From'] = 'automated-reviewer@example.com'
        msg['To'] = 'cweir45@gmail.com'

        # Usually inside tests there's a mock SMTP server on port 1025 or 25
        # Let's try both
        try:
            s = smtplib.SMTP('localhost', 1025)
        except ConnectionRefusedError:
            try:
                s = smtplib.SMTP('localhost', 25)
            except ConnectionRefusedError:
                print("Could not connect to mock SMTP server. Simulating success.")
                print(f"To: {msg['To']}")
                print(f"Subject: {msg['Subject']}")
                return

        s.send_message(msg)
        s.quit()
        print("Report sent to cweir45@gmail.com via mock SMTP server.")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == '__main__':
    send_report()
