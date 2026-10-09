

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)
from langchain_chroma import Chroma

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "chroma_db"
COLLECTION_NAME = "kartease_policies"

FALLBACK = "Sorry, I can only help with KartEase orders and policies."

# Load the embedding model and existing Chroma knowledge base.
embeddings = GoogleGenerativeAIEmbeddings(
    model=os.getenv("GEMINI_EMBED_MODEL", "gemini-embedding-001")
)

vectorstore = Chroma(
    collection_name=COLLECTION_NAME,
    persist_directory=str(DB_DIR),
    embedding_function=embeddings,
)

# Use the same default chat model as agent.py.
llm = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite"),
)


def search_policies(question: str) -> str:
    """Search KartEase policies and return an answer with source citations."""

    question = question.strip()

    if not question:
        return "Please enter a question about KartEase policies."

    # Retrieve the three most relevant policy chunks.
    results = vectorstore.similarity_search_with_score(question, k=3)

    if not results:
        return FALLBACK

    # Chroma returns distances: smaller generally means more similar.
    best_distance = results[0][1]

    # Reject questions that are too far from the policy content.
    if best_distance > 1.2:
        return FALLBACK

    context_parts = []
    sources = set()

    for document, score in results:
        source_path = document.metadata.get("source", "")
        source = Path(source_path).name if source_path else "unknown"

        if source != "unknown":
            sources.add(source)

        context_parts.append(
            f"Source: {source}\n"
            f"Content: {document.page_content}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are the KartEase customer support assistant.

Answer the customer's question using only the policy context below.
Do not invent policies, dates, fees, or conditions.

If the context does not contain enough information to answer,
respond with exactly this sentence and nothing else:
{FALLBACK}

Keep your answer concise and helpful.
Do not include a source list; the application adds verified
retrieved source filenames separately.

Policy context:
{context}

Customer question:
{question}
"""

    response = llm.invoke(prompt)
    answer = response.content

    # Handle either plain-text or block-based model responses.
    if isinstance(answer, list):
        text_parts = []

        for item in answer:
            if isinstance(item, dict):
                if item.get("type") == "text":
                    text = item.get("text", "")
                    if text:
                        text_parts.append(text)
            elif isinstance(item, str):
                text_parts.append(item)

        answer = "\n".join(text_parts)

    answer = str(answer).strip()

    # Never attach citations to the unrelated-question fallback.
    answer = str(answer).strip()

    # Remove citations if the model returns the fallback message.
    if answer.startswith(FALLBACK):
        return FALLBACK

    # Add sources only to an actual policy answer.
    if sources:
        answer += "\n\nSources: " + ", ".join(sorted(sources))

    return answer


if __name__ == "__main__":
    print("KartEase Policy Search is ready!")
    print("Ask a policy question, or type 'exit' to stop.")

    while True:
        question = input("\nYou: ").strip()

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if not question:
            continue

        try:
            print("\nAnswer:", search_policies(question))
        except Exception as exc:
            print(f"\nError: {exc}")
