# Desafio MBA Engenharia de Software com IA - Full Cycle

Sistema de perguntas e respostas baseado em RAG (Retrieval-Augmented Generation). O sistema ingere um PDF, armazena os embeddings no PostgreSQL com pgvector e responde perguntas com base exclusivamente no conteúdo do documento.

## Requisitos

- Python 3.12+
- Docker e Docker Compose
- Chave de API da OpenAI (obrigatoria para embeddings)
- Chave de API do Google Gemini (opcional, apenas se usar `LLM_PROVIDER=gemini`)

## Configuracao

### 1. Banco de dados

Suba o PostgreSQL com a extensao pgvector:

```bash
docker compose up -d
```

### 2. Variaveis de ambiente

Copie o arquivo de exemplo e preencha com suas chaves:

```bash
cp .env.example .env
```

Variaveis disponiveis no `.env`:

| Variavel | Descricao | Exemplo |
|---|---|---|
| `OPENAI_API_KEY` | Chave da API OpenAI | `sk-proj-...` |
| `GOOGLE_API_KEY` | Chave da API Google Gemini | `AIza...` |
| `OPENAI_MODEL` | Modelo de embeddings | `text-embedding-3-small` |
| `OPENAI_CHAT_MODEL` | Modelo de chat OpenAI | `gpt-4o-mini` |
| `GEMINI_CHAT_MODEL` | Modelo de chat Gemini | `gemini-2.0-flash` |
| `LLM_PROVIDER` | Provider de chat (`openai` ou `gemini`) | `openai` |
| `PGVECTOR_URL` | URL de conexao com o PostgreSQL | `postgresql+psycopg://postgres:postgres@localhost:5432/rag` |
| `PGVECTOR_COLLECTION` | Nome da colecao no banco | `minha_colecao` |
| `PDF_PATH` | Caminho para o arquivo PDF | `./document.pdf` |

### 3. Dependencias Python

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

## Ingestao do PDF

Coloque o arquivo PDF no caminho definido em `PDF_PATH` e execute:

```bash
python src/ingest.py
```

O processo divide o documento em chunks, gera os embeddings via OpenAI e armazena no PostgreSQL. A ingestao so precisa ser feita uma vez por documento. Para reingeri-lo, basta rodar o comando novamente.

## Rodando o chat

```bash
python src/chat.py
```

O sistema exibira uma mensagem de boas-vindas e aguardara suas perguntas. As respostas sao geradas em streaming conforme os tokens chegam.

- Digite sua pergunta e pressione Enter
- Digite `2` para encerrar o sistema

## Alternando entre OpenAI e Gemini

No `.env`, altere a variavel `LLM_PROVIDER`:

```
LLM_PROVIDER=openai   # usa OPENAI_CHAT_MODEL
LLM_PROVIDER=gemini   # usa GEMINI_CHAT_MODEL
```

Os embeddings sempre usam OpenAI independentemente do provider de chat.

## Estrutura do projeto

```
.
├── docker-compose.yml   # PostgreSQL com pgvector
├── requirements.txt     # Dependencias Python
├── .env                 # Variaveis de ambiente (nao versionar)
├── document.pdf         # PDF a ser ingerido
└── src/
    ├── ingest.py        # Ingestao do PDF no banco vetorial
    ├── search.py        # Busca semantica e montagem do prompt
    └── chat.py          # Interface de perguntas e respostas
```
