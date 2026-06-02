from __future__ import annotations

from pathlib import Path
import tempfile


class AudioService:
    def __init__(self, meta_client, whisper_client, temp_dir: str = "./data/tmp/audio"):
        self.meta_client = meta_client
        self.whisper_client = whisper_client
        self.temp_dir = Path(temp_dir)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def transcribe_media(self, media_id: str) -> str | None:
        audio_bytes = self.meta_client.download_media_bytes(media_id)
        with tempfile.NamedTemporaryFile(dir=self.temp_dir, suffix=".ogg", delete=False) as temp_file:
            temp_file.write(audio_bytes)
            temp_file.flush()
            temp_path = temp_file.name

        transcript = self.whisper_client.transcribe(temp_path)
        return transcript.strip() if transcript else None
