"""
Conversational Browser Control Agent
====================================

A conversational AI agent that controls web browsers through natural language.
This application demonstrates REAL browser automation - NO Gmail API or SMTP usage.

The agent:
- Opens actual browser windows
- Navigates to gmail.com
- Clicks on UI elements
- Types in form fields
- Takes screenshots at each step
- Shows screenshots in conversation flow

This is NOT an email automation tool - it's a browser control platform
that happens to demonstrate its capabilities by sending emails.
"""

import os
import logging
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.core.config import settings
from app.api.websocket import router as websocket_router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Conversational Browser Control Agent",
    description="""
    🤖 An AI-powered agent that controls web browsers through natural language conversation.
    
    ## Key Features:
    - **Real Browser Automation**: Uses Playwright to control actual browsers (NO APIs)
    - **Natural Language Interface**: Conversational commands like "send an email to my manager"
    - **Visual Feedback**: Screenshots embedded directly in chat conversation
    - **AI Content Generation**: Automatically generates professional email content
    - **Extensible Architecture**: Modular design for future website integrations
    
    ## What Makes This Special:
    This is NOT just another email tool. It's a demonstration of how AI agents can
    navigate and control the digital world like humans do - through actual UI interaction,
    not programmatic APIs.
    
    ## Technology Stack:
    - Backend: FastAPI + WebSockets
    - Browser Control: Playwright (REAL browser automation)
    - AI: OpenAI API for content generation
    - Frontend: React with real-time chat interface
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(websocket_router, prefix="/api")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Conversational Browser Control Agent API",
        "version": "1.0.0",
        "description": "AI agent that controls browsers through conversation - NO APIs, REAL automation",
        "features": [
            "🌐 Real browser automation using Playwright",
            "💬 Natural language conversation interface", 
            "📸 Screenshots embedded in chat flow",
            f"🤖 AI-powered content generation ({settings.AI_SERVICE.upper()})",
            "🏗️ Modular architecture for extensibility"
        ],
        "ai_services": {
            "current": settings.AI_SERVICE.upper(),
            "available": [
                "GROQ (FREE tier - recommended)",
                "HUGGINGFACE (FREE)",
                "OPENAI (if you have credits)"
            ],
            "setup_guides": {
                "groq": "Get free API key from https://console.groq.com/",
                "huggingface": "Get free token from https://huggingface.co/settings/tokens",
                "openai": "Get API key from https://platform.openai.com/"
            }
        },
        "endpoints": {
            "websocket": "/api/ws/{session_id}",
            "docs": "/docs",
            "health": "/api/health"
        },
        "tech_stack": {
            "browser_automation": "Playwright (NOT Gmail API)",
            "backend": "FastAPI + WebSockets",
            "ai": f"{settings.AI_SERVICE.upper()} (FREE)",
            "frontend": "React"
        }
    }

@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logger.info("🚀 Conversational Browser Control Agent starting up...")
    logger.info("📋 Features enabled:")
    logger.info("   ✅ Real browser automation (Playwright)")
    logger.info("   ✅ Natural language processing")
    logger.info("   ✅ Screenshot capture and transmission")
    logger.info(f"   ✅ AI content generation ({settings.AI_SERVICE.upper()})")
    logger.info("   ❌ NO Gmail API usage")
    logger.info("   ❌ NO SMTP libraries")
    
    # Check AI service configuration
    if settings.AI_SERVICE == "groq" and not settings.GROQ_API_KEY:
        logger.warning("⚠️  GROQ_API_KEY not set - Get free API key from https://console.groq.com/")
    elif settings.AI_SERVICE == "huggingface" and not settings.HUGGINGFACE_API_KEY:
        logger.warning("⚠️  HUGGINGFACE_API_KEY not set - Get free token from https://huggingface.co/settings/tokens")
    elif settings.AI_SERVICE == "openai" and not settings.OPENAI_API_KEY:
        logger.warning("⚠️  OPENAI_API_KEY not set - AI content generation may not work")
    
    logger.info("🌟 Ready to control browsers through conversation!")

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    logger.info("🛑 Conversational Browser Control Agent shutting down...")

if __name__ == "__main__":
    # Ensure screenshots directory exists
    os.makedirs("screenshots", exist_ok=True)
    
    # Check for required environment variables based on selected AI service
    if settings.AI_SERVICE == "groq" and not settings.GROQ_API_KEY:
        logger.warning("⚠️  GROQ_API_KEY not set - Get free API key from https://console.groq.com/")
    elif settings.AI_SERVICE == "huggingface" and not settings.HUGGINGFACE_API_KEY:
        logger.warning("⚠️  HUGGINGFACE_API_KEY not set - Get free token from https://huggingface.co/settings/tokens")
    elif settings.AI_SERVICE == "openai" and not settings.OPENAI_API_KEY:
        logger.warning("⚠️  OPENAI_API_KEY not set - AI content generation may not work")
    
    logger.info(f"🎯 Starting server on {settings.HOST}:{settings.PORT}")
    logger.info(f"📊 Debug mode: {settings.DEBUG}")
    logger.info(f"🤖 AI Service: {settings.AI_SERVICE.upper()}")
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
