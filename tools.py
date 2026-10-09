
import csv
from pathlib import Path

ORDERS_FILE = Path(__file__).resolve().parent / "orders.csv"


def get_order_status(order_id: str) -> str:
    """Look up a KartEase order by its ID."""

    requested_id = order_id.strip().upper()

    with ORDERS_FILE.open(
        mode="r",
        newline="",
        encoding="utf-8-sig",
    ) as file:
        reader = csv.DictReader(file)

        for order in reader:
            if order.get("order_id", "").strip().upper() == requested_id:
                return "\n".join(
                    f"{key}: {value}" for key, value in order.items()
                )

    return f"No order found with ID {requested_id}."


if __name__ == "__main__":
    print(get_order_status("KE1002"))
