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
    config.addinvalue_line(
        "markers", "smoke: test that verify basic application functionality"
    )
    config.addinvalue_line(
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
