# Tool Calling Request and Execution Lifecycle

This document outlines the step-by-step lifecycle of a user request processed by the AI Assistant service, detailing how tool interactions, validation loops, and final responses are orchestrated.

---

## Step 1: User Message Reception
* The client sends a POST request to `/assistant/chat` with a user prompt message.
* The API route handler receives the request and forwards the message to `ToolCallingService.process_chat()`.

## Step 2: Context and Tool Schema Initialization
* The service initializes a conversation history list with a system prompt and the user message.
* It retrieves all available tool schemas dynamically from the centralized `tool_registry`.
* The user message along with the tool definition list is transmitted to the LLM provider API.

## Step 3: Model Decision & Branching
The LLM evaluates the prompt against the provided tool definitions and branches into one of two paths:
* **Path A (Normal Response):** If the prompt requires no external tools (e.g., general conversation or greetings), the model directly generates a natural language response. The loop terminates and the response is returned to the user.
* **Path B (Tool Call Request):** If the prompt requires external computation or retrieval, the model returns a structured tool call object containing the target function name and argument payload.

## Step 4: Argument Validation and Secure Execution
* When a tool call is detected, the backend extracts the requested tool name and arguments.
* The backend verifies the tool name against the `tool_registry` to reject unknown or unauthorized functions.
* Tool arguments are parsed and validated via Pydantic models to ensure type safety and rule compliance (e.g., rejecting division by zero or invalid timezones).
* The corresponding Python function is executed in trusted backend code, returning a structured result dictionary.

## Step 5: Feeding Results Back to the LLM
* The tool execution output is serialized into JSON format and appended to the conversation history message stack as a tool response role.
* The conversation context is sent back to the LLM so the model can read the computed data.

## Step 6: Final Natural Language Generation
* The LLM consumes the tool output and translates the raw data into a polished, polite natural language response for the end user.
* Execution metadata (such as executed tool names and statuses) is attached to the final API payload.

## Safety Safeguards & Loop Controls
* **Maximum Round Limit:** A strict round counter (default maximum 5 rounds) ensures that runaway or repetitive tool calls terminate safely, preventing infinite loops, excessive latency, and token cost exhaustion.
* **Error Containment:** If a tool execution fails or throws an exception, the error message is caught and passed safely back to the LLM as data, ensuring the application never crashes or exposes server stack traces.