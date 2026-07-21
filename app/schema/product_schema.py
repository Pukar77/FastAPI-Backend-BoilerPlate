from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProductOutput(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
