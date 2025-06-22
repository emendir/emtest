
import sys
import os,sys
from emtest import configure_pytest_reporter, add_path_to_python

SRC_DIR=os.path.abspath(
    os.path.join(os.path.dirname(__file__), 
    "DemoProject"
    ))
add_path_to_python(SRC_DIR)

def pytest_configure(config):
    configure_pytest_reporter(config)
