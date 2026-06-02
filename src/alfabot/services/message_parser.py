from __future__ import annotations

from dataclasses import dataclass

from alfabot.domain.enums import MessageType


@dataclass(frozen=True)
class ParsedMessage:
    sender_phone: str
    message_type: MessageType
    text: str | None = None
    media_id: str | None = None
    reply_id: str | None = None


def _first_item(mapping: dict, key: str) -> dict:
    items = mapping.get(key) or []
    return items[0] if items else {}


def parse_meta_payload(payload: dict) -> ParsedMessage:
    entry = _first_item(payload, "entry")
    change = _first_item(entry, "changes")
    value = change.get("value") or {}
    message = _first_item(value, "messages")
    contact = _first_item(value, "contacts")

    sender_phone = message.get("from") or contact.get("wa_id") or ""
    message_type = message.get("type") or MessageType.SYSTEM.value

    if message_type == MessageType.TEXT.value:
        return ParsedMessage(
            sender_phone=sender_phone,
            message_type=MessageType.TEXT,
            text=(message.get("text") or {}).get("body"),
        )

    if message_type == MessageType.INTERACTIVE.value:
        interactive = message.get("interactive") or {}
        button_reply = interactive.get("button_reply") or {}
        return ParsedMessage(
            sender_phone=sender_phone,
            message_type=MessageType.INTERACTIVE,
            text=button_reply.get("title") or button_reply.get("id"),
            reply_id=button_reply.get("id"),
        )

    if message_type == MessageType.AUDIO.value:
        return ParsedMessage(
            sender_phone=sender_phone,
            message_type=MessageType.AUDIO,
            media_id=(message.get("audio") or {}).get("id"),
        )

    return ParsedMessage(sender_phone=sender_phone, message_type=MessageType.SYSTEM, text=None)
