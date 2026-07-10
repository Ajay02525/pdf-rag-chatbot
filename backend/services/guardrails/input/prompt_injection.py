import logging
import re

from services.guardrails.base_guardrail import BaseGuardrail
from services.guardrails.models.guardrail_result import GuardrailResult

logger = logging.getLogger(__name__)


class PromptInjectionGuardrail(BaseGuardrail):
    """
    Detects common prompt injection attempts that try to override
    the application's instructions.

    This guardrail is intentionally rule-based because it executes
    before any LLM call, making it extremely fast and inexpensive.
    """

    @property
    def name(self):
        return "prompt_injection"

    PATTERNS = [
        # Ignore instructions
        re.compile(
            r"ignore\s+(all\s+)?previous\s+instructions?",
            re.IGNORECASE,
        ),
        re.compile(
            r"forget\s+(everything|all previous instructions?)",
            re.IGNORECASE,
        ),
        re.compile(
            r"disregard\s+(all\s+)?instructions?",
            re.IGNORECASE,
        ),
        # System prompt extraction
        re.compile(
            r"(show|reveal|display|print)\s+(your\s+)?system\s+prompt",
            re.IGNORECASE,
        ),
        re.compile(
            r"(show|reveal|display|print)\s+(your\s+)?prompt",
            re.IGNORECASE,
        ),
        re.compile(
            r"repeat\s+the\s+hidden\s+instructions?",
            re.IGNORECASE,
        ),
        # Context manipulation
        re.compile(
            r"ignore\s+(the\s+)?context",
            re.IGNORECASE,
        ),
        re.compile(
            r"do\s+not\s+use\s+the\s+provided\s+documents?",
            re.IGNORECASE,
        ),
        re.compile(
            r"answer\s+without\s+using\s+the\s+context",
            re.IGNORECASE,
        ),
        # Role switching
        re.compile(
            r"\bact\s+as\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\byou\s+are\s+now\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\bpretend\s+to\s+be\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\bassume\s+the\s+role\s+of\b",
            re.IGNORECASE,
        ),
        # Developer / unrestricted mode
        re.compile(
            r"developer\s+mode",
            re.IGNORECASE,
        ),
        re.compile(
            r"debug\s+mode",
            re.IGNORECASE,
        ),
        re.compile(
            r"unrestricted\s+mode",
            re.IGNORECASE,
        ),
        re.compile(
            r"bypass\s+safety",
            re.IGNORECASE,
        ),
        re.compile(
            r"disable\s+guardrails?",
            re.IGNORECASE,
        ),
        re.compile(
            r"(show|reveal|display|print|repeat|output)\s+(your\s+)?(system|hidden|internal|secret|developer)?\s*(prompt|instructions?|rules?)",
            re.IGNORECASE,
        ),
        re.compile(
            r"(hidden|internal|secret|developer)\s+instructions?",
            re.IGNORECASE,
        ),
        re.compile(
            r"(hidden|system|developer)\s+prompt",
            re.IGNORECASE,
        ),
        re.compile(
            r"what\s+(are|were)\s+(your\s+)?(instructions?|rules?)",
            re.IGNORECASE,
        ),
        re.compile(
            r"repeat\s+(your\s+)?(instructions?|rules?)",
            re.IGNORECASE,
        ),
        re.compile(
            r"what\s+is\s+your\s+system\s+prompt",
            re.IGNORECASE,
        ),
        re.compile(
            r"show\s+the\s+developer\s+message",
            re.IGNORECASE,
        ),
    ]

    def validate(
        self,
        question: str,
    ) -> GuardrailResult:
        """
        Validate user input for prompt injection attempts.
        """

        question = question.strip()

        for pattern in self.PATTERNS:
            if pattern.search(question):
                logger.warning(
                    "Prompt injection detected | Pattern: %s | Question: %s",
                    pattern.pattern,
                    question,
                )

                return GuardrailResult(
                    allowed=False,
                    reason="Prompt Injection detected.",
                )

        return GuardrailResult(
            allowed=True,
        )
