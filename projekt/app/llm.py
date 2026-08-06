from __future__ import annotations

from abc import ABC, abstractmethod

from .models import TranslationRequest


class LLMProvider(ABC):
    """Minimal provider interface; replace OfflineLLM with a real adapter in production."""

    @abstractmethod
    def classify(self, request: TranslationRequest) -> dict[str, str]:
        raise NotImplementedError


class OfflineLLM(LLMProvider):
    """Deterministic, API-free classifier for a runnable portfolio demo."""

    def classify(self, request: TranslationRequest) -> dict[str, str]:
        subject = request.subject.lower()
        domain = next(
            (term for term in ("legal", "medical", "technical", "marketing") if term in subject),
            "general",
        )
        urgency = "urgent" if request.due_in_hours <= 24 else "standard"
        return {"domain": domain, "urgency": urgency}
