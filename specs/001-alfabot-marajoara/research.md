# Research Notes: Alfabot Marajoara

## 1. Web ingress and webhook processing

**Decision**: Use a Flask blueprint exposed at `/webhook` with a GET verification path and a POST ingestion path that forwards payloads to a dedicated `WebhookProcessor` service.

**Rationale**: Flask is the required server stack and the product is fundamentally a webhook-driven backend. Keeping verification and ingestion in a narrow route layer makes the Meta boundary easy to inspect and test.

**Alternatives considered**:
- FastAPI for automatic validation and docs, rejected because it would introduce an unnecessary framework change.
- A queue-first architecture, rejected for the first version because the requested pipeline is sequential and the simplest reliable delivery path is a direct service call behind a route.

## 2. Audio transcription and local generation

**Decision**: Use Faster-Whisper on CPU for audio transcription and Ollama for local generation with Llama 3.2 as the chat model.

**Rationale**: This matches the constitution, keeps AI execution local, and avoids paid or third-party hosted inference. Faster-Whisper is suitable for CPU-only deployment, and Ollama gives a single local runtime for generation.

**Alternatives considered**:
- Cloud transcription or cloud LLMs, rejected because the constitution requires a local-first stack.
- A second generation backend, rejected because the project already standardizes on Ollama.

## 3. RAG embeddings and retrieval

**Decision**: Store the marajoara corpus in ChromaDB and use a local Ollama embedding model for text vectorization so retrieval stays inside the same local runtime family.

**Rationale**: ChromaDB is the requested vector store, and using a local embedding model avoids adding another hosted dependency. It also keeps corpus management and retrieval deterministic for offline work.

**Alternatives considered**:
- Sentence-transformers, rejected for the first pass because it adds a separate model stack to maintain.
- Cloud embeddings, rejected because they violate the offline/local-first direction.

## 4. Persistence and learner profile state

**Decision**: Use SQLite with SQLAlchemy for learner profiles, onboarding status, and message history metadata.

**Rationale**: SQLite is sufficient for the expected scale, easy to ship, and fits the requirement to keep state local. SQLAlchemy gives a clean domain layer and testable repositories.

**Alternatives considered**:
- PostgreSQL, rejected because it is more operationally expensive than needed for the initial scope.
- Flat files, rejected because profile state and interaction history need relational queries and unique constraints.

## 5. Meta API boundary and media handling

**Decision**: Implement all Meta communication with direct `requests` calls in a dedicated client for message send, webhook verification support, and media download.

**Rationale**: The constitution explicitly requires manual HTTP integration without wrappers. A dedicated client keeps headers, retries, and payload shapes in one place.

**Alternatives considered**:
- Meta SDK wrappers, rejected by the project constraint.
- Generic HTTP abstraction libraries, rejected because they hide the required Meta request shapes.

## 6. Testing and observability

**Decision**: Use `pytest` for unit, integration, and contract tests; centralize runtime logging in `loguru`.

**Rationale**: `pytest` is the fastest path to broad test coverage and is well suited to mocking external boundaries. `loguru` gives consistent structured logs around webhook processing and AI calls.

**Alternatives considered**:
- unittest, rejected because pytest better matches the planned test matrix.
- Standard-library logging only, rejected because the constitution already standardizes on loguru.

## 7. Development tunneling

**Decision**: Use Hookdeck CLI in development to expose the local Flask webhook to Meta during manual or semi-manual testing.

**Rationale**: The feature request explicitly calls out Hookdeck CLI for dev traffic forwarding, which is appropriate for local webhook workflows.

**Alternatives considered**:
- ngrok, rejected because Hookdeck is already named in the feature request.
- No tunnel, rejected because local webhook testing would not reach Meta.
