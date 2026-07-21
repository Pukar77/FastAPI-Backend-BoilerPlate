from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CartAddInput(BaseModel):
    product_id: int
    quantity: int = 1

class CartUpdateInput(BaseModel):
    quantity: int

class CartItemOutput(BaseModel):
    id: int
    product_id: int
    product_name: str
    price: float
    quantity: int
    total: float
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class CartOutput(BaseModel):
    items: list[CartItemOutput]
    grand_total: float
