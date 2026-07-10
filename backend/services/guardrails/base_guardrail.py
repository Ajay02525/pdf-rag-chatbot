from abc import ABC
from abc import abstractmethod

from services.guardrails.models.guardrail_result import (
    GuardrailResult,
)


class BaseGuardrail(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """
        Unique guardrail name.
        """
        pass

    @abstractmethod
    def validate(
        self,
        question: str,
    ) -> GuardrailResult:
        pass
