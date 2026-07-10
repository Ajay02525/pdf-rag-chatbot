from dataclasses import dataclass, field
from typing import Any


from models.retrieval.ranked_document import RankedDocument


@dataclass
class RetrievalResult:
    """
    Final output produced by the retrieval pipeline.
    """

    documents: list[RankedDocument]

    retrieved_chunks: int

    highest_score: float

    average_score: float

    execution: list[dict[str, Any]] = field(default_factory=list)
