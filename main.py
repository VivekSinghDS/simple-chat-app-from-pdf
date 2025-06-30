from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn

from chatbot import Chatbot
from models import (
    ChatRequest, ChatResponse
)

app = FastAPI(
    title="Sample Chat API",
    description="A question answering chatbot powered by GPT-4o with PDF knowledge base",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize chatbot
chatbot = Chatbot()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Sample Chat API",
        "description": "A question answering chatbot powered by GPT-4o",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "sample-chat"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Send a message to the chatbot.
    
    If chat_id is not provided, a new chat session will be created.
    """
    try:
        # Create new chat if chat_id not provided
        if not request.chat_id:
            chat_id = chatbot.create_new_chat()
        else:
            chat_id = request.chat_id
        
        # Process the chat message
        result = chatbot.chat(chat_id, request.message)
        
        return ChatResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





@app.post("/chat/new")
async def create_new_chat():
    """Create a new chat session and return the chat ID"""
    try:
        chat_id = chatbot.create_new_chat()
        return {
            "success": True,
            "chat_id": chat_id,
            "message": "New chat session created"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 