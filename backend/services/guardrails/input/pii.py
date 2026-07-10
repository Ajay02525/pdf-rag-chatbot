import logging
import re

from services.guardrails.base_guardrail import BaseGuardrail
from services.guardrails.models.guardrail_result import GuardrailResult

logger = logging.getLogger(__name__)


class PIIGuardrail(BaseGuardrail):
    @property
    def name(self):
        return "input_pii"

    PATTERNS = {
        "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
        "phone": re.compile(r"\b(?:\+91[- ]?)?[6-9]\d{9}\b"),
        "aadhaar": re.compile(r"\b\d{4}\s?\d{4}\s?\d{4}\b"),
        "pan": re.compile(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"),
        "credit_card": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
    }

    def validate(
        self,
        question: str,
    ) -> GuardrailResult:

        for pii_type, pattern in self.PATTERNS.items():
            if pattern.search(question):
                logger.warning(
                    "%s detected in input",
                    pii_type,
                )

                return GuardrailResult(
                    allowed=False,
                    reason=f"{pii_type.upper()} detected in user input.",
                )

        return GuardrailResult(
            allowed=True,
        )
