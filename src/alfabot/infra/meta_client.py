from __future__ import annotations

from dataclasses import dataclass

import requests


@dataclass
class MetaClient:
    token: str
    phone_id: str
    base_url: str = "https://graph.facebook.com/v20.0"

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def send_text(self, to: str, body: str) -> requests.Response:
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": body},
        }
        return requests.post(
            f"{self.base_url}/{self.phone_id}/messages",
            headers=self._headers(),
            json=payload,
            timeout=30,
        )

    def send_buttons(self, to: str, payload: dict) -> requests.Response:
        message_payload = {"messaging_product": "whatsapp", "to": to, **payload}
        return requests.post(
            f"{self.base_url}/{self.phone_id}/messages",
            headers=self._headers(),
            json=message_payload,
            timeout=30,
        )

    def download_media_bytes(self, media_id: str) -> bytes:
        media_response = requests.get(
            f"{self.base_url}/{media_id}",
            headers=self._headers(),
            timeout=30,
        )
        media_response.raise_for_status()
        media_info = media_response.json()
        media_url = media_info.get("url", "")
        binary_response = requests.get(media_url, headers=self._headers(), timeout=30)
        binary_response.raise_for_status()
        return binary_response.content
