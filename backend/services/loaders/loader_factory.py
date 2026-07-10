from pathlib import Path

from services.loaders.pdf_loader import PDFLoader
from services.loaders.docx_loader import DOCXLoader
from services.loaders.txt_loader import TXTLoader


class LoaderFactory:
    LOADERS = {
        ".pdf": PDFLoader,
        ".docx": DOCXLoader,
        ".txt": TXTLoader,
    }

    @classmethod
    def is_supported(cls, filename: str) -> bool:
        return Path(filename).suffix.lower() in cls.LOADERS

    @classmethod
    def load(cls, file_path: str):
        extension = Path(file_path).suffix.lower()

        loader = cls.LOADERS.get(extension)
        if loader is None:
            raise ValueError(f"Unsupported file type: {extension}")

        return loader.load(file_path)
