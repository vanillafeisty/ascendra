@echo off
echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║       Ascendra — Local Test Mode                    ║
echo ╚══════════════════════════════════════════════════════╝
echo.

if not exist "backend\.env" (
    copy backend\.env.example backend\.env
    echo 📝 Open backend\.env and fill in your credentials, then re-run.
    notepad backend\.env
    pause & exit /b
)

echo 📦 Installing Python dependencies...
cd backend
pip install -r requirements.txt -q
python -m playwright install chromium
cd ..

if not exist "web\node_modules" (
    echo 📦 Installing Node dependencies...
    cd web && npm install --silent && cd ..
)
if not exist "web\.env.local" copy web\.env.example web\.env.local

echo.
echo 🚀 Starting Ascendra...
echo    Backend:   http://localhost:8000
echo    Web UI:    http://localhost:3000
echo    LinkedIn:  http://localhost:8000/api/linkedin/test
echo.

start "Ascendra Backend" cmd /k "cd backend && python api.py"
timeout /t 3 /nobreak >nul
start "Ascendra Web"     cmd /k "cd web && npm run dev"
timeout /t 5 /nobreak >nul
start http://localhost:3000

echo Both servers started in separate windows.
pause
