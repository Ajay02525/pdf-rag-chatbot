from groq import Groq
from config.setting import settings
from .base_provider import BaseProvider
from services.observability.decorators import measure_latency


class GroqProvider(BaseProvider):
    def __init__(self):

        self.client = Groq(api_key=settings.GROQ_API_KEY)

        self.model = settings.GROQ_MODEL

    @measure_latency("llm")
    def generate(self, prompt: str) -> str:

        response = self.client.chat.completions.create(
            model=self.model, messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    def stream(self, prompt: str):

        stream = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )

        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield (chunk.choices[0].delta.content)
