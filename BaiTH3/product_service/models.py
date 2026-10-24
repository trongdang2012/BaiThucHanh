from typing import Optional
from datetime import datetime

class Product:
    def __init__(
        self,
        id: Optional[int],
        name: str,
        description: Optional[str],
        price: float,
        quantity: int,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None
    ):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "quantity": self.quantity,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
