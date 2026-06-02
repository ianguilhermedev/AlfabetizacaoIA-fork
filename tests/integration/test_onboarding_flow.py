from __future__ import annotations


def test_new_user_receives_onboarding_and_can_select_level(client, app):
    sent_buttons = []
    sent_text = []

    def fake_send_buttons(to, payload):
        sent_buttons.append((to, payload))

    def fake_send_text(to, body):
        sent_text.append((to, body))

    app.extensions["alfabot"]["meta_client"].send_buttons = fake_send_buttons
    app.extensions["alfabot"]["meta_client"].send_text = fake_send_text

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

    first_response = client.post("/webhook", json=first_payload)
    assert first_response.status_code == 200
    assert first_response.get_json()["phase"] == "onboarding_started"
    assert sent_buttons

    second_payload = {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "changes": [
                    {
                        "value": {
                            "contacts": [{"wa_id": "5591999999999"}],
                            "messages": [{"from": "5591999999999", "type": "text", "text": {"body": "Básico"}}],
                        }
                    }
                ]
            }
        ],
    }

    second_response = client.post("/webhook", json=second_payload)
    assert second_response.status_code == 200
    assert second_response.get_json()["phase"] == "level_saved"
    assert sent_text
