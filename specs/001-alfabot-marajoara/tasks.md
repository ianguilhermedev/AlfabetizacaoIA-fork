# Tasks: Alfabot Marajoara

**Input**: Design documents from `/specs/001-alfabot-marajoara/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The feature request explicitly asks for pytest-based unit tests and mocks in the stabilization sprint, so test tasks are included throughout the user-story phases where they protect the touched behavior.

**Organization**: Tasks are grouped by user story to keep each slice independently implementable and testable.

## Phase 1: Setup (Sprint 1 - Infraestrutura Web e Recepção)

**Goal**: Establish the Python project, environment boundaries, and local development bootstrap for the webhook-driven backend.

**Independent Test**: The repository should contain the uv-managed Python project metadata, environment template, ignore rules, and a documented local tunnel setup before any business logic is added.

- [X] T001 [P] Inicializar o projeto Python com uv em pyproject.toml e src/alfabot/__init__.py
- [X] T002 [P] Registrar variáveis seguras em .env.example e bloquear segredos em .gitignore
- [X] T003 [P] Documentar o roteamento local com Hookdeck em specs/001-alfabot-marajoara/quickstart.md
- [X] T004 [P] Criar a estrutura inicial de pastas src/alfabot/, tests/ e deploy/ conforme o plano em specs/001-alfabot-marajoara/plan.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Goal**: Build the common application skeleton that all webhook, AI, storage, and messaging flows depend on.

**Independent Test**: The Flask factory, configuration loader, database bootstrap, and service adapters should import cleanly and expose testable seams without touching external services.

- [X] T005 [P] Implement configuration loading, .env integration, and loguru bootstrap em src/alfabot/config.py and src/alfabot/infra/logging.py
- [X] T006 [P] Create the Flask application factory and register the /webhook blueprint in src/alfabot/app.py and src/alfabot/web/routes.py
- [X] T007 [P] Configure SQLAlchemy engine, session factory, and base metadata in src/alfabot/infra/db.py
- [X] T008 [P] Define learner, interaction, and enum models in src/alfabot/domain/enums.py and src/alfabot/domain/models.py
- [X] T009 [P] Create client shells for Meta, Whisper, Ollama, and Chroma in src/alfabot/infra/meta_client.py, src/alfabot/infra/whisper_client.py, src/alfabot/infra/ollama_client.py, and src/alfabot/infra/chroma.py
- [X] T010 [P] Add prompt assembly scaffolding in src/alfabot/prompts/system_prompt.py and src/alfabot/services/response_builder.py

---

## Phase 3: User Story 1 - Acolhimento e diagnóstico inicial (Priority: P1)

**Goal**: When a new student starts a conversation, the bot should launch a guided button flow to capture the initial reading level.

**Independent Test**: A first-time WhatsApp sender should receive onboarding buttons, and selecting a level should persist the onboarding state without requiring free-text explanation.

### Tests for User Story 1

- [X] T011 [P] [US1] Add an integration test for first-contact onboarding in tests/integration/test_onboarding_flow.py
- [X] T012 [P] [US1] Add a unit test for interactive button mapping in tests/unit/test_onboarding_service.py

### Implementation for User Story 1

- [X] T013 [US1] Implement first-contact detection and onboarding state transitions in src/alfabot/services/onboarding_service.py
- [X] T014 [US1] Persist learner level selection and onboarding state in src/alfabot/services/profile_service.py and src/alfabot/domain/models.py
- [X] T015 [US1] Render onboarding button messages in src/alfabot/services/response_builder.py and src/alfabot/infra/meta_client.py
- [X] T016 [US1] Route new-user webhook events through the onboarding path in src/alfabot/services/webhook_processor.py

---

## Phase 4: User Story 2 - Resposta adaptada ao nível do aluno (Priority: P1)

**Goal**: Text and audio messages should be parsed and answered with vocabulary appropriate to the learner's current pedagogical level.

**Independent Test**: A known learner profile should produce different response complexity for Iniciante, Básico, and Intermediário inputs, both for text and transcribed audio.

### Tests for User Story 2

- [X] T017 [P] [US2] Add a unit test for message parsing in tests/unit/test_message_parser.py
- [X] T018 [P] [US2] Add a unit test for level-aware prompt assembly in tests/unit/test_response_builder.py
- [X] T019 [P] [US2] Add an integration test for text and audio happy paths in tests/integration/test_message_pipeline.py

### Implementation for User Story 2

- [X] T020 [US2] Implement payload parsing for text, audio, and interactive replies in src/alfabot/services/message_parser.py
- [X] T021 [US2] Implement OGG download and CPU Whisper transcription in src/alfabot/services/webhook_processor.py and src/alfabot/infra/whisper_client.py
- [X] T022 [US2] Implement level-aware prompt composition in src/alfabot/prompts/system_prompt.py and src/alfabot/services/response_builder.py
- [X] T023 [US2] Connect profile lookup to the adaptive response pipeline in src/alfabot/services/profile_service.py and src/alfabot/services/webhook_processor.py

---

## Phase 5: User Story 3 - Cultura marajoara nas interações (Priority: P2)

**Goal**: The bot should enrich answers with Marajoara cultural context using the local ChromaDB corpus and send replies through the Meta API manually with requests.

**Independent Test**: A prompt about learning content should retrieve relevant Marajoara context, include it in the response, and dispatch the final message to the Meta endpoint using the project-owned client.

### Tests for User Story 3

- [X] T024 [P] [US3] Add a contract test for outbound Meta text and button payloads in tests/contract/test_meta_client.py
- [X] T025 [P] [US3] Add a unit test for Chroma semantic search in tests/unit/test_rag_service.py
- [X] T026 [P] [US3] Add an integration test for RAG-enriched response dispatch in tests/integration/test_rag_pipeline.py

### Implementation for User Story 3

- [X] T027 [US3] Implement Chroma ingestion and semantic search in src/alfabot/infra/chroma.py and src/alfabot/services/rag_service.py
- [X] T028 [US3] Add Marajoara corpus loading scripts in scripts/load_marajoara_corpus.py
- [X] T029 [US3] Inject Marajoara retrieval results into the system prompt in src/alfabot/services/response_builder.py
- [X] T030 [US3] Implement manual requests-based Meta sender for text and button payloads in src/alfabot/infra/meta_client.py
- [X] T031 [US3] Wire the Parser → Whisper → Profile → ChromaDB → Ollama → Meta chain in src/alfabot/services/webhook_processor.py

---

## Phase 6: User Story 4 - Estabilização e deploy de produção (Priority: P2)

**Goal**: Harden the pipeline against failures, add structured logs and tests, and prepare the backend for production execution under Gunicorn and systemd.

**Independent Test**: Corrupted audio should trigger a retry prompt, API failures should be handled without crashing the server, and the service should have a runnable production entrypoint.

### Tests for User Story 4

- [ ] T032 [P] [US4] Add a unit test for unreadable audio fallback and exception mapping in tests/unit/test_error_handling.py
- [ ] T033 [P] [US4] Add an integration test for retry-on-bad-audio in tests/integration/test_audio_retry_flow.py
- [ ] T034 [P] [US4] Add fixture and mock coverage for external boundaries in tests/conftest.py

### Implementation for User Story 4

- [ ] T035 [US4] Implement graceful exception handling for IA and Meta calls in src/alfabot/services/webhook_processor.py and src/alfabot/infra/meta_client.py
- [ ] T036 [US4] Configure rotating loguru sinks in src/alfabot/infra/logging.py
- [ ] T037 [US4] Package a Gunicorn startup path and systemd service file in deploy/gunicorn.conf.py and deploy/systemd/alfabot.service
- [ ] T038 [US4] Update quickstart and deployment notes with smoke tests in specs/001-alfabot-marajoara/quickstart.md and README.md
- [ ] T039 [US4] Run the full pytest suite and fix regressions in tests/ and src/alfabot/

---

## Phase 7: Polish & Cross-Cutting Concerns

**Goal**: Close out documentation, simplify rough edges, and verify the feature slice remains coherent across modules.

**Independent Test**: The feature should have a clean final review pass with no unresolved placeholders, no dead code paths, and documentation that matches the implemented flow.

- [ ] T040 [P] Refresh README.md with setup, webhook, and local-model instructions
- [ ] T041 [P] Review log wording, prompt wording, and error messages across src/alfabot/
- [ ] T042 [P] Verify the spec set remains aligned in specs/001-alfabot-marajoara/plan.md, research.md, data-model.md, quickstart.md, and contracts/whatsapp-cloud-api.md

---

## Dependencies & Execution Order

### Phase Dependencies

- Setup (Phase 1) has no prerequisites and can start immediately.
- Foundational (Phase 2) depends on Setup and blocks all user stories.
- User Story 1 can start after Foundational and should be completed first because it establishes onboarding state.
- User Story 2 can start after Foundational and reuses the profile and prompt scaffolding.
- User Story 3 builds on the response pipeline and the Meta client from earlier phases.
- User Story 4 builds on all previous stories and stabilizes the full webhook processing chain.
- Polish depends on the desired user story phases being complete.

### User Story Dependencies

- User Story 1 can start after Phase 2 and does not depend on later stories.
- User Story 2 can start after Phase 2 and reuses the profile and prompt scaffolding from User Story 1.
- User Story 3 builds on the response pipeline from User Story 2 and the Meta client from Phase 2.
- User Story 4 builds on all previous stories and stabilizes the full webhook processing chain.

### Within Each User Story

- Tests are written first when included and should fail before implementation.
- Models and adapters should exist before service orchestration.
- Service orchestration should exist before webhook wiring and outbound dispatch.
- Each story should be independently testable before moving to the next phase.

### Parallel Opportunities

- Setup tasks marked [P] can run in parallel because they touch different files.
- Foundational tasks marked [P] can run in parallel once the repository structure exists.
- Test tasks inside a user story can often run in parallel because they validate distinct behaviors.
- User Stories 2 and 3 can proceed in parallel after User Story 1 if the team splits into pipeline and retrieval workstreams.
- Polish tasks marked [P] can run in parallel at the end.

## Parallel Example: User Story 2

```text
Task: T017 Add a unit test for message parsing in tests/unit/test_message_parser.py
Task: T018 Add a unit test for level-aware prompt assembly in tests/unit/test_response_builder.py
Task: T019 Add an integration test for text and audio happy paths in tests/integration/test_message_pipeline.py
```

## Implementation Strategy

### MVP First

1. Complete Phase 1 Setup.
2. Complete Phase 2 Foundational work.
3. Complete User Story 1 so new students can onboard and select a reading level.
4. Validate the onboarding flow before layering on media, RAG, and deployment features.

### Incremental Delivery

1. Add adaptive text and audio handling for existing learners.
2. Enrich responses with Marajoara context and manual Meta egress.
3. Harden failure handling, logging, and production packaging.
4. Finish with documentation and final cleanup.

### Parallel Team Strategy

1. One developer can own onboarding and profile persistence.
2. Another developer can own transcription, RAG, and prompt enrichment.
3. A third developer can own the Meta client, logging, tests, and deployment packaging.
