"""
Ascendra — FastAPI Backend (Groq Edition, Personal Testing Mode)
LLM: Groq llama-3.3-70b-versatile — 100% FREE, no billing needed.
"""
import sys, re, os, time
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "server"))

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
from dotenv import load_dotenv

load_dotenv(ROOT / ".env")

from server.config import (
    GROQ_API_KEY, validate_config,
    load_user_profile, save_user_profile,
    load_email_log
)

# ── Tool imports ───────────────────────────────────────────────────────────────
try:
    from server.tools.linkedin_tools import (
        get_my_profile, score_linkedin_profile, suggest_profile_photo_guidelines,
        search_people, bulk_connect, send_message, bulk_message,
        create_text_post, update_headline)
    LI_OK = True
except Exception as e:
    LI_OK = False
    print(f"⚠  LinkedIn not loaded: {e}")

try:
    from server.tools.email_tools import (
        send_email, send_cold_email_to_hr, send_follow_up_email)
    EMAIL_OK = True
except Exception as e:
    EMAIL_OK = False
    print(f"⚠  Email not loaded: {e}")

from server.tools.resume_tools import (
    build_resume, tailor_resume_to_jd, score_resume_against_jd, analyze_resume)
from server.tools.career_tools import (
    what_to_do_next, career_roadmap, find_target_companies,
    find_free_courses, get_must_do_certs)
from server.tools.content_tools import (
    generate_post, generate_weekly_content_calendar,
    get_trending_topics, generate_image_post_caption)

# ── App ────────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Ascendra API — Groq Edition",
    version="2.0.0-groq",
    description="Personal testing mode. LLM: Groq (free).",
)
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# ── Groq client ────────────────────────────────────────────────────────────────
_groq_client = None
def get_groq():
    global _groq_client
    if _groq_client is None:
        from groq import Groq
        _groq_client = Groq(api_key=GROQ_API_KEY)
    return _groq_client

# ── System prompt ──────────────────────────────────────────────────────────────
SYSTEM = """You are Ascendra — an autonomous AI career intelligence assistant.
You help users land their dream jobs through LinkedIn automation, email outreach,
ATS-semantic resume optimization, and career roadmapping — all through conversation.

Personality: Confident, warm, action-oriented. Always offer to DO things immediately.
Refer to yourself only as "Ascendra". Format responses with markdown.

Capabilities:
- LinkedIn: Connect HRs, send messages, post content, update profile (all HITL-gated)
- Email: Find HR emails, send cold emails and follow-ups via Gmail/SMTP
- Resume: ATS-Semantic Engine — NLP keyword alignment, 0-100 scoring, DOCX/PDF output
- Career: Skill gap analysis, roadmaps, "what to do next", target companies
- Courses: Free courses with YouTube-validated links, must-do certifications
- Content: LinkedIn posts, 4-week content calendars, image captions

Safety (absolute, non-negotiable):
- Never generate sexual, obscene, harassing, threatening, or discriminatory content
- Never help with fake credentials, phishing, or deceptive content
- When declining: be warm, explain briefly, immediately redirect to career help"""

# ── Moderation ─────────────────────────────────────────────────────────────────
_PATTERNS = [
    re.compile(r'\b(porn|nsfw|nude|naked|xxx|sexual|onlyfans|erotic|lewd|horny)\b', re.I),
    re.compile(r'\b(nigger|faggot|chink|spic|kike|cunt|slut|whore)\b', re.I),
    re.compile(r'\b(i will (?:kill|hurt|destroy) you|stalking|doxxing|blackmail)\b', re.I),
    re.compile(r'\b(how to (?:kill|murder)|bomb(?:ing|make)|assassinat)\b', re.I),
    re.compile(r'\b(fake (?:job|degree|certificate)|scam hr|phishing|impersonat)\b', re.I),
    re.compile(r'\b(post (?:bad|nasty|mean) about|trashtalking|publicly shame)\b', re.I),
]
_REFUSAL = ("I'm not able to help with that. Ascendra is here for your career growth 💛\n\n"
            "What career goal can I help you with?")

def blocked(text: str) -> bool:
    t = text.lower()
    return any(p.search(t) for p in _PATTERNS)

# ── HITL queue ──────────────────────────────────────────────────────────────────
_hitl: dict = {}

# ── Models ──────────────────────────────────────────────────────────────────────
class ChatReq(BaseModel):
    messages: List[dict]

