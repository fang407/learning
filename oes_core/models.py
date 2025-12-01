from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Any
import uuid

@dataclass
class Product:
    """
    Base class for all products. Initialization simplified by dataclass method.
    """
    # unique identifier, auto-generated and not required for init
    product_id: str = field(default_factory=lambda: str(uuid.uuid4()), init=False)

    # core attributes, required for init
    sku: str
    name: str
    price: float
    description: Optional[str]=None

    current_stock: int = 0
    safety_stock_threshold: int = 10

    # metadata
    create_at: datetime = field(default_factory=datetime.now, init=False)

    def __post_init__(self):
        if self.price <= 0:
            raise ValueError("Product price must be positive.")
        if self.safety_stock_threshold < 0:
            raise ValueError("Safety stock threshold cannot be negative.")
        if not self.sku.isalnum():
            raise ValueError("SKU must be alphanumeric.")

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Product):
            return NotImplemented
        return self.current_stock < other.current_stock

    def get_info(self) -> dict:
        return {
            'product_id': self.product_id,
            'sku': self.sku,
            'name': self.name,
            'price': self.price,
            'current_stock': self.current_stock
        }
