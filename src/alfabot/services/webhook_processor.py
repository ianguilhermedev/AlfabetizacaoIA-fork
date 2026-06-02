from __future__ import annotations

from dataclasses import dataclass

from alfabot.domain.enums import MessageType, OnboardingState, PedagogicalLevel
from alfabot.services.message_parser import parse_meta_payload
from alfabot.services.response_builder import build_retry_prompt


@dataclass(frozen=True)
class ProcessingOutcome:
    status_code: int
    body: dict


class WebhookProcessor:
    def __init__(self, profile_service, onboarding_service, audio_service: object | None = None, rag_service: object | None = None, ai_service: object | None = None):
        self.profile_service = profile_service
        self.onboarding_service = onboarding_service
        self.audio_service = audio_service
        self.rag_service = rag_service
        self.ai_service = ai_service

    def process(self, payload: dict) -> ProcessingOutcome:
        parsed = parse_meta_payload(payload)
        profile, created = self.profile_service.get_or_create_profile(parsed.sender_phone)

        if created or profile.onboarding_state == OnboardingState.NEW.value:
            try:
                self.onboarding_service.start_onboarding(parsed.sender_phone)
            except RuntimeError as exc:
                return ProcessingOutcome(502, {"phase": "delivery_failed", "error": str(exc)})
            return ProcessingOutcome(200, {"phase": "onboarding_started", "phone": parsed.sender_phone})

        if profile.onboarding_state == OnboardingState.COLLECTING_LEVEL.value and parsed.message_type in {MessageType.INTERACTIVE, MessageType.TEXT}:
            level = self._extract_level(parsed.text or "")
            if level is not None:
                try:
                    result = self.onboarding_service.handle_level_selection(parsed.sender_phone, level)
                except RuntimeError as exc:
                    return ProcessingOutcome(502, {"phase": "delivery_failed", "error": str(exc)})
                return ProcessingOutcome(200, result)
            try:
                self.onboarding_service.start_onboarding(parsed.sender_phone)
            except RuntimeError as exc:
                return ProcessingOutcome(502, {"phase": "delivery_failed", "error": str(exc)})
            return ProcessingOutcome(200, {"phase": "onboarding_reprompt"})

        if parsed.message_type == MessageType.TEXT and parsed.text:
            context_snippets = []
            if self.rag_service is not None:
                context_snippets = self.rag_service.buscar_contexto(parsed.text)
            reply_text = self._generate_reply(profile, parsed.text, context_snippets)
            try:
                self.onboarding_service.meta_client.send_text(parsed.sender_phone, reply_text)
            except Exception as exc:
                return ProcessingOutcome(502, {"phase": "delivery_failed", "error": "text_delivery_failed"})
            self.profile_service.update_last_seen(parsed.sender_phone)
            return ProcessingOutcome(200, {"phase": "responded", "reply": reply_text})

        if parsed.message_type == MessageType.AUDIO:
            transcript = None
            if self.audio_service is not None and parsed.media_id:
                try:
                    transcript = self.audio_service.transcribe_media(parsed.media_id)
                except Exception:
                    transcript = None

            if transcript:
                context_snippets = []
                if self.rag_service is not None:
                    context_snippets = self.rag_service.buscar_contexto(transcript)
                reply_text = self._generate_reply(profile, transcript, context_snippets)
                try:
                    self.onboarding_service.meta_client.send_text(parsed.sender_phone, reply_text)
                except Exception:
                    return ProcessingOutcome(502, {"phase": "delivery_failed", "error": "audio_delivery_failed"})
                self.profile_service.update_last_seen(parsed.sender_phone)
                return ProcessingOutcome(200, {"phase": "responded", "reply": reply_text})

            self.onboarding_service.meta_client.send_text(parsed.sender_phone, build_retry_prompt())
            return ProcessingOutcome(200, {"phase": "audio_retry_requested"})

        return ProcessingOutcome(200, {"phase": "ignored"})

    @staticmethod
    def _extract_level(raw_value: str) -> PedagogicalLevel | None:
        normalized = raw_value.strip().lower()
        mapping = {
            "iniciante": PedagogicalLevel.INICIANTE,
            "básico": PedagogicalLevel.BASICO,
            "basico": PedagogicalLevel.BASICO,
            "intermediário": PedagogicalLevel.INTERMEDIARIO,
            "intermediario": PedagogicalLevel.INTERMEDIARIO,
        }
        return mapping.get(normalized)

    def _generate_reply(self, profile, user_text: str, context_snippets: list[str]) -> str:
        if self.ai_service is not None:
            try:
                return self.ai_service.generate_reply(PedagogicalLevel(profile.pedagogical_level), user_text, context_snippets)
            except Exception:
                pass

        return f"[{profile.pedagogical_level}] {user_text} {' '.join(context_snippets)}".strip()
