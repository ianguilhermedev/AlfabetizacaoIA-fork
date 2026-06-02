from __future__ import annotations

from alfabot.domain.enums import OnboardingState, PedagogicalLevel
from alfabot.services.response_builder import build_onboarding_buttons, build_welcome_message


class OnboardingService:
    def __init__(self, profile_service, meta_client):
        self.profile_service = profile_service
        self.meta_client = meta_client

    def start_onboarding(self, phone_number: str) -> dict:
        self.profile_service.mark_collecting_level(phone_number)
        try:
            self.meta_client.send_buttons(phone_number, build_onboarding_buttons())
        except Exception as exc:
            raise RuntimeError("onboarding_button_delivery_failed") from exc
        return {"phase": "onboarding_started"}

    def handle_level_selection(self, phone_number: str, level: PedagogicalLevel) -> dict:
        profile = self.profile_service.save_level(phone_number, level)
        try:
            self.meta_client.send_text(phone_number, build_welcome_message(level))
        except Exception as exc:
            raise RuntimeError("welcome_message_delivery_failed") from exc
        return {"phase": "level_saved", "level": profile.pedagogical_level, "state": profile.onboarding_state}
