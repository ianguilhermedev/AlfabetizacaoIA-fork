from __future__ import annotations

from pathlib import Path

from flask import Flask

from alfabot.config import get_settings
from alfabot.domain.models import Base
from alfabot.infra.db import create_engine_for_url, get_session_factory, init_database
from alfabot.infra.logging import configure_logging
from alfabot.infra.meta_client import MetaClient
from alfabot.services.onboarding_service import OnboardingService
from alfabot.services.profile_service import ProfileService
from alfabot.services.rag_service import RagService
from alfabot.services.webhook_processor import WebhookProcessor
from alfabot.infra.chroma import ChromaService
from alfabot.infra.ollama_client import OllamaClient
from alfabot.infra.whisper_client import WhisperClient
from alfabot.services.ai_service import AIService
from alfabot.services.audio_service import AudioService
from alfabot.web.routes import webhook_blueprint


def create_app(settings=None) -> Flask:
    settings = settings or get_settings()
    app = Flask(__name__)
    app.config["WHATSAPP_VERIFY_TOKEN"] = settings.whatsapp_verify_token
    app.config["SETTINGS"] = settings

    configure_logging()

    if settings.database_url.startswith("sqlite:///") and settings.database_url not in {"sqlite:///", "sqlite:///:memory:"}:
        database_path = Path(settings.database_url.replace("sqlite:///", "", 1))
        database_path.parent.mkdir(parents=True, exist_ok=True)

    engine = create_engine_for_url(settings.database_url)
    init_database(engine)
    session_factory = get_session_factory(engine)

    meta_client = MetaClient(token=settings.whatsapp_token, phone_id=settings.whatsapp_phone_id)
    profile_service = ProfileService(session_factory)
    onboarding_service = OnboardingService(profile_service, meta_client)
    audio_service = AudioService(meta_client, WhisperClient(settings.whisper_model))
    rag_service = RagService(ChromaService(settings.chroma_path))
    ai_service = AIService(OllamaClient(settings.ollama_model))
    processor = WebhookProcessor(profile_service, onboarding_service, audio_service, rag_service, ai_service)

    app.extensions["alfabot"] = {
        "engine": engine,
        "session_factory": session_factory,
        "meta_client": meta_client,
        "profile_service": profile_service,
        "onboarding_service": onboarding_service,
        "audio_service": audio_service,
        "rag_service": rag_service,
        "ai_service": ai_service,
        "processor": processor,
    }

    app.register_blueprint(webhook_blueprint)
    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=get_settings().port, debug=get_settings().debug)
