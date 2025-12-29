
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
        # Hashmap (Dict): Key=Product ID, Value=Product object, which allows O(1) average time complexity for CRUD.
        self._products: Dict[str, Product] = {}
        # Stack (List): Used to record transaction history, simulating an undo stack.
        self._transaction_history: List[Transaction] = []
        logger.warning("InventoryManager initialized.")

    def add_product(self, product: Product) -> None:
        if product.product_id in self._products:
            raise ValueError(f"Product with ID {product.product_id} already exists.")

        self._products[product.product_id] = product
        logger.info(f"Added product: {product.name} ({product.product_id})")

    def get_product(self, product_id: str) -> Optional[Product]:
        logger.info(f"Fetching product #{product_id}...")
        return self._products.get(product_id)

    def list_all_products(self) -> List[Product]:
        return list(self._products.values())

    def update_stock(self, transaction: Transaction) -> None:
        """
        Update product stock based on a transaction and records the history.
        Checks for safety stock threshold after update.
        """
        product = self.get_product(transaction.product_id)

        if not product:
            raise ValueError(f"Product ID {transaction.product_id} not found for transaction.")
        # Update stock
        logger.info("Updating stock...")
        product.current_stock += transaction.quantity_change

        # ensure stock does not go negative for outbound transactions
        if product.current_stock < 0 and transaction.transaction_type == Transaction.TYPE_OUTBOUND:
            product.current_stock = 0
            logger.error(f"Stock went negative for {product.name}. Stock capped at 0.")

        # Record transaction
        self._transaction_history.append(transaction)

        # Check safety stock threshold
        if product.current_stock <= product.safety_stock_threshold:
            logger.warning(
                f"ALERT: Stock for {product.name} (ID: {product.product_id}) is at {product.current_stock}, "
                f"which is below the safety threshold of {product.safety_stock_threshold}."
            )

    def get_top_n_products_by_stock(self, n: int) -> List[Product]:
        """
        Returns the top N products with the highest stock levels using a Min-Heap (heapq).
        """
        if n <= 0:
            return []

        min_heap: List[Tuple[int, Product]] = []

        for product in self._products.values():
            stock = product.current_stock

            if len(min_heap) < n:
                heapq.heappush(min_heap, (stock, product))
            else:
                if stock > min_heap[0][0]:
                    heapq.heapreplace(min_heap, (stock, product))

        result_products = [item[1] for item in min_heap]
        result_products.sort(key=lambda p: p.current_stock, reverse=True)

        return result_products

    def check_and_process_item(self, product_id: str) -> str:
        """
        Performs external status check and handles various outcomes.
        """
        import oes_core.utils

        try:
            # External call that we will mock
            status_code = oes_core.utils.check_status(product_id)

            if status_code == 200:
                return "PROCESSED"
            elif status_code == 400:
                return "FAILED_VALIDATION"
            else:
                return "UNEXPECTED_CODE"
        except ValueError:
            return "FAILED_VALIDATION"
        except RuntimeError:
            return "ERROR_RUNTIME"

    def perform_batch_status_check(self, item_list: List[str]):
        import oes_core.utils

        for item in item_list:
            oes_core.utils.get_external_status(item)
