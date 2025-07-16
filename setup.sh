#!/bin/bash

# Installation and Setup Script for Conversational Browser Control Agent

echo "🤖 Setting up Conversational Browser Control Agent..."
echo "================================================="

# Check if Python is installed
if command -v python3 &> /dev/null; then
    echo "✅ Python found: $(python3 --version)"
elif command -v python &> /dev/null; then
    echo "✅ Python found: $(python --version)"
else
    echo "❌ Python not found. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if command -v node &> /dev/null; then
    echo "✅ Node.js found: $(node --version)"
else
    echo "❌ Node.js not found. Please install Node.js 16+ first."
    exit 1
fi

echo ""
echo "🔧 Setting up Backend..."

# Navigate to backend directory
cd backend

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv || python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install Playwright browsers
echo "Installing Playwright browsers..."
playwright install

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and choose your FREE AI service!"
    echo "   Option 1 (Recommended): Groq - https://console.groq.com/"
    echo "   Option 2: Hugging Face - https://huggingface.co/settings/tokens"
    echo "   Option 3: OpenAI - https://platform.openai.com/"
fi

echo "✅ Backend setup complete!"

echo ""
echo "🎨 Setting up Frontend..."

# Navigate to frontend directory
cd ../frontend

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

echo "✅ Frontend setup complete!"

# Navigate back to root
cd ..

echo ""
echo "🚀 Setup Complete!"
echo "================================================="
echo "Next steps:"
echo "1. Edit backend/.env and choose your FREE AI service:"
echo "   • Groq (recommended): https://console.groq.com/"
echo "   • Hugging Face: https://huggingface.co/settings/tokens"
echo "   • OpenAI: https://platform.openai.com/"
echo "2. Start backend: cd backend && python main.py"
echo "3. Start frontend: cd frontend && npm start"
echo "4. Open http://localhost:3000 in your browser"
echo ""
echo "⚠️  IMPORTANT: Only use test Gmail accounts!"
echo "🎯 This agent controls REAL browsers - no APIs used!"
