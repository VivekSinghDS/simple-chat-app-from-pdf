# Sample Chat - Question Answering Chatbot API

A simple FastAPI backend for a question answering chatbot powered by GPT-4o that uses a static 10-page PDF file as its knowledge base. The chatbot maintains chat sessions in MongoDB.

## Features

- 🤖 GPT-4o powered chatbot
- 📄 PDF knowledge base integration
- 💾 MongoDB chat session storage
- 🔄 Persistent chat history
- 🚀 FastAPI REST API
- 📊 Token usage tracking
- 🎯 Context-aware responses

## System Instructions

The chatbot is configured with the following system instructions:
> "You are a question answering chatbot. Your knowledge source is a static 10-page PDF file. You should answer questions based on the information available in this PDF. If a question cannot be answered from the PDF content, politely inform the user that the information is not available in your knowledge base. Always provide accurate and helpful responses based on the PDF content."

## Prerequisites

- Python 3.8+
- MongoDB (local or cloud)
- OpenAI API key
- A 10-page PDF file for the knowledge base

## Installation

1. **Navigate to the project directory:**
   ```bash
   cd sample-chat
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` file with your configuration:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   MONGODB_URI=mongodb://localhost:27017/
   MONGODB_DATABASE=sample_chat
   MONGODB_COLLECTION=chats
   PDF_FILE_PATH=./knowledge_base.pdf
   ```

4. **Add your PDF knowledge base:**
   - Place your 10-page PDF file in the project directory
   - Update the `PDF_FILE_PATH` in `.env` if needed

## Usage

### Starting the Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, visit `http://localhost:8000/docs` for interactive API documentation.

## API Endpoints

### 1. Chat with the Bot

**POST** `/chat`

Send a message to the chatbot. If no `chat_id` is provided, a new chat session will be created.

**Request Body:**
```json
{
  "message": "What is the main topic of the document?",
  "chat_id": "optional-existing-chat-id"
}
```

**Response:**
```json
{
  "success": true,
  "chat_id": "uuid-chat-id",
  "response": "Based on the PDF content, the main topic is...",
  "usage": {
    "prompt_tokens": 1500,
    "completion_tokens": 200,
    "total_tokens": 1700
  }
}
```

### 2. Get Chat History

**GET** `/chat/{chat_id}/history`

Retrieve the complete conversation history for a specific chat session.

**Response:**
```json
{
  "success": true,
  "chat_id": "uuid-chat-id",
  "messages": [
    {
      "role": "user",
      "content": "What is the main topic?",
      "timestamp": "2024-01-01T12:00:00Z"
    },
    {
      "role": "assistant",
      "content": "The main topic is...",
      "timestamp": "2024-01-01T12:00:01Z"
    }
  ]
}
```

### 3. List All Chats

**GET** `/chats`

Get a list of all chat sessions.

**Response:**
```json
{
  "success": true,
  "chats": [
    {
      "chat_id": "uuid-1",
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:05:00Z",
      "message_count": 4
    }
  ]
}
```

### 4. Create New Chat

**POST** `/chat/new`

Create a new chat session and return the chat ID.

**Response:**
```json
{
  "success": true,
  "chat_id": "new-uuid-chat-id",
  "message": "New chat session created"
}
```

### 5. Delete Chat

**DELETE** `/chat/{chat_id}`

Delete a specific chat session.

**Response:**
```json
{
  "success": true,
  "chat_id": "deleted-chat-id"
}
```

### 6. Health Check

**GET** `/health`

Check if the service is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "sample-chat"
}
```

## Example Usage

### Using curl

1. **Create a new chat and send a message:**
   ```bash
   curl -X POST "http://localhost:8000/chat" \
        -H "Content-Type: application/json" \
        -d '{"message": "What is the main topic of the document?"}'
   ```

2. **Continue the conversation:**
   ```bash
   curl -X POST "http://localhost:8000/chat" \
        -H "Content-Type: application/json" \
        -d '{"message": "Can you provide more details?", "chat_id": "your-chat-id"}'
   ```

3. **Get chat history:**
   ```bash
   curl -X GET "http://localhost:8000/chat/your-chat-id/history"
   ```

### Using Python

```python
import requests

# Send a message
response = requests.post("http://localhost:8000/chat", json={
    "message": "What is the main topic of the document?"
})

chat_data = response.json()
chat_id = chat_data["chat_id"]
print(f"Bot: {chat_data['response']}")

# Continue conversation
response = requests.post("http://localhost:8000/chat", json={
    "message": "Can you provide more details?",
    "chat_id": chat_id
})

print(f"Bot: {response.json()['response']}")
```

## Project Structure

```
sample-chat/
├── main.py              # FastAPI application
├── chatbot.py           # Main chatbot logic
├── database.py          # MongoDB operations
├── pdf_processor.py     # PDF text extraction
├── config.py            # Configuration management
├── models.py            # Pydantic models
├── requirements.txt     # Python dependencies
├── env.example          # Environment variables template
├── test_chatbot.py      # Test script
└── README.md           # This file
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `MONGODB_URI`: MongoDB connection string
- `MONGODB_DATABASE`: Database name (default: sample_chat)
- `MONGODB_COLLECTION`: Collection name (default: chats)
- `PDF_FILE_PATH`: Path to your knowledge base PDF

### Customization

You can modify the system instructions in `config.py` to change how the chatbot behaves:

```python
SYSTEM_INSTRUCTIONS = """Your custom system instructions here..."""
```

## Testing

Run the test script to verify functionality:

```bash
python test_chatbot.py
```

## Troubleshooting

1. **PDF not found error**: Ensure your PDF file exists at the specified path
2. **MongoDB connection error**: Check your MongoDB URI and ensure MongoDB is running
3. **OpenAI API error**: Verify your API key is correct and has sufficient credits
4. **Import errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`

## Development

To run in development mode with auto-reload:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## License

This project is for educational and demonstration purposes. 