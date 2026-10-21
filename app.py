import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, Dict
import uvicorn

from config import Config, BASE_DIR
from processor import process_task
from email_service import generate_email_html

app = FastAPI(title="Task Processor & Live Email Confirmation Service")

# Template directory
TEMPLATES_DIR = BASE_DIR / "templates"

# In-memory store for recent sent emails (for live web UI inspection)
RECENT_EMAILS: Dict[str, str] = {}

class ProcessRequest(BaseModel):
    recipient_email: str
    recipient_name: Optional[str] = "Valued User"
    task_name: Optional[str] = "Data Processing Pipeline"
    details: Optional[Dict[str, str]] = None

@app.get("/", response_class=HTMLResponse)
def index():
    index_file = TEMPLATES_DIR / "index.html"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="Index template not found")
    return index_file.read_text(encoding="utf-8")

@app.get("/api/config")
def get_config_status():
    mode = "HTTP API (Resend - Port 443)" if Config.RESEND_API_KEY else ("HTTP API (Brevo - Port 443)" if Config.BREVO_API_KEY else "SMTP Direct")
    return {
        "status": mode,
        "is_http_api": bool(Config.RESEND_API_KEY or Config.BREVO_API_KEY),
        "smtp_server": Config.SMTP_SERVER,
        "smtp_port": Config.SMTP_PORT,
        "sender_email": Config.SENDER_EMAIL,
        "sender_name": Config.SENDER_NAME
    }

@app.post("/api/process")
def trigger_process(req: ProcessRequest):
    result = process_task(
        recipient_email=req.recipient_email,
        recipient_name=req.recipient_name,
        task_name=req.task_name,
        custom_details=req.details
    )
    email_html = generate_email_html(result)
    RECENT_EMAILS[result["job_id"]] = email_html
    result["html_preview"] = email_html
    return result

@app.get("/api/preview/{job_id}", response_class=HTMLResponse)
def view_preview(job_id: str):
    if job_id in RECENT_EMAILS:
        return RECENT_EMAILS[job_id]
    
    return f"""
    <html>
        <body style="font-family:sans-serif;padding:30px;color:#666;text-align:center;">
            <h3>Email for {job_id} was dispatched live via SMTP.</h3>
            <p>Check the recipient inbox for the delivered email.</p>
        </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    print(f"Starting server on http://{host}:{port} ...")
    uvicorn.run("app:app", host=host, port=port)
