"""
CareerPilot AI - Email Tools
Sends cold emails, follow-ups, and targeted HR mails directly.

Supports:
  - Gmail via OAuth2 (preferred)
  - Any SMTP provider as fallback
"""

import smtplib
import json
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime
from pathlib import Path
from typing import Optional

from config import (
    GMAIL_CREDENTIALS, SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS,
    load_email_log, save_email_log
)


# ─────────────────────────────────────────────────────────────────────────────
# GMAIL OAUTH2 HELPER
# ─────────────────────────────────────────────────────────────────────────────

def _get_gmail_service():
    """Return authenticated Gmail API service using OAuth2."""
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build

        SCOPES = ["https://www.googleapis.com/auth/gmail.send",
                  "https://www.googleapis.com/auth/gmail.readonly"]

        token_path = Path(GMAIL_CREDENTIALS).parent / "gmail_token.json"
        creds = None

        if token_path.exists():
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not Path(GMAIL_CREDENTIALS).exists():
                    raise FileNotFoundError(
                        f"Gmail credentials not found at {GMAIL_CREDENTIALS}. "
                        "Download from Google Cloud Console and place at this path."
                    )
                flow = InstalledAppFlow.from_client_secrets_file(GMAIL_CREDENTIALS, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(token_path, "w") as f:
                f.write(creds.to_json())

        return build("gmail", "v1", credentials=creds)
    except ImportError:
        raise RuntimeError("Google API libraries not installed. Run: pip install google-api-python-client google-auth-oauthlib")


def _send_via_smtp(
    to: str, subject: str, body: str,
    attachment_path: Optional[str] = None,
    html_body: Optional[str] = None
) -> dict:
    """Send email via SMTP (fallback method)."""
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = SMTP_USER
        msg["To"] = to
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))
        if html_body:
            msg.attach(MIMEText(html_body, "html"))

        if attachment_path:
            att_path = Path(attachment_path)
            if att_path.exists():
                with open(att_path, "rb") as f:
                    part = MIMEApplication(f.read(), Name=att_path.name)
                part["Content-Disposition"] = f'attachment; filename="{att_path.name}"'
                msg.attach(part)

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)

        return {"success": True, "method": "smtp"}
    except Exception as e:
        return {"success": False, "reason": str(e)}


def _send_via_gmail(
    to: str, subject: str, body: str,
    attachment_path: Optional[str] = None
) -> dict:
    """Send email via Gmail API."""
    try:
        service = _get_gmail_service()

        msg = MIMEMultipart()
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        if attachment_path:
            att_path = Path(attachment_path)
            if att_path.exists():
                with open(att_path, "rb") as f:
                    part = MIMEApplication(f.read(), Name=att_path.name)
                part["Content-Disposition"] = f'attachment; filename="{att_path.name}"'
                msg.attach(part)

        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        service.users().messages().send(userId="me", body={"raw": raw}).execute()

        return {"success": True, "method": "gmail"}
    except Exception as e:
        return {"success": False, "reason": str(e)}


# ─────────────────────────────────────────────────────────────────────────────
# PUBLIC EMAIL TOOLS
# ─────────────────────────────────────────────────────────────────────────────

def send_email(
    to: str,
    subject: str,
    body: str,
    attachment_path: Optional[str] = None
) -> dict:
    """
    Send an email directly. Tries Gmail API first, falls back to SMTP.
    Logs the email to email_log.json.
    """
    # Try Gmail first, then SMTP
    result = None
    if Path(GMAIL_CREDENTIALS).exists():
        try:
            result = _send_via_gmail(to, subject, body, attachment_path)
        except Exception:
            pass

    if not result or not result.get("success"):
        if SMTP_USER and SMTP_PASS:
            result = _send_via_smtp(to, subject, body, attachment_path)
        else:
            return {
                "success": False,
                "reason": "No email method configured. Set up Gmail OAuth or SMTP credentials in .env"
            }

    # Log it
    if result.get("success"):
        log = load_email_log()
        log["emails"].append({
            "to": to,
            "subject": subject,
            "body_preview": body[:200],
            "sent_at": datetime.utcnow().isoformat(),
            "status": "sent",
            "method": result.get("method", "unknown"),
            "has_attachment": bool(attachment_path)
        })
        save_email_log(log)

    return result


def send_cold_email_to_hr(
    hr_name: str,
    hr_email: str,
    company: str,
    role: str,
    user_name: str,
    user_summary: str,
    resume_path: Optional[str] = None
) -> dict:
    """
    Draft and send a cold email to an HR/recruiter.
    AI-crafted subject + body, personalized to the person and role.
    """
    subject = f"Application – {role} | {user_name} | Excited to Contribute at {company}"

    body = f"""Hi {hr_name.split()[0]},

I hope this message finds you well. My name is {user_name}, and I came across the {role} opportunity at {company} and felt compelled to reach out directly.

{user_summary}

I'm particularly drawn to {company} because of its reputation for innovation and growth. I believe my background aligns well with what your team is looking for, and I'd love the chance to discuss how I can contribute.

I've attached my resume for your consideration. I'd be grateful for even 15 minutes of your time — feel free to reply to this email or suggest a time that works for you.

Thank you for taking the time to read this. I look forward to connecting!

Warm regards,
{user_name}
"""

    return send_email(
        to=hr_email,
        subject=subject,
        body=body,
        attachment_path=resume_path
    )


def send_bulk_cold_emails(
    recipients: list[dict],
    role: str,
    user_name: str,
    user_summary: str,
    resume_path: Optional[str] = None
) -> dict:
    """
    Send personalized cold emails to multiple HRs.
    Each recipient: {"name": "...", "email": "...", "company": "..."}
    """
    sent, failed = 0, 0
    details = []

    for r in recipients:
        result = send_cold_email_to_hr(
            hr_name=r.get("name", "Hiring Manager"),
            hr_email=r["email"],
            company=r.get("company", "your company"),
            role=role,
            user_name=user_name,
            user_summary=user_summary,
            resume_path=resume_path
        )
        if result.get("success"):
            sent += 1
            details.append(f"✅ {r.get('name', r['email'])} at {r.get('company', '')}")
        else:
            failed += 1
            details.append(f"❌ {r.get('name', r['email'])}: {result.get('reason', 'error')}")

    return {
        "sent": sent,
        "failed": failed,
        "details": details,
        "summary": f"Emails sent: {sent}/{len(recipients)} successful."
    }


def send_follow_up_email(original_thread_to: str, original_subject: str, user_name: str, days_since: int = 5) -> dict:
    """
    Send a follow-up email for a non-responded cold email.
    """
    subject = f"Re: {original_subject}"
    body = f"""Hi,

I just wanted to follow up on my previous email regarding the opportunity I mentioned.

I remain very interested and would love to hear back from you. I understand you're busy — even a brief response would mean a lot.

Thanks again for your time, and I hope to connect soon!

Best,
{user_name}
"""
    return send_email(to=original_thread_to, subject=subject, body=body)


def get_email_log() -> dict:
    """Return the full email activity log."""
    return load_email_log()
