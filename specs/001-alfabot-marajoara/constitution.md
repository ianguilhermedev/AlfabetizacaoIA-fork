<!--
Sync Impact Report
Version change: unversioned template -> 1.0.0
Modified principles:
- Principle 1 placeholder -> I. Local-First Python Stack
- Principle 2 placeholder -> II. Explicit Meta API Boundary
- Principle 3 placeholder -> III. Secrets and Logging Discipline
- Principle 4 placeholder -> IV. Pytest Coverage for Behavior Changes
- Principle 5 placeholder -> V. Simplicity and Local Determinism
Added sections:
- Technology Stack & Integration Boundaries
- Delivery Workflow & Quality Gates
Removed sections:
- none
Templates requiring updates:
- .specify/templates/plan-template.md ✅ reviewed, no changes required
- .specify/templates/spec-template.md ✅ reviewed, no changes required
- .specify/templates/tasks-template.md ✅ reviewed, no changes required
- .specify/templates/commands/ ⚠ not present in this workspace
Follow-up TODOs:
- none
-->

# AlfabetizacaoIA Constitution

## Core Principles

### I. Local-First Python Stack
The application MUST be implemented in Python 3 and managed with uv. The web
server MUST use Flask. Profile persistence MUST use SQLite through SQLAlchemy.
Vector retrieval MUST use ChromaDB. Audio transcription MUST use
Faster-Whisper on CPU. Text generation MUST use Ollama with Llama 3.2 running
locally. Introducing a different runtime, model host, database, or transcription
backend requires a constitution amendment before implementation.

### II. Explicit Meta API Boundary
All inbound Meta webhooks and all outbound text or interactive button responses
MUST be implemented with project-owned requests calls. No third-party wrapper,
SDK, or abstraction MAY own that boundary. Request payloads, retries, error
mapping, and webhook verification MUST be defined in this repository so the
integration remains inspectable and replaceable.

### III. Secrets and Logging Discipline
Operational logging MUST be centralized through loguru. Logs MUST capture the
request or job context needed to trace a user action across Flask, SQLAlchemy,
ChromaDB, transcription, generation, and Meta API calls. Secrets and runtime
configuration MUST come from environment variables, with sensitive values stored
outside the repository in .env or the execution environment. No API key,
credential, token, or secret MAY be committed in source, tests, fixtures, or
documentation.

### IV. Pytest Coverage for Behavior Changes
Behavioral changes MUST ship with pytest coverage that exercises the touched
slice before merge. Changes that affect storage, RAG retrieval, transcription,
local generation, or the Meta API boundary MUST include focused tests that
would fail if the contract regressed. The test suite MUST run without network
access except for explicitly mocked integration points.

### V. Simplicity and Local Determinism
Implement the smallest design that satisfies the user story and the fixed stack.
Prefer explicit code paths, local execution, and deterministic behavior over new
abstractions or extra dependencies. Any new package, service, or runtime
capability MUST be justified in the plan before it is adopted. The system MUST
remain usable offline for all local workflows except the external Meta API
boundary.

## Technology Stack & Integration Boundaries

- Python 3 MUST be the only application language.
- uv MUST manage the Python environment and project execution.
- Flask MUST provide the web server and HTTP routing layer.
- SQLite plus SQLAlchemy MUST be used for profile and relational data.
- ChromaDB MUST store and serve vector embeddings for RAG.
- Faster-Whisper MUST run on CPU for transcription.
- Ollama with Llama 3.2 MUST generate local text responses.
- requests MUST be the only allowed HTTP client for Meta API communication.
- loguru MUST be the central logging library.
- pytest MUST be the primary automated test framework.
- Environment-specific values and secrets MUST be loaded from environment
	variables, with .env reserved for local configuration.

## Delivery Workflow & Quality Gates

- Every feature plan MUST include a Constitution Check that names any proposed
	deviation from this document.
- Any implementation that would violate a principle MUST stop until the
	constitution is amended or the design is revised.
- Tests for the touched slice MUST be written or updated before the change is
	considered complete.
- Changes that affect external integration, storage, or model behavior MUST have
	a validation step that exercises the affected boundary directly.
- Complexity must be justified in the plan, and the simplest working approach
	MUST be preferred when multiple options satisfy the requirement.

## Governance

This constitution supersedes all other project guidance. Amendments MUST update
this file in the same change set as any dependent templates or runtime guidance
that rely on the changed rule. Each amendment MUST include the reason for the
change, the impact on existing work, and a version bump following semantic
versioning.

Versioning policy:

- MAJOR for breaking changes to a principle, removal of a principle, or a rule
	that changes the required development posture.
- MINOR for new principles, materially expanded guidance, or a new section that
	adds non-trivial governance or technical constraints.
- PATCH for wording clarifications, typo fixes, or other non-semantic edits.

Compliance review expectations:

- Spec, plan, and task documents MUST pass a constitution check before work is
	approved.
- Reviews MUST verify secret handling, logging, test coverage, and Meta API
	boundary compliance.
- If a temporary exception is ever approved, it MUST be documented with scope,
	risk, mitigation, and an expiration path.

**Version**: 1.0.0 | **Ratified**: 2026-06-01 | **Last Amended**: 2026-06-01
