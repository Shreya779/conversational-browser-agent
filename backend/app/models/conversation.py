from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from enum import Enum

class MessageType(str, Enum):
    USER = "user"
    AGENT = "agent"
    SYSTEM = "system"
    SCREENSHOT = "screenshot"
    STATUS = "status"

class ConversationState(str, Enum):
    INITIAL = "initial"
    COLLECTING_EMAIL = "collecting_email"
    COLLECTING_PASSWORD = "collecting_password"
    COLLECTING_RECIPIENT = "collecting_recipient"
    COLLECTING_SUBJECT = "collecting_subject"
    COLLECTING_CONTENT_CONTEXT = "collecting_content_context"
    PROCESSING = "processing"
    BROWSER_AUTOMATION = "browser_automation"
    COMPLETED = "completed"
    ERROR = "error"

class Message(BaseModel):
    id: str
    type: MessageType
    content: str
    timestamp: float
    metadata: Optional[Dict[str, Any]] = None

class UserCredentials(BaseModel):
    email: str
    password: str

class EmailData(BaseModel):
    to_email: str
    subject: str
    body: str
    context: Optional[str] = None

class ConversationContext(BaseModel):
    state: ConversationState
    credentials: Optional[UserCredentials] = None
    email_data: Optional[EmailData] = None
    messages: List[Message] = []
    current_action: Optional[str] = None

class BrowserAction(BaseModel):
    action_type: str
    description: str
    screenshot_path: Optional[str] = None
    success: bool
    error_message: Optional[str] = None

class AgentResponse(BaseModel):
    message: str
    action: Optional[BrowserAction] = None
    next_state: ConversationState
    requires_input: bool = False
