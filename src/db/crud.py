from sqlalchemy.orm import Session
from src.db.models import OrderModel
from typing import Dict

def save_order(db: Session, order_data: Dict) -> OrderModel:
    new_order = OrderModel(
        order_id=order_data["order_id"],  # ← novo campo
        customer=order_data["customer"],
        address=order_data.get("address", ""),
        payment_method=order_data["payment_method"],
        total=order_data["total"],
        status=order_data["status"]
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order
