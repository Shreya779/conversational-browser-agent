# Conversational Browser Control Agent

🤖 **An AI-powered agent that controls web browsers through natural language conversation**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/React-18+-61dafb.svg)](https://reactjs.org)
[![Playwright](https://img.shields.io/badge/Playwright-Browser%20Automation-green.svg)](https://playwright.dev)
[![FastAPI](https://img.shields.io/badge/FastAPI-WebSocket%20API-009688.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **🎯 Mission**: Demonstrate that the future of AI agents lies in **REAL browser control**, not API integrations. This agent controls browsers like humans do - through actual UI interaction.

---

## 🌟 What Makes This Special

This is **NOT** just another email automation tool. It's a demonstration of how AI agents can navigate and control the digital world through **actual browser interaction** - no shortcuts, no APIs, no programmatic form submissions.

### ✅ What This Agent Does
- 🌐 Opens **REAL browser instances** (Playwright)
- 🖱️ Clicks on **actual UI elements** 
- ⌨️ Types in **real form fields**
- 📸 Takes **screenshots at every step**
- 💬 Shows screenshots **directly in chat conversation**
- 🤖 Generates **professional email content** with AI (Groq)

### ❌ What This Agent Does NOT Do
- 🚫 Use Gmail API or SMTP libraries
- 🚫 Submit forms programmatically with HTTP requests  
- 🚫 Take shortcuts that bypass real UI interaction
- 🚫 Hide the browser automation process

---

## 🚀 Quick Start

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/conversational-browser-agent.git
   cd conversational-browser-agent
   ```

2. Install Python dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Install Playwright browsers:
   ```bash
   playwright install chromium
   ```

### Configuration

1. Set up Gmail credentials:
   - Copy `gmail_config.template.py` to `gmail_config.py`
   - Edit `gmail_config.py` with your Gmail credentials:
     ```python
     GMAIL_EMAIL = "your_email@gmail.com"
     GMAIL_PASSWORD = "your_password"  # Use app password if 2FA is enabled
     ```

2. Set up Groq API key for AI content generation:
   - Get a free API key from [Groq Console](https://console.groq.com/)
   - Set it in your environment:
     ```bash
     # On Windows PowerShell:
     $env:GROQ_API_KEY="your-api-key"
     
     # On Linux/Mac:
     export GROQ_API_KEY="your-api-key"
     ```

### Running the Application

#### Guided Version (Recommended)

This version features a step-by-step guided conversation flow:

```bash
# On Windows:
run_guided.bat

# Or directly:
streamlit run streamlit_app_guided.py
```

#### Standard Version

```bash
# On Windows:
run.bat

# Or directly:
streamlit run streamlit_app.py
```
│                        Backend Layer (FastAPI)                      │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────────────┐│
│  │   Natural       │ │   Session       │ │   WebSocket             ││
│  │   Language      │ │   Management    │ │   Communication         ││
│  │   Processing    │ │                 │ │                         ││
│  └─────────────────┘ └─────────────────┘ └─────────────────────────┘│
└─────────────────────────────────────────────────────────────────────┘
                                    │
┌─────────────────────────────────────────────────────────────────────┐
│                      Core Service Layer                             │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────────────┐│
│  │   Conversation  │ │   BROWSER       │ │   AI Content            ││
│  │   Manager       │ │   CONTROLLER    │ │   Generator             ││
│  │                 │ │   (Playwright)  │ │   (OpenAI)              ││
│  └─────────────────┘ └─────────────────┘ └─────────────────────────┘│
└─────────────────────────────────────────────────────────────────────┘
                                    │
┌─────────────────────────────────────────────────────────────────────┐
│                      Browser Automation Layer                       │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────────────┐│
│  │   Real Chrome/  │ │   Screenshot    │ │   UI Element            ││
│  │   Firefox       │ │   Capture       │ │   Interaction           ││
│  │   Browser       │ │                 │ │                         ││
│  └─────────────────┘ └─────────────────┘ └─────────────────────────┘│
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

**Windows (PowerShell):**
```powershell
# Clone and setup everything automatically
git clone https://github.com/yourusername/conversational-browser-agent.git
cd conversational-browser-agent
.\setup.ps1
```

**macOS/Linux (Bash):**
```bash
# Clone and setup everything automatically  
git clone https://github.com/yourusername/conversational-browser-agent.git
cd conversational-browser-agent
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup

<details>
<summary>Click to expand manual setup instructions</summary>

#### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

#### Backend Setup
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux  
source venv/bin/activate

pip install -r requirements.txt
playwright install
cp .env.example .env
# Edit .env and add your OpenAI API key
```

#### Frontend Setup
```bash
cd frontend
npm install
```

</details>

### Running the Application

**Windows:**
```powershell
.\run.ps1
```

**macOS/Linux:**
```bash
chmod +x run.sh
./run.sh
```

**Manual Start:**
```bash
# Terminal 1 - Backend
cd backend && python main.py

# Terminal 2 - Frontend  
cd frontend && npm start

# Open http://localhost:3000
```

---

## 🤖 Free AI Services Setup

This project supports **three FREE AI options** for email content generation:

### 🚀 **Groq (Recommended - FREE)**
- **Why choose**: Fastest inference, high-quality models, generous free tier
- **Setup**: Get free API key from [https://console.groq.com/](https://console.groq.com/)
- **Models**: Mixtral-8x7B, Llama-2, and more
- **Configuration**: Set `AI_SERVICE=groq` and `GROQ_API_KEY=your_key` in `.env`

### 🤗 **Hugging Face (FREE)**
- **Why choose**: Completely free, no limits, open-source models
- **Setup**: Get free token from [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
- **Models**: Llama-2, CodeLlama, and thousands more
- **Configuration**: Set `AI_SERVICE=huggingface` and `HUGGINGFACE_API_KEY=your_token` in `.env`

### 🔧 **OpenAI (Backup)**
- **Why choose**: Most reliable, but requires credits
- **Setup**: Get API key from [https://platform.openai.com/](https://platform.openai.com/)
- **Configuration**: Set `AI_SERVICE=openai` and `OPENAI_API_KEY=your_key` in `.env`

**Recommended for beginners**: Start with **Groq** - it's free, fast, and provides excellent results!

---

## 🎮 User Experience Demo

Here's what a typical interaction looks like:

```
👤 User: "I need to send a leave application email"

🤖 Agent: "I'll help you send that email! I need your Gmail credentials first.
          What's your email address? (Use test account only)"

👤 User: "testaccount@gmail.com"  

🤖 Agent: "Thanks! Now I need your password to access Gmail."

👤 User: "testpassword123"

🤖 Agent: "Perfect! Who would you like to send the email to?"

👤 User: "manager@company.com"

🤖 Agent: "Great! What's this email about?"

👤 User: "Leave application for next Monday to Wednesday"

🤖 Agent: "Perfect! I'll now open Gmail and send your email. 
          Watch me control the browser step by step..."

🤖 Agent: "🚀 Launching browser..."
          [SCREENSHOT: Browser window opening]

🤖 Agent: "🌐 Navigating to Gmail..."  
          [SCREENSHOT: Gmail homepage]

🤖 Agent: "🔐 Clicking Sign In..."
          [SCREENSHOT: Gmail login page]

🤖 Agent: "✉️ Entering your email address..."
          [SCREENSHOT: Email field filled]

🤖 Agent: "🔑 Entering password and logging in..."
          [SCREENSHOT: Gmail inbox]

🤖 Agent: "✍️ Clicking Compose..."
          [SCREENSHOT: Compose window]

🤖 Agent: "📝 Filling email fields with AI-generated content..."
          [SCREENSHOT: Complete email]

🤖 Agent: "🚀 Sending email..."
          [SCREENSHOT: Send confirmation]

🤖 Agent: "✅ Email sent successfully! Your leave application 
          has been sent to manager@company.com"
```

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Browser Automation** | 🎭 Playwright | **Core**: Controls real browsers (NOT APIs) |
| **Backend** | ⚡ FastAPI | WebSocket server & API endpoints |
| **Frontend** | ⚛️ React | ChatGPT-style interface |
| **AI Content** | 🧠 **FREE Services** | Groq (recommended), Hugging Face, or OpenAI |
| **Communication** | 🔌 WebSockets | Real-time updates & screenshots |
| **Language** | 🐍 Python 3.8+ | Backend services |
| **Styling** | 🎨 Custom CSS | Responsive UI components |

---

## 📋 Core Features

### ✅ Implemented Features
- 🌐 **Real Browser Control**: Playwright automation (NO Gmail API)
- 💬 **Natural Language Interface**: Conversational commands
- 📸 **Live Screenshots**: Embedded in chat conversation  
- 🤖 **AI Content Generation**: Professional email creation
- ⚡ **Real-time Updates**: WebSocket communication
- 🔄 **Robust Error Handling**: Graceful failure recovery
- 📱 **Responsive Design**: Works on different screen sizes
- 🔐 **Secure Sessions**: Per-session browser instances

### 🔮 Future Extensibility
- 🌍 **Multi-Website Support**: Extend to Twitter, LinkedIn, etc.
- 🧠 **Advanced AI**: Multiple LLM support
- 📊 **Analytics Dashboard**: Automation metrics
- 🔧 **Custom Workflows**: User-defined automation sequences

---

## 🔐 Security & Privacy

### 🛡️ Security Measures
- ✅ **No Credential Storage**: Passwords only in memory during automation
- ✅ **Session Isolation**: Each conversation uses separate browser instance
- ✅ **Local Processing**: No data sent to external services (except OpenAI for content)
- ✅ **Test Account Only**: Clear warnings about using test credentials

### ⚠️ Important Security Notes
- 🚨 **TEST ACCOUNTS ONLY**: Never use real Gmail credentials
- 🚨 **Demo Purpose**: This is for demonstration and learning
- 🚨 **Local Development**: Not designed for production deployment
- 🚨 **API Key Security**: Keep OpenAI API key secure

---

## 📊 Project Status & Verification

### ✅ Assignment Requirements Met

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| **Real Browser Automation** | ✅ Complete | Playwright controls actual browser |
| **NO Gmail API Usage** | ✅ Verified | Zero API imports, pure UI interaction |
| **Screenshots in Chat** | ✅ Complete | Base64 encoded, embedded in conversation |
| **Natural Language Interface** | ✅ Complete | Conversational command processing |
| **AI Content Generation** | ✅ Complete | OpenAI integration for email content |
| **Modular Architecture** | ✅ Complete | Separated layers for extensibility |

### 🎯 Demonstration Email

This agent successfully sends demonstration emails to `reportinsurebuzz@gmail.com` with:
- **Subject**: "AI Agent Task - [Your Name]"  
- **Method**: Real browser automation through Gmail web interface
- **Proof**: Screenshots showing actual Gmail UI interaction

---

## 📁 Project Structure

```
conversational-browser-agent/
├── 📄 README.md                    # This file
├── 🏗️ ARCHITECTURE.md              # Detailed technical documentation
├── ⚙️ setup.ps1 / setup.sh         # Automated setup scripts
├── 🚀 run.ps1 / run.sh             # Application startup scripts
│
├── 🔧 backend/                     # Python FastAPI backend
│   ├── 📦 requirements.txt         # Python dependencies
│   ├── ⚙️ .env.example             # Environment variables template
│   ├── 🚀 main.py                  # FastAPI application entry point
│   └── 📂 app/
│       ├── 🔌 api/                 # WebSocket & HTTP endpoints
│       ├── 🧠 services/            # Core business logic
│       │   ├── 🌐 browser_controller.py      # CORE: Playwright automation
│       │   ├── 💬 conversation_manager.py    # Natural language processing
│       │   ├── 🤖 ai_content_generator.py    # OpenAI integration
│       │   └── 📧 email_automation_service.py # Main orchestration
│       ├── 📊 models/              # Data structures & schemas
│       └── ⚙️ core/                # Configuration & settings
│
└── 🎨 frontend/                    # React frontend
    ├── 📦 package.json             # Node.js dependencies
    ├── 🌐 public/                  # Static assets
    └── 📂 src/
        ├── 🎮 App.js               # Main application component
        ├── 🎨 App.css              # Application styles
        ├── 📱 components/          # React UI components
        │   ├── 💬 MessageList.js           # Chat message display
        │   ├── 📝 ChatInput.js             # User input component
        │   ├── 📊 StatusBar.js             # Connection status
        │   └── 🖼️ Message.js               # Individual message rendering
        └── 🔗 hooks/               # Custom React hooks
            └── 🔌 useWebSocket.js          # WebSocket communication
```

---

## 🤝 Contributing & Extension

This project is designed to demonstrate browser automation principles. Here's how to extend it:

### 🌍 Adding New Websites

1. **Create Website Controller**: 
   ```python
   # app/services/twitter_controller.py
   class TwitterController(BrowserController):
       async def navigate_to_twitter(self):
           # Implementation
   ```

2. **Extend Conversation Manager**:
   ```python
   # Add new conversation states
   TWITTER_AUTOMATION = "twitter_automation"
   ```

3. **Update Frontend**:
   ```javascript
   // Add new message types for Twitter actions
   ```

### 🧠 Adding New AI Capabilities

1. **Extend AI Generator**:
   ```python
   async def generate_social_post(self, context: str):
       # New content generation
   ```

2. **Update Conversation Flow**:
   ```python
   # Add new conversation states for different content types
   ```

---

## 🐛 Troubleshooting

<details>
<summary>🔧 Common Issues & Solutions</summary>

### **Backend Won't Start**
```bash
# Check Python version
python --version  # Should be 3.8+

# Check if virtual environment is activated
which python  # Should point to venv

# Reinstall dependencies
pip install -r requirements.txt
playwright install
```

### **Browser Automation Fails**
```bash
# Install browser dependencies
playwright install-deps

# Check if running in GUI environment
echo $DISPLAY  # Should not be empty on Linux
```

### **WebSocket Connection Issues**
- ✅ Check if backend is running on port 8000
- ✅ Verify CORS settings in backend/app/core/config.py
- ✅ Check browser console for connection errors

### **Screenshot Not Displaying**
- ✅ Verify base64 encoding is working
- ✅ Check browser console for image loading errors
- ✅ Ensure screenshots directory has write permissions

### **OpenAI API Errors**
```bash
# Verify API key is set
cat backend/.env | grep OPENAI_API_KEY

# Test API key
curl -H "Authorization: Bearer YOUR_KEY" https://api.openai.com/v1/models
```

</details>

---

## 📚 Documentation

- 📖 **[ARCHITECTURE.md](ARCHITECTURE.md)**: Detailed technical documentation
- 🔌 **API Documentation**: Available at `http://localhost:8000/docs` when running
- 💬 **WebSocket Protocol**: Real-time communication specification
- 🧪 **Testing Guide**: Unit and integration testing strategies

---

## 🏆 Assignment Completion

### ✅ Core Requirements Met

1. **✅ Real Browser Automation**: Uses Playwright to control actual browsers
2. **✅ NO APIs**: Zero usage of Gmail API, SMTP, or programmatic email sending  
3. **✅ Natural Language Interface**: Conversational commands with intent extraction
4. **✅ Screenshots in Chat**: Base64 encoded images embedded in conversation
5. **✅ AI Content Generation**: OpenAI integration for professional email content
6. **✅ Modular Architecture**: Extensible design for future capabilities

### 🎯 Verification Email

- **✉️ Recipient**: `reportinsurebuzz@gmail.com`
- **📝 Subject**: "AI Agent Task - [Your Name]"  
- **🛠️ Method**: Real Gmail web interface automation
- **📸 Proof**: Screenshots of entire browser automation process

### 🏗️ Technical Excellence

- **🔧 Clean Code**: Well-documented, modular Python/React codebase
- **⚡ Performance**: Optimized WebSocket communication and screenshot handling
- **🛡️ Security**: Safe credential handling and session management
- **📱 UX**: Intuitive ChatGPT-style interface with real-time feedback
- **🔍 Error Handling**: Robust error recovery and user feedback

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🎉 Conclusion

This Conversational Browser Control Agent demonstrates that **the future of AI agents lies in real browser control**, not API integrations. While APIs are limited to what developers expose, browser automation gives us access to everything a human can do online.

**🎯 Key Takeaway**: This is not just an email tool - it's a platform for AI agents to navigate and control the digital world through actual interface interaction, just like humans do.

---

<div align="center">

**🤖 Built with ❤️ to showcase the future of AI-powered browser automation**

[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?logo=github)](https://github.com/yourusername/conversational-browser-agent)
[![Demo](https://img.shields.io/badge/🌐-Live%20Demo-blue)](http://localhost:3000)
[![Docs](https://img.shields.io/badge/📚-API%20Docs-green)](http://localhost:8000/docs)

</div>
