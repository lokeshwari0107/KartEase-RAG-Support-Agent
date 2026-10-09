
import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

from tools import get_order_status
from policy_search import search_policies

# Load API key and model settings from .env
load_dotenv()


# Tool 1: Order lookup
@tool
def order_lookup(order_id: str) -> str:
    """Look up a KartEase order using its order ID, such as KE1002."""
    return get_order_status(order_id)


# Tool 2: Policy lookup
@tool
def policy_lookup(question: str) -> str:
    """Search KartEase return, refund, shipping, warranty, and payment policies."""
    return search_policies(question)


# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite"),
    temperature=0,
)


# Create the KartEase support agent
agent = create_agent(
    model=llm,
    tools=[order_lookup, policy_lookup],
    system_prompt=(
        "You are the KartEase customer support assistant. "
        "Use order_lookup for questions about specific orders. "
        "Use policy_lookup for questions about KartEase policies. "
        "Use both tools when a question requires order details and policy information. "
        "Answer clearly and naturally using the information returned by the tools. "
        "Never invent order details or policies. "
        "For unrelated questions, reply exactly: "
        "Sorry, I can only help with KartEase orders and policies."
    ),
)


# Extract only readable text from the agent response
def ask(question: str) -> str:
    result = agent.invoke(
        {"messages": [{"role": "user", "content": question}]}
    )

    for message in reversed(result["messages"]):
        if getattr(message, "type", "") != "ai":
            continue

        content = message.content

        # Most straightforward response format
        if isinstance(content, str):
            return content

        # Gemini may return a list containing text and metadata
        if isinstance(content, list):
            text_parts = []

            for item in content:
                if isinstance(item, dict):
                    if item.get("type") == "text":
                        text = item.get("text", "")
                        if text:
                            text_parts.append(text)

            if text_parts:
                return "\n".join(text_parts)

    return "Sorry, I couldn't generate a response."


# Run the interactive support agent
if __name__ == "__main__":
    print("KartEase Support Agent is ready!")
    print("Ask a question, or type 'exit' to stop.")

    while True:
        question = input("\nYou: ").strip()

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if not question:
            continue

        try:
            answer = ask(question)
            print(f"\nKartEase: {answer}")

        except Exception as exc:
            print(f"\nError: {exc}")
