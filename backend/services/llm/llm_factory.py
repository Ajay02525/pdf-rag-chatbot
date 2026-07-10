import os

from dotenv import load_dotenv

from services.llm.providers.ollama_provider import OllamaProvider

from services.llm.providers.gemini_provider import GeminiProvider

from .providers.groq_provider import GroqProvider

load_dotenv()


class LLMFactory:
    _provider = None

    @classmethod
    def get_provider(cls):
        if cls._provider is None:
            provider = os.getenv("LLM_PROVIDER", "ollama")

            if provider == "groq":
                cls._provider = GroqProvider()
            elif provider == "gemini":
                cls._provider = GeminiProvider()
            else:
                cls._provider = OllamaProvider()

        return cls._provider
