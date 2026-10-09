
from policy_search import search_policies


def test_electronics_return_policy():
    result = search_policies(
        "What is the return window for electronics?"
    )

    assert "10 days" in result.lower()


def test_policy_search_returns_a_result():
    result = search_policies(
        "What are the warranty and repair policies?"
    )

    assert isinstance(result, str)
    assert len(result.strip()) > 0
