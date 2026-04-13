# Ascendra — Deployment Guide
### GitHub → Render (backend) + Vercel (web)

---

## Overview

```
Your Machine (local .env with credentials)
        │
        ▼
GitHub Repository  ──────────────────────────────┐
        │                                        │
        ▼                                        ▼
Render (backend API)                    Vercel (Next.js web)
https://ascendra-backend.onrender.com   https://ascendra.vercel.app
        │                                        │
        └──────────── talks to ─────────────────┘
```

**Important:** Your `.env` file (with LinkedIn password, Gmail password, Groq key)
is NEVER pushed to GitHub. You paste each secret directly into Render's dashboard.

---

## Part 1 — Push to GitHub

### 1.1 Create the GitHub repository

1. Go to **github.com** → click **New repository** (top right `+`)
2. Repository name: `ascendra`
3. Set to **Private** (important — keeps your code safe)
4. **Do NOT** check "Add README" or any other init options
5. Click **Create repository**

GitHub shows you a page with commands. Keep it open.

### 1.2 Initialize Git locally

Open your terminal, navigate to the `ascendra-groq/` folder:

```bash
cd ascendra-groq

# Initialize git
git init

# Add everything EXCEPT secrets (.gitignore handles this)
git add .

# Check what's staged — .env should NOT appear
git status
# You should see files like: backend/api.py, web/app/page.tsx, etc.
# You should NOT see: backend/.env, gmail_credentials.json

# First commit
git commit -m "feat: Ascendra v2.0 - Groq edition initial commit"
```

### 1.3 Connect to GitHub and push

Copy the commands GitHub showed you. They look like this:

```bash
git remote add origin https://github.com/YOUR_USERNAME/ascendra.git
git branch -M main
git push -u origin main
```

After pushing, refresh your GitHub repo — you should see all the files.

**Double-check:** Click into `backend/` on GitHub. You should see `api.py`, `requirements.txt`, etc. — but NO `.env` file. If you see `.env`, stop and run `git rm --cached backend/.env` then commit again.

---

## Part 2 — Deploy Backend on Render (Free)

### 2.1 Create a Render account
Go to **render.com** → Sign up with GitHub (easiest — links your repos automatically)

### 2.2 Create a new Web Service

1. Render dashboard → **New +** → **Web Service**
2. Connect your GitHub repo → select **ascendra**
3. Fill in these settings:

| Field | Value |
|-------|-------|
| **Name** | `ascendra-backend` |
| **Region** | Singapore (closest to India) or Oregon |
| **Branch** | `main` |
| **Root Directory** | `backend` |
| **Runtime** | `Python 3` |
| **Build Command** | `bash build.sh` |
| **Start Command** | `uvicorn api:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | Free |

4. Scroll down to **Environment Variables** — click **Add Environment Variable** for each:

| Key | Value |
|-----|-------|
| `GROQ_API_KEY` | `gsk_your_groq_key` |
| `LINKEDIN_EMAIL` | `your@email.com` |
| `LINKEDIN_PASSWORD` | `yourpassword` |
| `SMTP_HOST` | `smtp.gmail.com` |
| `SMTP_PORT` | `587` |
| `SMTP_USER` | `your@gmail.com` |
| `SMTP_PASS` | `xxxx-xxxx-xxxx-xxxx` |
| `LINKEDIN_MAX_CONNECTIONS_PER_DAY` | `20` |
| `LINKEDIN_DELAY_SECONDS` | `4.0` |

5. Click **Create Web Service**

Render will start building. First build takes ~5 minutes (installing packages + Playwright).

### 2.3 Verify backend is live

Once the build shows **Live** (green), click the URL Render gives you — something like:
```
https://ascendra-backend.onrender.com
```

You should see:
```json
{"name":"Ascendra","version":"2.0.0-groq","status":"running"}
```

Also check: `https://ascendra-backend.onrender.com/api/health`

**Save your Render URL** — you'll need it for Vercel.

---

## Part 3 — Deploy Web on Vercel (Free)

### 3.1 Create a Vercel account
Go to **vercel.com** → Sign up with GitHub

### 3.2 Import the project

