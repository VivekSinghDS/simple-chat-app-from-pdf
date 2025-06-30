from openai import OpenAI
from typing import List, Dict, Any, Optional
from config import Config
from database import ChatDatabase
from pdf_processor import PDFProcessor

class Chatbot:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.db = ChatDatabase()
        self.pdf_processor = PDFProcessor()
        self.knowledge_base = None
    
    def _load_knowledge_base(self) -> str:
        """Load the PDF knowledge base content"""
        if self.knowledge_base is None:
            try:
                self.knowledge_base = self.pdf_processor.extract_text()
            except FileNotFoundError:
                self.knowledge_base = "Knowledge base PDF not found. Please ensure the PDF file is available."
            except Exception as e:
                self.knowledge_base = f"Error loading knowledge base: {str(e)}"
        
        return self.knowledge_base
    
    def _prepare_messages(self, chat_id: str, user_message: str) -> List[Dict[str, str]]:
        """Prepare messages for OpenAI API including system instructions and chat history"""
        messages = []
        
        # Add system message with knowledge base
        knowledge_base = self._load_knowledge_base()
        system_message = f"{Config.SYSTEM_INSTRUCTIONS}\n\nKnowledge Base Content:\n{knowledge_base}"
        messages.append({"role": "system", "content": system_message})
        
        # Add chat history
        chat_history = self.db.get_chat_history(chat_id)
        if chat_history:
            for msg in chat_history:
                messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        return messages
    
    def chat(self, chat_id: str, user_message: str) -> Dict[str, Any]:
        """Process a chat message and return the response"""
        try:
            # Prepare messages for OpenAI
            messages = self._prepare_messages(chat_id, user_message)
            
            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            
            assistant_message = response.choices[0].message.content
            
            # Save messages to database
            self.db.add_message(chat_id, "user", user_message)
            self.db.add_message(chat_id, "assistant", assistant_message)
            
            return {
                "success": True,
                "chat_id": chat_id,
                "response": assistant_message,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "chat_id": chat_id
            }
    
    def create_new_chat(self) -> str:
        """Create a new chat session and return the chat ID"""
        return self.db.create_chat_session()
    
    def get_chat_history(self, chat_id: str) -> Optional[List[Dict[str, Any]]]:
        """Get chat history for a specific chat ID"""
        return self.db.get_chat_history(chat_id)
    
    def list_chats(self) -> List[Dict[str, Any]]:
        """List all chat sessions"""
        return self.db.list_chat_sessions()
    
    def delete_chat(self, chat_id: str) -> bool:
        """Delete a chat session"""
        return self.db.delete_chat_session(chat_id) 