from __future__ import annotations

from enum import Enum


class PedagogicalLevel(str, Enum):
    NEW = "new"
    INICIANTE = "iniciante"
    BASICO = "basico"
    INTERMEDIARIO = "intermediario"


class OnboardingState(str, Enum):
    NEW = "new"
    COLLECTING_LEVEL = "collecting_level"
    ACTIVE = "active"


class MessageType(str, Enum):
    TEXT = "text"
    AUDIO = "audio"
    INTERACTIVE = "interactive"
    SYSTEM = "system"


class ProcessingStatus(str, Enum):
    RECEIVED = "received"
    PROCESSED = "processed"
    FAILED = "failed"
    SENT = "sent"