class ProfileUpdate(BaseModel):
    name: Optional[str]=None; email: Optional[str]=None; phone: Optional[str]=None
    location: Optional[str]=None; target_role: Optional[str]=None
    skills: Optional[List[str]]=None; summary: Optional[str]=None
    linkedin_url: Optional[str]=None; github_url: Optional[str]=None
    portfolio_url: Optional[str]=None; experience: Optional[List[dict]]=None
    education: Optional[List[dict]]=None; certifications: Optional[List[str]]=None
    projects: Optional[List[dict]]=None

class BulkConnectReq(BaseModel):
    role: str; company: Optional[str]=None; location: Optional[str]=None
    count: int=10; note_template: str="Hi {name}, I'd love to connect!"; hitl_approved: bool=False

class BulkMsgReq(BaseModel):
    profile_ids: List[str]; message_template: str
    names: Optional[List[str]]=None; hitl_approved: bool=False

class PostReq(BaseModel):
    content: str; hashtags: Optional[List[str]]=[]; hitl_approved: bool=False

class EmailReq(BaseModel):
    to: str; subject: str; body: str
    attachment_path: Optional[str]=None; hitl_approved: bool=False

class ColdEmailReq(BaseModel):
    hr_name: str; hr_email: str; company: str; role: str
    resume_path: Optional[str]=None; hitl_approved: bool=False

class HeadlineReq(BaseModel):
    headline: str; hitl_approved: bool=False

class GenPostReq(BaseModel):
    topic: str; domain: Optional[str]="general"

class CalReq(BaseModel):
    domain: str="general"; weeks: int=4

class ImgCapReq(BaseModel):
    image_context: str; domain: str="general"

class TailorReq(BaseModel):
    resume_path: str; job_description: str

class ScoreReq(BaseModel):
    resume_text: str; job_description: str

class NextReq(BaseModel):
    current_skills: List[str]; target_role: str; experience_years: int=0

class FollowUpReq(BaseModel):
    to: str; original_subject: str; days_since: int=5

# ── Routes ─────────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"name":"Ascendra","version":"2.0.0-groq","llm":"Groq (free)","status":"running","docs":"/docs"}

@app.get("/api/health")
def health():
    cfg = validate_config()
    return {"status":"running","llm":"groq","integrations":cfg,"modules":{"linkedin":LI_OK,"email":EMAIL_OK}}

# ── Chat (Groq) ────────────────────────────────────────────────────────────────
@app.post("/api/chat")
async def chat(req: ChatReq):
    last = next((m for m in reversed(req.messages) if m.get("role")=="user"), None)
    if last and blocked(last.get("content","")):
        return {"message": _REFUSAL, "moderated": True}

    if not GROQ_API_KEY:
        return {"message": (
            "⚠️ **GROQ_API_KEY not set.**\n\n"
            "1. Go to **console.groq.com/keys** → create a free key (no card needed)\n"
            "2. Open `backend/.env`\n"
            "3. Add: `GROQ_API_KEY=gsk_...`\n"
            "4. Restart with `python api.py`"
        ), "error": True}

    try:
        client = get_groq()
        msgs = [{"role":"system","content":SYSTEM}]
        for m in req.messages:
            if m.get("role") in ("user","assistant") and m.get("content","").strip():
                msgs.append({"role": m["role"], "content": m["content"]})

        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=msgs,
            max_tokens=2048,
            temperature=0.7,
        )
        reply = resp.choices[0].message.content
        if blocked(reply):
            reply = _REFUSAL
        return {
            "message": reply,
            "moderated": False,
            "model": "llama-3.3-70b-versatile",
            "usage": {"prompt": resp.usage.prompt_tokens, "completion": resp.usage.completion_tokens}
        }
    except Exception as e:
        err = str(e)
        if "401" in err or "invalid_api_key" in err.lower():
            return {"message":"❌ Invalid Groq key. Get a new one at console.groq.com/keys and paste into backend/.env","error":True}
        if "429" in err or "rate_limit" in err.lower():
            return {"message":"⏳ Rate limit hit. Groq free tier: 30 req/min. Wait a moment and retry.","error":True}
        return {"message":f"Error: {err}","error":True}

# ── Profile ────────────────────────────────────────────────────────────────────
@app.get("/api/profile")
def get_profile(): return load_user_profile()

@app.post("/api/profile")
def set_profile(d: ProfileUpdate):
    p = load_user_profile()
    p.update({k:v for k,v in d.dict().items() if v is not None})
    save_user_profile(p)
    return {"success":True,"profile":p}

# ── LinkedIn ───────────────────────────────────────────────────────────────────
def _li_check():
    if not LI_OK:
        return {"error":"LinkedIn not configured","hint":"Add LINKEDIN_EMAIL + LINKEDIN_PASSWORD to backend/.env"}
    return None

