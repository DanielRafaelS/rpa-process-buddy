from sqlalchemy import Column, Integer, String, Float, UniqueConstraint
from src.db.database import Base


class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, unique=True, nullable=False)  # ← novo campo
    customer = Column(String, nullable=False)
    address = Column(String, nullable=True)
    payment_method = Column(String, nullable=False)
    total = Column(Float, nullable=False)
    status = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("order_id", name="uq_order_id"),
    )
