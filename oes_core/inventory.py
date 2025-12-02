import collections
import heapq
import logging
from typing import Dict, List, Optional, Tuple

from oes_core.models import Product, Transaction

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

class InventoryManager:
    """
    Manages the inventory of products and records all transactions.
    """
    def __init__(self):
        # Hashmap (Dict): Key=Product ID, Value=Product object.
        # This allows O(1) average time complexity for lookups, additions, and removals.
        self._products: Dict[str, Product] = {}
        # Stack (List): Used to record transaction history, simulating an undo stack.
        # This showcases using a List as a Stack (append/pop).
        self._transaction_history: List[Transaction] = []
        logger.warning("InventoryManager initialized.")

    def add_product(self, product: Product) -> None:
        if product.product_id in self._products:
            raise ValueError(f"Product with ID {product.product_id} already exists.")

        self._products[product.product_id] = product
        logger.info(f"Added product: {product.name} ({product.product_id})")

    def get_product(self, product_id: str) -> Optional[Product]:
        return self._products.get(product_id)

    def list_all_products(self) -> List[Product]:
        return list(self._products.values())

