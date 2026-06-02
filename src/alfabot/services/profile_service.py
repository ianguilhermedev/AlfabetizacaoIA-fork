from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select

from alfabot.domain.enums import OnboardingState, PedagogicalLevel
from alfabot.domain.models import LearnerProfile


class ProfileService:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def get_or_create_profile(self, phone_number: str) -> tuple[LearnerProfile, bool]:
        with self.session_factory() as session:
            profile = session.scalar(select(LearnerProfile).where(LearnerProfile.phone_number == phone_number))
            created = profile is None
            if profile is None:
                profile = LearnerProfile(
                    phone_number=phone_number,
                    pedagogical_level=PedagogicalLevel.NEW.value,
                    onboarding_state=OnboardingState.NEW.value,
                )
                session.add(profile)
                session.commit()
                session.refresh(profile)
            return profile, created

    def save_level(self, phone_number: str, level: PedagogicalLevel) -> LearnerProfile:
        with self.session_factory() as session:
            profile = session.scalar(select(LearnerProfile).where(LearnerProfile.phone_number == phone_number))
            if profile is None:
                profile = LearnerProfile(phone_number=phone_number)
                session.add(profile)
            profile.pedagogical_level = level.value
            profile.onboarding_state = OnboardingState.ACTIVE.value
            profile.last_seen_at = datetime.now(timezone.utc)
            session.commit()
            session.refresh(profile)
            return profile

    def mark_collecting_level(self, phone_number: str) -> LearnerProfile:
        with self.session_factory() as session:
            profile = session.scalar(select(LearnerProfile).where(LearnerProfile.phone_number == phone_number))
            if profile is None:
                profile = LearnerProfile(phone_number=phone_number)
                session.add(profile)
            profile.onboarding_state = OnboardingState.COLLECTING_LEVEL.value
            profile.last_seen_at = datetime.now(timezone.utc)
            session.commit()
            session.refresh(profile)
            return profile

    def update_last_seen(self, phone_number: str) -> None:
        with self.session_factory() as session:
            profile = session.scalar(select(LearnerProfile).where(LearnerProfile.phone_number == phone_number))
            if profile is None:
                return
            profile.last_seen_at = datetime.now(timezone.utc)
            session.commit()
