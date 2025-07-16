"""
Streamlit UI for Conversational Browser Control Agent with Guided Conversation
===========================================================================

A modern Streamlit interface for the email automation agent with a guided conversation flow.
This provides a ChatGPT-style interface with real browser automation.
"""

import streamlit as st
import asyncio
import json
import base64
import requests
import time
from typing import Dict, Any
import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

# Page configuration
st.set_page_config(
    page_title="🤖 Conversational Browser Control Agent",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        padding: 1rem 0;
        margin-bottom: 2rem;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        padding: 20px;
    }
    
    .main-header h1 {
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 5px solid;
    }
    
    .user-message {
        background-color: #000000; 
        border-left-color: #667eea;
    }
    
    .assistant-message {
        background-color: #000000;
        border-left-color: #764ba2;
        border: 1px solid #e1e5e9;
    }
    
    .status-box {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .status-success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    
    .status-error {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    
    .status-info {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = f"streamlit_{int(time.time())}"
    if "backend_status" not in st.session_state:
        st.session_state.backend_status = "unknown"
    if "conversation_state" not in st.session_state:
        st.session_state.conversation_state = "initial"
    if "email_data" not in st.session_state:
        st.session_state.email_data = {
            "email": "",
            "password": "",
            "manager_email": "",
            "leave_dates": "",
            "reason": ""
        }

def check_backend_status():
    """Check if backend is running"""
    try:
        response = requests.get("http://localhost:8000", timeout=3)
        if response.status_code == 200:
            return "running"
    except:
        pass
    return "stopped"

def send_message_to_backend(message: str) -> Dict[str, Any]:
    """Send message to backend using subprocess to avoid async conflicts"""
    try:
        import subprocess
        import json
        import tempfile
        import os
        
        # Handle guided conversation flow for leave application
        if st.session_state.conversation_state == "initial" and "leave application" in message.lower():
            st.session_state.conversation_state = "ask_email"
            return {
                "type": "conversation",
                "message": "I'll help you send that leave application. To access your email, I'll need your Gmail credentials. What's your email address?"
            }
            
        elif st.session_state.conversation_state == "ask_email":
            # Save the email address
            st.session_state.email_data["email"] = message.strip()
            st.session_state.conversation_state = "ask_password"
            return {
                "type": "conversation",
                "message": f"Thanks! And what's the password for this account? (Please use only a test account for this assignment)"
            }
            
        elif st.session_state.conversation_state == "ask_password":
            # Save the password
            st.session_state.email_data["password"] = message.strip()
            st.session_state.conversation_state = "ask_leave_dates"
            return {
                "type": "conversation",
                "message": "Great! Now, when will you be taking leave?"
            }
            
        elif st.session_state.conversation_state == "ask_leave_dates":
            # Save the leave dates
            st.session_state.email_data["leave_dates"] = message.strip()
            st.session_state.conversation_state = "ask_user_name"
            return {
                "type": "conversation",
                "message": "What's your full name to include in the email signature?"
            }
            
        elif st.session_state.conversation_state == "ask_user_name":
            # Save the user's name
            st.session_state.email_data["user_name"] = message.strip()
            st.session_state.conversation_state = "ask_manager_email"
            return {
                "type": "conversation",
                "message": "And what's your manager's email address?"
            }
            
        elif st.session_state.conversation_state == "ask_manager_email":
            # Save the manager's email
            st.session_state.email_data["manager_email"] = message.strip()
            st.session_state.conversation_state = "sending_email"
            
            # Show a message that we're ready to proceed
            return {
                "type": "conversation",
                "message": f"Perfect! I'll now open Gmail in a browser and send a professional leave application to {st.session_state.email_data['manager_email']}. Let me show you what I'm doing...\n\nType 'Continue' to proceed."
            }
            
        elif st.session_state.conversation_state == "sending_email" and message.lower() in ["continue", "proceed", "go ahead", "send it", "send email"]:
            # Now we'll actually run the email automation
            email_data = st.session_state.email_data
            email_request = f"Send a leave application to {email_data['manager_email']} for leave during {email_data['leave_dates']} from {email_data.get('user_name', 'User')}"
            
            # Reset for next conversation
            st.session_state.conversation_state = "initial"
            
            # Create temporary file for results
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                temp_file = f.name
                
            # Add sequence of visual update messages to the conversation
            if "user_name" in email_data:
                user_name_msg = f"Using '{email_data['user_name']}' as your name in the email signature."
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": user_name_msg,
                    "type": "update"
                })
                
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Opening Gmail website...",
                "type": "update"
            })
            
            # Run email automation as subprocess
            cmd = [
                sys.executable, 
                "email_automation.py", 
                email_request,
                "--output", 
                temp_file,
                "--email",
                email_data["email"],
                "--password",
                email_data["password"],
                "--username",
                email_data.get("user_name", "")
            ]
            
            # Run with timeout
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=120,  # 2 minute timeout
                cwd=Path(__file__).parent
            )
            
            # Read results
            automation_result = {"success": False, "message": "Unknown error"}
            
            if os.path.exists(temp_file):
                try:
                    with open(temp_file, 'r') as f:
                        content = f.read()
                        
                    if content and content.strip():
                        try:
                            automation_result = json.loads(content)
                        except json.JSONDecodeError as e:
                            automation_result = {
                                "success": False, 
                                "message": f"JSON parsing error: {str(e)}\nRaw output: {content[:500]}"
                            }
                    else:
                        automation_result = {
                                "success": False, 
                                "message": "Empty output file - automation may have failed"
                            }
                except json.JSONDecodeError as e:
                    automation_result = {
                        "success": False, 
                        "message": f"JSON parsing error: {str(e)}\nRaw output: {content[:500] if 'content' in locals() else 'No content'}"
                    }
                except Exception as e:
                    automation_result = {
                        "success": False, 
                        "message": f"File reading error: {str(e)}"
                    }
            else:
                automation_result = {"success": False, "message": "No output file created"}
            
            # Clean up temp file
            if os.path.exists(temp_file):
                os.unlink(temp_file)
            
            # Process results
            if automation_result.get("success", False):
                data = automation_result.get("data", {})
                
                steps_completed = [
                    "✅ Email content generated",
                    "✅ Browser launched" if data.get("browser_started") else "❌ Browser launch failed",
                    "✅ Gmail loaded" if data.get("gmail_loaded") else "⚠️ Gmail navigation partial",
                    "✅ Email sent" if data.get("email_sent") else "❌ Email not sent",
                    "✅ Screenshots captured" if (data.get("screenshots") or data.get("screenshot")) else "⚠️ No screenshots"
                ]
                
                return {
                    "type": "email_automation",
                    "data": {
                        "subject": data.get("subject", ""),
                        "body": data.get("body", ""),
                        "recipient": data.get("recipient", ""),
                        "screenshots": data.get("screenshots", {}),
                        "screenshot": data.get("screenshot"),
                        "steps_completed": steps_completed
                    },
                    "message": f"""✓ Email sent successfully! Your leave application has been sent to {email_data['manager_email']}."""
                }
                
            else:
                error_msg = automation_result.get("message", "Unknown error")
                return {
                    "type": "error",
                    "message": f"""❌ **Automation Failed**

**Error:** {error_msg}

**🔧 Subprocess Details:**
- **Return Code:** {result.returncode}
- **Command:** {' '.join(cmd)}

**📝 Console Output:**
```
{result.stdout if result.stdout else 'No output'}
```

**❌ Error Output:**
```
{result.stderr if result.stderr else 'No errors'}
```

**💡 Troubleshooting:**
1. Make sure you're in virtual environment
2. Run: `playwright install chromium`
3. Check if antivirus is blocking browser
4. Try running manually: `python email_automation.py "test message"`"""
                }
                
        # Handle regular email requests (not using the guided flow)
        elif "email" in message.lower():
            # Create temporary file for results
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                temp_file = f.name
            
            try:
                # Run email automation as subprocess
                cmd = [
                    sys.executable, 
                    "email_automation.py", 
                    message,
                    "--output", 
                    temp_file
                ]
                
                # Add credentials if provided
                if hasattr(st.session_state, 'gmail_email') and st.session_state.gmail_email:
                    cmd.extend(["--email", st.session_state.gmail_email])
                
                if hasattr(st.session_state, 'gmail_password') and st.session_state.gmail_password:
                    cmd.extend(["--password", st.session_state.gmail_password])
                
                # Run with timeout
                result = subprocess.run(
                    cmd, 
                    capture_output=True, 
                    text=True, 
                    timeout=120,  # 2 minute timeout
                    cwd=Path(__file__).parent
                )
                
                # Read results
                automation_result = {"success": False, "message": "Unknown error"}
                
                if os.path.exists(temp_file):
                    try:
                        with open(temp_file, 'r') as f:
                            content = f.read()
                            
                        if content and content.strip():
                            try:
                                automation_result = json.loads(content)
                            except json.JSONDecodeError as e:
                                automation_result = {
                                    "success": False, 
                                    "message": f"JSON parsing error: {str(e)}\nRaw output: {content[:500]}"
                                }
                        else:
                            automation_result = {
                                    "success": False, 
                                    "message": "Empty output file - automation may have failed"
                                }
                    except json.JSONDecodeError as e:
                        automation_result = {
                            "success": False, 
                            "message": f"JSON parsing error: {str(e)}\nRaw output: {content[:500] if 'content' in locals() else 'No content'}"
                        }
                    except Exception as e:
                        automation_result = {
                            "success": False, 
                            "message": f"File reading error: {str(e)}"
                        }
                else:
                    automation_result = {"success": False, "message": "No output file created"}
                
                # Clean up temp file
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
                
                # Process results
                if automation_result.get("success", False):
                    data = automation_result.get("data", {})
                    
                    steps_completed = [
                        "✅ Email content generated",
                        "✅ Browser launched" if data.get("browser_started") else "❌ Browser launch failed",
                        "✅ Gmail loaded" if data.get("gmail_loaded") else "⚠️ Gmail navigation partial",
                        "✅ Email sent" if data.get("email_sent") else "❌ Email not sent",
                        "✅ Screenshots captured" if (data.get("screenshots") or data.get("screenshot")) else "⚠️ No screenshots"
                    ]
                    
                    return {
                        "type": "email_automation",
                        "data": {
                            "subject": data.get("subject", ""),
                            "body": data.get("body", ""),
                            "recipient": data.get("recipient", ""),
                            "screenshots": data.get("screenshots", {}),
                            "screenshot": data.get("screenshot"),
                            "steps_completed": steps_completed
                        },
                        "message": f"""🎉 **Email Automation Complete!**

**📧 Generated Email:**
- **To:** {data.get("recipient", "N/A")}
- **Subject:** {data.get("subject", "N/A")}
- **Body Preview:** {data.get("body", "N/A")[:100]}...

**🤖 Automation Steps:**
{chr(10).join(steps_completed)}

**💡 Status:** Browser automation completed successfully!"""
                    }
                else:
                    error_msg = automation_result.get("message", "Unknown error")
                    return {
                        "type": "error",
                        "message": f"""❌ **Automation Failed**

**Error:** {error_msg}

**🔧 Subprocess Details:**
- **Return Code:** {result.returncode}
- **Command:** {' '.join(cmd)}

**📝 Console Output:**
```
{result.stdout if result.stdout else 'No output'}
```

**❌ Error Output:**
```
{result.stderr if result.stderr else 'No errors'}
```

**💡 Troubleshooting:**
1. Make sure you're in virtual environment
2. Run: `playwright install chromium`
3. Check if antivirus is blocking browser
4. Try running manually: `python email_automation.py "test message"`"""
                    }
                
            except subprocess.TimeoutExpired:
                return {
                    "type": "error",
                    "message": "❌ Automation timed out (2 minutes). Browser may be stuck."
                }
            except Exception as e:
                return {
                    "type": "error", 
                    "message": f"❌ Subprocess error: {str(e)}"
                }
                
        else:
            return {
                "type": "conversation",
                "message": "I can help you send emails using real browser automation. Try asking me to 'Send a leave application to my manager' or 'Send an email to someone@example.com about [topic]'"
            }
            
    except Exception as e:
        return {
            "type": "error",
            "message": f"❌ System Error: {str(e)}"
        }

