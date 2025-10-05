'''
tests/test_import.py
A script to test if all modules can be imported and work correctly
'''

import pytest

# List of modules to test
modules_to_test = [
    "core.task_manager",
    "core.workflow",
    "core.stores",
    "core.approval",
    "core.agent_manager",
    "core.logger",
    "core.memory",
    "agents.planner_agent",
]

@pytest.mark.parametrize("module_name", modules_to_test)
def test_module_import(module_name):
    """
    Ensure that each module can be imported without error.
    """
    try:
        __import__(module_name)  # Dynamically import the module
    except ImportError as e:
        pytest.fail(f"Failed to import module {module_name} due to ImportError: {str(e)}")
    except Exception as e:
        pytest.fail(f"Failed to import module {module_name} due to an unexpected error: {str(e)}")
