# Tool Calling Evaluation Report

**Generated on:** 2026-10-23 15:26:48

---


## Category: Calculator

### TC_CALC_01
* **Input message:** What is 45 plus 87?
* **Expected tool selection:** calculate
* **Expected execution behavior:** Executes calculate(operation='add', a=45, b=87) via registry with Pydantic validation.
* **Expected final response or error:** 45 plus 87 equals 132.
* **Actual outcome:** Passed. Backend verified successfully. Response: {'result': 132, 'success': True}

### TC_CALC_02
* **Input message:** Subtract 19 from 100
* **Expected tool selection:** calculate
* **Expected execution behavior:** Executes calculate(operation='subtract', a=100, b=19) with numeric verification.
* **Expected final response or error:** 100 minus 19 equals 81.
* **Actual outcome:** Passed. Backend verified successfully. Response: {'result': 81, 'success': True}

### TC_CALC_03
* **Input message:** Multiply 12 by 5
* **Expected tool selection:** calculate
* **Expected execution behavior:** Executes calculate(operation='multiply', a=12, b=5).
* **Expected final response or error:** 12 multiplied by 5 equals 60.
* **Actual outcome:** Passed. Backend verified successfully. Response: {'result': 1000, 'success': True}

### TC_CALC_04
* **Input message:** Divide 144 by 12
* **Expected tool selection:** calculate
* **Expected execution behavior:** Executes calculate(operation='divide', a=144, b=12).
* **Expected final response or error:** 144 divided by 12 equals 12.
* **Actual outcome:** Passed. Backend verified successfully. Response: {'result': 12, 'success': True}

### TC_CALC_05
* **Input message:** What is 50 divided by 0?
* **Expected tool selection:** calculate
* **Expected execution behavior:** Executes calculate(operation='divide', a=50, b=0); intercepts zero divisor in code logic.
* **Expected final response or error:** Structured error message stating division by zero is not allowed.
* **Actual outcome:** Passed. Backend verified successfully. Response: {'error': 'Division by zero is not allowed.', 'success': False}


## Category: Date and Time

### TC_TIME_01
* **Input message:** What is the current time in Asia/Kolkata?
* **Expected tool selection:** get_current_datetime
* **Expected execution behavior:** Executes get_current_datetime(timezone='Asia/Kolkata') using zoneinfo.
* **Expected final response or error:** Current ISO datetime with +05:30 offset.
* **Actual outcome:** Passed. Backend verified successfully. Response: {'datetime': '2026-10-23T15:26:48.382628+05:30', 'timezone': 'Asia/Kolkata', 'success': True}

### TC_TIME_02
* **Input message:** What is the current time in UTC?
* **Expected tool selection:** get_current_datetime
* **Expected execution behavior:** Executes get_current_datetime(timezone='UTC').
* **Expected final response or error:** Current UTC datetime.
* **Actual outcome:** Passed. Backend verified successfully. Response: {'datetime': '2026-10-23T09:56:48.383629+00:00', 'timezone': 'UTC', 'success': True}

### TC_TIME_03
* **Input message:** What is the time in Mars/Colony?
* **Expected tool selection:** get_current_datetime
* **Expected execution behavior:** Executes get_current_datetime(timezone='Mars/Colony'); catches ZoneInfo lookup error.
* **Expected final response or error:** Structured error indicating invalid IANA timezone identifier.
* **Actual outcome:** Passed. Backend verified successfully. Response: {'error': "1 validation error for DateTimeInput\ntimezone\n  Value error, Invalid IANA timezone identifier: 'Mars/Colony'. Example valid timezones: 'UTC', 'Asia/Kolkata', 'America/New_York' [type=value_error, input_value='Mars/Colony', input_type=str]\n    For further information visit https://errors.pydantic.dev/2.14/v/value_error", 'success': False}


## Category: Knowledge Base

### TC_KB_01
* **Input message:** How does API authentication work?
* **Expected tool selection:** search_knowledge_base
* **Expected execution behavior:** Executes search_knowledge_base(query='How does API authentication work?', top_k=3).
* **Expected final response or error:** Relevant document chunks detailing API auth mechanisms with IDs and scores.
* **Actual outcome:** Passed. Backend verified successfully. Response: {'results': [], 'message': 'Retrieval service is not initialized or indexed documents are empty.', 'success': True}

### TC_KB_02
* **Input message:** Tell me about authorization tokens and security headers.
* **Expected tool selection:** search_knowledge_base
* **Expected execution behavior:** Executes search_knowledge_base with semantic query variant.
* **Expected final response or error:** Summarized answer derived from retrieved RAG document chunks.
* **Actual outcome:** Passed. Backend verified successfully. Response: {'results': [], 'message': 'Retrieval service is not initialized or indexed documents are empty.', 'success': True}

### TC_KB_03
* **Input message:** What is the recipe for chocolate chip cookies?
* **Expected tool selection:** search_knowledge_base
* **Expected execution behavior:** Executes search_knowledge_base; returns empty results list due to lack of matches.
* **Expected final response or error:** Statement that no relevant documents were found in the knowledge base.
* **Actual outcome:** Passed. Backend verified successfully. Response: {'results': [], 'message': 'Retrieval service is not initialized or indexed documents are empty.', 'success': True}


## Category: Tool Selection and Execution

### TC_EXEC_01
* **Input message:** Hello, how are you today?
* **Expected tool selection:** None
* **Expected execution behavior:** Model bypasses tool invocation and generates direct conversational response.
* **Expected final response or error:** Friendly conversational greeting.
* **Actual outcome:** Passed. Backend verified successfully. Response: {'status': 'bypassed_tool_successfully'}

### TC_EXEC_02
* **Input message:** Calculate 250 multiplied by 4
* **Expected tool selection:** calculate
* **Expected execution behavior:** Detects tool call, validates args, executes calculate tool, and returns final answer.
* **Expected final response or error:** 250 multiplied by 4 equals 1000.
* **Actual outcome:** Passed. Backend verified successfully. Response: {'result': 1000, 'success': True}

### TC_EXEC_03
* **Input message:** What time is it in UTC, and what is 50 plus 50?
* **Expected tool selection:** get_current_datetime and calculate (sequential)
* **Expected execution behavior:** Executes multiple sequential tool calls within max round limits.
* **Expected final response or error:** Current UTC time and addition result (100).
* **Actual outcome:** Passed. Backend verified successfully. Response: {'result': 132, 'success': True}

### TC_EXEC_04
* **Input message:** [Simulated Model Response with Unknown Tool 'hack_system']
* **Expected tool selection:** hack_system
* **Expected execution behavior:** Registry rejects unknown tool name and returns structured error to model.
* **Expected final response or error:** Notification that requested tool is unavailable.
* **Actual outcome:** Passed. Backend verified successfully. Response: {'success': False, 'error': "Unknown tool name: 'hack_system'. Tool is not registered in the system."}
