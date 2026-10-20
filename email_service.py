import os
import smtplib
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from pathlib import Path
from datetime import datetime
from config import Config

def generate_email_html(data: dict) -> str:
    """Generate a clean, modern HTML confirmation email."""
    job_id = data.get("job_id", "N/A")
    task_name = data.get("task_name", "General Processing")
    recipient_name = data.get("recipient_name", "Valued User")
    status = data.get("status", "SUCCESS").upper()
    duration = data.get("duration", "0.0s")
    timestamp = data.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    details = data.get("details", {})
    steps = data.get("steps", [])
    
    # Fully customizable dynamic fields
    headline = data.get("headline", "Processing Confirmation")
    subheadline = data.get("subheadline", "Your request has been successfully processed")
    custom_message = data.get(
        "message",
        f"This email confirms that your task <strong>\"{task_name}\"</strong> has finished processing. You can find the summary and job details below."
    )
    company_name = data.get("company_name", Config.SENDER_NAME)

    status_color = "#10B981" if status == "SUCCESS" else "#3B82F6" if status == "PROCESSING" else "#EF4444"

    # Generate steps list HTML
    steps_html = ""
    for step in steps:
        steps_html += f"""
        <li style="margin-bottom: 8px; color: #374151;">
            <span style="color: #10B981; font-weight: bold; margin-right: 6px;">✓</span>
            {step}
        </li>
        """

    # Generate key-value details HTML
    details_rows = ""
    for k, v in details.items():
        details_rows += f"""
        <tr>
            <td style="padding: 8px 12px; border-bottom: 1px solid #E5E7EB; color: #6B7280; font-size: 14px;">{k}</td>
            <td style="padding: 8px 12px; border-bottom: 1px solid #E5E7EB; color: #111827; font-size: 14px; font-weight: 500;">{v}</td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{headline}</title>
</head>
<body style="margin: 0; padding: 0; background-color: #F3F4F6; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #F3F4F6; padding: 30px 10px;">
        <tr>
            <td align="center">
                <table role="presentation" width="100%" style="max-width: 600px; background-color: #FFFFFF; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%); padding: 32px 24px; text-align: center;">
                            <h1 style="color: #FFFFFF; margin: 0; font-size: 24px; font-weight: 700; letter-spacing: -0.5px;">
                                {headline}
                            </h1>
                            <p style="color: #DBEAFE; margin: 8px 0 0 0; font-size: 14px;">
                                {subheadline}
                            </p>
                        </td>
                    </tr>

                    <!-- Body Content -->
                    <tr>
                        <td style="padding: 32px 24px;">
                            <p style="font-size: 16px; color: #1F2937; margin: 0 0 16px 0;">
                                Hello <strong>{recipient_name}</strong>,
                            </p>
                            <p style="font-size: 15px; color: #4B5563; line-height: 1.5; margin: 0 0 24px 0;">
                                {custom_message}
                            </p>

                            <!-- Status Box -->
                            <div style="background-color: #F9FAFB; border: 1px solid #E5E7EB; border-radius: 8px; padding: 16px; margin-bottom: 24px;">
                                <table width="100%" cellspacing="0" cellpadding="0">
                                    <tr>
                                        <td>
                                            <span style="font-size: 12px; color: #6B7280; text-transform: uppercase; font-weight: 600;">Reference ID</span>
                                            <div style="font-size: 15px; font-family: monospace; font-weight: bold; color: #1F2937; margin-top: 4px;">{job_id}</div>
                                        </td>
                                        <td align="right">
                                            <span style="display: inline-block; background-color: {status_color}; color: #FFFFFF; padding: 4px 12px; border-radius: 9999px; font-size: 12px; font-weight: 700; text-transform: uppercase;">
                                                {status}
                                            </span>
                                        </td>
                                    </tr>
                                </table>
                            </div>

                            <!-- Processing Details Table -->
                            <h3 style="font-size: 16px; color: #111827; margin: 0 0 12px 0;">Task Summary</h3>
                            <table width="100%" cellspacing="0" cellpadding="0" style="border-collapse: collapse; margin-bottom: 24px;">
                                <tr>
                                    <td style="padding: 8px 12px; border-bottom: 1px solid #E5E7EB; color: #6B7280; font-size: 14px;">Task Name</td>
                                    <td style="padding: 8px 12px; border-bottom: 1px solid #E5E7EB; color: #111827; font-size: 14px; font-weight: 500;">{task_name}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px 12px; border-bottom: 1px solid #E5E7EB; color: #6B7280; font-size: 14px;">Completion Time</td>
                                    <td style="padding: 8px 12px; border-bottom: 1px solid #E5E7EB; color: #111827; font-size: 14px; font-weight: 500;">{timestamp}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px 12px; border-bottom: 1px solid #E5E7EB; color: #6B7280; font-size: 14px;">Execution Duration</td>
                                    <td style="padding: 8px 12px; border-bottom: 1px solid #E5E7EB; color: #111827; font-size: 14px; font-weight: 500;">{duration}</td>
                                </tr>
                                {details_rows}
                            </table>

                            <!-- Execution Steps -->
                            {f'''<h3 style="font-size: 16px; color: #111827; margin: 0 0 12px 0;">Completed Milestones</h3>
                            <ul style="list-style-type: none; padding-left: 0; margin: 0 0 24px 0;">
                                {steps_html}
                            </ul>''' if steps else ''}

                            <p style="font-size: 14px; color: #6B7280; margin: 24px 0 0 0; line-height: 1.5;">
                                If you have questions or didn't request this operation, please contact our support team.
                            </p>
                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #F9FAFB; padding: 20px 24px; text-align: center; border-top: 1px solid #E5E7EB;">
                            <p style="margin: 0; font-size: 12px; color: #9CA3AF;">
                                © {datetime.now().year} {company_name}. All rights reserved.
                            </p>
                            <p style="margin: 4px 0 0 0; font-size: 11px; color: #9CA3AF;">
                                This is an automated notification. Replies to this address are not monitored.
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>"""


