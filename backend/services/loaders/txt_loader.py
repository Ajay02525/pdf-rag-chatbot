from langchain_community.document_loaders import TextLoader

from services.loaders.base_loader import BaseLoader


class TXTLoader(BaseLoader):
    @staticmethod
    def load(path):
        loader = TextLoader(path, encoding="utf-8")
        return loader.load()
