from __future__ import annotations


def test_text_delivery_failure_returns_gateway_error(client, app):
    app.extensions["alfabot"]["meta_client"].send_text = lambda to, body: (_ for _ in ()).throw(RuntimeError("boom"))

    client.post(
        "/webhook",
        json={
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
        },
    )

    app.extensions["alfabot"]["profile_service"].save_level(
        "5591999999999",
        __import__("alfabot.domain.enums", fromlist=["PedagogicalLevel"]).PedagogicalLevel.BASICO,
    )

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
                                "messages": [{"from": "5591999999999", "type": "text", "text": {"body": "oi de novo"}}],
                            }
                        }
                    ]
                }
            ],
        },
    )

    assert response.status_code == 502
    assert response.get_json()["phase"] == "delivery_failed"
