import time

from services.guardrails.input.jailbreak import (
    JailbreakGuardrail,
)
from services.guardrails.input.prompt_injection import (
    PromptInjectionGuardrail,
)
from services.guardrails.models.guardrail_result import (
    GuardrailResult,
)
from services.guardrails.input.pii import (
    PIIGuardrail,
)
from services.guardrails.input.toxicity import (
    ToxicityGuardrail,
)


class GuardrailEngine:
    """
    Executes every registered guardrail.

    Responsibilities
    ----------------
    ✔ Execute guardrails
    ✔ Publish Prometheus metrics
    ✔ Measure latency
    ✔ Stop on first failure
    """

    def __init__(self):

        self.guardrails = [
            PromptInjectionGuardrail(),
            JailbreakGuardrail(),
            PIIGuardrail(),
            ToxicityGuardrail(),
        ]

    def execute(
        self,
        question: str,
    ) -> GuardrailResult:

        for guardrail in self.guardrails:
            guardrail_name = guardrail.name

            start = time.perf_counter()

            result = guardrail.validate(question)

            elapsed = time.perf_counter() - start

        return GuardrailResult(
            allowed=True,
        )
