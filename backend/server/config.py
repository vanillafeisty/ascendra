"""Ascendra Backend — Configuration (Groq Edition)"""
import os, json
from pathlib import Path
from dotenv import load_dotenv

# Walk up from server/ → backend/ → project root looking for .env
for candidate in [
    Path(__file__).parent.parent / ".env",
    Path(__file__).parent.parent.parent / ".env",
]:
    if candidate.exists():
        load_dotenv(candidate)
        break
else:
    load_dotenv()  # fallback: system env

BASE_DIR = Path(__file__).parent
DATA_DIR  = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

USER_PROFILE_PATH     = DATA_DIR / "user_profile.json"
CONNECTION_LOG_PATH   = DATA_DIR / "connection_log.json"
EMAIL_LOG_PATH        = DATA_DIR / "email_log.json"
CONTENT_CALENDAR_PATH = DATA_DIR / "content_calendar.json"
RESUMES_DIR           = DATA_DIR / "resumes"
RESUMES_DIR.mkdir(exist_ok=True)
(DATA_DIR / "uploads").mkdir(exist_ok=True)

# ── AI — Groq (free, no billing) ──────────────────────────────────────────────
GROQ_API_KEY   = os.getenv("GROQ_API_KEY", "")

# ── LinkedIn ───────────────────────────────────────────────────────────────────
LINKEDIN_EMAIL    = os.getenv("LINKEDIN_EMAIL", "")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD", "")

# ── Email ──────────────────────────────────────────────────────────────────────
GMAIL_CREDENTIALS = os.getenv("GMAIL_CREDENTIALS_PATH",
                               str(Path(__file__).parent.parent / "gmail_credentials.json"))
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")

# ── Optional integrations ──────────────────────────────────────────────────────
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
HUNTER_API_KEY  = os.getenv("HUNTER_API_KEY", "")

# ── Rate limits ────────────────────────────────────────────────────────────────
LINKEDIN_MAX_CONNECTIONS_PER_DAY = int(os.getenv("LINKEDIN_MAX_CONNECTIONS_PER_DAY", "20"))
LINKEDIN_MAX_MESSAGES_PER_DAY    = int(os.getenv("LINKEDIN_MAX_MESSAGES_PER_DAY", "20"))
LINKEDIN_DELAY_BETWEEN_ACTIONS   = float(os.getenv("LINKEDIN_DELAY_SECONDS", "4.0"))

# ── Default user profile ───────────────────────────────────────────────────────
DEFAULT_PROFILE = {
    "name": "", "email": "", "phone": "", "location": "", "target_role": "",
    "target_companies": [], "skills": [], "experience": [], "education": [],
    "certifications": [], "projects": [], "linkedin_url": "", "github_url": "",
    "portfolio_url": "", "summary": "", "hitl_enabled": True,
    "daily_connection_count": 0, "daily_connection_date": ""
}

def load_user_profile():
    if USER_PROFILE_PATH.exists():
        with open(USER_PROFILE_PATH) as f:
            return json.load(f)
    save_user_profile(DEFAULT_PROFILE)
    return DEFAULT_PROFILE.copy()

def save_user_profile(p):
    with open(USER_PROFILE_PATH, "w") as f:
        json.dump(p, f, indent=2)

def load_connection_log():
    if CONNECTION_LOG_PATH.exists():
        with open(CONNECTION_LOG_PATH) as f:
            return json.load(f)
    d = {"connections": []}
    with open(CONNECTION_LOG_PATH, "w") as f:
        json.dump(d, f)
    return d

def save_connection_log(l):
    with open(CONNECTION_LOG_PATH, "w") as f:
        json.dump(l, f, indent=2)

def load_email_log():
    if EMAIL_LOG_PATH.exists():
        with open(EMAIL_LOG_PATH) as f:
            return json.load(f)
    d = {"emails": []}
    with open(EMAIL_LOG_PATH, "w") as f:
        json.dump(d, f)
    return d

def save_email_log(l):
    with open(EMAIL_LOG_PATH, "w") as f:
        json.dump(l, f, indent=2)

def load_content_calendar():
    if CONTENT_CALENDAR_PATH.exists():
        with open(CONTENT_CALENDAR_PATH) as f:
            return json.load(f)
    d = {"posts": []}
    with open(CONTENT_CALENDAR_PATH, "w") as f:
        json.dump(d, f)
    return d

def save_content_calendar(c):
    with open(CONTENT_CALENDAR_PATH, "w") as f:
        json.dump(c, f, indent=2)

def validate_config():
    return {
        "groq":              bool(GROQ_API_KEY),
        "linkedin":          bool(LINKEDIN_EMAIL and LINKEDIN_PASSWORD),
        "gmail_oauth":       Path(GMAIL_CREDENTIALS).exists() if GMAIL_CREDENTIALS else False,
        "smtp":              bool(SMTP_USER and SMTP_PASS),
        "youtube":           bool(YOUTUBE_API_KEY),
        "hunter":            bool(HUNTER_API_KEY),
        "user_profile_set":  bool(load_user_profile().get("name")),
    }
