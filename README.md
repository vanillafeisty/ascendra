# Ascendra 🔺
### *Rise Without Limits*

> Autonomous AI Career Intelligence Platform — Land your dream job with zero manual effort.

**Stack:** Next.js 14 · Expo React Native · FastAPI · Groq (free LLM)  
**Deploy:** Vercel (web) + Render (backend) — both free tiers

---

## Quick Start (Local)

```bash
# 1. Backend
cd backend
cp .env.example .env        # fill in your keys
pip install -r requirements.txt
playwright install chromium
python api.py               # → http://localhost:8000

# 2. Web
cd web
cp .env.example .env.local  # NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
npm install
npm run dev                 # → http://localhost:3000

# 3. Mobile (optional)
cd mobile
npm install
npx expo start
```

## Deploy to Production

👉 **See [DEPLOY.md](./DEPLOY.md) for the complete step-by-step guide**

**GitHub → Render (backend) + Vercel (web)**

---

## Features

| | Feature |
|-|---------|
| 🤝 | Auto-connect with HRs and hiring managers (HITL-gated) |
| 📧 | Cold email engine — finds HR emails + sends directly |
| 📄 | ATS-Semantic resume builder (NLP keyword alignment) |
| 🗺️ | Career roadmaps and skill gap analysis |
| 📝 | LinkedIn post automation with anti-bot stealth |
| 🛡️ | Human-in-the-Loop — review everything before it sends |
| 🚫 | Content moderation — blocks unethical/harmful requests |
| 🎓 | Free course finder with YouTube-validated links |
| 🤖 | Powered by Groq (llama-3.3-70b) — 100% free, no billing |

---

## Environment Variables

**Backend (`backend/.env`):**
```
GROQ_API_KEY=gsk_...          # console.groq.com/keys — free
LINKEDIN_EMAIL=your@email.com
LINKEDIN_PASSWORD=yourpassword
SMTP_USER=your@gmail.com
SMTP_PASS=xxxx-xxxx-xxxx-xxxx # Gmail App Password
```

**Web (`web/.env.local`):**
```
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

---

## Project Structure

```
ascendra/
├── backend/          FastAPI + all career tools
│   ├── api.py        Main server (Groq chat + endpoints)
│   ├── build.sh      Render build script (installs Playwright)
│   ├── render.yaml   Render deployment config
│   └── server/tools/ LinkedIn, Email, Resume, Career, Content
│
├── web/              Next.js 14 chatbot
│   ├── app/page.tsx  Landing page
│   ├── app/chat/     Chat interface
│   └── vercel.json   Vercel deployment config
│
├── mobile/           Expo React Native (iOS + Android)
├── srs/              Software Requirements Specification v2.0
├── DEPLOY.md         Full deployment guide ← READ THIS
└── .github/workflows/ CI/CD pipelines
```

---

⚠️ LinkedIn automation may violate LinkedIn's ToS. Use responsibly. All bulk actions require HITL approval. Personal use only.

*Ascendra v2.0 · Groq Edition*
