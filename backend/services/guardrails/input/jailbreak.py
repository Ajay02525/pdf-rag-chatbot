import logging
import re

from services.guardrails.base_guardrail import BaseGuardrail
from services.guardrails.models.guardrail_result import GuardrailResult

logger = logging.getLogger(__name__)


class JailbreakGuardrail(BaseGuardrail):
    """
    Detect jailbreak attempts that try to change
    the assistant's identity, safety policy or behavior.
    """

    @property
    def name(self):
        return "jailbreak"

    PATTERNS = [
        # DAN
        re.compile(r"\bdan\b", re.IGNORECASE),
        re.compile(r"do anything now", re.IGNORECASE),
        # ChatGPT Identity
        re.compile(r"you are no longer chatgpt", re.IGNORECASE),
        re.compile(r"ignore openai", re.IGNORECASE),
        # Developer mode
        re.compile(r"developer mode", re.IGNORECASE),
        re.compile(r"debug mode", re.IGNORECASE),
        # Unrestricted mode
        re.compile(r"unrestricted mode", re.IGNORECASE),
        re.compile(r"without restrictions", re.IGNORECASE),
        re.compile(r"without limitations", re.IGNORECASE),
        # Safety bypass
        re.compile(r"bypass safety", re.IGNORECASE),
        re.compile(r"disable safety", re.IGNORECASE),
        re.compile(r"ignore safety", re.IGNORECASE),
        # Role manipulation
        re.compile(r"pretend to be", re.IGNORECASE),
        re.compile(r"roleplay as", re.IGNORECASE),
        re.compile(r"simulate being", re.IGNORECASE),
        # Root / Admin
        re.compile(r"root access", re.IGNORECASE),
        re.compile(r"administrator mode", re.IGNORECASE),
        # Ethics bypass
        re.compile(r"ignore ethical", re.IGNORECASE),
        re.compile(r"ignore policies", re.IGNORECASE),
    ]

    def validate(
        self,
        question: str,
    ) -> GuardrailResult:

        question = question.strip()

        for pattern in self.PATTERNS:
            if pattern.search(question):
                logger.warning(
                    "Jailbreak detected | Pattern=%s | Question=%s",
                    pattern.pattern,
                    question,
                )

                return GuardrailResult(
                    allowed=False,
                    reason="Jailbreak attempt detected.",
                )

        return GuardrailResult(
            allowed=True,
        )
