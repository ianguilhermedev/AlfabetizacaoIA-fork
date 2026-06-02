from __future__ import annotations


def test_transcribed_audio_follows_text_pipeline(client, app):
    sent_text = []

    def fake_send_text(to, body):
        sent_text.append((to, body))

    app.extensions["alfabot"]["meta_client"].send_text = fake_send_text
    app.extensions["alfabot"]["audio_service"].transcribe_media = lambda media_id: "Búfalo do Marajó"
    app.extensions["alfabot"]["ai_service"].generate_reply = lambda level, user_text, context_snippets: f"{user_text} {' '.join(context_snippets)}"

    first_payload = {
        "object": "whatsapp_business_account",
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
        ],
    }
    client.post("/webhook", json=first_payload)

    app.extensions["alfabot"]["profile_service"].save_level("5591999999999", __import__("alfabot.domain.enums", fromlist=["PedagogicalLevel"]).PedagogicalLevel.BASICO)

    audio_payload = {
        "object": "whatsapp_business_account",
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
        ],
    }

    response = client.post("/webhook", json=audio_payload)

    assert response.status_code == 200
    assert response.get_json()["phase"] == "responded"
    assert sent_text
