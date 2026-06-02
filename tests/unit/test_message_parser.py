from __future__ import annotations

from alfabot.domain.enums import MessageType
from alfabot.services.message_parser import parse_meta_payload


def test_parse_text_payload_extracts_sender_and_body():
    payload = {
        "entry": [
            {
                "changes": [
                    {
                        "value": {
                            "contacts": [{"wa_id": "5591999999999"}],
                            "messages": [{"from": "5591999999999", "type": "text", "text": {"body": "oi"}}],
                        }
                    }
                ]
            }
        ]
    }

    parsed = parse_meta_payload(payload)

    assert parsed.sender_phone == "5591999999999"
    assert parsed.message_type == MessageType.TEXT
    assert parsed.text == "oi"


def test_parse_audio_payload_extracts_media_id():
    payload = {
        "entry": [
            {
                "changes": [
                    {
                        "value": {
                            "contacts": [{"wa_id": "5591999999999"}],
                            "messages": [{"from": "5591999999999", "type": "audio", "audio": {"id": "media-123"}}],
                        }
                    }
                ]
            }
        ]
    }

    parsed = parse_meta_payload(payload)

    assert parsed.message_type == MessageType.AUDIO
    assert parsed.media_id == "media-123"


def test_parse_interactive_payload_extracts_reply_id():
    payload = {
        "entry": [
            {
                "changes": [
                    {
                        "value": {
                            "contacts": [{"wa_id": "5591999999999"}],
                            "messages": [
                                {
                                    "from": "5591999999999",
                                    "type": "interactive",
                                    "interactive": {"button_reply": {"id": "basico", "title": "Básico"}},
                                }
                            ],
                        }
                    }
                ]
            }
        ]
    }

    parsed = parse_meta_payload(payload)

    assert parsed.message_type == MessageType.INTERACTIVE
    assert parsed.reply_id == "basico"
    assert parsed.text == "Básico"
