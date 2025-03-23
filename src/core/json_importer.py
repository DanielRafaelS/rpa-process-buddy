import json
from pathlib import Path
from typing import List, Dict
from sqlalchemy.orm import Session
from src.db.models import OrderModel


def load_orders_from_folder(folder_path: str, db: Session) -> List[Dict]:
    """
    Loads orders from JSON files in a folder, where each file contains a list of orders.

    Args:
        folder_path (str): Path to the folder containing batch JSON files.
        db (Session): SQLAlchemy session for checking processed order_ids.

    Returns:
        List[Dict]: List of unprocessed (new) order dictionaries.
    """
    orders_to_process: List[Dict] = []
    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    for file in folder.glob("*.json"):
        try:
            with file.open("r", encoding="utf-8") as f:
                batch = json.load(f)

            if not isinstance(batch, list):
                print(f"File {file.name} does not contain a list of orders. Skipping.")
                continue

            for order in batch:
                order_id = order.get("order_id")
                if not order_id:
                    print(f"Order in {file.name} missing 'order_id'. Skipping.")
                    continue

                already_exists = db.query(OrderModel).filter_by(order_id=order_id).first()
                if already_exists:
                    print(f" Order {order_id} already processed. Skipping.")
                    continue

                orders_to_process.append(order)

        except Exception as e:
            print(f"Failed to read {file.name}: {e}")

    return orders_to_process
