import os
import uuid
from typing import List, Dict, Any, Optional
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# MongoDB Connection URI (env se uthayega ya default localhost)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "rag_agent_db")

class ChatSessionManager:
    def __init__(self):
        try:
            self.client = MongoClient(MONGO_URI)
            self.db = self.client[DB_NAME]
            self.sessions_collection = self.db["chat_sessions"]
            # Index on session_id for fast retrieval
            self.sessions_collection.create_index("session_id", unique=True)
        except Exception as e:
            print(f"Warning: MongoDB connection failed: {e}. Falling back to in-memory mode.")
            self.client = None

    def get_or_create_session(self, session_id: Optional[str] = None) -> tuple[str, List[Dict[str, Any]]]:
        if not session_id or not self.client:
            session_id = str(uuid.uuid4())

        if not self.client:
            return session_id, []

        # Find existing session in MongoDB
        session_doc = self.sessions_collection.find_one({"session_id": session_id})
        
        if session_doc:
            return session_id, session_doc.get("history", [])
        else:
            # Create a new session document
            new_session = {
                "session_id": session_id,
                "title": "Untitled",
                "history": []
            }
            self.sessions_collection.insert_one(new_session)
            return session_id, []

    def save_session_history(self, session_id: str, history: List[Dict[str, Any]]):
        """Updates the entire history array for a session in MongoDB."""
        if not self.client:
            return
        
        self.sessions_collection.update_one(
            {"session_id": session_id},
            {"$set": {"history": history}},
            upsert=True
        )

    def clear_session(self, session_id: str):
        if not self.client:
            return
        self.sessions_collection.update_one(
            {"session_id": session_id},
            {"$set": {"history": []}}
        )

    def get_session_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Returns history list for a session."""
        if not self.client:
            return []
        session_doc = self.sessions_collection.find_one({"session_id": session_id})
        return session_doc.get("history", []) if session_doc else []

    def add_message(self, session_id: str, role: str, content: str):
        """Appends a message to session history in MongoDB."""
        if not self.client:
            return
        history = self.get_session_history(session_id)
        history.append({"role": role, "content": content})
        self.save_session_history(session_id, history)