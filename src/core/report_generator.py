import csv
from pathlib import Path
from typing import List
from sqlalchemy.orm import Session
from src.db.models import OrderModel


def generate_report(db: Session, output_path: str = "data/report.csv") -> None:
    """
    Generates a CSV report with all processed orders.

    Args:
        db (Session): Active database session.
        output_path (str): Path to save the generated CSV file.
    """
    orders: List[OrderModel] = db.query(OrderModel).all()

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["order_id", "customer", "address", "payment_method", "total", "status"])

        for order in orders:
            writer.writerow([
                order.order_id,
                order.customer,
                order.address,
                order.payment_method,
                f"{order.total:.2f}",
                order.status
            ])
