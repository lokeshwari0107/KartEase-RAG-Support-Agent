
import gradio as gr
from agent import ask


def chat(message, history):
    """Send the user's question to the KartEase support agent."""
    if not message or not message.strip():
        return "Please enter a question about KartEase orders or policies."

    try:
        return ask(message.strip())
    except Exception:
        return (
            "Sorry, I couldn't process your question right now. "
            "Please try again."
        )


demo = gr.ChatInterface(
    fn=chat,
    title="KartEase Customer Support",
    description=(
        "Ask about your KartEase orders, returns, refunds, "
        "shipping, payments, and warranty policies."
    ),
    examples=[
        "Where is my order KE1002?",
        "What is the return window for electronics?",
        "Can I use COD for an order worth ₹12,000?",
        "What is the warranty policy?",
    ],
    chatbot=gr.Chatbot(height=450),
)

if __name__ == "__main__":
    demo.launch()
