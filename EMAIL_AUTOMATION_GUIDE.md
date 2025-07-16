# Email Automation Browser Agent

This system demonstrates browser automation through real browser control (Playwright) to send emails via Gmail's web interface.

## Setup Instructions

1. **Create a virtual environment**:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```
   pip install -r requirements_streamlit.txt
   pip install playwright
   playwright install chromium
   ```

3. **Configure Gmail credentials**:
   Edit `gmail_config.py` and add your Gmail credentials:
   ```python
   GMAIL_EMAIL = "your.email@gmail.com"  # Your Gmail address
   GMAIL_PASSWORD = "your-password"      # Your Gmail password
   ```
   
   **Note**: If you have 2FA enabled on your account, you need to create an App Password:
   1. Go to your Google Account > Security
   2. Under "Signing in to Google," select "App Passwords"
   3. Generate a new app password for "Mail" and use it instead of your regular password

4. **Run the application**:
   ```
   streamlit run streamlit_app.py
   ```

## Testing the Email Automation

1. Use natural language to instruct the agent to send an email:
   - "Send an email to someone@example.com about meeting tomorrow"
   - "Email john@example.com about project status update"
   - "Send Jane a quick email about the budget approval"

2. The agent will:
   - Generate appropriate email content using AI
   - Launch a real browser
   - Navigate to Gmail
   - Log in with your credentials
   - Compose and send the email
   - Capture screenshots of the process

## Troubleshooting

- **Browser doesn't launch**: Make sure Playwright is installed correctly: `playwright install chromium`
- **Login fails**: Check your credentials in `gmail_config.py`
- **Antivirus blocking**: Some antivirus software may block browser automation
- **2FA Issues**: If using 2FA, you must create an App Password as mentioned above
- **Unicode errors**: If you see errors about Unicode characters, the emoji characters were removed in the latest update

## Architecture

- **Streamlit**: Frontend UI with chat interface
- **Playwright**: Real browser automation 
- **Groq API**: AI-generated email content
- **Subprocess**: Isolation to avoid async conflicts

All code runs locally on your machine - no servers required!
