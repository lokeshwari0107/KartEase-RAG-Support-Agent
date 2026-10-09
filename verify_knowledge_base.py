
from pathlib import Path
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "chroma_db"
COLLECTION_NAME = "kartease_policies"

if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY is missing from .env")

embeddings = GoogleGenerativeAIEmbeddings(
    model=os.getenv("GEMINI_EMBED_MODEL", "gemini-embedding-001")
)

db = Chroma(
    collection_name=COLLECTION_NAME,
    persist_directory=str(DB_DIR),
    embedding_function=embeddings,
)

# Inspect stored records without generating new embeddings.
records = db.get(include=["documents", "metadatas"])
documents = records.get("documents") or []
metadatas = records.get("metadatas") or []

print(f"Total stored chunks: {len(documents)}")

if not documents:
    print("FAIL: No chunks were found.")
else:
    print("PASS: Chunks are stored in Chroma.")

sources = sorted({
    metadata.get("source", "")
    for metadata in metadatas
    if metadata and metadata.get("source")
})

print("\nSource filenames found:")
for source in sources:
    print(f"- {Path(source).name}")

if sources:
    print("\nPASS: Source filename metadata exists.")
else:
    print("\nFAIL: No source filename metadata found.")
