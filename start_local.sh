#!/bin/bash
# Ascendra — Local Test Launcher
# Starts both backend and frontend together

set -e
echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║       Ascendra — Local Test Mode                    ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# Check .env exists
if [ ! -f "backend/.env" ]; then
  echo "⚠️  No backend/.env found. Creating..."
  cp backend/.env.example backend/.env
  echo ""
  echo "📝 Open backend/.env and fill in:"
  echo "   GROQ_API_KEY=gsk_...          (console.groq.com/keys — free)"
  echo "   LINKEDIN_EMAIL=your@email.com"
  echo "   LINKEDIN_PASSWORD=yourpass"
  echo "   SMTP_USER=your@gmail.com"
  echo "   SMTP_PASS=xxxx-xxxx-xxxx-xxxx"
  echo ""
  echo "Then re-run: ./start_local.sh"
  exit 1
fi

# Install Python deps
echo "📦 Installing Python dependencies..."
cd backend
pip3 install -r requirements.txt -q 2>/dev/null || pip install -r requirements.txt -q
python3 -m playwright install chromium --quiet 2>/dev/null || true
cd ..

# Install Node deps
if [ ! -d "web/node_modules" ]; then
  echo "📦 Installing Node dependencies..."
  cd web && npm install --silent && cd ..
fi

# Copy .env for web
[ ! -f "web/.env.local" ] && cp web/.env.example web/.env.local

echo ""
echo "🚀 Starting Ascendra..."
echo ""
echo "  Backend:  http://localhost:8000"
echo "  Web UI:   http://localhost:3000"
echo "  LinkedIn: http://localhost:8000/api/linkedin/test"
echo "  API Docs: http://localhost:8000/docs"
echo ""
echo "  Press Ctrl+C to stop both servers"
echo ""

# Start backend in background
cd backend && python3 api.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 2

# Start Next.js
cd web && npm run dev &
FRONTEND_PID=$!
cd ..

# Open browser after 4 seconds
sleep 4
if command -v open &>/dev/null; then
  open http://localhost:3000
elif command -v xdg-open &>/dev/null; then
  xdg-open http://localhost:3000
fi

echo "Both servers running. Press Ctrl+C to stop."
wait $BACKEND_PID $FRONTEND_PID
