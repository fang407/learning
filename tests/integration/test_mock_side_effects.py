import pytest
import uuid
from oes_core.inventory import InventoryManager

def test_check_and_process_item_handles_sequential_results(mocker, empty_inventory_manager: InventoryManager):
    """
    Tests the InventoryManager against a sequence of Success, Known Failure,
    and Unknown failure results from a mocked dependency.
    """
    manager = empty_inventory_manager
    test_id = "ITEM123"

    # Mock the external utility function
    mock_checker = mocker.patch('oes_core.utils.check_status')

    # 1. Setup the Mocker with side_effect:
    # - Call 1: Success (returns 200)
    # - Call 2: Expected Known Error (raises ValueError)
    # - Call 3: Unexpected Runtime Error (raises generic Exception)
    mock_checker.side_effect = [
        200,
        ValueError("Invalid format detected."),
        RuntimeError("Database connection lost.")
    ]

    # --- 1st call: Success path ---
    result_1 = manager.check_and_process_item(test_id)
    assert result_1 == "PROCESSED"

    # --- 2nd call: known failure path ---
    result_2 = manager.check_and_process_item(test_id)
    assert result_2 == "FAILED_VALIDATION"

    # --- 3rd call: unknown failure path ---
    result_3 = manager.check_and_process_item(test_id)
    assert result_3 == "ERROR_RUNTIME"

    assert mock_checker.call_count == 3
