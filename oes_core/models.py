from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Any
import uuid
import logging

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

@dataclass
class Transaction:
    """
    model for recording all transaction types and quantities.
    """
    # TYPE CONSTANTS
    TYPE_INBOUND = "INBOUND"
    TYPE_OUTBOUND = "OUTBOUND"
    TYPE_ADJUSTMENT = "ADJUSTMENT"

    transaction_id: str = field(default_factory=lambda: str(uuid.uuid4()), init=False)

    # associated attribute
    product_id: str

    # core attribute
    quantity_change: int
    transaction_type: str
    # metadata
    timestamp: datetime = field(default_factory=datetime.now, init=False)

    def __post_init__(self):
        if self.transaction_type not in (self.TYPE_INBOUND, self.TYPE_OUTBOUND, self.TYPE_ADJUSTMENT):
            raise ValueError(f"Invalid transaction type: {self.transaction_type}")
        if self.transaction_type == self.TYPE_INBOUND and self.quantity_change <= 0:
            raise ValueError("INBOUND transaction must have a positive quantity change.")
        if self.transaction_type == self.TYPE_OUTBOUND and self.quantity_change >= 0:
            raise ValueError("OUTBOUND transaction must have a negative quantity change.")

        print("Testing here!")
        logging.info("How is this not saying?")
