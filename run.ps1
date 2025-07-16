# Conversational Browser Control Agent - Run Script

Write-Host "🤖 Starting Write-Host "🎯 Key Features:" -ForegroundColor Yellow
Write-Host "✅ Real browser automation (Playwright)" -ForegroundColor Green
Write-Host "✅ Natural language conversation" -ForegroundColor Green  
Write-Host "✅ Screenshots embedded in chat" -ForegroundColor Green
Write-Host "✅ FREE AI content generation (Groq/HuggingFace)" -ForegroundColor Green
Write-Host "❌ NO Gmail API usage" -ForegroundColor Redsational Browser Control Agent..." -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

# Function to check if a command exists
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

# Check dependencies
if (-not (Test-Command python)) {
    Write-Host "❌ Python not found. Please run setup.ps1 first." -ForegroundColor Red
    exit 1
}

if (-not (Test-Command node)) {
    Write-Host "❌ Node.js not found. Please run setup.ps1 first." -ForegroundColor Red
    exit 1
}

# Check if backend dependencies are installed
if (-not (Test-Path "backend\venv")) {
    Write-Host "❌ Virtual environment not found. Please run setup.ps1 first." -ForegroundColor Red
    exit 1
}

# Check if frontend dependencies are installed
if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "❌ Node modules not found. Please run setup.ps1 first." -ForegroundColor Red
    exit 1
}

# Check if .env file exists
if (-not (Test-Path "backend\.env")) {
    Write-Host "⚠️  .env file not found. Creating from template..." -ForegroundColor Yellow
    Copy-Item "backend\.env.example" "backend\.env"
    Write-Host "📝 Please edit backend\.env and choose your FREE AI service:" -ForegroundColor Yellow
    Write-Host "   • Groq (recommended): https://console.groq.com/" -ForegroundColor Green
    Write-Host "   • Hugging Face: https://huggingface.co/settings/tokens" -ForegroundColor Green  
    Write-Host "   • OpenAI: https://platform.openai.com/" -ForegroundColor Yellow
    Start-Process notepad "backend\.env"
    Read-Host "Press Enter after updating the .env file"
}

Write-Host "🚀 Starting Backend Server..." -ForegroundColor Yellow

# Start backend in a new PowerShell window
$backendScript = @"
Set-Location '$pwd\backend'
& .\venv\Scripts\Activate.ps1
Write-Host '🔧 Backend starting on http://localhost:8000' -ForegroundColor Green
Write-Host '📚 API docs available at http://localhost:8000/docs' -ForegroundColor Cyan
python main.py
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendScript

# Wait a moment for backend to start
Write-Host "⏳ Waiting for backend to start..." -ForegroundColor Cyan
Start-Sleep -Seconds 3

Write-Host "🎨 Starting Frontend Server..." -ForegroundColor Yellow

# Start frontend in a new PowerShell window  
$frontendScript = @"
Set-Location '$pwd\frontend'
Write-Host '🌐 Frontend starting on http://localhost:3000' -ForegroundColor Green
Write-Host '🤖 Conversational Browser Control Agent UI' -ForegroundColor Cyan
npm start
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendScript

Write-Host "`n✅ Both servers are starting!" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green
Write-Host "🌐 Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "🔧 Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "📚 API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "`n🎯 Key Features:" -ForegroundColor Yellow
Write-Host "✅ Real browser automation (Playwright)" -ForegroundColor Green
Write-Host "✅ Natural language conversation" -ForegroundColor Green  
Write-Host "✅ Screenshots embedded in chat" -ForegroundColor Green
Write-Host "✅ AI-generated email content" -ForegroundColor Green
Write-Host "❌ NO Gmail API usage" -ForegroundColor Red
Write-Host "`n⚠️  IMPORTANT: Only use test Gmail accounts!" -ForegroundColor Yellow

# Wait a bit more then open browser
Start-Sleep -Seconds 2
Write-Host "`n🌐 Opening browser..." -ForegroundColor Cyan
Start-Process "http://localhost:3000"
