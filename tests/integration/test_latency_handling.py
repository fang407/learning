
import pytest
import time
from oes_core.inventory import InventoryManager

def mock_slow_api_call(*args, **kwargs):
    """A side effect function that pauses execution for 0.1 seconds."""
    time.sleep(0.1)
    return 200

def test_slow_dependency_management(mocker, empty_inventory_manager: InventoryManager):
    """
    Tests that a function relying on a slow dependency executes within expected time limits.
    """
    manager = empty_inventory_manager
    mock_checker = mocker.patch('oes_core.utils.get_external_status', side_effect=mock_slow_api_call)

    MAX_EXPECTED_TIME = 0.33
    start_time = time.time()

    manager.perform_batch_status_check(['ItemA', 'ItemB', 'ItemC'])
    end_time = time.time()

    elapsed_time = end_time - start_time
    assert mock_checker.call_count == 3
    assert elapsed_time < MAX_EXPECTED_TIME

