from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class ChatRequest(BaseModel):
    message: str = Field(..., description="The user's message/query")


class ToolCallInfo(BaseModel):
    tool_name: str
    status: str


class ChatResponse(BaseModel):
    message: str
    tool_calls: List[ToolCallInfo]
    success: bool


class ToolsListResponse(BaseModel):
    tools: List[Dict[str, str]]


class HealthResponse(BaseModel):
    status: str
    details: Optional[Dict[str, Any]] = None