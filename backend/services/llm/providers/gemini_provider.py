import os

from google import genai
from dotenv import load_dotenv

from .base_provider import BaseProvider

load_dotenv()


class GeminiProvider(BaseProvider):
    def __init__(self):

        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

        self.model = "gemini-2.5-flash"

    def generate(self, prompt: str) -> str:

        response = self.client.models.generate_content(
            model=self.model, contents=prompt
        )

        return response.text

    def stream(self, prompt: str):

        return self.client.models.generate_content_stream(
            model=self.model, contents=prompt
        )
