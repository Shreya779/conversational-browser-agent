import asyncio
import logging
import time
import uuid
from typing import AsyncGenerator, Dict, Any
from ..models import ConversationContext, BrowserAction, Message, MessageType
from .browser_controller import BrowserController
from .conversation_manager import ConversationManager

logger = logging.getLogger(__name__)

class EmailAutomationService:
    """
    Main orchestration service that combines browser automation with conversation management
    """
    
    def __init__(self):
        self.conversation_manager = ConversationManager()
        self.active_sessions: Dict[str, BrowserController] = {}
    
    async def start_email_automation(self, session_id: str) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Start the complete email automation process with real-time updates
        
        This is the core function that demonstrates REAL browser automation,
        NOT API usage. Every step is performed through actual browser interactions.
        """
        
        context = self.conversation_manager.get_context(session_id)
        if not context or not context.credentials or not context.email_data:
            yield {
                "type": "error",
                "message": "Missing required information for email automation"
            }
            return
        
        # Initialize browser controller
        browser = BrowserController()
        self.active_sessions[session_id] = browser
        
        try:
            # Step 1: Launch Browser
            yield {
                "type": "status",
                "message": "🚀 Launching browser..."
            }
            
            success = await browser.start_browser(headless=False)  # Visible browser for demo
            if not success:
                yield {
                    "type": "error", 
                    "message": "Failed to launch browser"
                }
                return
            
            # Step 2: Navigate to Gmail
            yield {
                "type": "status",
                "message": "🌐 Navigating to Gmail..."
            }
            
            success, msg = await browser.navigate_to_gmail()
            screenshot = await browser.take_screenshot("Gmail homepage")
            
            yield {
                "type": "action",
                "action": "navigate_to_gmail",
                "message": msg,
                "success": success,
                "screenshot": screenshot
            }
            
            if not success:
                return
            
            await asyncio.sleep(2)
            
            # Step 3: Click Sign In
            yield {
                "type": "status",
                "message": "🔐 Looking for Sign In button..."
            }
            
            success, msg = await browser.click_sign_in()
            screenshot = await browser.take_screenshot("After clicking Sign In")
            
            yield {
                "type": "action",
                "action": "click_sign_in",
                "message": msg,
                "success": success,
                "screenshot": screenshot
            }
            
            if not success:
                return
            
            await asyncio.sleep(2)
            
            # Step 4: Enter Email
            yield {
                "type": "status",
                "message": f"✉️ Entering email address: {context.credentials.email}"
            }
            
            success, msg = await browser.enter_email(context.credentials.email)
            screenshot = await browser.take_screenshot("Email entered")
            
            yield {
                "type": "action",
                "action": "enter_email",
                "message": msg,
                "success": success,
                "screenshot": screenshot
            }
            
            if not success:
                return
            
            # Step 5: Click Next (after email)
            yield {
                "type": "status",
                "message": "➡️ Clicking Next..."
            }
            
            success, msg = await browser.click_next()
            screenshot = await browser.take_screenshot("After clicking Next")
            
            yield {
                "type": "action",
                "action": "click_next_email",
                "message": msg,
                "success": success,
                "screenshot": screenshot
            }
            
            if not success:
                return
            
            await asyncio.sleep(3)
            
            # Step 6: Enter Password
            yield {
                "type": "status",
                "message": "🔑 Entering password..."
            }
            
            success, msg = await browser.enter_password(context.credentials.password)
            screenshot = await browser.take_screenshot("Password entered")
            
            yield {
                "type": "action",
                "action": "enter_password",
                "message": msg,
                "success": success,
                "screenshot": screenshot
            }
            
            if not success:
                return
            
            # Step 7: Click Next (after password)
            yield {
                "type": "status",
                "message": "🔓 Logging in..."
            }
            
            success, msg = await browser.click_password_next()
            screenshot = await browser.take_screenshot("Logging in")
            
            yield {
                "type": "action",
                "action": "click_next_password",
                "message": msg,
                "success": success,
                "screenshot": screenshot
            }
            
            if not success:
                return
            
            # Step 8: Wait for Gmail Inbox
            yield {
                "type": "status",
                "message": "📥 Waiting for Gmail inbox to load..."
            }
            
            success, msg = await browser.wait_for_gmail_inbox()
            screenshot = await browser.take_screenshot("Gmail inbox loaded")
            
            yield {
                "type": "action",
                "action": "wait_inbox",
                "message": msg,
                "success": success,
                "screenshot": screenshot
            }
            
            if not success:
                return
            
            await asyncio.sleep(2)
            
            # Step 9: Click Compose
            yield {
                "type": "status",
                "message": "✍️ Clicking Compose button..."
            }
            
            success, msg = await browser.click_compose()
            screenshot = await browser.take_screenshot("Compose window opened")
            
            yield {
                "type": "action",
                "action": "click_compose",
                "message": msg,
                "success": success,
                "screenshot": screenshot
            }
            
            if not success:
                return
            
            await asyncio.sleep(2)
            
            # Step 10: Fill Email Fields
            yield {
                "type": "status",
                "message": f"📝 Filling email fields - To: {context.email_data.to_email}"
            }
            
            success, msg = await browser.fill_email_fields(
                context.email_data.to_email,
                context.email_data.subject,
                context.email_data.body
            )
            screenshot = await browser.take_screenshot("Email fields filled")
            
            yield {
                "type": "action",
                "action": "fill_email_fields",
                "message": msg,
                "success": success,
                "screenshot": screenshot,
                "email_data": {
                    "to": context.email_data.to_email,
                    "subject": context.email_data.subject,
                    "body": context.email_data.body[:100] + "..." if len(context.email_data.body) > 100 else context.email_data.body
                }
            }
            
            if not success:
                return
            
            await asyncio.sleep(2)
            
            # Step 11: Send Email
            yield {
                "type": "status",
                "message": "🚀 Sending email..."
            }
            
            success, msg = await browser.send_email()
            screenshot = await browser.take_screenshot("Email sent confirmation")
            
            yield {
                "type": "action",
                "action": "send_email",
                "message": msg,
                "success": success,
                "screenshot": screenshot
            }
            
            if success:
                yield {
                    "type": "completion",
                    "message": f"✅ Email sent successfully! Your email has been delivered to {context.email_data.to_email}",
                    "screenshot": screenshot
                }
                
                # Add completion message to conversation
                completion_msg = Message(
                    id=str(uuid.uuid4()),
                    type=MessageType.AGENT,
                    content=f"✅ Email sent successfully! Your email has been delivered to {context.email_data.to_email}",
                    timestamp=time.time()
                )
                self.conversation_manager.add_message(session_id, completion_msg)
            
        except Exception as e:
            logger.error(f"Email automation error: {e}")
            error_screenshot = await browser.take_screenshot("Error state")
            yield {
                "type": "error",
                "message": f"An error occurred during automation: {str(e)}",
                "screenshot": error_screenshot
            }
        
        finally:
            # Clean up browser
            await asyncio.sleep(3)  # Let user see final state
            await browser.close_browser()
            if session_id in self.active_sessions:
                del self.active_sessions[session_id]
    
    async def process_message(self, session_id: str, message: str):
        """Process a user message and return appropriate response"""
        return await self.conversation_manager.process_user_message(session_id, message)
    
    def get_conversation_history(self, session_id: str):
        """Get conversation history for a session"""
        return self.conversation_manager.get_conversation_history(session_id)
    
    async def stop_automation(self, session_id: str):
        """Stop automation for a specific session"""
        if session_id in self.active_sessions:
            browser = self.active_sessions[session_id]
            await browser.close_browser()
            del self.active_sessions[session_id]
