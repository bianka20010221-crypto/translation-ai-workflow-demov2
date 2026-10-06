from __future__ import annotations

from .data import FICTIONAL_LINGUISTS
from .llm import LLMProvider, OfflineLLM
from .models import Candidate, Linguist, TranslationRequest


class WorkflowService:
    def __init__(self, llm: LLMProvider | None = None, linguists: tuple[Linguist, ...] = FICTIONAL_LINGUISTS):
        self.llm = llm or OfflineLLM()
        self.linguists = linguists

    def run(self, request: TranslationRequest) -> dict:
        self._validate(request)
        classification = self.llm.classify(request)
        candidates = self._rank_candidates(request, classification["domain"])
        selected = candidates[0] if candidates else None
        return {
            "project_id": request.project_id,
            "classification": classification,
            "assignment": selected.to_dict() if selected else None,
            "manual_review_required": selected is None,
            "project_brief": self._brief(request, classification, selected),
            "qa_checklist": self._qa_checklist(classification["domain"]),
            "client_email_draft": self._email(request, selected),
        }

    @staticmethod
    def _validate(request: TranslationRequest) -> None:
        if request.word_count <= 0 or request.due_in_hours <= 0:
            raise ValueError("word_count and due_in_hours must be positive")
        if request.source_language == request.target_language:
            raise ValueError("source and target language must differ")

    def _rank_candidates(self, request: TranslationRequest, domain: str) -> list[Candidate]:
        candidates = []
        for linguist in self.linguists:
            if request.language_pair not in linguist.language_pairs or linguist.available_words < request.word_count:
                continue
            specialty_match = domain in linguist.specialties
            score = linguist.quality_score * 10 + (20 if specialty_match else 0)
            reasons = [f"Supports {request.language_pair}", f"Capacity: {linguist.available_words} words", f"Quality: {linguist.quality_score}/5"]
            if specialty_match:
                reasons.append(f"Specialty match: {domain}")
            candidates.append(Candidate(linguist, score, tuple(reasons)))
        return sorted(candidates, key=lambda item: item.score, reverse=True)

    @staticmethod
    def _brief(request: TranslationRequest, classification: dict[str, str], selected: Candidate | None) -> str:
        assignee = selected.linguist.name if selected else "Manual coordinator review"
        return (
            f"Project {request.project_id}: {request.word_count} words, {request.language_pair}. "
            f"Domain: {classification['domain']}; priority: {classification['urgency']}. "
            f"Recommended assignee: {assignee}. Notes: {request.notes or 'None provided.'}"
        )

    @staticmethod
    def _qa_checklist(domain: str) -> list[str]:
        checklist = ["Confirm language-pair formatting conventions", "Run terminology consistency check", "Perform second-person review"]
        if domain in {"legal", "medical", "technical"}:
            checklist.append(f"Validate {domain} terminology against approved glossary")
        return checklist

    @staticmethod
    def _email(request: TranslationRequest, selected: Candidate | None) -> str:
        status = "is under coordinator review" if selected is None else "has been scheduled with a qualified linguist"
        return (
            f"Subject: Translation project {request.project_id} received\n\n"
            f"Hello {request.client_name},\n\nYour {request.language_pair} request ({request.word_count} words) {status}. "
            f"We will confirm delivery timing shortly.\n\nBest regards,\nTranslation Operations"
        )
