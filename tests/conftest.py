import pytest
import datetime
import uuid
import logging
import io
from typing import Dict, List, Tuple
from oes_core.models import Product, Transaction
from oes_core.inventory import InventoryManager

# --- 1. Pytest hooks and configuration ---

def pytest_configure(config):
    """Register custom markers to avoid warning."""
    config.addinivalue_line(
        "markers", "smoke: test that verify basic application functionality"
    )
    config.addinivalue_line(
        "markers", "performance: tests that measure efficiency (e.g., Top K algorithm)"
    )

# --- 2. Basic Utility Fixtures ---

@pytest.fixture(scope="function")
def product_data() -> Dict:
    """Returns a dictionary of valid product creation data."""
    # Provides a clean dictionary data, independent of instance creation
    return {
        "sku": "LAP100",
        "name": "Base Laptop Model",
        "price": 999.99
    }

@pytest.fixture(scope="function")
def base_product(product_data: Dict) -> Product:
    """Returns a fresh Product instance for a single test function."""
    # Use the product_data fixture
    return Product(**product_data)

#  --- 3. Inventory Manager Fixtures ---
@pytest.fixture(scope="module")
def shared_inventory_manager() -> InventoryManager:
    """
    Returns an InventoryManager instance scope to the MODULE.
    All tests in a single file will share this instance.
    (Useful for integration tests where setup cost is high)
    """
    manager = InventoryManager()
    # Optional: pre-populate the shared manager (e.g., for performance tests)
    manager.add_product(Product(sku="A01", name="Product A", price=10, current_stock=50))
    manager.add_product(Product(sku="B02", name="Product B", price=20, current_stock=100))

    return manager

@pytest.fixture(scope="function")
def empty_inventory_manager() -> InventoryManager:
    """
    Returns a fresh, clean InventoryManager instance for every test function.
    (Ensure test isolation, which is preferred for unit tests)
    """
    return InventoryManager()

# --- 4. Mocking & Logging Fixtures ---

@pytest.fixture(scope="function")
def stock_warning_manager_setup(empty_inventory_manager: InventoryManager) -> Product:
    """
    Sets up a manager with a product and create the nessary transaction, but DOES NOT EXECUTE IT.
    """
    manager = empty_inventory_manager

    product = Product(
        sku="TESTLOW",
        name="Low Stock Item",
        price=5.0,
        current_stock=15,
        safety_stock_threshold=20 # Threshold is higher than current stock
    )
    manager.add_product(product)

    transaction = Transaction(
        product_id=product.product_id,
        quantity_change=-10,
        transaction_type=Transaction.TYPE_OUTBOUND
    )

    return manager, product, transaction

@pytest.fixture(scope="function")
def mock_transaction() -> Transaction:
    """Returns a valid outbound transaction for testing updates."""
    # Assumes a product with this UUID exists in the test scope, or it will raise an error.
    return Transaction(
        product_id=str(uuid.uuid4()),
        quantity_change=-5,
        transaction_type=Transaction.TYPE_OUTBOUND
    )
