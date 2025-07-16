#!/usr/bin/env python3
"""
Standalone Email Automation Script
=================================

This script runs email automation as a separate process,
avoiding Streamlit's async conflicts.
"""

import asyncio
import sys
import json
import argparse
import re
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

# Import Gmail credentials
try:
    from gmail_config import GMAIL_EMAIL, GMAIL_PASSWORD
except ImportError:
    GMAIL_EMAIL = None
    GMAIL_PASSWORD = None
    print("Warning: Gmail credentials not configured. Please edit gmail_config.py")

# Import services
from app.services.ai_content_generator import AIContentGenerator
from app.services.browser_controller import BrowserController

async def run_email_automation(message: str, email: str = None, password: str = None, username: str = None):
    """Run the full email automation workflow"""
    try:
        from app.services.ai_content_generator import AIContentGenerator
        from app.services.browser_controller import BrowserController
        import re
        
        result = {
            "success": False,
            "message": "",
            "data": {}
        }
        
        # Extract user name from message if not provided
        if not username and "from" in message:
            name_match = re.search(r'from\s+([^,\.]+)', message)
            if name_match:
                username = name_match.group(1).strip()
                print(f"Extracted username from message: {username}")
        
        # Use provided credentials or fall back to config file
        gmail_email = email or GMAIL_EMAIL
        gmail_password = password or GMAIL_PASSWORD
        
        # Extract name from email address if username still not available
        if not username and gmail_email:
            # Try to extract a name from the email address (e.g., johndoe@gmail.com -> John Doe)
            email_name_part = gmail_email.split('@')[0]
            
            # Convert common formats to proper names
            if '.' in email_name_part:
                # Format: first.last@gmail.com -> First Last
                name_parts = email_name_part.split('.')
                name_parts = [part.capitalize() for part in name_parts if part]
                username = ' '.join(name_parts)
            else:
                # First remove numbers
                name_parts = re.sub(r'[0-9]', '', email_name_part)
                
                # Try to split by common patterns
                # First, handle underscore separation
                if '_' in name_parts:
                    name_parts = name_parts.replace('_', ' ')
                
                # Handle common Indian names that don't have separators (like ayushladdha)
                # This uses a heuristic to find potential word boundaries in names without separators
                if len(name_parts) > 6 and not ' ' in name_parts:
                    # Try to find common prefixes/suffixes in Indian names
                    common_parts = ['kumar', 'lal', 'singh', 'sharma', 'devi', 'das', 'gupta', 'raj', 'laddha']
                    for part in common_parts:
                        if part in name_parts.lower():
                            index = name_parts.lower().find(part)
                            if index > 0:  # Not at the beginning
                                name_parts = name_parts[:index] + ' ' + name_parts[index:]
                    
                    # If still no spaces and longer than 6 chars, try to insert space in the middle
                    if len(name_parts) > 6 and not ' ' in name_parts:
                        # Try to split after consonant followed by vowel (common pattern in names)
                        name_parts = re.sub(r'([bcdfghjklmnpqrstvwxyz])([aeiou])', r'\1 \2', name_parts, flags=re.IGNORECASE, count=1)
                
                # Handle camelCase (johnDoe -> John Doe)
                name_parts = re.sub(r'([a-z])([A-Z])', r'\1 \2', name_parts)
                
                # Capitalize each part
                if name_parts:
                    name_parts = ' '.join([part.capitalize() for part in name_parts.split()])
                    username = name_parts
                else:
                    username = email_name_part.capitalize()
            
            print(f"Extracted name from email address: {username}")
        
        # Extract email context
        if "email" in message.lower():
            # Extract recipient email from message
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, message)
            recipient = emails[0] if emails else "example@company.com"
            
            print("Initializing AI content generator...")
            ai_generator = AIContentGenerator()
            
            print("Generating email content...")
            
            # Check if this is a leave application
            if "leave application" in message.lower() or "leave request" in message.lower():
                # Extract leave dates
                dates_match = re.search(r'during\s+([^,\.]+)', message)
                leave_dates = dates_match.group(1).strip() if dates_match else "the requested dates"
                
                subject, body = await ai_generator.generate_leave_application(
                    leave_dates=leave_dates,
                    manager_email=recipient,
                    user_name=username
                )
                print(f"Generated leave application email for {username} during {leave_dates}")
            else:
                subject, body = await ai_generator.generate_email_content(
                    context=message, 
                    recipient=recipient, 
                    user_name=username
                )
            
            print("Starting browser...")
            browser_controller = BrowserController()
            browser_started = await browser_controller.start_browser(headless=False)
            
            if not browser_started:
                print("Browser failed to start")
                result["message"] = "Failed to start browser"
                return result
            
            print("Navigating to Gmail...")
            gmail_loaded = await browser_controller.navigate_to_gmail()
            
            if not gmail_loaded:
                print("Failed to load Gmail")
                await browser_controller.cleanup()
                result["message"] = "Failed to load Gmail"
                return result
            
            # Take a screenshot after navigation
            print("Taking screenshot after navigation...")
            navigation_screenshot = await browser_controller.take_screenshot()
            
            # Check if Gmail credentials are available
            if not gmail_email or not gmail_password:
                print("Gmail credentials not provided")
                await browser_controller.cleanup()
                result["message"] = "Gmail credentials not provided. Please provide email and password."
                return result
            
            # Login process
            print("Logging into Gmail...")
            print(f"Entering email: {gmail_email}")
            email_entered, email_msg = await browser_controller.enter_email(gmail_email)
            if not email_entered:
                print(f"Failed to enter email: {email_msg}")
                await browser_controller.cleanup()
                result["message"] = f"Failed to enter email: {email_msg}"
                return result
            
            # Click Next after email
            print("Clicking Next...")
            next_clicked, next_msg = await browser_controller.click_next()
            if not next_clicked:
                print(f"Failed to click Next: {next_msg}")
                await browser_controller.cleanup()
                result["message"] = f"Failed to click Next: {next_msg}"
                return result
            
            # Enter password
            print("Entering password...")
            password_entered, password_msg = await browser_controller.enter_password(gmail_password)
            if not password_entered:
                print(f"Failed to enter password: {password_msg}")
                await browser_controller.cleanup()
                result["message"] = f"Failed to enter password: {password_msg}"
                return result
            
            # Click Next after password
            print("Clicking password Next...")
            password_next_clicked, password_next_msg = await browser_controller.click_password_next()
            if not password_next_clicked:
                print(f"Failed to click password Next: {password_next_msg}")
                await browser_controller.cleanup()
                result["message"] = f"Failed to click password Next: {password_next_msg}"
                return result
            
            # Wait for Gmail inbox to load
            print("Waiting for Gmail inbox...")
            inbox_loaded, inbox_msg = await browser_controller.wait_for_gmail_inbox()
            if not inbox_loaded:
                print(f"Failed to load inbox: {inbox_msg}")
                await browser_controller.cleanup()
                result["message"] = f"Failed to load inbox: {inbox_msg}"
                return result
            
            # Click Compose
            print("Clicking Compose...")
            compose_clicked, compose_msg = await browser_controller.click_compose()
            if not compose_clicked:
                print(f"Failed to click Compose: {compose_msg}")
                await browser_controller.cleanup()
                result["message"] = f"Failed to click Compose: {compose_msg}"
                return result
            
            # Fill email fields
            print(f"Filling email to {recipient} with subject '{subject}'...")
            fields_filled, fields_msg = await browser_controller.fill_email_fields(recipient, subject, body)
            if not fields_filled:
                print(f"Failed to fill email fields: {fields_msg}")
                await browser_controller.cleanup()
                result["message"] = f"Failed to fill email fields: {fields_msg}"
                return result
            
            # Take screenshot before sending
            print("Taking screenshot before sending...")
            pre_send_screenshot = await browser_controller.take_screenshot()
            
            # Send email
            print("Sending email...")
            email_sent, send_msg = await browser_controller.send_email()
            if not email_sent:
                print(f"Failed to send email: {send_msg}")
                await browser_controller.cleanup()
                result["message"] = f"Failed to send email: {send_msg}"
                return result
            
            print("Email sent successfully!")
            
            # Take screenshot after sending
            print("Taking final screenshot...")
            final_screenshot = await browser_controller.take_screenshot()
            
            print("Cleaning up...")
            await browser_controller.cleanup()
            
            result["success"] = True
            result["data"] = {
                "subject": subject,
                "body": body,
                "recipient": recipient,
                "screenshots": {
                    "navigation": navigation_screenshot,
                    "pre_send": pre_send_screenshot,
                    "final": final_screenshot
                },
                "browser_started": browser_started,
                "gmail_loaded": gmail_loaded,
                "email_sent": email_sent
            }
            result["message"] = f"✓ Email sent successfully! Your leave application has been sent to {recipient}."
            
            return result
            
        else:
            result["message"] = "No email request detected"
            return result
            
    except Exception as e:
        print(f"Error: {e}")
        result["message"] = f"Error: {str(e)}"
        return result

def main():
    parser = argparse.ArgumentParser(description="Run email automation")
    parser.add_argument("message", help="The email request message")
    parser.add_argument("--output", help="Output file for results", default=None)
    parser.add_argument("--email", help="Gmail email address", default=None)
    parser.add_argument("--password", help="Gmail password", default=None)
    parser.add_argument("--username", help="User's full name for email signature", default=None)
    
    args = parser.parse_args()
    
    print("Starting Email Automation...")
    print(f"Request: {args.message}")
    
    if not args.email or not args.password:
        print("No Gmail credentials provided via command line arguments.")
        print("Will attempt to use credentials from gmail_config.py if available.")
    else:
        print(f"Using provided Gmail credentials for: {args.email}")
    
    # Run automation
    result = asyncio.run(run_email_automation(args.message, args.email, args.password, args.username))
    
    # Output results
    if args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)
    else:
        print("\nResults:")
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
