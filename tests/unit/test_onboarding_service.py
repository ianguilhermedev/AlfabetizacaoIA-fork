from __future__ import annotations

from alfabot.domain.enums import PedagogicalLevel
from alfabot.services.onboarding_service import OnboardingService


class DummyProfileService:
    def __init__(self):
        self.marked = []
        self.saved = []

    def mark_collecting_level(self, phone_number):
        self.marked.append(phone_number)

    def save_level(self, phone_number, level):
        self.saved.append((phone_number, level))
        return type("Profile", (), {"pedagogical_level": level.value, "onboarding_state": "active"})()


class DummyMetaClient:
    def __init__(self):
        self.sent_buttons = []
        self.sent_text = []

    def send_buttons(self, to, payload):
        self.sent_buttons.append((to, payload))

    def send_text(self, to, body):
        self.sent_text.append((to, body))


def test_start_onboarding_marks_collecting_level_and_sends_buttons():
    profile_service = DummyProfileService()
    meta_client = DummyMetaClient()
    service = OnboardingService(profile_service, meta_client)

    result = service.start_onboarding("5591999999999")

    assert result["phase"] == "onboarding_started"
    assert profile_service.marked == ["5591999999999"]
    assert meta_client.sent_buttons


def test_handle_level_selection_saves_level_and_sends_welcome():
    profile_service = DummyProfileService()
    meta_client = DummyMetaClient()
    service = OnboardingService(profile_service, meta_client)

    result = service.handle_level_selection("5591999999999", PedagogicalLevel.BASICO)

    assert result["phase"] == "level_saved"
    assert profile_service.saved[0][1] == PedagogicalLevel.BASICO
    assert meta_client.sent_text[0][0] == "5591999999999"