def generate_email_text(data: dict) -> str:
    """Generate plain-text fallback content."""
    job_id = data.get("job_id", "N/A")
    task_name = data.get("task_name", "General Processing")
    recipient_name = data.get("recipient_name", "Valued User")
    status = data.get("status", "SUCCESS")
    duration = data.get("duration", "0.0s")
    timestamp = data.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    company_name = data.get("company_name", Config.SENDER_NAME)
    headline = data.get("headline", "Processing Confirmation")

    lines = [
        f"{headline}",
        f"{'=' * len(headline)}",
        f"Hello {recipient_name},",
        f"",
        f"Your task '{task_name}' has finished processing.",
        f"",
        f"Reference ID: {job_id}",
        f"Status:       {status}",
        f"Completed At: {timestamp}",
        f"Duration:     {duration}",
        f"",
    ]
    
    details = data.get("details", {})
    if details:
        lines.append("Details:")
        for k, v in details.items():
            lines.append(f"  * {k}: {v}")
        lines.append("")

    steps = data.get("steps", [])
    if steps:
        lines.append("Completed Milestones:")
        for step in steps:
            lines.append(f"  [✓] {step}")
        lines.append("")

    lines.append(f"Best regards,\n{company_name}")
    return "\n".join(lines)


def send_via_resend(recipient_email: str, subject: str, html_body: str, text_body: str) -> dict:
    """Send via Resend HTTP API over Port 443 (HTTPS) - Works on Render Free Tier."""
    from_addr = os.getenv("RESEND_FROM") or f"{Config.SENDER_NAME} <onboarding@resend.dev>"
    headers = {
        "Authorization": f"Bearer {Config.RESEND_API_KEY.strip()}",
        "Content-Type": "application/json"
    }
    payload = {
        "from": from_addr,
        "to": [recipient_email],
        "subject": subject,
        "html": html_body,
        "text": text_body
    }
    try:
        resp = requests.post("https://api.resend.com/emails", headers=headers, json=payload, timeout=12)
        if resp.status_code in (200, 201):
            print(f"[HTTP API] Successfully delivered via Resend to {recipient_email}")
            return {
                "success": True,
                "message": f"Confirmation email successfully sent via Resend API to {recipient_email}."
            }
        else:
            print(f"[ERROR] Resend API error: {resp.status_code} - {resp.text}")
            return {
                "success": False,
                "error": resp.text,
                "message": f"Resend API error ({resp.status_code}): {resp.text}"
            }
    except Exception as e:
        print(f"[ERROR] HTTP request to Resend failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"HTTP request failed: {e}"
        }


