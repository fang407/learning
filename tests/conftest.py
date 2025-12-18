import pytest
import tempfile
import uuid
import os
from typing import Dict
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
    config.addinivalue_line(
        "markers", "data_integrity: Mark tests as focusing on data validation and fuzz boundary checks."
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
def stock_warning_manager_setup(empty_inventory_manager: InventoryManager):
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

@pytest.fixture(scope="function")
def temporary_file_resource(request):
    """
    Creates a temporary file resource for a single test function's use.
    Uses a finalizer to ensure the file is closed and deleted, guaranteeing cleanup.
    """
    temp_filename = os.path.join(tempfile.gettempdir(), f"test_data_{uuid.uuid4()}.txt")

    f = open(temp_filename, 'w')
    f.write("Initial resource state data.")
    f.close()

    print(f"\n[SETUP] Created temporary resource: {temp_filename}")

    # YIELD: The fixture provides the path to the test function
    yield temp_filename

    # TEARDOWN PHASE: cleanup the resource. the yield mechanism ensures this block runs even if test fails
    try:
        os.remove(temp_filename)
        print(f"\n[TEARDOWN] Successfully deleted resource: {temp_filename}")
    except OSError as e:
        # Handle cases where the file might have been deleted by the test itself
        print(f"\n[TEARDOWN] Could not delete resource: {e}")


@pytest.fixture(scope="function", autouse=True)
def enforce_data_integrity(shared_inventory_manager: InventoryManager):
    """
    AUTOUSE fixture that verifies all test data in the manager adheres to the core validation rules.
    This prevents flawed test data from reaching the application code.
    """
    manager = shared_inventory_manager

    for product in manager.list_all_products():
        assert product.sku.isalnum(), (
            f"DATA RIGOR FAILURE: SKU '{Product.sku}' is not alphanumeric. "
            f"Fix the fixture populating this data (e.g. populated_manager)."
        )
        assert product.price > 0, (
            f"DATA RIGOR FAILURE: Price for {product.sku} is not positive."
        )

    # Allow the actual test to run
    yield
    # TEARDOWN PHASE
    pass
