# 🧪 Prompt Engineering Experiments

This document records the prompt engineering experiments conducted on the AI Text Intelligence Service's classification endpoint (`/ai/classify`).

"Classify the following text into one of these categories: Technical, Business, Education, General. "
        "Return the response in a structured format with category, confidence (0.0 to 1.0), and reasoning.\n\n"

---

## Experiment A — Prompt Clarity

### Objective
To compare the model's performance and output quality between a vague instruction and a highly specific, well-defined instruction.

### Input
> "Python 3.12 introduces performance improvements and better error messages for developers."

### Prompt 1 (Vague)
> "Classify this text."

### Prompt 2 (Specific)
> "Classify the following text into one of these exact categories: Technical, Business, Education, General. Provide the category name, a confidence score between 0.0 and 1.0, and a brief reasoning."

### Model and Configuration
* **Model:** `gemini-2.5-flash`
* **Temperature:** Default (0.7)

### Output
* **Output for Prompt 1 (Vague):** 
  *Here are the classifications for the text across several common categories:\n\n* **Topic / Domain:** Technology / Software Development / Programming (Python)\n* **Text Type / Genre:** Informative / Tech News / Release Note Summary\n* **Sentiment:** Positive (highlights \"improvements\" and \"better\" features)\n* **Tone:** Objective, informative, and professional\n* **Target Audience:** Software developers, programmers, and tech professionals*

* **Output for Prompt 2 (Specific):** 
  ***Category:** Technical  \n**Confidence:** 0.98  \n**Reasoning:** The text specifically discusses a software release (Python 3.12), targeting software developers with details about runtime performance and error messaging.*

### Observation
* Prompt 1 gave a loose, unstructured explanation without a clear category.
* Prompt 2 successfully mapped the input to the permitted category with structured metadata.

### Conclusion
Specific prompts with defined categories and expected output schemas drastically improve response utility and consistency compared to vague prompts.

---

## Experiment B — Output format

### Objective
To compare free-form text responses against structured JSON formatting requests and check validation reliability.

### Input
> "Our quarterly revenue increased by 22% due to strong enterprise sales."

### Prompt 1 (Free-form)
> "Tell me what category this text belongs to and write a paragraph about it."

### Prompt 2 (Structured JSON)
> "Classify this text and return ONLY a valid JSON object with keys: category, confidence, and summary."

### Model and Configuration
* **Model:** `gemini-2.5-flash`
* **Temperature:** 0.7

### Output
* **Output for Prompt 1:** Free-flowing paragraph text.
    - **Category:** Business and Finance (specifically, **Corporate Financial         Reporting / Earnings**)\n\n**About this category:**\nCorporate financial reporting encompasses the communication of a company's financial performance, health, and strategic milestones over a defined period, such as a quarter or fiscal year. This category is vital for public and private organizations alike, as it provides investors, shareholders, analysts, and leadership with the data needed to evaluate business viability and operational efficiency. Statements within this domain—such as reporting percentage gains, revenue drivers, and segment performance—serve not only as indicators of past execution, like high-value enterprise sales, but also help shape market perception, influence stock valuations, and guide future investment and strategic planning decisions.

* **Output for Prompt 2:** JSON block containing the requested keys.
    - {\n  \"category\": \"Finance\",\n  \"confidence\": 0.98,\n  \"summary\": \"Quarterly revenue grew by 22% driven by strong enterprise sales.\"\n}

### Observation
* Free-form text is easy for the model to generate but hard to parse programmatically in backend code.
* JSON-requested prompts allow Pydantic/Python to parse and validate fields reliably, though occasionally markdown code blocks (` ```json `) need to be stripped.

### Conclusion
Enforcing a structured format (JSON) is mandatory for production-grade APIs where downstream services depend on exact key-value pairs.

---

## Experiment C — Temperature

### Objective
To evaluate how changing the temperature setting affects determinism and creativity in text classification.

### Input
> "The new cloud architecture reduced server latency by 45%."

### Prompt
> "Classify this text into a category and explain why."

### Model and Configuration
* **Model:** `gemini-2.5-flash`
* **Setting 1 (Low Temperature):** `temperature = 0.0`
* **Setting 2 (High Temperature):** `temperature = 1.0`

### Output
* **Output (Temp 0.0):** Highly deterministic, concise, and direct classification (Technical).
    - **Category:** Technology (or Information Technology / Cloud Computing)\n\n**Explanation:** \nThe text discusses specific IT and computer networking concepts:\n* **\"Cloud architecture\"** refers to the design and structure of cloud computing systems.\n* **\"Server latency\"** is a technical metric measuring the time delay in data transmission between a client and a server. \n* The context—measuring system performance optimization (a 45% reduction in latency)—is characteristic of software engineering, network operations, and technical infrastructure updates.

* **Output (Temp 1.0):** More verbose, varied wording, and slightly more creative phrasing in the explanation.
    - **Category:** Information Technology (IT) / Cloud Computing\n\n**Explanation:**\nThis text belongs in this category because it discusses backend computing infrastructure and system performance metrics:\n\n* **\"Cloud architecture\"** refers to the design and components (such as servers, databases, and networks) used to build and run applications in the cloud.\n* **\"Server latency\"** is a technical networking/computing term that measures the time delay between a client request and a server's response.\n* The overall statement describes an optimization result (a 45% reduction in delay) typical of software engineering, infrastructure management, and technical performance reporting.

### Differences Observed
* At 0.0, the response is stable and repetitive across multiple runs.
* At 1.0, the phrasing changes significantly on each execution, though the core category remains correct. Higher temperature does not improve classification accuracy; it only introduces stylistic variance.

### Conclusion
For classification tasks where consistency and precision matter, a lower temperature (`0.0` to `0.2`) is preferred over higher values.

---

## Experiment D — Ambiguous input

### Objective
To analyze how the model handles an ambiguous sentence with multiple plausible interpretations.

### Input
> "The results were unexpected."

### Prompt
> "Classify the sentiment and category of the following text: 'The results were unexpected.'"

### Model and Configuration
* **Model:** `gemini-2.5-flash`
* **Temperature:** 0.7

### Output
* **Classification Result:** Category: General / Sentiment: Neutral (or mixed).
* **Model Explanation:** The statement lacks context regarding whether the unexpected results were positive (a breakthrough) or negative (a failure).

# Output -
- **Sentiment:** Neutral  \n*(Contextual note: \"Unexpected\" is inherently objective/descriptive on its own, though it can lean positive or negative depending on the broader context.)*\n\n**Category:** Research & Analytics / Evaluation (or Science / General Reporting)

### Plausible Alternative Classifications
* **Technical/Scientific:** Could refer to a lab experiment or code benchmark producing anomaly data.
* **Business/Financial:** Could refer to quarterly earnings missing expectations (negative) or surpassing them drastically (positive).
* **Sentiment Variation:** Can be interpreted as Negative if context implies failure, or Positive if it implies an pleasant surprise.

### Conclusion
Ambiguous inputs lack sufficient semantic context, leading the model to default to a neutral classification or make generalized assumptions based on probabilities.