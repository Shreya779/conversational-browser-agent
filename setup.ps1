# Installation and Setup Script for Conversational Browser Control Agent

Write-Host "🤖 Setting up Conversational Browser Control Agent..." -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8+ first." -ForegroundColor Red
    exit 1
}

# Check if Node.js is installed
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✅ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js not found. Please install Node.js 16+ first." -ForegroundColor Red
    exit 1
}

Write-Host "`n🔧 Setting up Backend..." -ForegroundColor Yellow

# Navigate to backend directory
Set-Location backend

# Create virtual environment
Write-Host "Creating Python virtual environment..." -ForegroundColor Cyan
python -m venv venv

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& .\venv\Scripts\Activate.ps1

# Install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt

# Install Playwright browsers
Write-Host "Installing Playwright browsers..." -ForegroundColor Cyan
playwright install

# Create .env file if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file..." -ForegroundColor Cyan
    Copy-Item ".env.example" ".env"
    Write-Host "⚠️  Please edit .env file and choose your FREE AI service!" -ForegroundColor Yellow
    Write-Host "   Option 1 (Recommended): Groq - https://console.groq.com/" -ForegroundColor Green
    Write-Host "   Option 2: Hugging Face - https://huggingface.co/settings/tokens" -ForegroundColor Green
    Write-Host "   Option 3: OpenAI - https://platform.openai.com/" -ForegroundColor Yellow
}

Write-Host "✅ Backend setup complete!" -ForegroundColor Green

Write-Host "`n🎨 Setting up Frontend..." -ForegroundColor Yellow

# Navigate to frontend directory
Set-Location ..\frontend

# Install Node.js dependencies
Write-Host "Installing Node.js dependencies..." -ForegroundColor Cyan
npm install

Write-Host "✅ Frontend setup complete!" -ForegroundColor Green

# Navigate back to root
Set-Location ..

Write-Host "`n🚀 Setup Complete!" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor White
Write-Host "1. Edit backend/.env and choose your FREE AI service:" -ForegroundColor White
Write-Host "   • Groq (recommended): https://console.groq.com/" -ForegroundColor Green
Write-Host "   • Hugging Face: https://huggingface.co/settings/tokens" -ForegroundColor Green
Write-Host "   • OpenAI: https://platform.openai.com/" -ForegroundColor Yellow
Write-Host "2. Start backend: cd backend && python main.py" -ForegroundColor White
Write-Host "3. Start frontend: cd frontend && npm start" -ForegroundColor White
Write-Host "4. Open http://localhost:3000 in your browser" -ForegroundColor White
Write-Host "`n⚠️  IMPORTANT: Only use test Gmail accounts!" -ForegroundColor Yellow
Write-Host "🎯 This agent controls REAL browsers - no APIs used!" -ForegroundColor Green