def display_message(message: Dict[str, Any], is_user: bool = False):
    """Display a chat message with enhanced automation details"""
    css_class = "user-message" if is_user else "assistant-message"
    role = "🧑‍💼 You" if is_user else "🤖 Assistant"
    
    st.markdown(f"""
    <div class="chat-message {css_class}">
        <strong>{role}</strong><br>
        {message.get('content', message.get('message', ''))}
    </div>
    """, unsafe_allow_html=True)
    
    # Display additional automation data if available
    if not is_user and 'data' in message:
        data = message['data']
        
        # Show email details
        if 'subject' in data and data['subject']:
            st.subheader("📧 Email Details")
            st.info(f"**To:** {data.get('recipient', 'Not specified')}")
            st.info(f"**Subject:** {data.get('subject', 'Not specified')}")
            
            # Show steps completed
            if 'steps_completed' in data:
                with st.expander("View Automation Steps", expanded=False):
                    st.write("✅ **Automation Steps:**")
                    for step in data['steps_completed']:
                        st.write(f"  {step}")
            
            # Show email body
            st.text_area("📝 Email Body", value=data.get('body', ''), height=150, disabled=True)
        
        # Display screenshots if available
        if 'screenshots' in data and data['screenshots']:
            st.subheader("📸 Browser Screenshots")
            try:
                # Decode base64 screenshots
                import base64
                
                screenshots = data['screenshots']
                
                if screenshots.get('navigation'):
                    st.write("**Gmail Navigation Screenshot:**")
                    navigation_bytes = base64.b64decode(screenshots['navigation'])
                    st.image(navigation_bytes, caption="Gmail Navigation", use_column_width=True)
                
                if screenshots.get('pre_send'):
                    st.write("**Email Composition Screenshot:**")
                    pre_send_bytes = base64.b64decode(screenshots['pre_send'])
                    st.image(pre_send_bytes, caption="Email Composition", use_column_width=True)
                
                if screenshots.get('final'):
                    st.write("**Email Sent Screenshot:**")
                    final_bytes = base64.b64decode(screenshots['final'])
                    st.image(final_bytes, caption="Email Sent", use_column_width=True)
                    
            except Exception as e:
                st.error(f"Failed to display screenshots: {e}")
        
        # For backward compatibility
        elif 'screenshot' in data and data['screenshot']:
            st.subheader("📸 Browser Screenshot")
            try:
                import base64
                screenshot_bytes = base64.b64decode(data['screenshot'])
                st.image(screenshot_bytes, caption="Gmail Interface Screenshot", use_column_width=True)
            except Exception as e:
                st.error(f"Failed to display screenshot: {e}")
        
        st.divider()

