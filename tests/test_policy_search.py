
from policy_search import search_policies, FALLBACK


def test_electronics_return_policy():
    result = search_policies(
        "What is the return window for electronics?"
    )

    assert "10 days" in result.lower()
    assert "returns_and_refunds.md" in result


def test_policy_search_returns_a_result():
    result = search_policies(
        "What are the warranty and repair policies?"
    )

    assert isinstance(result, str)
    assert len(result.strip()) > 0


def test_unrelated_question_returns_fallback():
    result = search_policies(
        "What is the capital of France?"
    )

    assert result.strip() == FALLBACK


def test_warranty_answer_includes_source():
    result = search_policies(
        "What is the warranty policy for electronics?"
    )

    assert "warranty" in result.lower()
    assert "warranty_and_repairs.md" in result
