import json
import google.generativeai as genai
from app.core.config import settings

# Configure the Gemini API client globally
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

class LLMService:
    """Service to interact with Google's Gemini LLM."""
    
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        # We use gemini-2.5-flash as the default for fast, cost-effective reasoning
        self.model = genai.GenerativeModel(model_name)

    async def generate_response(self, prompt: str, temperature: float = 0.7) -> str:
        """Generate a raw text response from the model."""
        response = await self.model.generate_content_async(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
            )
        )
        return response.text

    async def generate_json_response(self, prompt: str, temperature: float = 0.2) -> dict:
        """
        Generate a JSON response from the model. 
        Ensures the output is structured JSON.
        """
        # Using response_mime_type="application/json" forces JSON output
        response = await self.model.generate_content_async(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                response_mime_type="application/json",
            )
        )
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            # Fallback in case the model wraps the JSON in markdown code blocks
            cleaned = response.text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:-3]
            elif cleaned.startswith("```"):
                cleaned = cleaned[3:-3]
            return json.loads(cleaned.strip())

# Global singleton instance for easy imports
llm_service = LLMService()
