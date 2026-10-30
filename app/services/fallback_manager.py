import logging
import time
from app.services.groq_service import GroqProvider
from app.services.gemini_service import GeminiProvider
from app.services.huggingface_service import HuggingFaceProvider
from app.services.ollama_service import OllamaProvider

logger = logging.getLogger(__name__)

class FallbackLLMOrchestrator:
    def __init__(self):
        # Priority Chain: Groq -> Gemini -> Hugging Face -> Ollama
        self.providers = [
            GroqProvider(),
            GeminiProvider(),
            HuggingFaceProvider(),
            OllamaProvider()
        ]

    def generate(self, contents, tools=None):
        last_exception = None

        for provider in self.providers:
            try:
                logger.info(f"--- [LOOP START] Attempting generation with provider: {provider.name} ---")
                
                start_time = time.time()
                response = provider.generate(contents, tools=tools)
                duration = time.time() - start_time
                
                logger.info(f"Successfully generated response using {provider.name} in {duration:.2f} seconds")
                return response, provider.name, duration
                
            except Exception as e:
                logger.error(f"!! Provider [{provider.name}] CRASHED with error: {str(e)} !!")
                error_str = str(e).lower()
                last_exception = e
                
                # Check for Rate Limits (429), Exhaustion, Quotas, Credits, Timeouts, or Connection errors
                is_exhausted_or_limited = any(term in error_str for term in [
                    "429", "402", "rate limit", "resource exhausted", "quota", 
                    "exhausted", "too many requests", "payment required", "credits"
                ])
                
                is_timeout_or_crash = any(term in error_str for term in [
                    "timeout", "connection", "server error", "503", "500", "unavailable"
                ])
                
                # Agar inme se koi bhi cloud provider error aati hai, toh next fallback par jao
                if is_exhausted_or_limited or is_timeout_or_crash:
                    logger.warning(
                        f"Provider [{provider.name}] failed/exhausted with error: {e}. "
                        f"Falling back to the next provider..."
                    )
                    continue
                else:
                    # Agar koi code validation/syntax error hai, toh raise karo
                    raise e
                    
        raise Exception(f"All model providers exhausted or failed. Last error: {str(last_exception)}")

    def generate_stream(self, contents, tools=None):
        """Tries providers in fallback order for streaming chunks."""
        for provider in self.providers:
            try:
                # Har provider ki apni streaming client call yahan handle hogi
                for chunk in provider.stream(contents, tools=tools):
                    yield chunk, provider.name
                return
            except Exception as e:
                logger.warning(f"Provider {provider.name} streaming failed: {str(e)}, trying next...")
        raise Exception("All fallback providers failed streaming.")

    """ def generate(self, contents, tools=None):
        last_exception = None

        for provider in self.providers:
            try:
                logger.info(f"Attempting generation with provider: {provider.name}")
                
                # Start timer before calling provider
                start_time = time.time()
                
                # Call provider's generate method
                response = provider.generate(contents, tools=tools)
                
                # Calculate total duration taken by this provider
                duration = time.time() - start_time
                
                logger.info(f"Successfully generated response using {provider.name} in {duration:.2f} seconds")
                
                # Return response, provider name, and duration
                return response, provider.name, duration

            except groq.RateLimitError as e:
                logger.warning(f"Groq Rate Limit Triggered (429)! Switching to next provider. Error: {e}")
                last_exception = e
                continue
                
            except groq.APIStatusError as e:
                # Agar status code 429 (Rate limit) ya 5xx (Server down) hai
                if e.status_code == 429 or e.status_code >= 500:
                    logger.warning(f"Groq API Error Status {e.status_code}! Switching to next provider.")
                    last_exception = e
                    continue
                else:
                    raise e # Agar bad request ya invalid API key hai toh crash hone dein
                
            except Exception as e:
                error_str = str(e).lower()
                last_exception = e
                
                # Check for Rate Limits (429), Exhaustion, Quotas, Timeouts, or Connection errors
                is_exhausted_or_limited = any(term in error_str for term in [
                    "429", "rate limit", "resource exhausted", "quota", "exhausted"
                ])
                
                is_timeout_or_crash = any(term in error_str for term in [
                    "timeout", "connection", "server error", "503", "500", "unavailable"
                ])
                
                if is_exhausted_or_limited or is_timeout_or_crash:
                    logger.warning(
                        f"Provider [{provider.name}] failed/exhausted with error: {e}. "
                        f"Falling back to the next provider..."
                    )
                    continue
                else:
                    # Agar koi code/logic error hai jo model se related nahi hai, toh raise karo
                    raise e
                    
        raise Exception(f"All model providers exhausted or failed. Last error: {str(last_exception)}") """

    