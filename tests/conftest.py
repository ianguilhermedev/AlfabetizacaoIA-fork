from __future__ import annotations

import pytest

from alfabot.app import create_app
from alfabot.config import Settings


@pytest.fixture()
def app():
    settings = Settings(
        whatsapp_token="test-whatsapp-token",
        whatsapp_phone_id="123456789",
        whatsapp_verify_token="test-token",
        ollama_model="llama3.2",
        whisper_model="base",
        database_url="sqlite://",
        chroma_path="./tmp/chroma",
        flask_env="testing",
        port=5000,
        debug=True,
    )
    app = create_app(settings)
    app.config.update(TESTING=True)
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
