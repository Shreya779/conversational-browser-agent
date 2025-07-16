#!/bin/bash

# Conversational Browser Control Agent - Run Script

echo "🤖 Starting Conversational Browser Control Agent..."
echo "================================================="

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check dependencies
if ! command_exists python3 && ! command_exists python; then
    echo "❌ Python not found. Please run setup.sh first."
    exit 1
fi

if ! command_exists node; then
    echo "❌ Node.js not found. Please run setup.sh first."
    exit 1
fi

# Check if backend dependencies are installed
if [ ! -d "backend/venv" ]; then
    echo "❌ Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Check if frontend dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo "❌ Node modules not found. Please run setup.sh first."
    exit 1
fi

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp "backend/.env.example" "backend/.env"
    echo "📝 Please edit backend/.env and choose your FREE AI service:"
    echo "   • Groq (recommended): https://console.groq.com/"
    echo "   • Hugging Face: https://huggingface.co/settings/tokens"
    echo "   • OpenAI: https://platform.openai.com/"
    read -p "Press Enter after updating the .env file..."
fi

echo "🚀 Starting Backend Server..."

# Start backend in background
cd backend
source venv/bin/activate
echo "🔧 Backend starting on http://localhost:8000"
echo "📚 API docs available at http://localhost:8000/docs"
python main.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
echo "⏳ Waiting for backend to start..."
sleep 3

echo "🎨 Starting Frontend Server..."

# Start frontend
cd frontend
echo "🌐 Frontend starting on http://localhost:3000"
echo "🤖 Conversational Browser Control Agent UI"
npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Both servers are starting!"
echo "================================================="
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend:  http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "🎯 Key Features:"
echo "✅ Real browser automation (Playwright)"
echo "✅ Natural language conversation"
echo "✅ Screenshots embedded in chat"
echo "✅ FREE AI content generation (Groq/HuggingFace)"
echo "❌ NO Gmail API usage"
echo ""
echo "⚠️  IMPORTANT: Only use test Gmail accounts!"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit
}

# Trap cleanup function on script exit
trap cleanup SIGINT SIGTERM

# Wait for user to press Ctrl+C
echo ""
echo "Press Ctrl+C to stop both servers"
wait
