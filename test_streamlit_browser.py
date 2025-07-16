#!/usr/bin/env python3
"""
Simple Browser Test for Streamlit Integration
============================================
"""

import asyncio
import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

async def test_browser_simple():
    """Simple browser test"""
    try:
        from playwright.async_api import async_playwright
        
        print("🔄 Starting Playwright...")
        playwright = await async_playwright().start()
        
        print("🌐 Launching browser...")
        browser = await playwright.chromium.launch(headless=True)
        
        print("📄 Creating page...")
        page = await browser.new_page()
        
        print("🔗 Navigating to Google...")
        await page.goto("https://www.google.com", timeout=10000)
        
        print("📋 Getting page title...")
        title = await page.title()
        
        print(f"✅ SUCCESS: {title}")
        
        await browser.close()
        await playwright.stop()
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_imports():
    """Test if all imports work"""
    try:
        print("🔄 Testing imports...")
        
        # Test Playwright
        from playwright.async_api import async_playwright
        print("✅ Playwright import OK")
        
        # Test backend services
        from app.services.ai_content_generator import AIContentGenerator
        print("✅ AI Content Generator import OK")
        
        from app.services.browser_controller import BrowserController
        print("✅ Browser Controller import OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    print("🧪 Browser Diagnostic Test")
    print("=" * 40)
    
    # Test imports first
    if not test_imports():
        print("\n💡 Fix import issues first:")
        print("1. pip install playwright")
        print("2. playwright install")
        return
    
    # Test browser
    print(f"\n🌐 Testing browser automation...")
    result = asyncio.run(test_browser_simple())
    
    if result:
        print("\n🎉 Browser test passed!")
        print("✅ Browser automation should work in Streamlit")
    else:
        print("\n❌ Browser test failed!")
        print("💡 Try these steps:")
        print("1. playwright install chromium")
        print("2. Check antivirus/firewall settings")
        print("3. Try running as administrator")

if __name__ == "__main__":
    main()
