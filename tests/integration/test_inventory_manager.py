import pytest
import uuid
import random
from typing import List
from oes_core.models import Product
from oes_core.inventory import InventoryManager, Transaction

def test_add_and_get_product_success(empty_inventory_manager: InventoryManager, base_product: Product):
    """Test O(1) addition and retrieval via product ID."""
    manager = empty_inventory_manager
    initial_id = base_product.product_id

    manager.add_product(base_product)
    retrieved_product = manager.get_product(initial_id)

    assert retrieved_product is not None
    assert retrieved_product.name == "Base Laptop Model"
    assert len(manager.list_all_products()) == 1

def test_add_duplicate_product_raise_error(empty_inventory_manager: InventoryManager, base_product: Product):
    """Tests that adding a product with an existing ID is prevented."""
    manager = empty_inventory_manager
    manager.add_product(base_product)

    with pytest.raises(ValueError, match="already exists."):
        manager.add_product(base_product)

def test_get_non_existent_product_returns_none(empty_inventory_manager: InventoryManager):
    """Test the safe retrival of a non-existing product."""
    manager = empty_inventory_manager
    assert manager.get_product(str(uuid.uuid4())) is None

def test_update_stock_flow_and_history(empty_inventory_manager: InventoryManager, base_product: Product):
    """Test stock update logic, history recording, and boundary checks."""
    manager = empty_inventory_manager
    manager.add_product(base_product)
    product_id = base_product.product_id

    assert manager.get_product(product_id).current_stock == 0

    # 1. INBOUND transaction to increase stock
    inbound_tx = Transaction(
        product_id=product_id,
        quantity_change=50,
        transaction_type=Transaction.TYPE_INBOUND
    )
    manager.update_stock(inbound_tx)

    assert manager.get_product(product_id).current_stock == 50
    assert len(manager._transaction_history) == 1

    # 2. OUTBOUND Transaction to decrease stock
    outbound_tx = Transaction(
        product_id=product_id,
        quantity_change=-15,
        transaction_type=Transaction.TYPE_OUTBOUND
    )
    manager.update_stock(outbound_tx)

    assert manager.get_product(product_id).current_stock == 35
    assert len(manager._transaction_history) == 2
    assert manager._transaction_history[-1].transaction_type == Transaction.TYPE_OUTBOUND

def test_update_stock_prevents_negative_stock(empty_inventory_manager: InventoryManager, base_product: Product):
    """Test the boundary condition where stock should be capped at zero."""
    manager = empty_inventory_manager
    manager.add_product(base_product)
    product_id = base_product.product_id

    outbound_tx = Transaction(
        product_id=product_id,
        quantity_change=-10,
        transaction_type=Transaction.TYPE_OUTBOUND
    )
    manager.update_stock(outbound_tx)

    assert manager.get_product(product_id).current_stock == 0
    assert len(manager._transaction_history) == 1

# --- Parametrized Top K Test ---

@pytest.mark.parametrize(
    "n, expected_skus",
    [
        (0, []),
        (1, ["SKU5"]),
        (3, ["SKU5", "SKU3", "SKU1"]),
        (10, ["SKU5", "SKU3", "SKU1", "SKU2", "SKU4"]),
    ]
)
@pytest.mark.performance
def test_get_top_n_products_by_stock_parametrized(
        populated_manager: InventoryManager,
        n: int,
        expected_skus: List[str]
):
    """
    Tests the Top K algorithm using parametrized inputs.
    Verifies output order (highest stock first).
    """
    manager = populated_manager

    top_n_products = manager.get_top_n_products_by_stock(n)
    result_skus = [p.sku for p in top_n_products]

    assert result_skus == expected_skus
