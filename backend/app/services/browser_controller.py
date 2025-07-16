import asyncio
import base64
import io
import os
import time
from typing import Optional, Tuple
from playwright.async_api import async_playwright, Browser, Page, BrowserContext
from PIL import Image
import logging

logger = logging.getLogger(__name__)

class BrowserController:
    """
    Core browser automation engine using Playwright.
    This is the heart of the system - controls REAL browsers, NO APIs.
    """
    
    def __init__(self):
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.screenshots_dir = "screenshots"
        os.makedirs(self.screenshots_dir, exist_ok=True)
    
    async def start_browser(self, headless: bool = False) -> bool:
        """
        Launch a real browser instance - NOT API calls
        """
        try:
            logger.info("🚀 Launching browser...")
            self.playwright = await async_playwright().start()
            
            # Launch Chromium browser with enhanced options for Windows
            launch_options = {
                'headless': headless,
                'args': [
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-extensions',
                    '--no-first-run',
                    '--disable-default-apps',
                    '--disable-web-security',
                    '--allow-running-insecure-content'
                ]
            }
            
            # Try to launch browser
            try:
                self.browser = await self.playwright.chromium.launch(**launch_options)
            except Exception as browser_error:
                logger.warning(f"Chromium launch failed: {browser_error}")
                logger.info("Trying Firefox as fallback...")
                try:
                    self.browser = await self.playwright.firefox.launch(headless=headless)
                except Exception as firefox_error:
                    logger.error(f"Firefox launch also failed: {firefox_error}")
                    logger.error("Please run: playwright install")
                    return False
            
            # Create new context
            self.context = await self.browser.new_context(
                viewport={'width': 1280, 'height': 720},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            # Create new page
            self.page = await self.context.new_page()
            
            logger.info("✅ Browser launched successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start browser: {e}")
            return False
    
    async def take_screenshot(self, description: str = "") -> Optional[str]:
        """
        Capture screenshot of current browser state
        """
        if not self.page:
            return None
            
        try:
            timestamp = int(time.time() * 1000)
            filename = f"screenshot_{timestamp}.png"
            filepath = os.path.join(self.screenshots_dir, filename)
            
            # Take full page screenshot
            await self.page.screenshot(path=filepath, full_page=True)
            
            # Convert to base64 for transmission
            with open(filepath, "rb") as image_file:
                base64_string = base64.b64encode(image_file.read()).decode('utf-8')
            
            logger.info(f"Screenshot taken: {description}")
            return base64_string
            
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            return None
    
    async def navigate_to_gmail(self) -> Tuple[bool, str]:
        """
        Navigate to Gmail.com - ACTUAL browser navigation, not API
        """
        try:
            if not self.page:
                return False, "Browser not initialized"
            
            logger.info("Navigating to Gmail...")
            await self.page.goto("https://gmail.com", wait_until="networkidle")
            await asyncio.sleep(2)  # Wait for page to stabilize
            
            return True, "Successfully navigated to Gmail"
            
        except Exception as e:
            error_msg = f"Failed to navigate to Gmail: {e}"
            logger.error(error_msg)
            return False, error_msg
    
    async def click_sign_in(self) -> Tuple[bool, str]:
        """
        Click the Sign In button - REAL UI interaction
        """
        try:
            # Multiple selectors for Gmail sign in
            selectors = [
                'a[data-action="sign in"]',
                'a[href*="accounts.google.com"]',
                'text="Sign in"',
                '.gmail-nav__nav-link--sign-in'
            ]
            
            for selector in selectors:
                try:
                    element = await self.page.wait_for_selector(selector, timeout=5000)
                    if element:
                        await element.click()
                        await asyncio.sleep(2)
                        return True, "Clicked Sign In button"
                except:
                    continue
            
            # If no standard selectors work, try finding any sign in link
            await self.page.click('text="Sign in"')
            await asyncio.sleep(2)
            return True, "Clicked Sign In button"
            
        except Exception as e:
            error_msg = f"Failed to click Sign In: {e}"
            logger.error(error_msg)
            return False, error_msg
    
    async def enter_email(self, email: str) -> Tuple[bool, str]:
        """
        Type email address in login field - REAL typing, not API
        """
        try:
            # Wait for email input field
            email_selectors = [
                'input[type="email"]',
                'input[id="identifierId"]',
                '#identifierId',
                'input[name="identifier"]'
            ]
            
            for selector in email_selectors:
                try:
                    email_input = await self.page.wait_for_selector(selector, timeout=5000)
                    if email_input:
                        await email_input.fill(email)
                        await asyncio.sleep(1)
                        return True, f"Entered email: {email}"
                except:
                    continue
            
            return False, "Could not find email input field"
            
        except Exception as e:
            error_msg = f"Failed to enter email: {e}"
            logger.error(error_msg)
            return False, error_msg
    
    async def click_next(self) -> Tuple[bool, str]:
        """
        Click Next button after email entry
        """
        try:
            next_selectors = [
                'button[id="identifierNext"]',
                '#identifierNext',
                'button:has-text("Next")',
                'input[type="submit"][value="Next"]'
            ]
            
            for selector in next_selectors:
                try:
                    next_button = await self.page.wait_for_selector(selector, timeout=5000)
                    if next_button:
                        await next_button.click()
                        await asyncio.sleep(3)  # Wait for password page
                        return True, "Clicked Next button"
                except:
                    continue
            
            return False, "Could not find Next button"
            
        except Exception as e:
            error_msg = f"Failed to click Next: {e}"
            logger.error(error_msg)
            return False, error_msg
    
    async def enter_password(self, password: str) -> Tuple[bool, str]:
        """
        Type password - REAL typing, not API
        """
        try:
            # Wait for password input field
            password_selectors = [
                'input[type="password"]',
                'input[name="password"]',
                '#password',
                'input[id="password"]'
            ]
            
            for selector in password_selectors:
                try:
                    password_input = await self.page.wait_for_selector(selector, timeout=5000)
                    if password_input:
                        await password_input.fill(password)
                        await asyncio.sleep(1)
                        return True, "Entered password"
                except:
                    continue
            
            return False, "Could not find password input field"
            
        except Exception as e:
            error_msg = f"Failed to enter password: {e}"
            logger.error(error_msg)
            return False, error_msg
    
    async def click_password_next(self) -> Tuple[bool, str]:
        """
        Click Next button after password entry
        """
        try:
            next_selectors = [
                'button[id="passwordNext"]',
                '#passwordNext',
                'button:has-text("Next")',
                'input[type="submit"]'
            ]
            
            for selector in next_selectors:
                try:
                    next_button = await self.page.wait_for_selector(selector, timeout=5000)
                    if next_button:
                        await next_button.click()
                        await asyncio.sleep(5)  # Wait for Gmail to load
                        return True, "Clicked Next button - logging in"
                except:
                    continue
            
            return False, "Could not find Next button"
            
        except Exception as e:
            error_msg = f"Failed to click password Next: {e}"
            logger.error(error_msg)
            return False, error_msg
    
    async def wait_for_gmail_inbox(self) -> Tuple[bool, str]:
        """
        Wait for Gmail inbox to load completely
        """
        try:
            # Wait for Gmail inbox elements
            inbox_selectors = [
                '[data-tooltip="Compose"]',
                '.T-I-KE',
                'div[role="button"][data-tooltip="Compose"]',
                'text="Compose"'
            ]
            
            for selector in inbox_selectors:
                try:
                    await self.page.wait_for_selector(selector, timeout=10000)
                    return True, "Gmail inbox loaded successfully"
                except:
                    continue
            
            # Check if we're in Gmail by URL
            if "mail.google.com" in self.page.url:
                return True, "Gmail loaded (detected by URL)"
            
            return False, "Gmail inbox did not load properly"
            
        except Exception as e:
            error_msg = f"Failed to wait for Gmail inbox: {e}"
            logger.error(error_msg)
            return False, error_msg
    
    async def click_compose(self) -> Tuple[bool, str]:
        """
        Click the Compose button - REAL UI interaction
        """
        try:
            compose_selectors = [
                '[data-tooltip="Compose"]',
                '.T-I-KE',
                'div[role="button"][data-tooltip="Compose"]',
                'text="Compose"'
            ]
            
            for selector in compose_selectors:
                try:
                    compose_button = await self.page.wait_for_selector(selector, timeout=5000)
                    if compose_button:
                        await compose_button.click()
                        await asyncio.sleep(2)
                        return True, "Clicked Compose button"
                except:
                    continue
            
            return False, "Could not find Compose button"
            
        except Exception as e:
            error_msg = f"Failed to click Compose: {e}"
            logger.error(error_msg)
            return False, error_msg
    
    async def fill_email_fields(self, to_email: str, subject: str, body: str) -> Tuple[bool, str]:
        """
        Fill email compose fields - REAL typing, not API
        """
        try:
            # Fill TO field
            to_selectors = [
                'input[name="to"]',
                'textarea[name="to"]',
                'div[data-name="to"] input',
                'input[aria-label*="To"]'
            ]
            
            for selector in to_selectors:
                try:
                    to_field = await self.page.wait_for_selector(selector, timeout=3000)
                    if to_field:
                        await to_field.fill(to_email)
                        await asyncio.sleep(1)
                        break
                except:
                    continue
            
            # Fill Subject field
            subject_selectors = [
                'input[name="subjectbox"]',
                'input[placeholder*="Subject"]',
                'input[aria-label*="Subject"]'
            ]
            
            for selector in subject_selectors:
                try:
                    subject_field = await self.page.wait_for_selector(selector, timeout=3000)
                    if subject_field:
                        await subject_field.fill(subject)
                        await asyncio.sleep(1)
                        break
                except:
                    continue
            
            # Fill Body field
            body_selectors = [
                'div[aria-label*="Message Body"]',
                'div[role="textbox"]',
                'div[contenteditable="true"]',
                'textarea[aria-label*="Message Body"]'
            ]
            
            for selector in body_selectors:
                try:
                    body_field = await self.page.wait_for_selector(selector, timeout=3000)
                    if body_field:
                        await body_field.fill(body)
                        await asyncio.sleep(1)
                        break
                except:
                    continue
            
            return True, "Filled email fields successfully"
            
        except Exception as e:
            error_msg = f"Failed to fill email fields: {e}"
            logger.error(error_msg)
            return False, error_msg
    
    async def send_email(self) -> Tuple[bool, str]:
        """
        Click Send button - REAL UI interaction, not API
        """
        try:
            send_selectors = [
                'div[data-tooltip="Send"]',
                'div[role="button"][aria-label*="Send"]',
                'div[data-tooltip="Send ‪(Ctrl+Enter)‬"]',
                'text="Send"'
            ]
            
            for selector in send_selectors:
                try:
                    send_button = await self.page.wait_for_selector(selector, timeout=5000)
                    if send_button:
                        await send_button.click()
                        await asyncio.sleep(3)
                        return True, "Email sent successfully!"
                except:
                    continue
            
            return False, "Could not find Send button"
            
        except Exception as e:
            error_msg = f"Failed to send email: {e}"
            logger.error(error_msg)
            return False, error_msg
    
    async def close_browser(self):
        """
        Clean up browser resources
        """
        try:
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
                
            logger.info("Browser closed successfully")
            
        except Exception as e:
            logger.error(f"Error closing browser: {e}")
    
    async def get_current_url(self) -> str:
        """Get current page URL"""
        if self.page:
            return self.page.url
        return ""
    
    async def get_page_title(self) -> str:
        """Get current page title"""
        if self.page:
            return await self.page.title()
        return ""
    
    async def cleanup(self):
        """Cleanup method - alias for close_browser"""
        await self.close_browser()
