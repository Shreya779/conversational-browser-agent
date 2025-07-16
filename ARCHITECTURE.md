# Architecture Documentation

## Overview

The Conversational Browser Control Agent is designed as a modular, extensible system that demonstrates how AI can control web browsers through natural language conversation. This is **NOT** an email automation tool - it's a browser control platform that happens to use email sending as a demonstration of its capabilities.

## Core Principle: Real Browser Automation

**CRITICAL**: This system uses **REAL browser automation** through Playwright. It does NOT use:
- Gmail API
- SMTP libraries  
- HTTP requests to submit forms
- Any programmatic email sending

Instead, it:
- Opens actual browser windows
- Navigates to gmail.com by typing the URL
- Clicks on real UI elements
- Types in actual form fields
- Takes screenshots at each step

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend Layer                           │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐│
│  │   React UI      │ │   WebSocket     │ │   Screenshot    ││
│  │   Components    │ │   Client        │ │   Display       ││
│  └─────────────────┘ └─────────────────┘ └─────────────────┘│
└─────────────────────────────────────────────────────────────┘
                               │
                         WebSocket Connection
                               │
┌─────────────────────────────────────────────────────────────┐
│                  Backend Layer                              │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐│
│  │   FastAPI       │ │   WebSocket     │ │   Session       ││
│  │   Application   │ │   Server        │ │   Management    ││
│  └─────────────────┘ └─────────────────┘ └─────────────────┘│
└─────────────────────────────────────────────────────────────┘
                               │
┌─────────────────────────────────────────────────────────────┐
│                 Service Layer                               │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐│
│  │   Conversation  │ │   Browser       │ │   AI Content    ││
│  │   Manager       │ │   Controller    │ │   Generator     ││
│  └─────────────────┘ └─────────────────┘ └─────────────────┘│
└─────────────────────────────────────────────────────────────┘
                               │
┌─────────────────────────────────────────────────────────────┐
│                Automation Layer                             │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐│
│  │   Playwright    │ │   Screenshot    │ │   Error         ││
│  │   Browser       │ │   Capture       │ │   Handling      ││
│  │   Automation    │ │                 │ │                 ││
│  └─────────────────┘ └─────────────────┘ └─────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Frontend Layer (React)

**Purpose**: Provides ChatGPT-style interface with embedded screenshots

**Key Components**:
- `App.js`: Main application container
- `MessageList.js`: Displays conversation with embedded screenshots
- `Message.js`: Individual message rendering (user, agent, actions, screenshots)
- `ChatInput.js`: Input field with real-time status
- `StatusBar.js`: Connection and automation status
- `Header.js`: Application branding and feature highlights

**Key Features**:
- Real-time WebSocket communication
- Screenshots embedded directly in chat flow
- Different message types (user, agent, status, action, error, completion)
- Visual indicators for automation progress
- Responsive design

### 2. Backend Layer (FastAPI)

**Purpose**: HTTP server and WebSocket handler

**Key Files**:
- `main.py`: FastAPI application with CORS and routing
- `api/websocket.py`: WebSocket endpoint for real-time communication

**Responsibilities**:
- Handle WebSocket connections
- Route messages to appropriate services
- Manage session lifecycle
- Serve API documentation

### 3. Service Layer

#### Conversation Manager (`services/conversation_manager.py`)

**Purpose**: Natural language understanding and conversation flow

**Key Functions**:
- `process_user_message()`: Interprets user intent and manages state
- `_handle_initial_state()`: Detects email-related commands
- `_handle_email_collection()`: Validates and stores email addresses
- `_handle_password_collection()`: Securely handles credentials
- `_handle_recipient_collection()`: Validates recipient emails
- `_handle_content_context_collection()`: Captures email purpose

**Conversation States**:
- `INITIAL`: Waiting for user command
- `COLLECTING_EMAIL`: Getting Gmail credentials
- `COLLECTING_PASSWORD`: Getting password
- `COLLECTING_RECIPIENT`: Getting recipient email
- `COLLECTING_CONTENT_CONTEXT`: Getting email purpose
- `BROWSER_AUTOMATION`: Running browser automation
- `COMPLETED`: Automation finished

#### Browser Controller (`services/browser_controller.py`)

**Purpose**: Core browser automation using Playwright

**Key Functions**:
- `start_browser()`: Launch Playwright browser instance
- `navigate_to_gmail()`: Navigate to gmail.com
- `click_sign_in()`: Find and click sign-in button
- `enter_email()`: Type email in login field
- `click_next()`: Click next button
- `enter_password()`: Type password
- `wait_for_gmail_inbox()`: Wait for inbox to load
- `click_compose()`: Click compose button
- `fill_email_fields()`: Fill to, subject, body fields
- `send_email()`: Click send button
- `take_screenshot()`: Capture browser state

**Browser Interaction Strategy**:
- Uses multiple selector strategies for robustness
- Implements explicit waits (not sleep)
- Handles dynamic Gmail interface
- Takes screenshots at each major step
- Provides detailed error messages

