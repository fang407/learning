import pytest
import uuid
import datetime
from oes_core.models import Product, Transaction

# Helper function to create a base product for reuse
def create_base_product():
    """Returns a valid product instance for testing."""
    return Product(
        sku="P001",
        name="Macbook Pro",
        price=1200.50
    )

# Test product initialization and attributes
def test_product_successful_creation():
    """Test a product is generated with correct input and auto-generated fields."""
    product = create_base_product()

    assert isinstance(product.product_id, str)
    assert len(product.product_id) > 10
    assert isinstance(product.create_at, datetime.datetime)

    assert product.current_stock == 0
    assert product.safety_stock_threshold == 10

    assert product.sku == "P001"
    assert product.price == 1200.50

def test_product_lt_comparison():
    """Test __lt__ method."""
    p_low = create_base_product()
    p_low.current_stock = 5

    p_high = Product(sku="P002", name="Monitor", price=300.00)
    p_high.current_stock = 15

    assert p_low < p_high
    assert not (p_high < p_low)

    p_same = Product(sku="P003", name="Mouse", price=25.00)
    p_same.current_stock = 15
    assert not (p_same < p_high)

# Test product validation
def test_product_sku_value_error():
    invalid_sku = "P-001!"

    with pytest.raises(ValueError, match="SKU must be alphanumeric."):
        Product(sku=invalid_sku, name="Invalid item", price=10.00)

def test_product_price_value_error():
    with pytest.raises(ValueError, match="Product price must be positive."):
        Product(sku="P004", name="Zero Price Item", price=0.00)
    with pytest.raises(ValueError, match="Product price must be positive."):
        Product(sku="P005", name="Negative Price Item", price=-5.00)

# Testing transaction model Integrity and Validation
def test_transaction_inbound_creation():
    t = Transaction(
        product_id=str(uuid.uuid4()),
        quantity_change=50,
        transaction_type=Transaction.TYPE_INBOUND
    )
    assert t.quantity_change == 50
    assert t.transaction_type == "INBOUND"

def test_transaction_type_value_error():
    with pytest.raises(ValueError, match="Invalid transaction type: BOGUS"):
        Transaction(
            product_id="some_id",
            quantity_change=10,
            transaction_type="BOGUS"
        )

def test_transaction_quantity_value_error():
    with pytest.raises(ValueError, match="INBOUND transaction must have a positive quantity change."):
        Transaction(
            product_id="some_id",
            quantity_change=0,
            transaction_type=Transaction.TYPE_INBOUND
        )

    with pytest.raises(ValueError, match="OUTBOUND transaction must have a negative quantity change."):
        Transaction(
            product_id="some_id",
            quantity_change=0,
            transaction_type=Transaction.TYPE_OUTBOUND
        )

    with pytest.raises(ValueError, match="OUTBOUND transaction must have a negative quantity change."):
        Transaction(
            product_id="some_id",
            quantity_change=10,
            transaction_type=Transaction.TYPE_OUTBOUND
        )
