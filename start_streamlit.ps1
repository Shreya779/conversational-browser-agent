#!/usr/bin/env powershell
<#
.SYNOPSIS
    Streamlit UI Startup Script for Conversational Browser Control Agent

.DESCRIPTION
    This script sets up and runs the Streamlit interface for the email automation agent.
    It includes automatic dependency installation and browser setup.
#>

Write-Host "🚀 Conversational Browser Control Agent - Streamlit Edition" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

# Check if in virtual environment
if ($env:VIRTUAL_ENV) {
    Write-Host "✅ Virtual environment active: $env:VIRTUAL_ENV" -ForegroundColor Green
} else {
    Write-Host "⚠️  No virtual environment detected" -ForegroundColor Yellow
    Write-Host "💡 Consider activating your venv first" -ForegroundColor Yellow
}

# Install Streamlit dependencies
Write-Host "`n📦 Installing Streamlit dependencies..." -ForegroundColor Yellow
pip install -r requirements_streamlit.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Setup browser automation
Write-Host "`n🌐 Setting up browser automation..." -ForegroundColor Yellow
python setup_browser.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Browser setup had issues, but continuing..." -ForegroundColor Yellow
}

# Check if backend is running
Write-Host "`n🔍 Checking backend status..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000" -TimeoutSec 3
    Write-Host "✅ Backend is running" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Backend not running. Starting in integrated mode..." -ForegroundColor Yellow
    Write-Host "💡 For full functionality, start backend separately:" -ForegroundColor Cyan
    Write-Host "   cd backend && python main.py" -ForegroundColor Cyan
}

# Start Streamlit
Write-Host "`n🎨 Starting Streamlit UI..." -ForegroundColor Green
Write-Host "🌐 Opening: http://localhost:8501" -ForegroundColor Cyan
Write-Host "`n" + "=" * 60 -ForegroundColor Cyan

# Launch Streamlit
streamlit run streamlit_app.py --server.port 8501 --server.address localhost
