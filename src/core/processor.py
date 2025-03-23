import uuid
import random
from faker import Faker
from typing import List, Dict

fake = Faker()


def process_orders(n: int = 10) -> List[Dict]:
    """
    Generates and processes a list of fake customer orders.

    Each order includes a unique order_id, customer data, payment method,
    address, calculated total, and a fixed status.

    Args:
        n (int): Number of fake orders to generate.

    Returns:
        List[Dict]: A list of processed order dictionaries.
    """
    orders: List[Dict] = []

    for _ in range(n):
        products = [
            {
                "name": fake.word().capitalize(),
                "quantity": random.randint(1, 5),
                "price": round(random.uniform(10.0, 300.0), 2)
            }
            for _ in range(random.randint(1, 4))
        ]

        total = round(sum(p["quantity"] * p["price"] for p in products), 2)

        order = {
            "order_id": str(uuid.uuid4()),
            "customer": fake.name(),
            "address": fake.address().replace("\n", ", "),
            "payment_method": random.choice(["Credit Card", "Pix", "Boleto", "Debit"]),
            "products": products,
            "total": total,
            "status": "processed"
        }

        orders.append(order)

    return orders
