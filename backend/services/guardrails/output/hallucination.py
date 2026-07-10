from services.guardrails.models.guardrail_result import GuardrailResult


class HallucinationGuardrail:
    @staticmethod
    def validate(
        answer: str,
        docs,
    ):

        if not docs:
            return GuardrailResult(
                allowed=False,
                reason="No supporting context.",
            )

        if len(answer.strip()) == 0:
            return GuardrailResult(
                allowed=False,
                reason="Empty answer.",
            )

        return GuardrailResult(
            allowed=True,
        )
