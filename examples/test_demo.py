# This test file demonstrates emtest's dual execution pattern:
# - Run with pytest: 'pytest test_demo.py' (standard pytest output)
# - Run standalone: 'python test_demo.py' (minimal output with custom settings)

# DUAL EXECUTION PATTERN:
# This import allows us to run this script with either pytest or python
import _auto_run_with_pytest  # noqa

# Import the source directory path configured in conftest.py
from conftest import SRC_DIR
# Import the module we want to test (made available by conftest.py path setup)
import demo_project
import pytest
# Import emtest utilities for source validation, thread cleanup, and custom test running
from emtest import assert_is_loaded_from_source, await_thread_cleanup, run_pytest


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    """Wrap around tests, running preparations and cleaning up afterwards.

    A module-level fixture that runs once for all tests in this file.
    """
    # Setup: code here runs before tests that uses this fixture
    print(f"\nRunning tests for {__name__}\n")

    # CRITICAL: Verify we're testing source code, not an installed package
    # This prevents testing the wrong version of your code
    assert_is_loaded_from_source(SRC_DIR, demo_project)

    yield  # This separates setup from teardown

    # Teardown: code here runs after the tests
    print(f"\nFinished tests for {__name__}\n")


# Basic functionality test - should pass
def test_pass():
    """Test the basic functionality of our demo module."""
    assert demo_project.add_numbers(1, 1) == 2

# Intentionally failing test for demonstration purposes


def test_fail():
    """This test intentionally fails to show failure output in different execution modes."""
    assert demo_project.add_numbers(1, 1) != 2

# Thread cleanup validation test


def test_threads_cleanup():
    """Verify that all background threads have properly exited.

    This is important for tests that spawn background threads, ensuring
    clean test isolation and preventing resource leaks.
    """
    assert await_thread_cleanup(timeout=2)

