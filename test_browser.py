import asyncio
import sys
from playwright.async_api import async_playwright

async def test_browser():
    try:
        print("Starting browser test...")
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
    result = asyncio.run(test_browser())
    sys.exit(0 if result else 1)
