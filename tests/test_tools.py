
from tools import get_order_status


def test_existing_order():
    result = get_order_status("KE1002")

    assert "KE1002" in result
    assert "Prestige pressure cooker" in result
    assert "Shipped" in result


def test_order_id_is_case_insensitive():
    result = get_order_status("ke1002")

    assert "KE1002" in result


def test_nonexistent_order():
    result = get_order_status("KE9999")

    assert "No order found" in result
