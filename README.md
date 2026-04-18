# Ascendra — Local Test Build
### Beige & Sage Edition · LinkedIn Connected from Your Machine

---

## Start in 3 steps

### Step 1 — Add credentials
```bash
cp backend/.env.example backend/.env
```
Open `backend/.env`:
```
GROQ_API_KEY=gsk_...          # console.groq.com/keys (free)
LINKEDIN_EMAIL=your@email.com
LINKEDIN_PASSWORD=yourpassword
SMTP_USER=your@gmail.com
SMTP_PASS=xxxx-xxxx-xxxx-xxxx  # Gmail App Password
```

### Step 2 — Start everything
**Mac/Linux:**
```bash
chmod +x start_local.sh
./start_local.sh
```
**Windows:** double-click `start_local.bat`

### Step 3 — Test LinkedIn is working
Open in browser: **http://localhost:8000/api/linkedin/test**

You should see:
```json
{
  "connected": true,
  "message": "✅ LinkedIn connected as: Your Name",
  "profile": { "name": "...", "headline": "...", "connections": 500 }
}
```

The chat UI also shows a **LinkedIn status pill** in the sidebar — green = working.

---

## URLs

| | URL |
|-|-----|
| **Web UI** | http://localhost:3000 |
| **API Docs** | http://localhost:8000/docs |
| **LinkedIn Test** | http://localhost:8000/api/linkedin/test |
| **Health Check** | http://localhost:8000/api/health |

---

## Design

New UI: **beige + sage green + warm brown** — clean, minimal, professional.
- Background: warm cream `#F7F3EE`
- Accent: sage green `#7D9B76`
- Typography: Playfair Display + DM Sans

---

## Why LinkedIn works locally but not on Render

| | Local | Render |
|-|-------|--------|
| IP address | Your home IP ✅ | AWS data center ❌ |
| Browser session | Persistent ✅ | Wiped on restart ❌ |
| LinkedIn detection | Looks human ✅ | Flagged as bot ❌ |

**Architecture:** Groq AI chat lives on Render. LinkedIn/Gmail actions run locally.
