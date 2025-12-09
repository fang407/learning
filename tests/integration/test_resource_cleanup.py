
import pytest
import os
from oes_core.inventory import InventoryManager
from oes_core.models import Product

def test_resource_is_available(temporary_file_resource):
    """Tests that the resource path exists and is readable during the test. """
    file_path = temporary_file_resource
    assert os.path.exists(file_path)

    with open(file_path, 'r') as f:
        content = f.read()
    assert "Initial resource state data." in content

@pytest.mark.performance
@pytest.mark.xfail
def test_resource_cleanup_runs_on_failure(temporary_file_resource):
    """Tests that the teardown still runs even if the test intentionally fails."""
    file_path = temporary_file_resource
    assert os.path.exists(file_path)

    # Intentional failure
    print("\n--- INTENTIONAL TEST FAILURE ---")
    assert 1 == 0, "Simulating a critical bug in the test execution."
