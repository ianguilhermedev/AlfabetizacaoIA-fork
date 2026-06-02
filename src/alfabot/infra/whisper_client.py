from __future__ import annotations


class WhisperClient:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self._model = None

    def transcribe(self, file_path: str) -> str:
        if self._model is None:
            try:
                from faster_whisper import WhisperModel
            except ModuleNotFoundError as exc:  # pragma: no cover - exercised in manual runtime setup
                raise RuntimeError("faster-whisper is not installed") from exc

            self._model = WhisperModel(self.model_name, device="cpu", compute_type="int8")

        segments, _info = self._model.transcribe(file_path, language="pt")
        return " ".join(segment.text.strip() for segment in segments if segment.text).strip()
