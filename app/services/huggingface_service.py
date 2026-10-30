import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

class HuggingFaceProvider:
    def __init__(self):
        self.name = "HuggingFace"
        # FIX: Pin the model directly to the client instance. 
        # This forces the library to use the free api-inference endpoint.
        self.model = "meta-llama/Llama-3.1-8B-Instruct"
        self.client = InferenceClient(
            model=self.model,
            api_key=os.getenv("HF_TOKEN")
        )

    def generate(self, messages, tools=None):
        hf_messages = []
        for msg in messages:
            if isinstance(msg, dict):
                role = msg.get("role", "user")
                content = msg.get("content") or msg.get("parts", [""])
                if isinstance(content, dict) and "text" in content:
                    content = content["text"]
                elif isinstance(content, list):
                    content = " ".join([str(p) for p in content])
                hf_messages.append({"role": role, "content": str(content)})

        # FIX: Call chat_completion directly from the client (do not use .chat.completions.create)
        response = self.client.chat_completion(
            messages=hf_messages,
            max_tokens=500,
            temperature=0.7
        )
        
        return {
            "content": response.choices[0].message.content,
            "tool_calls": None
        }
