"""
Streamlit UI for Conversational Browser Control Agent
====================================================

A modern Streamlit interface for the email automation agent.
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

# Custom CSS for ChatGPT-like styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
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
        
        # Extract email context
        if "email" in message.lower():
            # Check if credentials are provided
            if not hasattr(st.session_state, 'gmail_email') or not st.session_state.gmail_email or not hasattr(st.session_state, 'gmail_password') or not st.session_state.gmail_password:
                return {
                    "type": "error",
                    "message": "❌ **Missing Gmail Credentials**\n\nPlease enter your Gmail email and password in the sidebar to send emails."
                }
                
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
                if os.path.exists(temp_file):
                    try:
                        with open(temp_file, 'r') as f:
                            content = f.read().strip()
                            if content:
                                automation_result = json.loads(content)
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
                "message": "I can help you send emails using real browser automation. Try asking me to 'Send an email to someone@example.com about [topic]'"
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
        if 'subject' in data and 'body' in data:
            st.subheader("📧 Generated Email Details")
            col1, col2 = st.columns(2)
            
            with col1:
                st.text_input("📮 Recipient", value=data.get('recipient', ''), disabled=True)
                st.text_input("📋 Subject", value=data.get('subject', ''), disabled=True)
            
            with col2:
                if 'steps_completed' in data:
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
        
        # Gmail credentials
        st.subheader("Gmail Credentials")
        
        # Initialize session state for credentials if not exist
        if "gmail_email" not in st.session_state:
            st.session_state.gmail_email = ""
        if "gmail_password" not in st.session_state:
            st.session_state.gmail_password = ""
        
        st.session_state.gmail_email = st.text_input("Gmail Email", value=st.session_state.gmail_email)
        st.session_state.gmail_password = st.text_input("Gmail Password", value=st.session_state.gmail_password, type="password")
        
        st.markdown("""
        **Note**: If using 2FA, enter an app-specific password
        """)
        
        if not st.session_state.gmail_email or not st.session_state.gmail_password:
            st.warning("⚠️ Please enter your Gmail credentials to send emails")
        
        st.divider()
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
        - 💬 **Natural Language Interface**
        """)
        
        st.divider()
        
        # Quick actions
        st.header("⚡ Quick Actions")
        if st.button("🔄 Refresh Backend Status"):
            st.rerun()
        
        if st.button("🧪 Test Browser Setup"):
            # Test browser in sidebar
            with st.spinner("Testing browser..."):
                try:
                    import subprocess
                    result = subprocess.run(
                        ["python", "test_streamlit_browser.py"], 
                        capture_output=True, 
                        text=True,
                        timeout=30
                    )
                    if result.returncode == 0:
                        st.success("✅ Browser test passed!")
                    else:
                        st.error("❌ Browser test failed")
                        st.code(result.stderr)
                except Exception as e:
                    st.error(f"Test error: {e}")
        
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
    
    # Main chat interface
    st.header("💬 Conversation")
    
    # Display chat history
    for message in st.session_state.messages:
        display_message(message, message.get("is_user", False))
    
    # Chat input
    with st.container():
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_input = st.text_input(
                "Type your message...",
                placeholder="e.g., 'Send an email to john@company.com about tomorrow's meeting'",
                key="user_input"
            )
        
        with col2:
            send_button = st.button("Send", type="primary")
    
    # Process user input
    if send_button and user_input:
        # Add user message
        user_message = {"content": user_input, "is_user": True}
        st.session_state.messages.append(user_message)
        
        # Show real-time progress for automation
        progress_container = st.container()
        
        with progress_container:
            if "email" in user_input.lower():
                st.info("🚀 Starting email automation workflow...")
                
                # Create progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Simulate progress updates (in real implementation, this would be integrated with the automation)
                import time
                steps = [
                    "🤖 Initializing AI content generator...",
                    "📝 Generating email content...", 
                    "🌐 Launching browser...",
                    "📧 Navigating to Gmail...",
                    "📸 Capturing screenshot...",
                    "✅ Automation complete!"
                ]
                
                for i, step in enumerate(steps):
                    status_text.text(step)
                    progress_bar.progress((i + 1) / len(steps))
                    time.sleep(0.5)  # Brief delay for visual effect
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
            
            # Get response from backend
            with st.spinner("🤖 Finalizing automation..."):
                response = send_message_to_backend(user_input)
        
        # Add assistant response with data
        assistant_message = {
            "content": response.get("message", ""), 
            "is_user": False,
            "data": response.get("data", {})
        }
        st.session_state.messages.append(assistant_message)
        
        # Clear input and rerun
        st.rerun()
    
    # Example prompts
    st.header("💡 Example Prompts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📧 Send leave application email"):
            example = "Send an email to manager@company.com about leave application for tomorrow"
            st.session_state.messages.append({"content": example, "is_user": True})
            response = send_message_to_backend(example)
            st.session_state.messages.append({"content": response.get("message", ""), "is_user": False})
            st.rerun()
    
    with col2:
        if st.button("📅 Send meeting reminder"):
            example = "Send an email to team@company.com about tomorrow's project meeting at 2 PM"
            st.session_state.messages.append({"content": example, "is_user": True})
            response = send_message_to_backend(example)
            st.session_state.messages.append({"content": response.get("message", ""), "is_user": False})
            st.rerun()

if __name__ == "__main__":
    main()
