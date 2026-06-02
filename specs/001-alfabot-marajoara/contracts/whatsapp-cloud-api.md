# WhatsApp Cloud API Contract

## Purpose

Define the inbound webhook and outbound messaging contract for the Alfabot Marajoara integration with the Meta WhatsApp Cloud API.

## Inbound webhook

### Verification request

- **Method**: `GET`
- **Path**: `/webhook`
- **Query parameters**:
  - `hub.mode`
  - `hub.verify_token`
  - `hub.challenge`

### Verification behavior

- If `hub.mode` is `subscribe` and `hub.verify_token` matches the configured `WHATSAPP_VERIFY_TOKEN`, the service returns the raw `hub.challenge` value with HTTP 200.
- If the token does not match, the service returns HTTP 403.

### Event ingestion

- **Method**: `POST`
- **Path**: `/webhook`
- **Content-Type**: `application/json`

### Expected payload families

- Text message events
- Audio/voice note events
- Interactive reply events
- Status delivery updates

### Ingestion behavior

- The service must parse the Meta payload and identify the sender phone number.
- The service must classify the message type before downstream processing.
- The service must accept valid payloads and hand them to the processing pipeline without exposing secrets in logs.

## Media download contract

### Media metadata lookup

- **Method**: `GET`
- **Path**: `/{media-id}` on the Meta Graph API
- **Authorization**: Bearer token from `WHATSAPP_TOKEN`

### Binary download

- The returned media URL must be fetched with the same authorization context.
- The service must store the file temporarily in a runtime-managed local directory before transcription.

## Outbound messaging

### Send message

- **Method**: `POST`
- **Path**: `/{phone-number-id}/messages`
- **Authorization**: Bearer token from `WHATSAPP_TOKEN`
- **Body types**:
  - text messages
  - interactive button messages
  - reply messages tied to an inbound conversation

### Required behavior

- The service must send only the fields required by the selected message type.
- The service must preserve the pedagogical tone and the Marajoara context in the generated text.
- The service must classify send failures separately from generation or transcription failures.

## Error handling expectations

- Invalid verification attempts return 403.
- Malformed JSON payloads return 400.
- Meta send failures are logged and converted into a retryable application error when appropriate.
