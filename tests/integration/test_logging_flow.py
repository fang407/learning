
import pytest
import logging
from unittest.mock import MagicMock
from oes_core.models import Product, Transaction
from oes_core.inventory import InventoryManager

def test_stock_update_triggers_warning_log(caplog, stock_warning_manager_setup: Product):
    """
    Tests that the InventoryManager correctly emits a WARNING log when stock drops below the safety threshold.
    """
    manager, product, transaction = stock_warning_manager_setup

    with caplog.at_level(logging.WARNING):
        manager.update_stock(transaction)

        assert caplog.record_tuples[0][1] == logging.WARNING
        warning_message = f"ALERT: Stock for {product.name}"
        assert warning_message in caplog.text
        assert len(caplog.record_tuples) == 1

def test_stock_update_does_not_trigger_warning_above_threshold(caplog, empty_inventory_manager: InventoryManager):
    """
    Tests that no WARNING is logged if stock remains above the threshold.
    """
    manager = empty_inventory_manager
    product = Product(sku="SAFE01", name="Safe Item", price=10, current_stock=50, safety_stock_threshold=10)
    manager.add_product(product)

    safe_tx = Transaction(
        product_id=product.product_id,
        quantity_change=5,
        transaction_type=Transaction.TYPE_INBOUND
    )

    with caplog.at_level(logging.WARNING):
        manager.update_stock(safe_tx)
        assert "ALERT" not in caplog.text
        assert len(caplog.record_tuples) == 0 # Only INFO/DEBUG logs might be there, but WARNING should be empty

def test_stock_update_calls_external_reporting_system(mocker, empty_inventory_manager: InventoryManager):
    """
    Tests that a hypothetical 'send_alert_email' function is called exactly once when the stock threshold is breached.
    """
    manager = empty_inventory_manager
    product = Product(
        sku="MOCK01",
        name="Mocked Item",
        price=10,
        current_stock=25,
        safety_stock_threshold=30
    )
    manager.add_product(product)

    mock_email_sender = mocker.patch('logging.Logger.warning')

    outbound_tx = Transaction(
        product_id=product.product_id,
        quantity_change=-5,
        transaction_type=Transaction.TYPE_OUTBOUND
    )
    manager.update_stock(outbound_tx)

    mock_email_sender.assert_called_once()

    called_message = mock_email_sender.call_args[0][0]
    assert called_message.startswith("ALERT")
    assert product.product_id in called_message

def test_stock_update_does_not_call_sender_when_safe(mocker, empty_inventory_manager: InventoryManager):
    """Tests that the mock function is NOT called if the threshold is safe."""
    manager = empty_inventory_manager
    product = Product(sku="MOCK02", name="Safe Mock Item", price=10, current_stock=50, safety_stock_threshold=10)
    manager.add_product(product)

    mock_email_sender = mocker.patch('logging.Logger.warning')

    outbound_tx = Transaction(
        product_id=product.product_id,
        quantity_change=-5,
        transaction_type=Transaction.TYPE_OUTBOUND
    )
    manager.update_stock(outbound_tx)

    mock_email_sender.assert_not_called()
