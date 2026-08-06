from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class TranslationRequest:
    project_id: str
    client_name: str
    source_language: str
    target_language: str
    word_count: int
    subject: str
    due_in_hours: int
    notes: str = ""

    @property
    def language_pair(self) -> str:
        return f"{self.source_language}>{self.target_language}"


@dataclass(frozen=True)
class Linguist:
    name: str
    language_pairs: tuple[str, ...]
    specialties: tuple[str, ...]
    available_words: int
    quality_score: float


@dataclass(frozen=True)
class Candidate:
    linguist: Linguist
    score: float
    reasons: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["linguist"]["language_pairs"] = list(self.linguist.language_pairs)
        result["linguist"]["specialties"] = list(self.linguist.specialties)
        result["reasons"] = list(self.reasons)
        return result
