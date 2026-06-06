# Alfabot Marajoara

O **Alfabot Marajoara** é um backend Python projetado para atuar como um tutor de alfabetização inteligente via WhatsApp. O projeto utiliza IA generativa local e RAG (Retrieval-Augmented Generation) com base cultural marajoara para oferecer suporte pedagógico personalizado.

## Funcionalidades Implementadas
* **Webhooks Assíncronos:** Processamento de mensagens via WhatsApp Cloud API com resposta imediata para evitar timeouts, utilizando *threading* para processamento pesado em segundo plano.
* **Pipeline de IA Local:**
    * **Transcrição:** Conversão de áudios do WhatsApp para texto usando o *Faster-Whisper* (CPU).
    * **Geração de Texto:** Respostas pedagógicas contextuais geradas pelo *Llama 3.2* via *Ollama*.
* **Memória Cultural (RAG):** Busca semântica integrada com *ChromaDB* para recuperar conteúdos sobre a cultura marajoara (fauna, lendas, história), garantindo respostas culturalmente alinhadas.
* **Gestão de Aprendizado:** Banco de dados SQLite com SQLAlchemy para mapear perfis, níveis de leitura (iniciante, básico, intermediário) e histórico de interações.

## Estrutura do Projeto
A estrutura foi organizada para manter a lógica de negócio separada da integração com APIs externas (Meta):

```text
/alfabot-marajoara
├── app/
│   ├── models/          # Modelos de dados (SQLAlchemy)
│   ├── services/        # Lógica de IA, Voz, RAG e WhatsApp
│   ├── routes/          # Definição dos Webhooks (Flask)
│   └── database.py      # Configuração do SQLite
├── data/                # Artefatos de áudio temporários
├── deploy/              # Configurações para produção (Systemd, Gunicorn)
├── tests/               # Testes unitários e de integração (Pytest)
├── .env.example         # Template de variáveis de ambiente
├── main.py              # Ponto de entrada da aplicação
└── pyproject.toml       # Dependências gerenciadas pelo uv
## Tecnologias
* **Backend:** Python 3, Flask, Gunicorn.
* **IA/ML:** Ollama (Llama 3.2), Faster-Whisper, ChromaDB.
* **Database:** SQLite, SQLAlchemy.
* **Observabilidade:** Loguru para monitoramento em produção.
* **Ferramenta de Build/Gestão:** `uv`.

## Como Executar
1.  **Configuração:** Instale as dependências com `uv sync`.
2.  **Ambiente:** Renomeie `.env.example` para `.env` e configure seu `WHATSAPP_TOKEN`.
3.  **IA:** Certifique-se de que o Ollama esteja rodando localmente (`ollama serve`).
4.  **Túnel:** Utilize o Hookdeck para expor a porta 5000: `hookdeck listen 5000`.
5.  **Rodar:** Inicie a aplicação com `uv run python main.py`.