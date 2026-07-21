from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class OrderItemOutput(BaseModel):
    id: int
    product_id: int
    product_name: str
    quantity: int
    price: float
    total: float
    created_at: datetime

class OrderOutput(BaseModel):
    id: int
    status: str
    total: float
    items: list[OrderItemOutput]
    created_at: datetime
    updated_at: datetime
