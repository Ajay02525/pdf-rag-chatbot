from pydantic import BaseModel


class JudgeResult(BaseModel):
    grounded: bool

    hallucination: bool

    faithfulness: float

    completeness: float

    relevance: float

    unsupported_claims: list[str]

    reason: str
