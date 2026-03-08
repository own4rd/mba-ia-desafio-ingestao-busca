import os
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from ingest import validate_env

load_dotenv()
PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_prompt(question=None):
    validate_env()
    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_MODEL","text-embedding-3-small"))

    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PGVECTOR_COLLECTION"),
        connection=os.getenv("PGVECTOR_URL"),
        use_jsonb=True,
    )

    results = store.similarity_search_with_score(question, k=10)

    contexto = "\n\n".join(doc.page_content.strip() for doc, _ in results)
    return PROMPT_TEMPLATE.format(contexto=contexto, pergunta=question)

