#!/usr/bin/env python3
"""
Browser Setup and Diagnostic Script
==================================

This script helps diagnose and fix browser automation issues.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and return success status"""
    print(f"\n🔄 {description}...")
    print(f"Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            return True
        else:
            print(f"❌ {description} - FAILED")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - EXCEPTION: {e}")
        return False

def main():
    print("🔧 Browser Setup and Diagnostic Tool")
    print("=" * 50)
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment detected")
    else:
        print("⚠️  Not in a virtual environment - make sure to activate your venv")
    
    # Install Playwright
    print("\n📦 Installing/Updating Playwright...")
    success1 = run_command("pip install playwright", "Playwright installation")
    
    # Install browsers
    print("\n🌐 Installing browser binaries...")
    success2 = run_command("playwright install", "Browser binaries installation")
    
    # Install Chromium specifically (most reliable)
    print("\n🔍 Installing Chromium specifically...")
    success3 = run_command("playwright install chromium", "Chromium installation")
    
    # Test browser launch
    print("\n🧪 Testing browser launch...")
    test_script = '''
import asyncio
import sys
from playwright.async_api import async_playwright

async def test_browser():
    try:
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.google.com")
        title = await page.title()
        print(f"SUCCESS: Browser test passed! Page title: {title}")
        await browser.close()
        await playwright.stop()
        return True
    except Exception as e:
        print(f"ERROR: Browser test failed: {e}")
        return False

if __name__ == "__main__":
    import asyncio
    result = asyncio.run(test_browser())
    sys.exit(0 if result else 1)
'''
    
    # Write test script
    test_file = Path("test_browser.py")
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(test_script)
    
    success4 = run_command("python test_browser.py", "Browser launch test")
    
    # Clean up
    if test_file.exists():
        test_file.unlink()
    
    # Summary
    print("\n📊 Setup Summary")
    print("=" * 50)
    results = [
        ("Playwright installation", success1),
        ("Browser binaries", success2),
        ("Chromium installation", success3),
        ("Browser launch test", success4)
    ]
    
    for task, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{task:<25} {status}")
    
    if all(success for _, success in results):
        print("\n🎉 All tests passed! Browser automation is ready.")
        print("\n🚀 Next steps:")
        print("1. Start backend: cd backend && python main.py")
        print("2. Start Streamlit: streamlit run streamlit_app.py")
    else:
        print("\n⚠️  Some tests failed. Common solutions:")
        print("1. Make sure you're in the correct virtual environment")
        print("2. Try: pip install --upgrade playwright")
        print("3. Try: playwright install --force")
        print("4. On Windows, you might need to install Visual C++ Redistributable")

if __name__ == "__main__":
    main()
