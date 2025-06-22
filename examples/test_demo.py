

from conftest import SRC_DIR
import demo_project
import pytest
from emtest import assert_is_loaded_from_source, await_thread_cleanup, run_pytest


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    # Setup: code here runs before tests that uses this fixture
    print(f"\nRunning tests for {__name__}\n")
    assert_is_loaded_from_source(SRC_DIR, demo_project)

    yield  # This separates setup from teardown

    # Teardown: code here runs after the tests
    print(f"\nFinished tests for {__name__}\n")


def test_pass():
    assert demo_project.add_numbers(1,1) == 2

def test_fail():
    assert demo_project.add_numbers(1,1) != 2

def test_threads_cleanup():
    assert await_thread_cleanup(timeout=2)

BREAKPOINTS = False
if __name__ == "__main__":

    run_pytest(
        test_path=__file__,
         breakpoints=BREAKPOINTS,
         deactivate_pytest_output=True,
          enable_print=True
      )
