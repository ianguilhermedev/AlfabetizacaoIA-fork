from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from alfabot.domain.enums import OnboardingState, PedagogicalLevel
from alfabot.infra.db import Base


class LearnerProfile(Base):
    __tablename__ = "learner_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    phone_number: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)
    pedagogical_level: Mapped[str] = mapped_column(String(32), nullable=False, default=PedagogicalLevel.NEW.value)
    onboarding_state: Mapped[str] = mapped_column(String(32), nullable=False, default=OnboardingState.NEW.value)
    display_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    interactions: Mapped[list["InteractionRecord"]] = relationship(back_populates="profile", cascade="all, delete-orphan")


class InteractionRecord(Base):
    __tablename__ = "interaction_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("learner_profiles.id"), nullable=False)
    direction: Mapped[str] = mapped_column(String(16), nullable=False)
    message_type: Mapped[str] = mapped_column(String(32), nullable=False)
    raw_payload: Mapped[str] = mapped_column(Text, nullable=False)
    transcript_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    prompt_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    response_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    error_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    profile: Mapped[LearnerProfile] = relationship(back_populates="interactions")


class KnowledgeChunk(Base):
    __tablename__ = "knowledge_chunks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_title: Mapped[str] = mapped_column(String(255), nullable=False)
    chunk_text: Mapped[str] = mapped_column(Text, nullable=False)
    topic_tags: Mapped[str | None] = mapped_column(String(255), nullable=True)
    embedding_key: Mapped[str | None] = mapped_column(String(255), nullable=True)
    language: Mapped[str | None] = mapped_column(String(32), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class MediaArtifact(Base):
    __tablename__ = "media_artifacts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("learner_profiles.id"), nullable=False)
    source_media_id: Mapped[str] = mapped_column(String(128), nullable=False)
    local_path: Mapped[str] = mapped_column(String(512), nullable=False)
    mime_type: Mapped[str | None] = mapped_column(String(128), nullable=True)
    transcription_status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
