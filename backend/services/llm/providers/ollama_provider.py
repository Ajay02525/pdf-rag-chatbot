from langchain_ollama import ChatOllama

from .base_provider import BaseProvider


class OllamaProvider(BaseProvider):
    def __init__(self):

        self.llm = ChatOllama(model="phi3:latest ", think=False)

    def generate(self, prompt: str) -> str:

        response = self.llm.invoke(prompt)

        return response.content

    def stream(self, prompt: str):

        return self.llm.stream(prompt)
