import json
import logging
from typing import List, Dict, Any, Optional
from google import genai
from google.genai import types
from app.tools.tools_registry import tool_registry

logger = logging.getLogger(__name__)


class ToolCallingService:
    """
    Manages the Google Gemini interaction loop, tool detection, argument parsing, 
    backend tool execution, and max round safeguards.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-flash-latest", max_rounds: int = 5):
        # Initialize Gemini client using Google AI Studio API key
        self.client = genai.Client(api_key=api_key) if api_key else genai.Client()
        self.model = model
        self.max_rounds = max_rounds

    def process_chat(self, user_message: str, retrieval_service: Optional[Any] = None) -> Dict[str, Any]:
        # Convert tool registry definitions into Gemini declaration format
        gemini_tools = []
        for tool in tool_registry._tools.values():
            gemini_tools.append(
                types.Tool(
                    function_declarations=[
                        types.FunctionDeclaration(
                            name=tool["name"],
                            description=tool["description"],
                            parameters=tool["parameters"]
                        )
                    ]
                )
            )

        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=user_message)]
            )
        ]

        executed_tools = []
        round_count = 0

        while round_count < self.max_rounds:
            round_count += 1
            try:
                config = types.GenerateContentConfig(
                    tools=gemini_tools if gemini_tools else None,
                    temperature=0.3
                )
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=contents,
                    config=config
                )
            except Exception as e:
                logger.error(f"Gemini API communication error: {str(e)}")
                return {
                    "message": "I encountered an error communicating with the AI service. Please try again later.",
                    "tool_calls": executed_tools,
                    "success": False
                }

            # Check if Gemini requested a function call
            function_calls = response.function_calls

            if function_calls:
                # Append model response content to history
                if response.candidates and response.candidates[0].content:
                    contents.append(response.candidates[0].content)

                for fc in function_calls:
                    function_name = fc.name
                    function_args = dict(fc.args) if fc.args else {}

                    # Execute tool securely via centralized registry
                    tool_result = tool_registry.execute_tool(
                        name=function_name,
                        arguments=function_args,
                        retrieval_service=retrieval_service
                    )

                    executed_tools.append({
                        "tool_name": function_name,
                        "status": "success" if tool_result.get("success", True) else "error"
                    })

                    # Send tool execution result back to Gemini as a function response
                    contents.append(
                        types.Content(
                            role="tool",
                            parts=[
                                types.Part.from_function_response(
                                    name=function_name,
                                    response={"result": tool_result}
                                )
                            ]
                        )
                    )

                # Continue loop so Gemini can read the tool output and generate final answer
                continue
            else:
                # Final natural language response from Gemini
                final_content = response.text or ""
                return {
                    "message": final_content,
                    "tool_calls": executed_tools,
                    "success": True
                }

        # Safeguard: Maximum execution rounds exceeded
        return {
            "message": "The assistant reached the maximum execution round limit without completing the response.",
            "tool_calls": executed_tools,
            "success": False
        }