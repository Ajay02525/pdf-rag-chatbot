from pathlib import Path
import logging

from langchain_core.documents import Document
from docling.document_converter import DocumentConverter

logger = logging.getLogger(__name__)


class DoclingLoader:
    _converter = DocumentConverter()

    @classmethod
    def load(cls, file_path: str) -> list[Document]:
        try:
            result = cls._converter.convert(file_path)

            markdown = result.document.export_to_markdown()

            metadata = {
                "source": Path(file_path).name,
                "parser": "docling",
            }

            return [
                Document(
                    page_content=markdown,
                    metadata=metadata,
                )
            ]

        except Exception as e:
            logger.exception("Docling failed.")

            raise RuntimeError(f"Failed to parse {file_path}") from e
