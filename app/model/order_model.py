import enum
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM
from datetime import datetime, timezone
from app.database.base import Base


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "Order"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("User.id", ondelete="CASCADE"), nullable=False)
    status = Column(PG_ENUM(OrderStatus, name="orderstatus", create_type=False, values_callable=lambda obj: [e.value for e in obj]), default=OrderStatus.PENDING, nullable=False)
    total = Column(Float, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class OrderItem(Base):
    __tablename__ = "OrderItem"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("Order.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("Product.id", ondelete="CASCADE"), nullable=False)
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
