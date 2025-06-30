#!/usr/bin/env python3
"""
Simple test script for the Sample Chat chatbot
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check: {response.status_code} - {response.json()}")
    return response.status_code == 200

def test_create_chat():
    """Test creating a new chat session"""
    print("\nTesting chat creation...")
    response = requests.post(f"{BASE_URL}/chat/new")
    if response.status_code == 200:
        data = response.json()
        print(f"New chat created: {data['chat_id']}")
        return data['chat_id']
    else:
        print(f"Failed to create chat: {response.status_code}")
        return None

def test_chat_message(chat_id, message):
    """Test sending a message to the chatbot"""
    print(f"\nSending message: '{message}'")
    payload = {
        "message": message,
        "chat_id": chat_id
    }
    response = requests.post(f"{BASE_URL}/chat", json=payload)
    if response.status_code == 200:
        data = response.json()
        print(f"Bot response: {data['response']}")
        if 'usage' in data:
            print(f"Token usage: {data['usage']}")
        return True
    else:
        print(f"Failed to send message: {response.status_code}")
        return False

def test_chat_history(chat_id):
    """Test retrieving chat history"""
    print(f"\nTesting chat history for {chat_id}...")
    response = requests.get(f"{BASE_URL}/chat/{chat_id}/history")
    if response.status_code == 200:
        data = response.json()
        print(f"Chat history: {len(data['messages'])} messages")
        for msg in data['messages']:
            print(f"  {msg['role']}: {msg['content'][:50]}...")
        return True
    else:
        print(f"Failed to get chat history: {response.status_code}")
        return False

def test_list_chats():
    """Test listing all chats"""
    print("\nTesting list chats...")
    response = requests.get(f"{BASE_URL}/chats")
    if response.status_code == 200:
        data = response.json()
        print(f"Found {len(data['chats'])} chat sessions")
        return True
    else:
        print(f"Failed to list chats: {response.status_code}")
        return False

def main():
    """Run all tests"""
    print("Starting Sample Chat tests...")
    
    # Test health
    if not test_health():
        print("Health check failed. Make sure the server is running.")
        return
    
    # Test creating a new chat
    chat_id = test_create_chat()
    if not chat_id:
        print("Failed to create chat. Exiting.")
        return
    
    # Test sending messages
    test_messages = [
        "Hello, what is this document about?",
        "Can you summarize the main points?",
        "What are the key takeaways?"
    ]
    
    for message in test_messages:
        test_chat_message(chat_id, message)
        time.sleep(1)  # Small delay between messages
    
    # Test chat history
    test_chat_history(chat_id)
    
    # Test listing chats
    test_list_chats()
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    main() 