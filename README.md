# Ascendra — Personal Testing Guide
### Rise Without Limits · Groq Edition (100% Free)

---

## Step 1 — Get Your Groq API Key (2 minutes, free, no card)

1. Go to **https://console.groq.com/keys**
2. Sign up (free) → Create API Key
3. Copy the key — it starts with `gsk_...`

---

## Step 2 — Configure Your Credentials

```bash
cd backend
cp .env.example .env
```

Open `backend/.env` and fill in:

```env
# REQUIRED — Groq (free AI)
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxx

# REQUIRED — Your LinkedIn login
LINKEDIN_EMAIL=your@email.com
LINKEDIN_PASSWORD=yourpassword

# REQUIRED for emails — Gmail App Password
# Get at: myaccount.google.com → Security → App Passwords → Generate
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@gmail.com
SMTP_PASS=xxxx-xxxx-xxxx-xxxx

# OPTIONAL (leave blank for now)
YOUTUBE_API_KEY=
HUNTER_API_KEY=
```

---

## Step 3 — Start the Backend

**Mac / Linux:**
```bash
cd backend
chmod +x start.sh
./start.sh
```

**Windows:**
```
Double-click backend/start.bat
```

You'll see:
```
✅  groq
✅  linkedin
✅  smtp
```

---

## Step 4 — Start the Web App

Open a second terminal:

```bash
cd web
cp .env.example .env.local   # no keys needed — AI runs in backend
npm install
npm run dev
```

Open **http://localhost:3000** in your browser.

---

## Step 5 — Test It

Try these in the chat:

```
"What is Ascendra and what can you do for me?"
```
```
"I know HTML, CSS, JavaScript and React basics.
 My goal is to get a job as a frontend developer at a product company.
 Tell me exactly what to do next."
```
```
"Connect me with 5 HRs in Bangalore hiring React developers"
```
```
"Draft a cold email to Priya Sharma at Razorpay about my frontend profile"
```

---

## Step 6 — Mobile App (Optional)

```bash
cd mobile
npm install
npx expo start
```

Scan the QR code with **Expo Go** (iOS/Android).

For real device: change `BACKEND_URL` in
`mobile/src/lib/constants.ts` to your PC's local IP:
```
http://192.168.x.x:8000
```

---

## How LinkedIn & Gmail Actually Work

| Integration | How | What you provide |
|------------|-----|-----------------|
| LinkedIn | Logs in AS YOU via unofficial API + stealth Playwright | Email + password in `.env` |
| Gmail | Sends FROM your Gmail via SMTP | Gmail App Password in `.env` |

**Your credentials stay 100% on your machine.** Nothing is sent to any third-party.

**LinkedIn safety defaults:**
- Max 20 connections/day (conservative for testing)
- 4-second delay between actions
- Every bulk action shows a HITL preview first

---

## Groq Free Tier Limits

| Limit | Value |
|-------|-------|
| Requests/minute | 30 |
| Requests/day | 14,400 |
| Model | llama-3.3-70b-versatile |
| Cost | $0 forever (no billing) |

---

## Project Structure

```
ascendra/
├── backend/         FastAPI + all career tools (start this first)
│   ├── api.py       Main server (Groq-powered chat + all endpoints)
│   ├── .env         YOUR credentials (never commit this)
│   └── server/
│       ├── config.py
│       └── tools/
│           ├── linkedin_tools.py   (anti-bot stealth layer)
│           ├── email_tools.py
│           ├── resume_tools.py     (ATS-Semantic Engine)
│           ├── career_tools.py
│           └── content_tools.py
│
├── web/             Next.js 14 chatbot (deploy to Vercel)
│   ├── app/
│   │   ├── page.tsx         Landing page
│   │   ├── chat/page.tsx    Chat UI
│   │   └── api/chat/        Proxies to backend (no Anthropic key)
│   └── components/
│
└── mobile/          Expo React Native (iOS + Android)
    └── app/
        ├── index.tsx    Landing screen
        └── chat.tsx     Chat screen
```

---

## Deploy to Production (after testing)

**Web → Vercel (free):**
```bash
cd web && npx vercel deploy
# Set env var: NEXT_PUBLIC_BACKEND_URL=https://your-backend-url.com
```

**Backend → Railway (free tier):**
- Connect GitHub repo
- Root Directory: `backend`
- Start Command: `python api.py`
- Add all `.env` variables in Railway dashboard

---

*Ascendra v2.0 · Groq Edition · Personal Testing Mode*
