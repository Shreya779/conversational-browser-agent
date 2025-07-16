#!/usr/bin/env python3
"""
Groq API Configuration Test Script
=================================

This script tests your Groq API configuration to ensure everything is working
before you run the main application.
"""

import os
import sys
from pathlib import Path

# Add the backend app to Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

try:
    from app.core.config import settings
    from groq import Groq
    print("📦 Dependencies loaded successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure you've installed dependencies: pip install -r backend/requirements.txt")
    sys.exit(1)

def test_groq_api():
    """Test Groq API configuration"""
    print("\n🤖 Testing Groq API Configuration...")
    print("=" * 50)
    
    # Check configuration
    print(f"🔧 AI Service: {settings.AI_SERVICE}")
    
    if settings.AI_SERVICE != "groq":
        print(f"⚠️  AI_SERVICE is set to '{settings.AI_SERVICE}', not 'groq'")
        print("💡 Set AI_SERVICE=groq in your .env file")
        return False
    
    if not settings.GROQ_API_KEY:
        print("❌ GROQ_API_KEY not found in environment")
        print("💡 Add GROQ_API_KEY=your_key_here to your .env file")
        print("💡 Get free API key from: https://console.groq.com/")
        return False
    
    print(f"✅ GROQ_API_KEY found: {settings.GROQ_API_KEY[:8]}...{settings.GROQ_API_KEY[-4:]}")
    
    # Test API connection
    try:
        print("\n🔗 Testing API connection...")
        
        # Initialize client with only API key (no extra parameters)
        client = Groq(api_key=settings.GROQ_API_KEY)
        
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Generate a short professional email subject about a test email."}
            ],
            max_tokens=50,
            temperature=0.3
        )
        
        result = response.choices[0].message.content
        print(f"✅ API test successful!")
        print(f"📧 Sample generation: {result[:60]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        if "401" in str(e) or "authentication" in str(e).lower():
            print("💡 This usually means your API key is invalid")
            print("💡 Double-check your API key at https://console.groq.com/")
        elif "rate_limit" in str(e).lower():
            print("💡 Rate limit exceeded - this is normal for free tier")
            print("💡 Wait a moment and try again")
        elif "proxies" in str(e).lower() or "unexpected keyword" in str(e).lower():
            print("💡 Groq client version issue detected")
            print("💡 Try updating: pip install --upgrade groq")
        else:
            print("💡 Check your internet connection and API key")
        return False

def test_email_generation():
    """Test email generation functionality"""
    print("\n📧 Testing Email Generation...")
    print("=" * 50)
    
    try:
        from app.services.ai_content_generator import AIContentGenerator
        
        # Initialize generator
        generator = AIContentGenerator()
        
        # Test email generation
        print("🔄 Generating test email...")
        import asyncio
        
        async def run_test():
            subject, body = await generator.generate_email_content(
                "leave application for next Monday to Wednesday",
                "manager@company.com"
            )
            return subject, body
        
        subject, body = asyncio.run(run_test())
        
        print("✅ Email generation successful!")
        print(f"📧 Subject: {subject}")
        print(f"📝 Body preview: {body[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Email generation failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Groq API Configuration Test")
    print("=" * 50)
    print("This script will test your Groq API setup for the")
    print("Conversational Browser Control Agent project.")
    print()
    
    # Check if .env file exists
    env_file = Path("backend/.env")
    if not env_file.exists():
        print("❌ .env file not found!")
        print("💡 Copy backend/.env.example to backend/.env")
        print("💡 Add your Groq API key to the .env file")
        return
    
    print(f"✅ Found .env file: {env_file}")
    
    # Run tests
    api_test_passed = test_groq_api()
    
    if api_test_passed:
        email_test_passed = test_email_generation()
        
        if email_test_passed:
            print("\n🎉 All tests passed!")
            print("=" * 50)
            print("✅ Your Groq API is configured correctly")
            print("✅ Email generation is working")
            print("🚀 You're ready to run the main application!")
            print()
            print("Next steps:")
            print("1. Run: cd backend && python main.py")
            print("2. Run: cd frontend && npm start")
            print("3. Open: http://localhost:3000")
        else:
            print("\n⚠️  API works but email generation failed")
            print("💡 Check the error messages above")
    else:
        print("\n❌ API test failed")
        print("💡 Fix the API configuration before proceeding")

if __name__ == "__main__":
    main()
