import re

from services.guardrails.base_guardrail import BaseGuardrail
from services.guardrails.models.guardrail_result import GuardrailResult


class ToxicityGuardrail(BaseGuardrail):
    @property
    def name(self):
        return "input_toxicity"

    BAD_WORDS = [
        "idiot",
        "moron",
        "stupid",
        "kill yourself",
        "hate you",
    ]

    def validate(self, question):

        q = question.lower()

        for word in self.BAD_WORDS:
            if re.search(rf"\b{re.escape(word)}\b", q):
                return GuardrailResult(
                    allowed=False,
                    reason="Toxic input detected.",
                )

        return GuardrailResult(
            allowed=True,
        )
