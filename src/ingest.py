import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()


def validate_env(check_pdf: bool = False) -> None:
    required = ["OPENAI_API_KEY", "OPENAI_MODEL", "PGVECTOR_URL", "PGVECTOR_COLLECTION"]
    if check_pdf:
        required.append("PDF_PATH")

    missing = [var for var in required if not os.getenv(var)]
    if missing:
        raise SystemExit(f"Variáveis de ambiente não configuradas: {', '.join(missing)}")

    if check_pdf:
        pdf_path = os.getenv("PDF_PATH")
        if not os.path.exists(pdf_path):
            raise SystemExit(f"PDF não encontrado: {pdf_path}")


def ingest_pdf() -> None:
    validate_env(check_pdf=True)
    pdf_path = os.getenv("PDF_PATH")
    docs = PyPDFLoader(str(pdf_path)).load()
    splits = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=150, add_start_index=False
    ).split_documents(docs)
    if not splits:
        raise SystemExit(0)
    enriched = [
        Document(
            page_content=d.page_content,
            metadata={k: v for k, v in d.metadata.items() if v not in ("", None)},
        )
        for d in splits
    ]

    ids = [f"doc-{i}" for i in range(len(enriched))]

    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_MODEL","text-embedding-3-small"))

    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PGVECTOR_COLLECTION"),
        connection=os.getenv("PGVECTOR_URL"),
        use_jsonb=True,
    )

    store.add_documents(documents=enriched, ids=ids)

if __name__ == "__main__":
    ingest_pdf()
