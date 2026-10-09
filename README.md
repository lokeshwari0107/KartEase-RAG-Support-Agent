
# KartEase RAG Support Agent

An AI-powered customer support assistant built with Python, Gemini,
LangChain, and ChromaDB. It answers customer policy questions using
retrieval-augmented generation (RAG) and retrieves order information
from a CSV dataset.

## Features

- Policy search across four Markdown knowledge-base documents
- Semantic retrieval using ChromaDB
- Gemini-powered natural-language responses
- Order lookup by order ID
- Support for order and policy questions through a LangChain agent
- Automated tests using pytest

## Tech Stack

- Python
- Google Gemini API
- LangChain
- ChromaDB
- Retrieval-Augmented Generation (RAG)
- Pandas/CSV data handling
- Pytest

## Project Structure

```text
kartease_starter/
├── data/
│   ├── payments_and_offers.md
│   ├── returns_and_refunds.md
│   ├── shipping_and_delivery.md
│   └── warranty_and_repairs.md
├── tests/
│   ├── test_tools.py
│   └── test_policy_search.py
├── agent.py
├── ingest.py
├── policy_search.py
├── tools.py
├── orders.csv
├── requirements-langchain.txt
└── README.md
```

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements-langchain.txt
   ```

3. Create a `.env` file using `.env.example` as a template.
4. Add your Google Gemini API key and model settings to `.env`.
5. Build the policy knowledge base:

   ```bash
   python ingest.py
   ```

6. Start the support agent:

   ```bash
   python agent.py
   ```

## Example Questions

- Where is my order KE1002?
- What is the return window for electronics?
- Can I use COD for an order worth ₹12,000?

## Run Tests

```bash
python -m pytest tests -v
```

## Security

Keep API keys in `.env`. Never commit secrets or customer-sensitive
information to a public repository.

## Test Results

Tests executed using `pytest`.

| Test case | Expected behavior | Result |
|---|---|---|
| Existing order lookup | Returns order details for KE1002 | PASS |
| Case-insensitive order ID | Finds KE1002 when entered as ke1002 | PASS |
| Nonexistent order | Returns a not-found message | PASS |
| Electronics return policy | Retrieves the 10-day return window | PASS |
| Policy search response | Returns a non-empty response | PASS |

**Total: 5 passed, 0 failed.**

Command: `python -m pytest tests -v`
