# Tool Registry Architecture

The Tool Registry (`app/tools/tool_registry.py`) serves as the centralized dispatcher and security boundary for all executable tools in the AI Assistant application.

---

## Key Responsibilities
1. **Centralized Registration:** Maintains a dictionary of all allowed tools (`calculate`, `get_current_datetime`, `search_knowledge_base`).
2. **Schema Definition:** Stores JSON Schemas defining parameter types, descriptions, and required fields for LLM tool invocation.
3. **Lookup & Validation:** Validates tool names against the registry before execution, preventing the model from invoking arbitrary functions.
4. **Structured Error Handling:** Catches runtime exceptions during tool execution and returns standardized error payloads.
5. **Separation of Concerns:** Keeps tool dispatching and registration entirely decoupled from FastAPI route handlers.

---

## Registered Tools Overview

| Tool Name            |     Description         |      Key Parameters     |  Backend Function  |
|              :---    |        :---            |             :---         |       :---          |
| `calculate` | Performs basic arithmetic operations | `operation`, `a`, `b` | `calculator.py` |
|`get_current_datetime`| Returns live ISO datetime for a timezone | `timezone` | `datetime_tool.py` |
|`search_knowledge_base`| Searches indexed RAG documents |`query`, `top_k`|`knowledge_base_tool py` |

---

## Security Boundary
The LLM never has direct access to Python modules or runtime namespaces. It receives only tool metadata definitions. When the model requests a tool call, the backend verifies the tool name against `tool_registry.get_tool(name)`, ensuring that only pre-approved, safe functions can ever be executed.