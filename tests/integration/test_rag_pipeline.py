from __future__ import annotations


def test_text_message_injects_rag_context_and_sends_reply(client, app):
    sent_text = []

    def fake_send_text(to, body):
        sent_text.append((to, body))

    app.extensions["alfabot"]["meta_client"].send_text = fake_send_text
    app.extensions["alfabot"]["ai_service"].generate_reply = lambda level, user_text, context_snippets: f"{user_text} {' '.join(context_snippets)}"
    app.extensions["alfabot"]["rag_service"].chroma_service.add_document(
        "Búfalo do Marajó",
        "O búfalo do Marajó é um animal muito presente no cotidiano marajoara.",
    )

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
                                "messages": [{"from": "5591999999999", "type": "text", "text": {"body": "búfalo"}}],
                            }
                        }
                    ]
                }
            ],
        },
    )

    assert response.status_code == 200
    assert response.get_json()["phase"] == "responded"
    assert sent_text
    assert "búfalo" in sent_text[0][1].lower()