#### AI Content Generator (`services/ai_content_generator.py`)

**Purpose**: Generate professional email content using OpenAI

**Key Functions**:
- `generate_email_content()`: Creates subject and body based on context
- `generate_leave_application()`: Specialized leave email generation
- `generate_meeting_email()`: Meeting-related emails
- `generate_general_email()`: General purpose emails

**Content Generation Process**:
1. Analyze user's email context/purpose
2. Generate appropriate subject line
3. Create professional email body
4. Adapt tone based on purpose (formal for leave, casual for team updates)

#### Email Automation Service (`services/email_automation_service.py`)

**Purpose**: Orchestrates the complete automation workflow

**Key Functions**:
- `start_email_automation()`: Main automation workflow
- `process_message()`: Handle incoming user messages
- `stop_automation()`: Emergency stop functionality

**Automation Workflow**:
1. Launch browser (visible for demonstration)
2. Navigate to Gmail
3. Click Sign In
4. Enter email address
5. Click Next
6. Enter password
7. Click Next (login)
8. Wait for inbox to load
9. Click Compose
10. Fill email fields
11. Send email
12. Capture confirmation

Each step includes:
- Status message to user
- Screenshot capture
- Error handling
- Real-time progress updates

### 4. Data Models (`models/conversation.py`)

**Purpose**: Define data structures and enums

**Key Classes**:
- `ConversationState`: Enum for conversation flow states
- `MessageType`: Types of messages (user, agent, screenshot, etc.)
- `Message`: Individual message structure
- `UserCredentials`: Email and password storage
- `EmailData`: Email content structure
- `ConversationContext`: Complete conversation state
- `BrowserAction`: Browser action result
- `AgentResponse`: Agent response structure

## Communication Flow

### WebSocket Message Types

1. **User Message**:
```json
{
  "type": "user_message",
  "content": "I need to send an email"
}
```

2. **Agent Response**:
```json
{
  "type": "agent_message", 
  "content": "I'll help you send that email...",
  "requires_input": true,
  "state": "collecting_email"
}
```

3. **Status Update**:
```json
{
  "type": "status",
  "message": "🚀 Launching browser..."
}
```

4. **Browser Action**:
```json
{
  "type": "action",
  "action": "navigate_to_gmail",
  "message": "Successfully navigated to Gmail",
  "success": true,
  "screenshot": "base64_encoded_image"
}
```

5. **Completion**:
```json
{
  "type": "completion",
  "message": "✅ Email sent successfully!",
  "screenshot": "base64_encoded_image"
}
```

## Security Considerations

### Credential Handling
- Passwords are stored only in memory during automation
- No persistent storage of credentials
- WebSocket connections are session-specific
- Clear instructions to use test accounts only

### Browser Security
- Browser runs with standard security settings
- No privileged access required
- Screenshots are base64 encoded for transmission
- Browser instances are properly cleaned up

## Extensibility Design

### Adding New Websites
The architecture is designed to be extended to other websites:

1. Create new controller in `services/` (e.g., `twitter_controller.py`)
2. Define website-specific actions
3. Add new conversation states
4. Update conversation manager routing
5. Create website-specific automation service

### Adding New AI Capabilities
- Extend `AIContentGenerator` with new content types
- Add specialized generation methods
- Update conversation flow to capture required context

### Adding New Communication Channels
- Implement new WebSocket message types
- Add corresponding frontend components
- Update message routing logic

## Error Handling Strategy

### Browser Automation Errors
- Multiple selector strategies for robustness
- Graceful degradation when elements not found
- Screenshot capture on errors for debugging
- Clear error messages to user

### Network and Connection Errors
- WebSocket reconnection logic
- Timeout handling for browser operations
- User notification of connection issues

### AI Service Errors
- Fallback content generation
- Graceful handling of API failures
- User notification of AI service issues

## Performance Optimization

### Screenshot Handling
- Base64 encoding for WebSocket transmission
- Image compression to reduce data size
- Cleanup of screenshot files

### Browser Performance
- Headless mode option for production
- Browser instance reuse where possible
- Proper resource cleanup

### WebSocket Optimization
- Message batching for rapid updates
- Connection pooling for multiple sessions
- Memory management for long conversations

## Testing Strategy

### Unit Tests
- Individual service method testing
- Conversation flow logic testing
- Message routing verification

### Integration Tests
- Complete automation workflow testing
- WebSocket communication testing
- Error scenario handling

### Browser Testing
- Cross-browser compatibility (Chromium, Firefox, Safari)
- Different screen resolutions
- Various Gmail interface versions

## Deployment Considerations

### Environment Variables
- OpenAI API key configuration
- Browser automation settings
- CORS origin configuration

### Dependencies
- Playwright browser installation
- Python virtual environment
- Node.js dependency management

### Resource Requirements
- Browser automation requires GUI environment
- Screenshot storage space
- Memory for browser instances

This architecture demonstrates that the future of AI agents lies not in API integrations, but in the ability to navigate and control the digital world as humans do - through actual interface interaction.
