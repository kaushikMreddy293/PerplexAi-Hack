import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["chat_db"]             # database
chat_collection = db["messages"]   # collection

def save_message(role, content, citations=None):
    chat_collection.insert_one({
        "role": role,
        "content": content,
        "citations": citations or [],
    })

def get_chat_history():
    return list(chat_collection.find({}, {"_id": 0}))  # exclude MongoDB _id
