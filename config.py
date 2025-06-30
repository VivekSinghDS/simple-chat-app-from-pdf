import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = "gpt-4o"
    
    # MongoDB Configuration
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "sample_chat")
    MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "chats")
    
    # PDF File Path
    PDF_FILE_PATH = os.getenv("PDF_FILE_PATH", "./knowledge_base.pdf")
    
    # System Instructions
    SYSTEM_INSTRUCTIONS = """You are a question answering chatbot. Your knowledge source is a static 10-page PDF file. 
    You should answer questions based on the information available in this PDF. 
    If a question cannot be answered from the PDF content, politely inform the user that the information is not available in your knowledge base.
    Always provide accurate and helpful responses based on the PDF content.""" 