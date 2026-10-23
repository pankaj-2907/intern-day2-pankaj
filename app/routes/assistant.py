from fastapi import APIRouter, HTTPException, Depends
from typing import Any, Optional
from app.services.tool_calling_service import ToolCallingService
from app.tools.tools_registry import tool_registry
from app.schemas.assistant_schema import (
    ChatRequest,
    ChatResponse,
    ToolCallInfo,
    ToolsListResponse,
    HealthResponse
)

router = APIRouter(prefix="/assistant", tags=["Assistant"])


# Dependency injector for ToolCallingService
def get_tool_service() -> ToolCallingService:
    return ToolCallingService()


# Dependency injector placeholder for Day 6 Retrieval Service
def get_retrieval_service() -> Optional[Any]:
    return None


@router.post("/chat", response_model=ChatResponse)
def assistant_chat(
    payload: ChatRequest,
    service: ToolCallingService = Depends(get_tool_service),
    retrieval_service: Optional[Any] = Depends(get_retrieval_service)
):
    """
    Endpoint 1 — POST /assistant/chat
    Accepts a user message, lets the LLM decide if a tool is needed,
    executes the tool securely, and returns the final answer with execution metadata.
    """
    try:
        result = service.process_chat(
            user_message=payload.message,
            retrieval_service=retrieval_service
        )
        return ChatResponse(
            message=result.get("message", ""),
            tool_calls=[
                ToolCallInfo(tool_name=tc["tool_name"], status=tc["status"])
                for tc in result.get("tool_calls", [])
            ],
            success=result.get("success", True)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal assistant error: {str(e)}")


@router.get("/tools", response_model=ToolsListResponse)
def list_registered_tools():
    """
    Endpoint 2 — GET /assistant/tools
    Returns the list of registered tools, including their names and descriptions.
    """
    try:
        tools = tool_registry.list_tools()
        return ToolsListResponse(tools=tools)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch tools: {str(e)}")


@router.get("/health", response_model=HealthResponse)
def assistant_health():
    """
    Endpoint 3 — GET /assistant/health
    Returns the application's actual readiness status based on component initialization.
    """
    try:
        tools_count = len(tool_registry._tools)
        if tools_count == 0:
            return HealthResponse(status="degraded", details={"reason": "No tools registered in registry"})
        
        return HealthResponse(status="ok", details={"registered_tools_count": tools_count})
    except Exception as e:
        return HealthResponse(status="error", details={"reason": str(e)})