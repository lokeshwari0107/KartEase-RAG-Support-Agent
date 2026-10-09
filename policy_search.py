
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "chroma_db"
COLLECTION_NAME = "kartease_policies"

embeddings = GoogleGenerativeAIEmbeddings(
    model=os.getenv("GEMINI_EMBED_MODEL", "gemini-embedding-001")
)

vectorstore = Chroma(
    collection_name=COLLECTION_NAME,
    persist_directory=str(DB_DIR),
    embedding_function=embeddings,
)

llm = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL", "gemini-3.7-flash"),
    temperature=0,
)

FALLBACK = "Sorry, I can only help with KartEase orders and policies."


def search_policies(question: str) -> str:
    results = vectorstore.similarity_search_with_score(question, k=3)

    if not results:
        return FALLBACK

    # Refuse unrelated questions when the retrieved text is not relevant.
    best_distance = results[0][1]
    if best_distance > 1.2:
        return FALLBACK

    context_parts = []
    sources = set()

    for document, score in results:
        source = Path(document.metadata.get("source", "unknown")).name
        sources.add(source)
        context_parts.append(
            f"Source: {source}\nContent: {document.page_content}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are the KartEase customer support assistant.

Answer only using the policy context below.
If the context does not contain the answer, respond exactly:
{FALLBACK}

Keep the answer concise. Do not invent policy details.
At the end, list the source file(s) used.

Policy context:
{context}

Customer question:
{question}
"""

    response = llm.invoke(prompt)
    answer = response.content

    if isinstance(answer, list):
        answer = " ".join(
            item.get("text", "") if isinstance(item, dict) else str(item)
            for item in answer
        )

    return str(answer)


if __name__ == "__main__":
    while True:
        question = input("\nAsk about KartEase policies (or type exit): ")

        if question.strip().lower() == "exit":
            break

        try:
            print("\nAnswer:", search_policies(question))
        except Exception as exc:
            print(f"\nError: {exc}")
