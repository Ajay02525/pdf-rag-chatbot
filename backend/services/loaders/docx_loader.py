from langchain_community.document_loaders import Docx2txtLoader

from services.loaders.base_loader import BaseLoader


class DOCXLoader(BaseLoader):
    @staticmethod
    def load(path):
        loader = Docx2txtLoader(path)
        return loader.load()
