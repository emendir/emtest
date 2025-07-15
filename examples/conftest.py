"""Script for configuring tests.

Runs automatically when pytest runs a test before loading the test module.
"""
import pytest
import os
from emtest import configure_pytest_reporter, add_path_to_python


PRINT_ERRORS = True  # whether or not to print error messages after failed tests

# add source code paths to python's search paths
SRC_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "DemoProject"
))
add_path_to_python(SRC_DIR)


@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    """Make changes to pytest's behaviour."""
    configure_pytest_reporter(config, print_errors=PRINT_ERRORS)
