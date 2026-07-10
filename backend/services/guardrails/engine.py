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

from services.observability.metrics import (
    GUARDRAIL_BLOCKED,
    GUARDRAIL_LATENCY,
    GUARDRAIL_REQUESTS,
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

            GUARDRAIL_REQUESTS.labels(
                guardrail=guardrail_name,
            ).inc()

            GUARDRAIL_LATENCY.labels(
                guardrail=guardrail_name,
            ).observe(elapsed)

            if not result.allowed:
                GUARDRAIL_BLOCKED.labels(
                    guardrail=guardrail_name,
                ).inc()

                return result

        return GuardrailResult(
            allowed=True,
        )
