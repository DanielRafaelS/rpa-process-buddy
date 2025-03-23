import logging
import sys

from typing import List
from pathlib import Path
from sqlalchemy.exc import IntegrityError

from src.core.processor import process_orders
from src.core.json_importer import load_orders_from_folder
from src.core.report_generator import generate_report
from src.core.config import get_env, load_env
from src.db.database import create_tables, get_session
from src.db.crud import save_order
from src.db.models import OrderModel

sys.path.append(str(Path(__file__).resolve().parent.parent))

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

def main() -> None:
    """
    Entry point of the script. Processes orders based on input mode,
    stores them in the database, and logs a summary.
    """

    load_env("src/env.json")
    create_tables()
    db = get_session()

    logging.info("Starting order processing...")

    if get_env("INPUT_MODE", as_type=str) == "faker":
        orders: List[dict] = process_orders(n=get_env("FAKER_QUANTITY", as_type=int))

    elif get_env("INPUT_MODE", as_type=str) == "json":
        json_path = get_env("JSON_INPUT_PATH", as_type=str)
        orders = load_orders_from_folder(folder_path=json_path, db=db)

    else:
        logging.error("Invalid INPUT_MODE. Use 'faker' or 'json'.")
        db.close()
        return

    for order_data in orders:
        # Processamento básico
        if "total" not in order_data:
            order_data["total"] = round(sum(
                p["quantity"] * p["price"] for p in order_data["products"]
            ), 2)

        if "status" not in order_data:
            order_data["status"] = "processed"

        try:
            order: OrderModel = save_order(db, order_data)
            logging.info(
                f"Saved order {order.id} - {order.customer} - Total: R${order.total:.2f}"
            )
        except IntegrityError:
            db.rollback()
            logging.warning(
                f"Order already exists and was skipped (order_id={order_data['order_id']})"
            )
            
    if get_env("GENERATE_REPORT", as_type=bool):
        generate_report(db=db)

    db.close()

    logging.info("All orders processed and saved.")


if __name__ == "__main__":
    main()