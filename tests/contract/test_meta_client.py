from __future__ import annotations

from alfabot.infra.meta_client import MetaClient


class DummyResponse:
    def __init__(self, payload=None, content=b"", status_code=200):
        self._payload = payload or {}
        self.content = content
        self.status_code = status_code

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


def test_send_text_posts_expected_payload(monkeypatch):
    captured = {}

    def fake_post(url, headers=None, json=None, timeout=None):
        captured["url"] = url
        captured["headers"] = headers
        captured["json"] = json
        captured["timeout"] = timeout
        return DummyResponse()

    monkeypatch.setattr("requests.post", fake_post)

    client = MetaClient(token="token", phone_id="phone-123")
    client.send_text("5591999999999", "Olá")

    assert captured["url"].endswith("/phone-123/messages")
    assert captured["json"]["type"] == "text"
    assert captured["json"]["text"]["body"] == "Olá"


def test_send_buttons_posts_interactive_payload(monkeypatch):
    captured = {}

    def fake_post(url, headers=None, json=None, timeout=None):
        captured["url"] = url
        captured["json"] = json
        return DummyResponse()

    monkeypatch.setattr("requests.post", fake_post)

    client = MetaClient(token="token", phone_id="phone-123")
    client.send_buttons("5591999999999", {"type": "interactive", "interactive": {"type": "button"}})

    assert captured["json"]["type"] == "interactive"