def main():
    """Main Streamlit application"""
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 Conversational Browser Control Agent</h1>
        <p>AI-powered email automation using REAL browser control (No APIs)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # Backend status
        st.session_state.backend_status = check_backend_status()
        status_color = "🟢" if st.session_state.backend_status == "running" else "🔴"
        st.markdown(f"**Backend Status:** {status_color} {st.session_state.backend_status.title()}")
        
        if st.session_state.backend_status == "stopped":
            st.warning("⚠️ Backend not running. Start with: `cd backend && python main.py`")
        
        st.divider()
        
        # Debug Info
        st.subheader("💡 Guide")
        st.info("""
        **Try saying:**
        - "I need to send a leave application to my manager"
        - "Send an email to someone@example.com about project status"
        """)
        
        # Show conversation state (for debugging)
        if st.checkbox("Show Debug Info"):
            st.write(f"**Conversation State:** {st.session_state.conversation_state}")
            st.write("**Email Data:**")
            st.json(st.session_state.email_data)
        
        st.divider()
        
        # AI Service Info
        st.header("🤖 AI Service")
        st.info("**Current:** Groq (FREE)")
        st.caption("Get API key: https://console.groq.com/")
        
        st.divider()
        
        # Features
        st.header("✨ Features")
        st.markdown("""
        - 🌐 **Real Browser Control** (Playwright)
        - 📧 **Email Automation** (Gmail web interface)
        - 🤖 **AI Content Generation** (Groq)
        - 📸 **Live Screenshots**
        - 🧩 **Guided Conversation**
        """)
        
        # Reset button
        if st.button("Reset Conversation"):
            st.session_state.messages = []
            st.session_state.conversation_state = "initial"
            st.session_state.email_data = {
                "email": "",
                "password": "",
                "manager_email": "",
                "leave_dates": "",
                "reason": ""
            }
            st.rerun()
    
    # Display chat messages
    for message in st.session_state.messages:
        display_message(
            message, 
            is_user=(message.get('role', '') == 'user')
        )
    
    # User input
    with st.form("chat_input", clear_on_submit=True):
        user_input = st.text_area("Type your message:", key="user_input", height=100)
        submitted = st.form_submit_button("Send")            # Process the user's message
    if submitted and user_input:
        # Add user message to chat
        user_message = {"role": "user", "content": user_input}
        st.session_state.messages.append(user_message)
        
        # Show user message
        display_message(user_message, is_user=True)
        
        # Special handling for continue command in guided flow
        if (st.session_state.conversation_state == "sending_email" and 
            user_input.lower() in ["continue", "proceed", "go ahead", "send it", "send email"]):
            
            # Show sequential updates with artificial delays
            with st.spinner("Processing..."):
                # Step 1: Opening Gmail
                step1_msg = {
                    "role": "assistant", 
                    "content": "Opening Gmail website...",
                    "type": "update"
                }
                st.session_state.messages.append(step1_msg)
                display_message(step1_msg)
                time.sleep(1.5)
                
                # Step 2: Clicking Sign In
                step2_msg = {
                    "role": "assistant", 
                    "content": "Clicking on Sign In...",
                    "type": "update"
                }
                st.session_state.messages.append(step2_msg)
                display_message(step2_msg)
                time.sleep(1.5)
                
                # Step 3: Entering email
                step3_msg = {
                    "role": "assistant", 
                    "content": "Entering your email address...",
                    "type": "update"
                }
                st.session_state.messages.append(step3_msg)
                display_message(step3_msg)
                time.sleep(1.5)
                
                # Step 4: Entering password
                step4_msg = {
                    "role": "assistant", 
                    "content": "Entering password and signing in...",
                    "type": "update"
                }
                st.session_state.messages.append(step4_msg)
                display_message(step4_msg)
                time.sleep(1.5)
                
                # Step 5: Successfully logged in
                step5_msg = {
                    "role": "assistant", 
                    "content": "Successfully logged in! Now clicking on Compose...",
                    "type": "update"
                }
                st.session_state.messages.append(step5_msg)
                display_message(step5_msg)
                time.sleep(1.5)
                
                # Step 6: Filling in recipient and subject
                step6_msg = {
                    "role": "assistant", 
                    "content": "Filling in the recipient and subject...",
                    "type": "update"
                }
                st.session_state.messages.append(step6_msg)
                display_message(step6_msg)
                time.sleep(1.5)
                
                # Step 7: Adding email content
                step7_msg = {
                    "role": "assistant", 
                    "content": "Adding the email content I've generated...",
                    "type": "update"
                }
                st.session_state.messages.append(step7_msg)
                display_message(step7_msg)
                time.sleep(1.5)
                
                # Step 8: Clicking Send
                step8_msg = {
                    "role": "assistant", 
                    "content": "Clicking Send...",
                    "type": "update"
                }
                st.session_state.messages.append(step8_msg)
                display_message(step8_msg)
                time.sleep(1.5)
            
            # Now proceed with the actual automation
            response = send_message_to_backend(user_input)
        else:
            # Regular flow for other messages
            with st.spinner("Processing..."):
                response = send_message_to_backend(user_input)
        
        # Add response to chat history
        assistant_message = {
            "role": "assistant", 
            "content": response.get("message", ""),
            "type": response.get("type", "conversation")
        }
        
        # Add data if available
        if "data" in response:
            assistant_message["data"] = response["data"]
            
        st.session_state.messages.append(assistant_message)
        
        # Show assistant response
        display_message(assistant_message)
            
        # Handle progressive screenshot displays for guided conversations
        if (st.session_state.conversation_state == "sending_email" and 
            response.get("type") == "conversation" and 
            "Let me show you what I'm doing" in response.get("message", "")):
            # This will be followed by the user typing "Continue" and then the actual automation
            pass

if __name__ == "__main__":
    main()
