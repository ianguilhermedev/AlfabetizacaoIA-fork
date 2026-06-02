from __future__ import annotations


def test_unreadable_audio_requests_retry(client, app):
    sent_text = []

    def fake_send_text(to, body):
        sent_text.append((to, body))

    app.extensions["alfabot"]["meta_client"].send_text = fake_send_text
    app.extensions["alfabot"]["audio_service"].transcribe_media = lambda media_id: None

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

    response = client.post(
        "/webhook",
        json={
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
        },
    )

    assert response.status_code == 200
    assert response.get_json()["phase"] == "audio_retry_requested"
    assert sent_text
