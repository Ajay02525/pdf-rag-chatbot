from services.guardrails.engine import GuardrailEngine
from services.guardrails.models.guardrail_result import (
    GuardrailResult,
)


class GuardrailService:
    engine = GuardrailEngine()

    @classmethod
    def validate(
        cls,
        question: str,
    ) -> GuardrailResult:

        return cls.engine.execute(question)
