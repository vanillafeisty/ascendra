#!/bin/bash
# Ascendra — Backend Starter (Groq Edition)
set -e

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║       Ascendra v2.0 — Personal Test Mode        ║"
echo "║       LLM: Groq (FREE — no billing)             ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

command -v python3 &>/dev/null || { echo "❌ Python 3 not found. Install from https://python.org"; exit 1; }
echo "✅ $(python3 --version)"

if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
    echo ""
    echo "📝 Open backend/.env and fill in:"
    echo ""
    echo "   GROQ_API_KEY=gsk_...         ← console.groq.com/keys (free)"
    echo "   LINKEDIN_EMAIL=your@email.com"
    echo "   LINKEDIN_PASSWORD=yourpassword"
    echo "   SMTP_USER=your@gmail.com"
    echo "   SMTP_PASS=xxxx-xxxx-xxxx-xxxx  ← Gmail App Password"
    echo ""
    echo "Then re-run: ./start.sh"
    echo ""
    exit 1
fi

echo "📦 Installing Python packages..."
pip3 install -r requirements.txt -q

echo "🌐 Checking Playwright browsers..."
python3 -m playwright install chromium --quiet 2>/dev/null || true

mkdir -p server/data/resumes server/data/uploads

echo ""
echo "🚀 Starting Ascendra backend..."
echo "   API:   http://localhost:8000"
echo "   Docs:  http://localhost:8000/docs"
echo ""
echo "   Then in another terminal:"
echo "   cd web && npm run dev → http://localhost:3000"
echo ""

python3 api.py
