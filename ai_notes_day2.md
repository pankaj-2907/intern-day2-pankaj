# AI Notes - Day 2 Assignment

### 1. What is an LLM API?
An **LLM (Large Language Model) API** is a bridge that allows your software application to communicate with a powerful AI model hosted on a remote server. Instead of running a massive AI model locally on your own computer, your code sends a structured request over the internet (via HTTP), and the LLM API processes it and sends back a text response. 
* **Practical Example:** When we build a customer support chatbot in FastAPI, your code doesn't generate answers itself; it uses the Google Gemini API to figure out what the customer is asking and generate a reply.

---

### 2. What happens when an application sends a request to an LLM API?
When app sends a request to an LLM API, several steps happen behind the scenes:
1. **Serialization:** Your application packages your prompt, settings (like model name), and credentials into a secure HTTP POST request (usually JSON).
2. **Transmission & Authentication:** The request travels over the internet to the AI provider's servers. The server checks your API key to ensure you are authorized.
3. **Processing:** The LLM receives the prompt, processes the tokens through its neural network layers, and predicts the next best sequence of words based on your instructions.
4. **Response:** The provider wraps the generated text back into an HTTP response and sends it to your application, where your code unpacks it and displays it to the user.

---

### 3. What is the purpose of an API key?
An **API key** is a unique, secret string of characters that acts as your application’s password and ID card when talking to an external service. Its main purposes are:
* **Authentication:** Proving who you are so the provider knows you have permission to access the model.
* **Rate Limiting & Billing:** Tracking how many requests your application makes so usage can be monitored, restricted, or billed accurately.
* **Security:** Preventing unauthorized users from stealing your quota or running up costs on your account.

---

### 4. What is the difference between a system instruction and user input?
* **System Instruction:** This is the underlying "rulebook" or persona given to the AI *before* the conversation starts. It dictates how the AI should behave, what tone to use, or safety constraints to follow. It persists across the session.
* **User Input:** This is the specific question, paragraph, or task provided by the end-user in real-time. It is the raw data the AI needs to process *right now*.
* **Practical Example:** If you build a translator app, your **system instruction** is *"You are a strict, professional French translator. Only output the translated text."* The **user input** is whatever sentence the user types in, like *"Hello, how are you today?"*

---

### 5. Why can an LLM return incorrect information?
LLMs are probabilistic prediction engines, not databases. They generate responses by predicting which words statistically follow the previous ones based on patterns in their training data. Because of this, they can return incorrect information due to:
* **Hallucinations:** Inventing facts, citations, or data that sound completely believable because they fit grammatical patterns, even if they are factually false.
* **Outdated Training Data:** If an event happened after the model's knowledge cutoff, it won't know the real facts unless provided via context.
* **Ambiguous Prompts:** If the user's prompt is vague, the model fills in the gaps with probabilistic guesses.

---

### 6. Why should an application validate an LLM's response?
An application should never blindly trust external data, including output from an AI model. Validating an LLM's response is crucial because:
* **Format Consistency:** If your app expects JSON data to populate a database or UI component, but the LLM returns conversational filler text, your app will crash. Validation ensures the structure matches your needs.
* **Safety :** Validation can catch offensive language, prompt injection leaks, or inappropriate content before it reaches your users.
* **Data Integrity:** Ensuring the response actually answers the query instead of returning empty strings or error messages.

---

### 7. What is the difference between an HTTP 400 error, a 401 error, a 429 error, and a 500 error?
These are standard HTTP status codes that tell your application why a request failed:
* **`400 Bad Request`:** The server couldn't understand the request because the client sent malformed data, invalid JSON, or failed validation rules (e.g., text was too short).
* **`401 Unauthorized`:** Authentication failed. Your application either forgot to include an API key, or the API key provided is invalid or expired.
* **`429 Too Many Requests`:** You have hit your rate limit (sent too many requests too fast) or exceeded your quota for the billing period.
* **`500 Internal Server Error`:** A generic catch-all error meaning something went wrong on the *remote server's* side (e.g., Google's AI servers crashed or experienced an unexpected bug).

---

### 8. Why should an AI API call have error handling?
External networks are inherently unpredictable. An AI API call should always be wrapped in error handling (`try...except` blocks) because:
* If the internet drops or the AI provider experiences a temporary outage (like a 503 service unavailable), unhandled exceptions will crash your entire backend server.
* Error handling allows your code to catch the failure and return a friendly, understandable message to your users (e.g., *"Our AI service is busy right now, please try again in a moment"*).
* It allows your application to log specific error codes, implement exponential backoff retry mechanisms, or fallback to secondary systems.