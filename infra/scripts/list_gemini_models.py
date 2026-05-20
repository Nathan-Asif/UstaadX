import os
import sys
from pathlib import Path
import google.generativeai as genai

backend_dir = Path(__file__).parent.parent.parent / "apps" / "backend_api"
sys.path.insert(0, str(backend_dir))

# pyrefly: ignore [missing-import]
from app.core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

print("Available models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
