
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_DIR = BASE_DIR / "chroma_db"
COLLECTION_NAME = "kartease_policies"


def build_knowledge_base():
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY is missing from .env")

    # Reuse the existing vector database if it already has data.
    if DB_DIR.exists():
        try:
            existing_db = Chroma(
                collection_name=COLLECTION_NAME,
                persist_directory=str(DB_DIR),
                embedding_function=GoogleGenerativeAIEmbeddings(
                    model=os.getenv(
                        "GEMINI_EMBED_MODEL",
                        "gemini-embedding-001",
                    )
                ),
            )
            if existing_db._collection.count() > 0:
                print("Knowledge base already exists. Reusing stored vectors.")
                return
        except Exception as exc:
            print(f"Could not reuse existing database: {exc}")

    loader = DirectoryLoader(
        str(DATA_DIR),
        glob="*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    documents = loader.load()

    if not documents:
        raise ValueError(f"No policy documents found in {DATA_DIR}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    chunks = splitter.split_documents(documents)

    print(f"Loaded {len(documents)} policy documents.")
    print(f"Created {len(chunks)} chunks.")

    embeddings = GoogleGenerativeAIEmbeddings(
        model=os.getenv("GEMINI_EMBED_MODEL", "gemini-embedding-001")
    )

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=str(DB_DIR),
    )

    print(f"Knowledge base saved to: {DB_DIR}")


if __name__ == "__main__":
    build_knowledge_base()
