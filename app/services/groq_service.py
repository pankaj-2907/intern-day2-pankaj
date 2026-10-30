import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class GroqProvider:
    def __init__(self):
        self.name = "Groq"
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "openai/gpt-oss-120b" # "openai/gpt-oss-safeguard-20b"

    def generate(self, contents, tools=None):
        messages = []
        for item in contents:
            if isinstance(item, dict):
                role = item.get("role", "user")
                
                if role == "tool":
                    messages.append({
                        "role": "tool",
                        "tool_call_id": item.get("tool_call_id"),
                        "content": item.get("content")
                    })
                elif role == "assistant":
                    assistant_msg = {
                        "role": "assistant",
                        "content": item.get("content")
                    }
                    tool_calls = item.get("tool_calls")
                    if tool_calls:  # Only add tool_calls if they actually exist
                        assistant_msg["tool_calls"] = tool_calls
                    messages.append(assistant_msg)
                else:
                    # 🚀 FIX: Pehle check karo agar direct 'content' key available hai, nahi toh parts se banao
                    content_text = item.get("content")
                    
                    if not content_text and "parts" in item:
                        parts = item.get("parts", [])
                        content_text = ""
                        for part in parts:
                            if isinstance(part, str):
                                content_text += part
                            elif isinstance(part, dict):
                                if "text" in part:
                                    content_text += part["text"]
                                elif "function_response" in part:
                                    content_text += json.dumps(part["function_response"])
                            else:
                                content_text += str(part)
                                
                    messages.append({"role": role, "content": content_text or ""})
            else:
                messages.append({"role": "user", "content": str(item)})

        formatted_tools = None
        if tools:
            formatted_tools = []
            for tool in tools:
                name = tool.get("name") if isinstance(tool, dict) else getattr(tool, "name", None)
                desc = tool.get("description") if isinstance(tool, dict) else getattr(tool, "description", None)
                params = tool.get("parameters") if isinstance(tool, dict) else getattr(tool, "parameters", None)
                
                if name:
                    formatted_tools.append({
                        "type": "function",
                        "function": {
                            "name": name,
                            "description": desc,
                            "parameters": params
                        }
                    })

        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.5,
            "extra_body": {
                "reasoning_effort": "medium"
            }
        }
        if formatted_tools:
            kwargs["tools"] = formatted_tools
            kwargs["tool_choice"] = "auto"

        completion = self.client.chat.completions.create(**kwargs)
        message = completion.choices[0].message
        
        # Convert Groq tool calls to universal format
        formatted_tool_calls = None
        if message.tool_calls:
            formatted_tool_calls = []
            for tc in message.tool_calls:
                formatted_tool_calls.append({
                    "id": tc.id,
                    "name": tc.function.name,
                    "arguments": tc.function.arguments
                })

        return {
            "content": message.content,
            "tool_calls": formatted_tool_calls
        }
        pass


    def generate_stream(self, contents, tools=None):
        """Streams response chunks directly from Groq API."""
        messages = []
        for item in contents:
            if isinstance(item, dict):
                role = item.get("role", "user")
                if role == "tool":
                    messages.append({
                        "role": "tool",
                        "tool_call_id": item.get("tool_call_id"),
                        "content": item.get("content")
                    })
                elif role == "assistant":
                    assistant_msg = {"role": "assistant", "content": item.get("content")}
                    if item.get("tool_calls"):
                        assistant_msg["tool_calls"] = item.get("tool_calls")
                    messages.append(assistant_msg)
                else:
                    content_text = item.get("content") or ""
                    messages.append({"role": role, "content": content_text})
            else:
                messages.append({"role": "user", "content": str(item)})

        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.5,
            "stream": True,  # 🚀 Direct true streaming enable kiya
        }
        
        stream = self.client.chat.completions.create(**kwargs)
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content, self.name