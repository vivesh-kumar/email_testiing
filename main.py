import argparse
import sys
from processor import process_task
from config import Config

# Ensure Windows terminal can print unicode without crashing
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def main():
    parser = argparse.ArgumentParser(description="Run a processing job and dispatch a confirmation email.")
    parser.add_argument(
        "--email",
        type=str,
        default="user@example.com",
        help="Recipient email address to receive confirmation (default: user@example.com)"
    )
    parser.add_argument(
        "--name",
        type=str,
        default="Alex Developer",
        help="Recipient's name (default: Alex Developer)"
    )
    parser.add_argument(
        "--task",
        type=str,
        default="Financial Batch Settlement & Reconciliation",
        help="Name of the processing task"
    )

    args = parser.parse_args()

    print("=" * 65)
    print("      [*] AUTOMATED TASK PROCESSOR & EMAIL CONFIRMATION       ")
    print("=" * 65)
    print(f"SMTP Server: {Config.SMTP_SERVER}:{Config.SMTP_PORT}")
    print(f"Sender:      {Config.SENDER_NAME} <{Config.SENDER_EMAIL}>")
    print(f"Recipient:   {args.name} <{args.email}>")
    print(f"Task:        {args.task}")
    print("-" * 65)

    result = process_task(
        recipient_email=args.email,
        recipient_name=args.name,
        task_name=args.task
    )

    print("\n" + "=" * 65)
    print("                     EXECUTION SUMMARY                       ")
    print("=" * 65)
    print(f"Job ID:      {result['job_id']}")
    print(f"Status:      {result['status']}")
    print(f"Duration:    {result['duration']}")
    print(f"Email Sent:  {result['email_result']['message']}")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    main()
