@echo off
echo.
echo ╔══════════════════════════════════════════════════╗
echo ║       Ascendra v2.0 — Personal Test Mode        ║
echo ║       LLM: Groq (FREE — no billing)             ║
echo ╚══════════════════════════════════════════════════╝
echo.

python --version >nul 2>&1 || (echo ❌ Python not found. Install from https://python.org & pause & exit /b)

if not exist ".env" (
    echo ⚠️  No .env found. Creating from template...
    copy .env.example .env
    echo.
    echo 📝 Open backend\.env and fill in:
    echo    GROQ_API_KEY=gsk_...
    echo    LINKEDIN_EMAIL=your@email.com
    echo    LINKEDIN_PASSWORD=yourpassword
    echo    SMTP_USER=your@gmail.com
    echo    SMTP_PASS=xxxx-xxxx-xxxx-xxxx
    echo.
    notepad .env
    pause & exit /b
)

echo 📦 Installing packages...
pip install -r requirements.txt -q

echo 🌐 Installing Playwright...
python -m playwright install chromium

if not exist "server\data\resumes" mkdir server\data\resumes
if not exist "server\data\uploads" mkdir server\data\uploads

echo.
echo 🚀 Starting Ascendra backend...
start "" /B cmd /C "timeout /t 3 /nobreak >nul && start http://localhost:8000/docs"
python api.py
pause
