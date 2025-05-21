import os
from dotenv import load_dotenv
from pymongo import MongoClient
from uuid import uuid4
from datetime import datetime

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["chat_db"]
chat_collection = db["messages"]
chats_collection = db["chats"]

# Save individual message
def save_message(role, content, chat_id, citations=None):
    chat_collection.insert_one({
        "chat_id": chat_id,
        "role": role,
        "content": content,
        "citations": citations or [],
        "timestamp": datetime.utcnow()
    })

# Create a new chat group with title
def start_new_chat(title="New Chat"):
    chat_id = str(uuid4())
    create_chat_session(chat_id, title)
    return chat_id

# Insert metadata for a chat group
def create_chat_session(chat_id, title="New Chat"):
    chats_collection.insert_one({
        "chat_id": chat_id,
        "title": title,
        "created_at": datetime.utcnow()
    })

# Get chat history by chat_id
def get_chat_history(chat_id):
    return list(chat_collection.find({"chat_id": chat_id}, {"_id": 0}))

# Get all available chat sessions (titles for sidebar)
def get_all_chats():
    return list(chats_collection.find({}, {"_id": 0}))

# Rename a chat group
def update_chat_title(chat_id, new_title):
    chats_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"title": new_title}}
    )
