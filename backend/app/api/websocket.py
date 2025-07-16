from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, List
import json
import logging
import asyncio
import uuid
from ..services import EmailAutomationService
from ..models import ConversationState

logger = logging.getLogger(__name__)

router = APIRouter()
automation_service = EmailAutomationService()

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket
        logger.info(f"WebSocket connected for session: {session_id}")
    
    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]
            logger.info(f"WebSocket disconnected for session: {session_id}")
    
    async def send_message(self, session_id: str, message: dict):
        if session_id in self.active_connections:
            websocket = self.active_connections[session_id]
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Error sending message to {session_id}: {e}")
                self.disconnect(session_id)

manager = ConnectionManager()

@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for real-time communication
    """
    await manager.connect(websocket, session_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            message_type = message_data.get("type")
            content = message_data.get("content", "")
            
            if message_type == "user_message":
                # Process user message through conversation manager
                response = await automation_service.process_message(session_id, content)
                
                # Send agent response
                await manager.send_message(session_id, {
                    "type": "agent_message",
                    "content": response.message,
                    "requires_input": response.requires_input,
                    "state": response.next_state.value
                })
                
                # If ready for browser automation, start it
                if response.next_state == ConversationState.BROWSER_AUTOMATION:
                    await asyncio.sleep(1)  # Brief pause before starting automation
                    
                    # Start email automation with real-time updates
                    async for update in automation_service.start_email_automation(session_id):
                        await manager.send_message(session_id, update)
                        await asyncio.sleep(0.5)  # Small delay between updates for better UX
            
            elif message_type == "stop_automation":
                await automation_service.stop_automation(session_id)
                await manager.send_message(session_id, {
                    "type": "status",
                    "message": "Automation stopped"
                })
    
    except WebSocketDisconnect:
        manager.disconnect(session_id)
        # Clean up any ongoing automation
        await automation_service.stop_automation(session_id)
    except Exception as e:
        logger.error(f"WebSocket error for session {session_id}: {e}")
        manager.disconnect(session_id)

@router.get("/conversation/{session_id}")
async def get_conversation_history(session_id: str):
    """
    Get conversation history for a session
    """
    try:
        history = automation_service.get_conversation_history(session_id)
        return {
            "session_id": session_id,
            "messages": [
                {
                    "id": msg.id,
                    "type": msg.type.value,
                    "content": msg.content,
                    "timestamp": msg.timestamp,
                    "metadata": msg.metadata
                }
                for msg in history
            ]
        }
    except Exception as e:
        logger.error(f"Error getting conversation history: {e}")
        raise HTTPException(status_code=500, detail="Failed to get conversation history")

@router.post("/session/create")
async def create_session():
    """
    Create a new conversation session
    """
    try:
        session_id = str(uuid.uuid4())
        return {"session_id": session_id}
    except Exception as e:
        logger.error(f"Error creating session: {e}")
        raise HTTPException(status_code=500, detail="Failed to create session")

@router.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """
    Delete a conversation session and stop any ongoing automation
    """
    try:
        await automation_service.stop_automation(session_id)
        manager.disconnect(session_id)
        return {"message": f"Session {session_id} deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting session: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete session")

@router.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "message": "Conversational Browser Control Agent is running",
        "features": [
            "Real browser automation (NO APIs)",
            "Natural language conversation",
            "Screenshots in chat",
            "AI-generated email content"
        ]
    }
