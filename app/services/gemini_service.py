import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class GeminiProvider:
    def __init__(self):
        self.name = "Gemini"
        # Naya official google-genai client setup
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = "gemini-3.5-flash-lite"  # Highly recommended stable tool-use model for genai SDK

    def generate(self, messages, tools=None):
        #raise Exception("Rate limit reached 429 Too Many Requests")
        # 1. Transform conversations into unified contents array compatible with Google SDK types
        gemini_contents = []
        for msg in messages:
            role = msg.get("role", "user")
            # Map roles properly to 'user' or 'model'
            gemini_role = "model" if role == "assistant" else "user"
            
            # Extract basic text message
            content_text = msg.get("content", "")
            if not content_text and "parts" in msg:
                content_text = msg["parts"][0] if isinstance(msg["parts"], list) else str(msg["parts"])
                
            gemini_contents.append(
                types.Content(
                    role=gemini_role,
                    parts=[types.Part.from_text(text=str(content_text))]
                )
            )

        # 2. Map incoming structured tool definitions to types.FunctionDeclaration array
        formatted_tools = None
        if tools:
            func_declarations = []
            for tool in tools:
                func_declarations.append(
                    types.FunctionDeclaration(
                        name=tool.get("name"),
                        description=tool.get("description", ""),
                        parameters=tool.get("parameters")
                    )
                )
            formatted_tools = [types.Tool(function_declarations=func_declarations)]

        # 3. Compile call configurations safely
        config = types.GenerateContentConfig(
            temperature=0.7,
            tools=formatted_tools if formatted_tools else None
        )

        # 4. Fire structured content generation request
        response = self.client.models.generate_content(
            model=self.model,
            contents=gemini_contents,
            config=config
        )
        
        # 5. Safely extract standard response components without breaking on missing attributes
        text_content = ""
        try:
            text_content = response.text or ""
        except Exception:
            pass

        # 6. Parse structured functional callbacks directly from native response candidate maps
        formatted_tool_calls = None
        try:
            # Safe layout extraction matching naye generation payload configurations
            parts = response.candidates[0].content.parts
            native_function_calls = [p.function_call for p in parts if p.function_call]
            
            if native_function_calls:
                formatted_tool_calls = []
                for idx, fc in enumerate(native_function_calls):
                    # Arguments evaluation checks
                    args_dict = {}
                    if fc.args:
                        # Convert structure metadata maps straight to native python dict structures
                        args_dict = dict(fc.args)

                    formatted_tool_calls.append({
                        "id": f"gemini_call_{idx}",
                        "name": fc.name,
                        "arguments": args_dict
                    })
        except Exception:
            # Fallback safe assignment if no dynamic layout values map out
            formatted_tool_calls = None

        # Return standardized uniform layout directly to FallbackLLMOrchestrator
        return {
            "content": text_content,
            "tool_calls": formatted_tool_calls
        }
