import os
import requests
from dotenv import load_dotenv

load_dotenv()

class OllamaProvider:
    def __init__(self):
        self.name = "Ollama"
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = "llama3.2:1b"  # Ensure this model is pulled locally via ollama run llama3.2:1b

    def generate(self, contents, tools=None):
        url = f"{self.base_url}/api/chat"
        
        # Format messages for Ollama chat endpoint
        formatted_messages = []
        for msg in contents:
            if isinstance(msg, dict):
                role = msg.get("role", "user")
                content = msg.get("content") or msg.get("parts", [""])[0]
                if isinstance(content, dict) and "text" in content:
                    content = content["text"]
                formatted_messages.append({"role": role, "content": str(content)})

        # Format tools for Ollama schema if provided
        formatted_tools = None
        if tools:
            formatted_tools = []
            for tool in tools:
                formatted_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.get("name"),
                        "description": tool.get("description"),
                        "parameters": tool.get("parameters")
                    }
                })

        payload = {
            "model": self.model,
            "messages": formatted_messages,
            "stream": False
        }
        if formatted_tools:
            payload["tools"] = formatted_tools

        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        
        resp_data = response.json()
        message = resp_data.get("message", {})
        content = message.get("content", "")
        native_tool_calls = message.get("tool_calls", None)

        formatted_tool_calls = None
        if native_tool_calls:
            formatted_tool_calls = []
            for idx, tc in enumerate(native_tool_calls):
                func = tc.get("function", {})
                formatted_tool_calls.append({
                    "id": f"ollama_call_{idx}",
                    "name": func.get("name"),
                    "arguments": func.get("arguments", {})
                })

        return {
            "content": content,
            "tool_calls": formatted_tool_calls
        }