@app.get("/api/linkedin/profile")
def li_profile():
    e=_li_check()
    if e: return e
    try: return get_my_profile()
    except Exception as ex: return {"error":str(ex),"hint":"Check your LinkedIn credentials in backend/.env"}

@app.get("/api/linkedin/score")
def li_score():
    e=_li_check()
    if e: return e
    try: return score_linkedin_profile()
    except Exception as ex: return {"error":str(ex)}

@app.get("/api/linkedin/photo-guidelines")
def li_photo(): return suggest_profile_photo_guidelines()

@app.post("/api/linkedin/headline")
def li_headline(req: HeadlineReq):
    if not req.hitl_approved:
        return {"hitl_required":True,"preview":req.headline,
                "message":f"Ready to set your LinkedIn headline to:\n\n**\"{req.headline}\"**\n\nSend again with `hitl_approved: true` to apply."}
    e=_li_check()
    if e: return e
    try: return update_headline(req.headline)
    except Exception as ex: return {"error":str(ex)}

@app.get("/api/linkedin/search")
def li_search(role:str, company:Optional[str]=None, location:Optional[str]=None, limit:int=15):
    e=_li_check()
    if e: return e
    try: return {"results":search_people(role=role,company=company,location=location,limit=limit)}
    except Exception as ex: return {"error":str(ex)}

@app.post("/api/linkedin/bulk-connect")
def li_bulk_connect(req: BulkConnectReq):
    e=_li_check()
    if e: return e
    if not req.hitl_approved:
        try:
            preview = search_people(role=req.role,company=req.company,location=req.location,limit=req.count)
            qid = f"connect_{int(time.time())}"
            _hitl[qid] = {"type":"bulk_connect","req":req.dict(),"preview":preview}
            return {"hitl_required":True,"queue_id":qid,"preview":preview,"count":len(preview),
                    "message":f"Found **{len(preview)} people**. Review above.\nSend again with `hitl_approved: true` to connect."}
        except Exception as ex: return {"error":str(ex)}
    try: return bulk_connect(role=req.role,company=req.company,location=req.location,
                              count=req.count,note_template=req.note_template)
    except Exception as ex: return {"error":str(ex)}

@app.post("/api/linkedin/bulk-message")
def li_bulk_msg(req: BulkMsgReq):
    if not req.hitl_approved:
        previews=[{"profile_id":pid,"name":(req.names[i] if req.names and i<len(req.names) else ""),
                   "preview":req.message_template.replace("{name}",(req.names[i].split()[0] if req.names and i<len(req.names) else "there"))[:120]}
                  for i,pid in enumerate(req.profile_ids)]
        return {"hitl_required":True,"previews":previews,
                "message":f"Ready to send to **{len(previews)} connections**. Review above.\nSend with `hitl_approved: true` to dispatch."}
    e=_li_check()
    if e: return e
    try: return bulk_message(req.profile_ids,req.message_template,req.names)
    except Exception as ex: return {"error":str(ex)}

@app.post("/api/linkedin/post")
def li_post(req: PostReq):
    if blocked(req.content): return {"blocked":True,"message":_REFUSAL}
    if not req.hitl_approved:
        return {"hitl_required":True,"preview":req.content,
                "message":f"Post preview:\n\n{req.content[:400]}\n\nSend with `hitl_approved: true` to publish."}
    e=_li_check()
    if e: return e
    try: return create_text_post(req.content,req.hashtags)
    except Exception as ex: return {"error":str(ex)}

@app.post("/api/linkedin/generate-post")
def li_gen_post(req: GenPostReq):
    result = generate_post(topic=req.topic,domain=req.domain)
    if blocked(result.get("content","")): return {"blocked":True,"message":_REFUSAL}
    return result

# ── Email ──────────────────────────────────────────────────────────────────────
def _email_check():
    if not EMAIL_OK:
        return {"error":"Email not configured","hint":"Add SMTP_USER + SMTP_PASS (or GMAIL_CREDENTIALS_PATH) to backend/.env"}
    return None

@app.post("/api/email/send")
def email_send(req: EmailReq):
    if blocked(req.body) or blocked(req.subject): return {"blocked":True,"message":_REFUSAL}
    if not req.hitl_approved:
        return {"hitl_required":True,
                "preview":{"to":req.to,"subject":req.subject,"body_preview":req.body[:400]},
                "message":f"Ready to email **{req.to}**\n**Subject:** {req.subject}\n\n{req.body[:300]}...\n\nSend with `hitl_approved: true`."}
    e=_email_check()
    if e: return e
    try: return send_email(req.to,req.subject,req.body,req.attachment_path)
    except Exception as ex: return {"error":str(ex)}

