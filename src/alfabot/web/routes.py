from __future__ import annotations

from flask import Blueprint, current_app, jsonify, request


webhook_blueprint = Blueprint("webhook", __name__)


@webhook_blueprint.get("/webhook")
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    expected_token = current_app.config.get("WHATSAPP_VERIFY_TOKEN", "")
    if mode == "subscribe" and token == expected_token and challenge is not None:
        return challenge, 200

    return jsonify({"error": "forbidden"}), 403


@webhook_blueprint.post("/webhook")
def receive_webhook():
    payload = request.get_json(silent=True) or {}
    processor = current_app.extensions["alfabot"]["processor"]
    outcome = processor.process(payload)
    return jsonify(outcome.body), outcome.status_code
