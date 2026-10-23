from typing import Dict, Any, Callable, List, Optional
from app.tools.calculator import calculate
from app.tools.date_time import get_current_datetime
from app.tools.knowledge_base import search_knowledge_base


class ToolRegistry:
    """
    Centralized registry for managing, validating, and executing tools available to the LLM.
    """

    def __init__(self):
        self._tools: Dict[str, Dict[str, Any]] = {}
        self._register_default_tools()

    def register(
        self,
        name: str,
        description: str,
        parameters_schema: Dict[str, Any],
        func: Callable[..., Dict[str, Any]]
    ) -> None:
        """Registers a new tool into the registry."""
        if not name or not isinstance(name, str):
            raise ValueError("Tool name must be a non-empty string.")
        
        self._tools[name] = {
            "name": name,
            "description": description,
            "parameters": parameters_schema,
            "function": func
        }

    def _register_default_tools(self) -> None:
        """Registers the core built-in tools (Calculator, DateTime, Knowledge Base Search)."""
        
        # 1. Calculator Tool
        self.register(
            name="calculate",
            description="Performs basic arithmetic operations (add, subtract, multiply, divide) on two numbers.",
            parameters_schema={
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["add", "subtract", "multiply", "divide"],
                        "description": "The arithmetic operation to perform."
                    },
                    "a": {
                        "type": "number",
                        "description": "The first numeric operand."
                    },
                    "b": {
                        "type": "number",
                        "description": "The second numeric operand."
                    }
                },
                "required": ["operation", "a", "b"]
            },
            func=calculate
        )

        # 2. Date and Time Tool
        self.register(
            name="get_current_datetime",
            description="Returns the current date and time in ISO format for a specified valid IANA timezone.",
            parameters_schema={
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "Valid IANA timezone identifier, e.g., 'Asia/Kolkata', 'UTC'."
                    }
                },
                "required": ["timezone"]
            },
            func=get_current_datetime
        )

        # 3. Knowledge Base Search Tool
        self.register(
            name="search_knowledge_base",
            description="Searches indexed documents in the knowledge base for relevant information.",
            parameters_schema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query string."
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "Number of top matching documents to retrieve (1 to 10).",
                        "default": 3
                    }
                },
                "required": ["query"]
            },
            func=search_knowledge_base
        )

    def get_tool(self, name: str) -> Optional[Dict[str, Any]]:
        """Looks up a tool by its unique name."""
        return self._tools.get(name)

    def list_tools(self) -> List[Dict[str, str]]:
        """Returns a list of all registered tool names and descriptions (safe for API response)."""
        return [
            {"name": tool["name"], "description": tool["description"]}
            for tool in self._tools.values()
        ]

    def get_llm_tool_definitions(self) -> List[Dict[str, Any]]:
        """Returns tool definitions formatted for LLM provider API ingestion."""
        definitions = []
        for tool in self._tools.values():
            definitions.append({
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": tool["parameters"]
                }
            })
        return definitions

    def execute_tool(self, name: str, arguments: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
        """
        Safely executes a registered tool with the provided arguments.
        Rejects unknown tools and returns structured errors on failure.
        """
        tool = self.get_tool(name)
        if not tool:
            return {
                "success": False,
                "error": f"Unknown tool name: '{name}'. Tool is not registered in the system."
            }

        func = tool["function"]
        try:
            # Pass any extra runtime dependencies (like retrieval_service) if accepted by the function
            import inspect
            sig = inspect.signature(func)
            if "retrieval_service" in sig.parameters and "retrieval_service" in kwargs:
                arguments["retrieval_service"] = kwargs["retrieval_service"]

            result = func(**arguments)
            return result
        except Exception as e:
            return {
                "success": False,
                "error": f"Tool execution failed for '{name}': {str(e)}"
            }


# Global singleton instance of the tool registry
tool_registry = ToolRegistry()