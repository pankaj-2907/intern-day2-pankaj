from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel, Field
from typing import Optional
from app.services.tool_calling_service import ToolCallingService
from app.services.retrieval_service import RetrievalService
import os
import json

app = FastAPI(title="Secure Tool-Calling RAG Assistant with Memory")

# Mount static files directory if it exists
if os.path.exists("app/static"):
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Initialize services
retrieval_service = RetrievalService(documents_path="data/documents.json")
tool_service = ToolCallingService()

# Root endpoint to serve the UI
@app.get("/")
def read_index():
    if os.path.exists("app/static/index.html"):
        return FileResponse("app/static/index.html")
    return {"message": "Welcome to the Tool-Calling RAG API. Visit /docs for Swagger UI."}

class ChatRequest(BaseModel):
    message: str = Field(..., description="The user chat message")
    session_id: Optional[str] = Field(default=None, description="Unique session ID for multi-turn chat history")

@app.post("/chat")
def chat_endpoint(payload: ChatRequest):
    try:
        result = tool_service.process_chat(
            user_message=payload.message,
            session_id=payload.session_id,
            retrieval_service=retrieval_service
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"An internal error occurred: {str(e)}"
        )

@app.post("/chat/stream")
async def chat_stream(payload: ChatRequest):
    def event_generator():
        try:
            # Regular for loop for synchronous generator
            for chunk_data in tool_service.process_stream(
                user_message=payload.message,
                session_id=payload.session_id,
                retrieval_service=retrieval_service
            ):
                yield f"data: {json.dumps(chunk_data)}\n\n"
                
            yield f"data: {json.dumps({'status': 'done'})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/sessions")
def get_all_sessions():
    """Fetches all chat sessions (session_id and title) for sidebar."""
    try:
        sessions = list(tool_service.session_manager.sessions_collection.find({}, {"_id": 0, "session_id": 1, "title": 1}))
        return {"sessions": sessions, "success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/session/{session_id}")
def get_session_history(session_id: str):
    """Fetches full conversation history for a given session from MongoDB."""
    try:
        session_doc = tool_service.session_manager.sessions_collection.find_one({"session_id": session_id})
        if not session_doc:
            return {"session_id": session_id, "history": [], "success": True}
        
        return {
            "session_id": session_id,
            "history": session_doc.get("history", []),
            "success": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/session/{session_id}")
def delete_session(session_id: str):
    """Deletes a chat session from MongoDB."""
    try:
        result = tool_service.session_manager.sessions_collection.delete_one({"session_id": session_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Session not found")
        return {"success": True, "message": "Session deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))