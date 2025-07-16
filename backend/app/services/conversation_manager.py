import re
import uuid
import time
from typing import List, Tuple, Optional
from ..models import (
    ConversationState, 
    ConversationContext, 
    Message, 
    MessageType, 
    UserCredentials, 
    EmailData,
    AgentResponse,
    BrowserAction
)
from .ai_content_generator import AIContentGenerator
import logging

logger = logging.getLogger(__name__)

class ConversationManager:
    """
    Manages conversation flow and natural language understanding
    """
    
    def __init__(self):
        self.contexts = {}  # session_id -> ConversationContext
        self.ai_generator = AIContentGenerator()
    
    def create_session(self, session_id: str) -> ConversationContext:
        """Create new conversation session"""
        context = ConversationContext(
            state=ConversationState.INITIAL,
            messages=[]
        )
        self.contexts[session_id] = context
        return context
    
    def get_context(self, session_id: str) -> Optional[ConversationContext]:
        """Get conversation context for session"""
        return self.contexts.get(session_id)
    
    async def process_user_message(self, session_id: str, message: str) -> AgentResponse:
        """
        Process user message and determine appropriate response
        """
        context = self.get_context(session_id)
        if not context:
            context = self.create_session(session_id)
        
        # Add user message to context
        user_msg = Message(
            id=str(uuid.uuid4()),
            type=MessageType.USER,
            content=message,
            timestamp=time.time()
        )
        context.messages.append(user_msg)
        
        # Process based on current state
        if context.state == ConversationState.INITIAL:
            return await self._handle_initial_state(context, message)
        elif context.state == ConversationState.COLLECTING_EMAIL:
            return await self._handle_email_collection(context, message)
        elif context.state == ConversationState.COLLECTING_PASSWORD:
            return await self._handle_password_collection(context, message)
        elif context.state == ConversationState.COLLECTING_RECIPIENT:
            return await self._handle_recipient_collection(context, message)
        elif context.state == ConversationState.COLLECTING_CONTENT_CONTEXT:
            return await self._handle_content_context_collection(context, message)
        else:
            return AgentResponse(
                message="I'm processing your request. Please wait...",
                next_state=context.state,
                requires_input=False
            )
    
    async def _handle_initial_state(self, context: ConversationContext, message: str) -> AgentResponse:
        """Handle initial conversation state"""
        message_lower = message.lower()
        
        # Check if user wants to send an email
        email_keywords = [
            'send email', 'email', 'send a message', 'compose', 'write email',
            'leave application', 'leave request', 'vacation', 'time off',
            'meeting', 'appointment', 'schedule'
        ]
        
        if any(keyword in message_lower for keyword in email_keywords):
            context.state = ConversationState.COLLECTING_EMAIL
            return AgentResponse(
                message="I'll help you send that email! To access your Gmail account, I'll need your email address. Please use a test account only for this demonstration.",
                next_state=ConversationState.COLLECTING_EMAIL,
                requires_input=True
            )
        else:
            return AgentResponse(
                message="Hello! I'm a conversational browser control agent. I can help you send emails by controlling a real web browser. Try saying something like 'I need to send an email' or 'Send a leave application to my manager'.",
                next_state=ConversationState.INITIAL,
                requires_input=True
            )
    
    async def _handle_email_collection(self, context: ConversationContext, message: str) -> AgentResponse:
        """Handle email address collection"""
        # Basic email validation
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, message)
        
        if emails:
            email = emails[0]
            if not context.credentials:
                context.credentials = UserCredentials(email=email, password="")
            else:
                context.credentials.email = email
            
            context.state = ConversationState.COLLECTING_PASSWORD
            return AgentResponse(
                message=f"Thanks! I've noted your email as {email}. Now I need your password to access Gmail. (Remember: only use test accounts for this demonstration)",
                next_state=ConversationState.COLLECTING_PASSWORD,
                requires_input=True
            )
        else:
            return AgentResponse(
                message="I don't see a valid email address in your message. Please provide your Gmail address (e.g., testaccount@gmail.com):",
                next_state=ConversationState.COLLECTING_EMAIL,
                requires_input=True
            )
    
    async def _handle_password_collection(self, context: ConversationContext, message: str) -> AgentResponse:
        """Handle password collection"""
        if context.credentials:
            context.credentials.password = message.strip()
        
        context.state = ConversationState.COLLECTING_RECIPIENT
        return AgentResponse(
            message="Perfect! I've securely stored your credentials. Now, who would you like to send the email to? Please provide the recipient's email address:",
            next_state=ConversationState.COLLECTING_RECIPIENT,
            requires_input=True
        )
    
    async def _handle_recipient_collection(self, context: ConversationContext, message: str) -> AgentResponse:
        """Handle recipient email collection"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, message)
        
        if emails:
            recipient = emails[0]
            if not context.email_data:
                context.email_data = EmailData(to_email=recipient, subject="", body="")
            else:
                context.email_data.to_email = recipient
            
            context.state = ConversationState.COLLECTING_CONTENT_CONTEXT
            return AgentResponse(
                message=f"Great! I'll send the email to {recipient}. Now, what's this email about? Please describe the purpose (e.g., 'leave application for next Monday to Wednesday', 'meeting about project update', etc.):",
                next_state=ConversationState.COLLECTING_CONTENT_CONTEXT,
                requires_input=True
            )
        else:
            return AgentResponse(
                message="I don't see a valid email address. Please provide the recipient's email address:",
                next_state=ConversationState.COLLECTING_RECIPIENT,
                requires_input=True
            )
    
    async def _handle_content_context_collection(self, context: ConversationContext, message: str) -> AgentResponse:
        """Handle email content context collection"""
        if context.email_data:
            context.email_data.context = message.strip()
            
            # Generate email content using AI
            try:
                subject, body = await self.ai_generator.generate_email_content(
                    context.email_data.context,
                    context.email_data.to_email
                )
                context.email_data.subject = subject
                context.email_data.body = body
                
                context.state = ConversationState.BROWSER_AUTOMATION
                return AgentResponse(
                    message=f"Perfect! I've generated a professional email about '{message}'. I'll now open a browser and navigate to Gmail to send your email. Let me show you what I'm doing step by step...",
                    next_state=ConversationState.BROWSER_AUTOMATION,
                    requires_input=False
                )
                
            except Exception as e:
                logger.error(f"Failed to generate email content: {e}")
                return AgentResponse(
                    message="I encountered an issue generating the email content. Let me proceed with a basic email template.",
                    next_state=ConversationState.BROWSER_AUTOMATION,
                    requires_input=False
                )
        
        return AgentResponse(
            message="There was an issue processing your request. Please try again.",
            next_state=ConversationState.COLLECTING_CONTENT_CONTEXT,
            requires_input=True
        )
    
    def _extract_email_intent(self, message: str) -> Optional[str]:
        """Extract email intent from natural language"""
        message_lower = message.lower()
        
        # Leave application patterns
        leave_patterns = [
            r'leave\s+application',
            r'time\s+off',
            r'vacation\s+request',
            r'leave\s+request',
            r'personal\s+leave',
            r'sick\s+leave'
        ]
        
        for pattern in leave_patterns:
            if re.search(pattern, message_lower):
                return "leave_application"
        
        # Meeting patterns
        meeting_patterns = [
            r'meeting\s+request',
            r'schedule\s+meeting',
            r'appointment',
            r'call\s+meeting'
        ]
        
        for pattern in meeting_patterns:
            if re.search(pattern, message_lower):
                return "meeting_request"
        
        return "general_email"
    
    def add_message(self, session_id: str, message: Message):
        """Add message to conversation history"""
        context = self.get_context(session_id)
        if context:
            context.messages.append(message)
    
    def get_conversation_history(self, session_id: str) -> List[Message]:
        """Get conversation history for session"""
        context = self.get_context(session_id)
        return context.messages if context else []
