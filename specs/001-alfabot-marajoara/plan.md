# Implementation Plan: Alfabot Marajoara

**Branch**: `001-alfabot-marajoara` | **Date**: 2026-06-02 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-alfabot-marajoara/spec.md`

## Summary

Construir um backend Flask orientado a webhook para o WhatsApp Cloud API que recebe mensagens em `/webhook`, processa texto e áudio em uma pipeline local de parsing, transcrição, contexto pedagógico, recuperação RAG e geração com Ollama, e envia a resposta final manualmente via requests para a Meta API.

## Technical Context

**Language/Version**: Python 3 gerenciado com uv

**Primary Dependencies**: Flask, SQLAlchemy, SQLite, ChromaDB, Faster-Whisper (CPU), Ollama, requests, loguru, pytest, python-dotenv

**Storage**: SQLite para perfis e histórico; ChromaDB para vetores e metadados do corpus marajoara; filesystem local para artefatos temporários de mídia

**Testing**: pytest com cobertura unitária, integração e contrato; mocks para Meta, Ollama, Whisper e Chroma

**Target Platform**: Serviço web Python para desenvolvimento local e implantação institucional em máquinas com CPU; webhook exposto localmente via Hookdeck durante desenvolvimento

**Project Type**: Web service backend sem frontend próprio

**Performance Goals**: Responder rapidamente a mensagens de texto e manter a transcrição de áudio em janela curta em hardware CPU comum; preservar latência previsível na rota de webhook

**Constraints**: Integração Meta somente com requests; IA local-first; segredos em variáveis de ambiente; respostas precisam manter tom pedagógico acolhedor; o fluxo local deve funcionar offline exceto a troca com a Meta

**Scale/Scope**: Uma única aplicação atendendo múltiplos alunos por número de telefone, com crescimento incremental do corpus cultural marajoara

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|---|---|---|
| I. Local-First Python Stack | PASS | Mantém Python 3, uv, Flask, SQLite/SQLAlchemy, ChromaDB, Faster-Whisper CPU e Ollama local. |
| II. Explicit Meta API Boundary | PASS | Entrada e saída com a Meta ficam isoladas em clientes próprios usando requests. |
| III. Secrets and Logging Discipline | PASS | Configuração por ambiente e logging central via loguru. |
| IV. Pytest Coverage for Behavior Changes | PASS | O plano prevê testes nas bordas críticas do webhook, áudio, RAG e envio. |
| V. Simplicity and Local Determinism | PASS | Estrutura de serviço único, adaptadores explícitos e pipeline sequencial. |

## Project Structure

### Documentation (this feature)

```text
specs/001-alfabot-marajoara/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── whatsapp-cloud-api.md
└── tasks.md
```

### Source Code (repository root)

```text
src/
└── alfabot/
    ├── __init__.py
    ├── app.py
    ├── config.py
    ├── web/
    │   └── routes.py
    ├── domain/
    │   ├── enums.py
    │   └── models.py
    ├── infra/
    │   ├── chroma.py
    │   ├── db.py
    │   ├── meta_client.py
    │   ├── ollama_client.py
    │   └── whisper_client.py
    ├── services/
    │   ├── message_parser.py
    │   ├── onboarding_service.py
    │   ├── profile_service.py
    │   ├── rag_service.py
    │   ├── response_builder.py
    │   └── webhook_processor.py
    └── prompts/
        └── system_prompt.py

tests/
├── contract/
├── integration/
└── unit/
```

**Structure Decision**: Estrutura única em `src/alfabot` porque o produto é um backend orientado a webhook, sem frontend próprio, e a divisão por camadas mantém o pipeline previsível e testável sem introduzir complexidade desnecessária.

## Complexity Tracking

Nenhuma violação da constituição foi identificada, então não há justificativas de complexidade adicionais.
