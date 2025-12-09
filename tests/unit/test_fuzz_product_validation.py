
import pytest
from oes_core.models import Product

# Fuzz Testing using parametrization
@pytest.mark.parametrize(
    "sku, price, stock_threshold, reason",
    [
        # --- Invalid SKU Tests ---
        ("SKU-123", 10.00, 5, "Contains hyphen (not alphanumeric)"),
        ("SKU 123", 10.00, 5, "Contains space (not alphanumeric)"),
        ("", 10.00, 5, "Empty string"),
        # --- Invalid price tests ---
        ("SKU999", -0.01, 5, "Negative price"),
        ("SKU999", 0.00, 5, "Zero price"),
        # --- Invalid threshold tests --
        ("SKU999", 10.00, -1, "Negative stock threshold"),
    ]
)
@pytest.mark.data_integrity
def test_product_creation_fuzz_invalid_inputs_raises_value_error(
        sku: str,
        price: float,
        stock_threshold: int,
        reason: str
):
    with pytest.raises(ValueError):
        Product(
            sku=sku,
            name=f"Fuzz item ({reason})",
            price=price,
            safety_stock_threshold=stock_threshold
        )
