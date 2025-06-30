from pymongo import MongoClient
from datetime import datetime
from typing import List, Dict, Any, Optional
from config import Config
import uuid

class ChatDatabase:
    def __init__(self):
        self.client = MongoClient(Config.MONGODB_URI)
        self.db = self.client[Config.MONGODB_DATABASE]
        self.collection = self.db[Config.MONGODB_COLLECTION]
    
    def create_chat_session(self) -> str:
        """Create a new chat session and return the chat ID"""
        chat_id = str(uuid.uuid4())
        chat_session = {
            "chat_id": chat_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "messages": []
        }
        self.collection.insert_one(chat_session)
        return chat_id
    
    def add_message(self, chat_id: str, role: str, content: str) -> bool:
        """Add a message to an existing chat session"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow()
        }
        
        result = self.collection.update_one(
            {"chat_id": chat_id},
            {
                "$push": {"messages": message},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        return result.modified_count > 0
    
    def get_chat_history(self, chat_id: str) -> Optional[List[Dict[str, Any]]]:
        """Get the chat history for a specific chat ID"""
        chat_session = self.collection.find_one({"chat_id": chat_id})
        if chat_session:
            return chat_session.get("messages", [])
        return None
    
    def get_chat_session(self, chat_id: str) -> Optional[Dict[str, Any]]:
        """Get the complete chat session"""
        return self.collection.find_one({"chat_id": chat_id})
    
    def list_chat_sessions(self) -> List[Dict[str, Any]]:
        """List all chat sessions"""
        sessions = self.collection.find({}, {
            "chat_id": 1, 
            "created_at": 1, 
            "updated_at": 1, 
            "message_count": {"$size": "$messages"}
        })
        return list(sessions)
    
    def delete_chat_session(self, chat_id: str) -> bool:
        """Delete a chat session"""
        result = self.collection.delete_one({"chat_id": chat_id})
        return result.deleted_count > 0 