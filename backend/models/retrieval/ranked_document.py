from dataclasses import dataclass

from langchain_core.documents import Document


@dataclass
class RankedDocument:
    """
    A retrieved document together with its reranker score.
    """

    document: Document
    score: float
