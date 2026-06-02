from __future__ import annotations


def test_webhook_verification_accepts_matching_token(client):
    response = client.get(
        "/webhook",
        query_string={
            "hub.mode": "subscribe",
            "hub.verify_token": "test-token",
            "hub.challenge": "12345",
        },
    )

    assert response.status_code == 200
    assert response.data == b"12345"


def test_webhook_verification_rejects_bad_token(client):
    response = client.get(
        "/webhook",
        query_string={
            "hub.mode": "subscribe",
            "hub.verify_token": "wrong-token",
            "hub.challenge": "12345",
        },
    )

    assert response.status_code == 403


def test_webhook_post_routes_first_time_sender_to_onboarding(client, app):
    sent_messages = []

    def fake_send_buttons(to, payload):
        sent_messages.append((to, payload))

    app.extensions["alfabot"]["meta_client"].send_buttons = fake_send_buttons

    payload = {
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

    response = client.post("/webhook", json=payload)

    assert response.status_code == 200
    assert response.get_json()["phase"] == "onboarding_started"
    assert sent_messages and sent_messages[0][0] == "5591999999999"