def send_via_brevo(recipient_email: str, subject: str, html_body: str, text_body: str, data: dict) -> dict:
    """Send via Brevo HTTP API over Port 443 (HTTPS) - Works on Render Free Tier."""
    headers = {
        "api-key": Config.BREVO_API_KEY.strip(),
        "Content-Type": "application/json"
    }
    payload = {
        "sender": {"name": Config.SENDER_NAME, "email": Config.SENDER_EMAIL},
        "to": [{"email": recipient_email, "name": data.get("recipient_name", "Valued User")}],
        "subject": subject,
        "htmlContent": html_body,
        "textContent": text_body
    }
    try:
        resp = requests.post("https://api.brevo.com/v3/smtp/email", headers=headers, json=payload, timeout=12)
        if resp.status_code in (200, 201):
            print(f"[HTTP API] Successfully delivered via Brevo to {recipient_email}")
            return {
                "success": True,
                "message": f"Confirmation email successfully sent via Brevo API to {recipient_email}."
            }
        else:
            print(f"[ERROR] Brevo API error: {resp.status_code} - {resp.text}")
            return {
                "success": False,
                "error": resp.text,
                "message": f"Brevo API error ({resp.status_code}): {resp.text}"
            }
    except Exception as e:
        print(f"[ERROR] HTTP request to Brevo failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"HTTP request failed: {e}"
        }


def send_via_smtp(recipient_email: str, subject: str, html_body: str, text_body: str) -> dict:
    """Send via traditional SMTP (port 587 / 465)."""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = formataddr((Config.SENDER_NAME, Config.SENDER_EMAIL))
        msg["To"] = recipient_email

        # Attach text and html versions
        msg.attach(MIMEText(text_body, "plain", "utf-8"))
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        # Connect and send via SMTP
        if Config.SMTP_PORT == 465 or (not Config.SMTP_USE_TLS and Config.SMTP_PORT != 587):
            with smtplib.SMTP_SSL(Config.SMTP_SERVER, Config.SMTP_PORT, timeout=15) as server:
                if Config.SMTP_USERNAME and Config.SMTP_PASSWORD:
                    server.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
                server.sendmail(Config.SENDER_EMAIL, [recipient_email], msg.as_string())
        else:
            with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT, timeout=15) as server:
                server.ehlo()
                if Config.SMTP_USE_TLS:
                    server.starttls()
                    server.ehlo()
                if Config.SMTP_USERNAME and Config.SMTP_PASSWORD:
                    server.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
                server.sendmail(Config.SENDER_EMAIL, [recipient_email], msg.as_string())

        print(f"[LIVE EMAIL SENT] Successfully delivered to {recipient_email}")
        return {
            "success": True,
            "message": f"Confirmation email successfully sent to {recipient_email}."
        }
    except Exception as exc:
        print(f"[ERROR] Failed to send email via SMTP: {exc}")
        return {
            "success": False,
            "error": str(exc),
            "message": f"SMTP delivery failed: {exc}"
        }


def send_confirmation_email(recipient_email: str, data: dict) -> dict:
    """
    Send the confirmation email using HTTP REST API (port 443) or SMTP.
    If RESEND_API_KEY or BREVO_API_KEY is configured, it sends via HTTPS (bypassing Render's SMTP block).
    Otherwise, it sends via SMTP.
    """
    subject = f"Confirmation: {data.get('task_name', 'Process')} Completed [{data.get('job_id', '')}]"
    html_body = generate_email_html(data)
    text_body = generate_email_text(data)

    # 1. Use Resend HTTP REST API if RESEND_API_KEY is present
    if Config.RESEND_API_KEY:
        return send_via_resend(recipient_email, subject, html_body, text_body)

    # 2. Use Brevo HTTP REST API if BREVO_API_KEY is present
    if Config.BREVO_API_KEY:
        return send_via_brevo(recipient_email, subject, html_body, text_body, data)

    # 3. Fallback to direct SMTP
    return send_via_smtp(recipient_email, subject, html_body, text_body)
