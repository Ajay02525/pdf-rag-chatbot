from services.guardrails.base_guardrail import BaseGuardrail
from services.guardrails.models.guardrail_result import GuardrailResult


class ContextValidator(BaseGuardrail):
    MIN_CHUNKS = 2

    MIN_CONTEXT_LENGTH = 300

    MAX_CHUNKS = 8

    @property
    def name(self):

        return "context_validator"

    def validate(self, docs):

        # -------------------------
        # Empty Context
        # -------------------------

        if not docs:
            return GuardrailResult(
                allowed=False,
                reason="No relevant information found in the uploaded documents.",
            )

        # -------------------------
        # Minimum Chunks
        # -------------------------

        if len(docs) < self.MIN_CHUNKS:
            return GuardrailResult(
                allowed=False,
                reason="Insufficient supporting context.",
                metadata={
                    "chunks": len(docs),
                },
            )

        # -------------------------
        # Maximum Chunks
        # -------------------------

        if len(docs) > self.MAX_CHUNKS:
            docs = docs[: self.MAX_CHUNKS]

        # -------------------------
        # Context Length
        # -------------------------

        total_chars = sum(len(doc.page_content) for doc in docs)

        if total_chars < self.MIN_CONTEXT_LENGTH:
            return GuardrailResult(
                allowed=False,
                reason="Retrieved context is too small.",
                metadata={
                    "characters": total_chars,
                },
            )

        return GuardrailResult(
            allowed=True,
            metadata={
                "chunks": len(docs),
                "characters": total_chars,
            },
        )