1. Vercel dashboard → **Add New** → **Project**
2. Import from GitHub → select **ascendra**
3. Vercel auto-detects it as Next.js ✅
4. Under **Root Directory** → click **Edit** → type `web` → click **Continue**

### 3.3 Configure environment variables

In the **Environment Variables** section, add:

| Name | Value |
|------|-------|
| `NEXT_PUBLIC_BACKEND_URL` | `https://ascendra-backend.onrender.com` |

(Use your actual Render URL from Part 2)

### 3.4 Deploy

Click **Deploy**. Vercel builds in ~2 minutes.

Once done, you get a URL like:
```
https://ascendra.vercel.app
```

Open it — the full Ascendra chat interface loads. Type something to test.

---

## Part 4 — Wire Them Together

The web app (Vercel) needs to talk to the backend (Render).

### Update NEXT_PUBLIC_BACKEND_URL in Vercel

If the chat says "cannot reach backend":

1. Vercel dashboard → your project → **Settings** → **Environment Variables**
2. Find `NEXT_PUBLIC_BACKEND_URL`
3. Set value to: `https://YOUR-NAME.onrender.com` (your exact Render URL)
4. Click **Save**
5. Go to **Deployments** → click the three dots on latest deploy → **Redeploy**

### Test end-to-end

Open your Vercel URL → type in the chat:
```
Hello Ascendra, what can you do?
```

If you get a response from the AI — everything is working. 🎉

---

## Part 5 — Auto-Deploy on Every Push

After the initial setup, every time you push to `main`:
- **Render** automatically rebuilds the backend
- **Vercel** automatically rebuilds the web app

```bash
# Make a change → push → both platforms update automatically
git add .
git commit -m "update: improved cold email template"
git push
```

---

## Troubleshooting

### Backend build fails on Render

**Problem:** `playwright install chromium` fails  
**Fix:** Make sure `Build Command` is set to `bash build.sh` (not `pip install -r requirements.txt`)

**Problem:** `ModuleNotFoundError: No module named 'groq'`  
**Fix:** Check that `groq>=0.9.0` is in `requirements.txt` and redeploy

### Web shows "cannot reach backend"

**Problem:** CORS error or connection refused  
**Fix:** 
1. Verify `NEXT_PUBLIC_BACKEND_URL` in Vercel matches your exact Render URL
2. Check Render logs — backend might be sleeping (free tier sleeps after 15min inactivity)
3. Hit `https://your-render-url.onrender.com/api/health` directly to wake it up

### Render free tier sleeps

Free Render services sleep after 15 minutes of inactivity and take ~30 seconds to wake up.
The first message after inactivity will be slow — that's normal.

**To avoid this:** Upgrade to Render's $7/month Starter plan, or use a free uptime monitor like UptimeRobot to ping your backend every 14 minutes.

### LinkedIn/Gmail not working on Render

LinkedIn automation uses Playwright (a real browser) which works on Render but the free tier has limited memory. If LinkedIn actions fail:
1. Check Render logs for memory errors
2. Reduce `LINKEDIN_MAX_CONNECTIONS_PER_DAY` to 5 during testing
3. Consider keeping LinkedIn/Gmail automation local only, and using Render just for the chat AI

---

## Final URLs

After deployment you'll have:

| Service | URL |
|---------|-----|
| Web App | `https://ascendra.vercel.app` |
| Backend API | `https://ascendra-backend.onrender.com` |
| API Docs | `https://ascendra-backend.onrender.com/docs` |
| Health Check | `https://ascendra-backend.onrender.com/api/health` |

---

## GitHub Secrets (for auto-deploy workflow)

If you want the GitHub Actions deploy workflow to auto-push to Vercel on every push,
add these in **GitHub → repo → Settings → Secrets and variables → Actions → New secret**:

| Secret | Where to get it |
|--------|----------------|
| `VERCEL_TOKEN` | vercel.com → Account Settings → Tokens → Create |
| `VERCEL_ORG_ID` | vercel.com → Account Settings → General → Your ID |
| `VERCEL_PROJECT_ID` | Vercel project → Settings → General → Project ID |
| `BACKEND_URL` | Your Render URL |

---

*Ascendra v2.0 · Groq Edition · Rise Without Limits*
