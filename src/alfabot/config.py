from __future__ import annotations

from dataclasses import dataclass
import os

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    whatsapp_token: str
    whatsapp_phone_id: str
    whatsapp_verify_token: str
    ollama_model: str
    whisper_model: str
    database_url: str
    chroma_path: str
    flask_env: str
    port: int
    debug: bool

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            whatsapp_token=os.getenv("WHATSAPP_TOKEN", ""),
            whatsapp_phone_id=os.getenv("WHATSAPP_PHONE_ID", ""),
            whatsapp_verify_token=os.getenv("WHATSAPP_VERIFY_TOKEN", ""),
            ollama_model=os.getenv("OLLAMA_MODEL", "llama3.2"),
            whisper_model=os.getenv("WHISPER_MODEL", "base"),
            database_url=os.getenv("DATABASE_URL", "sqlite:///./data/alfabot.db"),
            chroma_path=os.getenv("CHROMA_PATH", "./data/chroma"),
            flask_env=os.getenv("FLASK_ENV", "development"),
            port=int(os.getenv("PORT", "5000")),
            debug=os.getenv("FLASK_ENV", "development") == "development",
        )


def get_settings() -> Settings:
    return Settings.from_env()
