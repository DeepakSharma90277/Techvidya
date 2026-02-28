# 🚀 Quick Start - Run All Services

# Windows PowerShell Script
# Run this from the Techvidya root directory

Write-Host "🚀 Starting TechVidya Platform..." -ForegroundColor Cyan
Write-Host ""

# Check if in correct directory
if (-not (Test-Path ".\ai-agent") -or -not (Test-Path ".\server")) {
    Write-Host "❌ Error: Please run this script from the Techvidya root directory" -ForegroundColor Red
    exit 1
}

# Check if .env exists in ai-agent
if (-not (Test-Path ".\ai-agent\.env")) {
    Write-Host "⚠️  Warning: ai-agent\.env not found!" -ForegroundColor Yellow
    Write-Host "Please create .env file from .env.example and add your API keys" -ForegroundColor Yellow
    Write-Host ""
    $continue = Read-Host "Continue anyway? (y/n)"
    if ($continue -ne "y") {
        exit 0
    }
}

Write-Host "📦 Step 1/4: Starting Backend Server..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\server'; Write-Host '🔧 Backend Server' -ForegroundColor Yellow; npm run dev"

Write-Host "⏳ Waiting for backend to initialize..." -ForegroundColor Gray
Start-Sleep -Seconds 8

Write-Host "🤖 Step 2/4: Starting AI Agent..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\ai-agent'; Write-Host '🎓 AI Agent' -ForegroundColor Magenta; streamlit run app.py"

Write-Host "⏳ Waiting for AI agent to initialize..." -ForegroundColor Gray
Start-Sleep -Seconds 5

Write-Host "⚛️  Step 3/4: Starting React Frontend..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; Write-Host '📱 React Frontend' -ForegroundColor Blue; npm start"

Write-Host "⏳ Waiting for frontend to build..." -ForegroundColor Gray
Start-Sleep -Seconds 10

Write-Host ""
Write-Host "✅ All services started successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Access your services at:" -ForegroundColor Cyan
Write-Host "   📱 Frontend:    http://localhost:3000" -ForegroundColor White
Write-Host "   🤖 AI Agent:    http://localhost:8501" -ForegroundColor White
Write-Host "   🔧 Backend:     http://localhost:4000" -ForegroundColor White
Write-Host ""
Write-Host "💡 Tips:" -ForegroundColor Yellow
Write-Host "   - Click 'AI Assistant' in the navbar to access the AI Agent"
Write-Host "   - Use your User ID from MongoDB to login to AI Agent"
Write-Host "   - Check ai-agent/SETUP.md for API key configuration"
Write-Host ""
Write-Host "🛑 To stop all services:" -ForegroundColor Red
Write-Host "   Close each PowerShell window or run: Get-NetTCPConnection -LocalPort 3000,4000,8501 | % { Stop-Process -Id `$_.OwningProcess -Force }"
Write-Host ""
Write-Host "Press any key to exit this window..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