@app.post("/api/email/cold-hr")
def email_cold(req: ColdEmailReq):
    profile = load_user_profile()
    uname = profile.get("name","Your Name")
    subj = f"Application – {req.role} | {uname} | {req.company}"
    body = (f"Hi {req.hr_name.split()[0]},\n\nMy name is {uname}. "
            f"I came across the {req.role} role at {req.company} and felt compelled to reach out.\n\n"
            f"{profile.get('summary','I am a passionate professional looking to contribute to great teams.')}\n\n"
            f"I'd love to connect — even 15 minutes would be valuable.\n\nWarm regards,\n{uname}")
    if not req.hitl_approved:
        return {"hitl_required":True,"preview":{"to":req.hr_email,"subject":subj,"body":body},
                "message":f"Ready to email **{req.hr_name}** at {req.company}.\n\n**Subject:** {subj}\n\n{body[:300]}...\n\nSend with `hitl_approved: true`."}
    e=_email_check()
    if e: return e
    try: return send_cold_email_to_hr(hr_name=req.hr_name,hr_email=req.hr_email,company=req.company,
                                       role=req.role,user_name=uname,user_summary=profile.get("summary",""),
                                       resume_path=req.resume_path)
    except Exception as ex: return {"error":str(ex)}

@app.post("/api/email/follow-up")
def email_fu(req: FollowUpReq):
    e=_email_check()
    if e: return e
    profile = load_user_profile()
    try: return send_follow_up_email(req.to,req.original_subject,profile.get("name",""),req.days_since)
    except Exception as ex: return {"error":str(ex)}

@app.get("/api/email/log")
def email_log(): return load_email_log()

# ── Resume ──────────────────────────────────────────────────────────────────────
@app.post("/api/resume/build")
def r_build(): return build_resume()

@app.post("/api/resume/tailor")
def r_tailor(req: TailorReq): return tailor_resume_to_jd(req.resume_path,req.job_description)

@app.post("/api/resume/score")
def r_score(req: ScoreReq): return score_resume_against_jd(req.resume_text,req.job_description)

@app.post("/api/resume/analyze")
async def r_analyze(file: UploadFile=File(...)):
    from server.config import DATA_DIR
    p = DATA_DIR/"uploads"/file.filename
    with open(p,"wb") as f: f.write(await file.read())
    return analyze_resume(str(p))

# ── Career ──────────────────────────────────────────────────────────────────────
@app.post("/api/career/next-steps")
def c_next(req: NextReq): return what_to_do_next(req.current_skills,req.target_role,req.experience_years)

@app.get("/api/career/roadmap")
def c_roadmap(goal: str): return career_roadmap(goal)

@app.get("/api/career/companies")
def c_companies(role: str): return find_target_companies(role)

# ── Courses ─────────────────────────────────────────────────────────────────────
@app.get("/api/courses/find")
def co_find(skill: str, limit: int=5): return find_free_courses(skill,limit)

@app.get("/api/courses/must-do")
def co_mustdo(role: str): return get_must_do_certs(role)

# ── Content ─────────────────────────────────────────────────────────────────────
@app.post("/api/content/calendar")
def ct_cal(req: CalReq): return generate_weekly_content_calendar(req.domain,req.weeks)

@app.get("/api/content/trending")
def ct_trending(domain: str="general"): return get_trending_topics(domain)

@app.post("/api/content/image-caption")
def ct_cap(req: ImgCapReq): return generate_image_post_caption(req.image_context,req.domain)

# ── HITL queue ───────────────────────────────────────────────────────────────────
@app.get("/api/hitl/queue")
def hitl_queue(): return {"pending":list(_hitl.values())}

# ── Main ─────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════╗
║       Ascendra v2.0 — Personal Test Mode            ║
║  LLM:  Groq (FREE — llama-3.3-70b)                 ║
║  API:  http://localhost:8000                        ║
║  Docs: http://localhost:8000/docs                   ║
╚══════════════════════════════════════════════════════╝""")
    cfg = validate_config()
    print("\nConfig:")
    for k,v in cfg.items():
        print(f"  {'✅' if v else '❌'}  {k}")
    if not cfg.get("groq"):
        print("\n⚠️  Add GROQ_API_KEY to backend/.env")
        print("   Free key: https://console.groq.com/keys\n")
    print()
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
