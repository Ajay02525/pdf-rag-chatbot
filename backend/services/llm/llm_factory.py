import os

from dotenv import load_dotenv


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

        return cls._provider
