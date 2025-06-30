from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class ChatMessage(BaseModel):
    role: str = Field(..., description="Role of the message sender (user/assistant)")
    content: str = Field(..., description="Content of the message")
    timestamp: Optional[datetime] = Field(None, description="Timestamp of the message")

class ChatRequest(BaseModel):
    message: str = Field(..., description="User message to send to the chatbot")
    chat_id: Optional[str] = Field(None, description="Existing chat ID. If not provided, a new chat will be created")

class ChatResponse(BaseModel):
    success: bool = Field(..., description="Whether the request was successful")
    chat_id: str = Field(..., description="Chat session ID")
    response: Optional[str] = Field(None, description="Assistant's response message")
    error: Optional[str] = Field(None, description="Error message if request failed")
    usage: Optional[Dict[str, int]] = Field(None, description="Token usage information")

class ChatHistoryResponse(BaseModel):
    success: bool = Field(..., description="Whether the request was successful")
    chat_id: str = Field(..., description="Chat session ID")
    messages: List[ChatMessage] = Field(default_factory=list, description="List of chat messages")
    error: Optional[str] = Field(None, description="Error message if request failed")

class ChatSession(BaseModel):
    chat_id: str = Field(..., description="Chat session ID")
    created_at: datetime = Field(..., description="When the chat session was created")
    updated_at: datetime = Field(..., description="When the chat session was last updated")
    message_count: Optional[int] = Field(None, description="Number of messages in the chat")

class ChatListResponse(BaseModel):
    success: bool = Field(..., description="Whether the request was successful")
    chats: List[ChatSession] = Field(default_factory=list, description="List of chat sessions")
    error: Optional[str] = Field(None, description="Error message if request failed")

class DeleteChatResponse(BaseModel):
    success: bool = Field(..., description="Whether the deletion was successful")
    chat_id: str = Field(..., description="Chat session ID that was deleted")
    error: Optional[str] = Field(None, description="Error message if deletion failed") 