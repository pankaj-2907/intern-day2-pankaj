import json
import logging
from typing import List, Dict, Any, Optional
from app.tools.tools_registry import tool_registry
from app.services.fallback_manager import FallbackLLMOrchestrator
from app.services.session_store import ChatSessionManager

logger = logging.getLogger(__name__)

class ToolCallingService:
    def __init__(self, max_rounds: int = 5):
        self.max_rounds = max_rounds
        self.fallback_orchestrator = FallbackLLMOrchestrator()
        self.session_manager = ChatSessionManager()

    def process_chat(self, user_message: str, session_id: Optional[str] = None, retrieval_service: Optional[Any] = None) -> Dict[str, Any]:
        # 1. Get or create session and its existing history
        active_session_id, history = self.session_manager.get_or_create_session(session_id)

        # Deep sanitize loaded history to remove any None tool_calls completely
        sanitized_history = []
        for msg in history:
            if isinstance(msg, dict):
                cleaned_msg = msg.copy()
                if cleaned_msg.get("role") == "assistant" and cleaned_msg.get("tool_calls") is None:
                    cleaned_msg.pop("tool_calls", None)
                sanitized_history.append(cleaned_msg)
            else:
                sanitized_history.append(msg)
        history = sanitized_history

        # Build tools list
        tools_list = []
        for tool in tool_registry._tools.values():
            tools_list.append({
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["parameters"]
            })

        # 2. Construct system prompt
        system_prompt = {
            "role": "system",
            "content": (
                "You are a concise, direct, and helpful RAG assistant. "
                "CRITICAL INSTRUCTIONS:\n"
                "1. Always reply in casual, friendly Hinglish (Latin script, like 'Bhai, ye aise hoga...'), just like a developer friend. Never use pure Devanagari Hindi or long formal essays.\n"
                "2. Keep your answers short, crisp, and to the point. No fluff or unnecessary explanations.\n"
                "3. When users ask factual questions about APIs, FastAPI, Python, RAG, or project documentation, use the search_knowledge_base tool first.\n"
                "4. Speak like a developer talking to another developer—short, technical, and actionable."
            )
        }

        # If history is empty, initialize with system prompt
        if not history:
            history.append(system_prompt)
        elif history[0].get("role") != "system":
            history.insert(0, system_prompt)

        # Append current user message to session history
        user_msg_entry = {"role": "user", "parts": [user_message], "content": user_message}
        history.append(user_msg_entry)

        user_msg_count = sum(1 for m in history if m.get("role") == "user")
        session_doc = self.session_manager.sessions_collection.find_one({"session_id": active_session_id})
        current_title = session_doc.get("title", "Untitled") if session_doc else "Untitled"

        # 🚀 Safe check: Count actual user messages in history
        user_msg_count = sum(1 for m in history if isinstance(m, dict) and m.get("role") == "user")
        
        session_doc = self.session_manager.sessions_collection.find_one({"session_id": active_session_id})
        current_title = session_doc.get("title", "New Chat") if session_doc else "New Chat"

        # Jab 4 ya usse zyada messages ho jayein aur title abhi bhi default ho, tabhi naya dynamic title generate karo
        if user_msg_count >= 4 and current_title in ["New Chat", "Untitled", ""]:
            new_title = self.generate_chat_title(history)
            if new_title and new_title != "General Chat":
                self.session_manager.sessions_collection.update_one(
                    {"session_id": active_session_id},
                    {"$set": {"title": new_title}}
                )

        executed_tools = []
        round_count = 0

        while round_count < self.max_rounds:
            round_count += 1
            try:
                final_history_to_save = []
                for msg in history:
                    if isinstance(msg, dict):
                        cleaned_msg = msg.copy()
                        if cleaned_msg.get("role") == "assistant" and cleaned_msg.get("tool_calls") is None:
                            cleaned_msg.pop("tool_calls", None)
                        final_history_to_save.append(cleaned_msg)
                    else:
                        final_history_to_save.append(msg)
                
                self.session_manager.save_session_history(active_session_id, final_history_to_save)

                unified_response, active_provider, duration = self.fallback_orchestrator.generate(
                    contents=final_history_to_save, 
                    tools=tools_list if tools_list else None
                )
            except Exception as e:
                logger.error(f"All fallback providers failed: {str(e)}")
                return {
                    "session_id": active_session_id,
                    "message": "I encountered an error communicating with all available AI services. Please try again later.",
                    "tool_calls": executed_tools,
                    "success": False
                }

            assistant_content = unified_response.get("content", "")
            tool_calls = unified_response.get("tool_calls", None)

            if tool_calls:
                sanitized_tool_calls = []
                for tc in tool_calls:
                    sanitized_tc = {
                        "id": tc.get("id", "call_univ_1"),
                        "type": "function",
                        "function": {
                            "name": tc.get("name") or (tc.get("function", {}).get("name") if isinstance(tc.get("function"), dict) else None),
                            "arguments": tc.get("arguments") or (tc.get("function", {}).get("arguments") if isinstance(tc.get("function"), dict) else "{}")
                        }
                    }
                    sanitized_tool_calls.append(sanitized_tc)

                assistant_entry = {
                    "role": "assistant",
                    "content": assistant_content,
                    "tool_calls": sanitized_tool_calls
                }
                history.append(assistant_entry)

                for tc in sanitized_tool_calls:
                    func_obj = tc.get("function", {})
                    function_name = func_obj.get("name")
                    function_args = func_obj.get("arguments", {})
                    
                    if isinstance(function_args, str):
                        try:
                            function_args = json.loads(function_args)
                        except:
                            function_args = {}

                    tool_result = tool_registry.execute_tool(
                        name=function_name,
                        arguments=function_args,
                        retrieval_service=retrieval_service
                    )

                    executed_tools.append({
                        "tool_name": function_name,
                        "status": "success" if tool_result.get("success", True) else "error"
                    })

                    tool_entry = {
                        "role": "tool",
                        "tool_call_id": tc.get("id", "call_univ_1"),
                        "content": json.dumps(tool_result),
                        "parts": [{"function_response": {"name": function_name, "response": {"result": tool_result}}}]
                    }
                    history.append(tool_entry)
                continue
            else:
                assistant_final_entry = {
                    "role": "assistant",
                    "content": assistant_content or "Done."
                }
                history.append(assistant_final_entry)
                self.session_manager.save_session_history(active_session_id, history)

                return {
                    "session_id": active_session_id,
                    "message": assistant_content or "Done.",
                    "tool_calls": executed_tools,
                    "success": True,
                    "provider_used": unified_response.get("model", active_provider),
                    "response_time_seconds": round(duration, 2)
                }

        return {
            "session_id": active_session_id,
            "message": "The assistant reached the maximum execution round limit without completing the response.",
            "tool_calls": executed_tools,
            "success": False
        }

    def generate_chat_title(self, history: List[Dict[str, Any]]) -> str:
        """Generates an accurate topic title from user prompts avoiding system prompt noise."""
        try:
            # 🚀 Filter out system messages and extract only clean user text
            user_messages = [
                m.get('content') for m in history 
                if isinstance(m, dict) and m.get('role') == 'user' and isinstance(m.get('content'), str)
            ]
            
            if not user_messages:
                return "General Chat"

            # Combine last 3 user messages for better context
            combined_context = " | ".join([msg[:60] for msg in user_messages[-3:]])

            conv_summary_prompt = [
                {
                    "role": "system",
                    "content": (
                        "Create a short 2 to 4 word category title summarizing this conversation context "
                        "(e.g., 'FastAPI RAG Setup', 'Tool Debugging', 'MongoDB Schema'). "
                        "Rules: NO greetings, NO punctuation, NO quotes, NO conversational filler. Return ONLY the short title."
                    )
                },
                {
                    "role": "user",
                    "content": combined_context
                }
            ]
            
            response, _, _ = self.fallback_orchestrator.generate(contents=conv_summary_prompt, tools=None)
            title = response.get("content", "").strip().strip('"\'*#.- \n')
            
            # 🚀 Strict validation: Agar title bekaar aaye ya lamba ho, toh fallback me first message ki jagah ek smart topic name do
            if not title or len(title) > 35 or len(title.split()) > 5 or title.lower() in combined_context.lower() or "hello" in title.lower():
                # Fallback to first few words of the *latest* message instead of strict raw first message
                latest_msg = user_messages[-1] if user_messages else "General Chat"
                words = latest_msg.split()
                return " ".join(words[:3]).capitalize() if words else "General Chat"
                
            return title
        except Exception as e:
            logger.error(f"Title generation error: {str(e)}")
            return "General Chat"

    def generate_stream(self, contents, tools=None):
        """Streams response chunks from Groq API."""
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
            "stream": True,
        }
        
        stream = self.client.chat.completions.create(**kwargs)
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                yield delta.content, self.name

    def process_stream(self, user_message: str, session_id: str = None, retrieval_service = None):
        """Streams response chunks smoothly with system prompt and title generation."""
        if not session_id:
            session_id, _ = self.session_manager.get_or_create_session(None)
        else:
            session_id, _ = self.session_manager.get_or_create_session(session_id)
        
        self.session_manager.add_message(session_id, "user", user_message)
        yield {"session_id": session_id}
        
        full_response = ""
        provider_used = "Groq"
        
        try:
            history = self.session_manager.get_session_history(session_id)
            
            # 🚀 System Prompt Injection for Streaming
            system_prompt = {
                "role": "system",
                "content": (
                    "You are a concise, direct, and helpful RAG assistant. "
                    "CRITICAL INSTRUCTIONS:\n"
                    "1. Always reply in casual, friendly Hinglish (Latin script, like 'Bhai, ye aise hoga...'), just like a developer friend. Never use pure Devanagari Hindi or long formal essays.\n"
                    "2. Keep your answers short, crisp, and to the point. No fluff or unnecessary explanations.\n"
                    "3. When users ask factual questions about APIs, FastAPI, Python, RAG, or project documentation, use the search_knowledge_base tool first.\n"
                    "4. Speak like a developer talking to another developer—short, technical, and actionable."
                )
            }
            
            if not history or history[0].get("role") != "system":
                history = [system_prompt] + history

            provider = (
                getattr(self, "groq_provider", None) or 
                getattr(self, "provider", None) or 
                getattr(self, "llm", None)
            )
            if not provider:
                from app.services.groq_service import GroqProvider
                provider = GroqProvider()
                self.groq_provider = provider
            
            if hasattr(provider, "generate_stream"):
                for chunk, prov in provider.generate_stream(history):
                    full_response += chunk
                    provider_used = prov
                    yield {"chunk": chunk, "provider": provider_used}
            else:
                res = provider.generate(history)
                full_response = res.get("content", "") if isinstance(res, dict) else str(res)
                provider_used = getattr(provider, "name", "Groq")
                
                for i in range(0, len(full_response), 2):
                    chunk = full_response[i:i + 2]
                    yield {"chunk": chunk, "provider": provider_used}
                
        except Exception as e:
            full_response = f"Error during generation: {str(e)}"
            yield {"chunk": full_response, "provider": "Error"}

        if full_response:
            self.session_manager.add_message(session_id, "assistant", full_response)
        
        # 🚀 ADDED: Title generation check for stream as well!
        updated_history = self.session_manager.get_session_history(session_id)
        user_msg_count = sum(1 for m in updated_history if isinstance(m, dict) and m.get("role") == "user")
        
        session_doc = self.session_manager.sessions_collection.find_one({"session_id": session_id})
        current_title = session_doc.get("title", "New Chat") if session_doc else "New Chat"

        if user_msg_count >= 2 and current_title in ["New Chat", "Untitled", ""]:
            new_title = self.generate_chat_title(updated_history)
            if new_title and new_title != "General Chat":
                self.session_manager.sessions_collection.update_one(
                    {"session_id": session_id},
                    {"$set": {"title": new_title}}
                )