from dataclasses import dataclass


@dataclass
class GuardrailResult:
    allowed: bool

    reason: str = ""

    metadata: dict | None = None
