# Task Processing & Live Email Confirmation System

A lightweight, production-ready Python project that executes processing tasks and automatically dispatches live HTML and plain-text confirmation emails via SMTP.

---

## 🌟 Key Features

- **Automated Workflow**: Triggers confirmation emails immediately upon completion of any data/job processing task.
- **Dedicated Live SMTP**: Connected directly to `smtp19.mycloudmailbox.com` (B3 Communications).
- **Dual Interface**:
  - **CLI Runner (`main.py`)**: Quick command-line execution with custom flags.
  - **Web Dashboard & REST API (`app.py`)**: Modern, interactive FastAPI interface with real-time job execution and delivered email viewer.
- **Responsive Email Design**: Modern HTML email with reference IDs, status badges, execution duration, milestone logs, and plain-text fallback.

---

## 📁 Project Structure

```text
email_setup/
├── config.py           # Configuration loader (.env parser)
├── email_service.py    # HTML email generator & Live SMTP delivery engine
├── processor.py        # Core processing logic / task runner
├── main.py             # Interactive CLI execution tool
├── app.py              # FastAPI web server and REST API
├── requirements.txt    # Python dependencies
├── .env                # Active live SMTP credentials
├── .env.example        # Configuration template
├── templates/
│   └── index.html      # Modern TailwindCSS web dashboard
└── README.md           # Documentation
```

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run via Command Line (CLI)
```bash
python main.py --email recipient@example.com --name "Recipient Name" --task "Data Processing Run"
```

### 3. Run via Web Dashboard
```bash
python app.py
```
Open your browser to:
[http://localhost:8000](http://localhost:8000)

Fill in the recipient email and click **Execute Task & Send Live Email**.

---

## ✉️ Active SMTP Configuration

The project is configured for **B3 Communications** in [`.env`](.env):

```ini
SMTP_SERVER=smtp19.mycloudmailbox.com
SMTP_PORT=587
SMTP_USE_TLS=True
SMTP_USERNAME=B3Communications@b3intelligence.com
SMTP_PASSWORD=Password123!
SENDER_NAME="B3 Communications"
SENDER_EMAIL=B3Communications@b3intelligence.com
```

---

## 💻 How to Use in Your Own Project

Import `send_confirmation_email` into any script or backend:

```python
from email_service import send_confirmation_email

data = {
    "job_id": "JOB-90210",
    "headline": "Processing Completed",
    "task_name": "Monthly Billing Batch",
    "recipient_name": "Vipin",
    "status": "SUCCESS",
    "duration": "1.2s",
    "steps": [
        "Invoices generated",
        "Payment gateways verified",
        "Dispatched successfully"
    ],
    "details": {
        "Total Invoices": "1,200",
        "Status": "Completed"
    }
}

send_confirmation_email("recipient@example.com", data)
```
