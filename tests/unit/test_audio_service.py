from __future__ import annotations

from pathlib import Path

from alfabot.services.audio_service import AudioService


class FakeMetaClient:
    def download_media_bytes(self, media_id):
        assert media_id == "media-123"
        return b"fake-ogg-bytes"


class FakeWhisperClient:
    def __init__(self):
        self.received_paths = []

    def transcribe(self, file_path):
        self.received_paths.append(file_path)
        return "Transcrição de teste"


def test_audio_service_downloads_and_transcribes(tmp_path):
    meta_client = FakeMetaClient()
    whisper_client = FakeWhisperClient()
    service = AudioService(meta_client, whisper_client, temp_dir=str(tmp_path))

    transcript = service.transcribe_media("media-123")

    assert transcript == "Transcrição de teste"
    assert whisper_client.received_paths
    assert Path(whisper_client.received_paths[0]).exists()
