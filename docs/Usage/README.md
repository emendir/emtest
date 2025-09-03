# Usage

This directory demonstrates how to use emtest utilities in a real testing scenario with source code validation and dual execution patterns.

This example serves as a template for setting up your own testing workflows with emtest utilities.

## Directory Structure

```
docs/Usage/
├── README.md           # This file
├── conftest.py         # Pytest configuration and path setup
├── test_demo.py        # Main test file with dual execution
└── DemoProject/
    └── demo_project.py # Simple demo module to test
```

## File Breakdown

### `conftest.py` - Essential Setup File
This file is **required** for the testing setup to work properly. It performs two critical functions:

1. **Path Configuration**: Adds the `DemoProject` directory to Python's path so we can import `demo_project`
2. **Reporter Setup**: Configures the minimal pytest reporter for clean output

**Why conftest.py is necessary:**
- Without it, Python can't find the `demo_project` module to import or may load the module from a pip installation instead of your source code
- The pytest reporter configuration ensures clean, minimal output when running tests
- It's automatically loaded by pytest before running any tests

### `test_demo.py` - The Test File
This file contains your test functions and demonstrates how to structure code for preparation and cleanup operations.
It supports the **dual execution pattern** - it can be run both as a pytest test and as a standalone Python script.


**Key Components:**

1. **Auto-Run Import** (enables dual execution):
   ```python
   import _auto_run_with_pytest  # noqa
   ```

2. **Module Import & Validation** (can be placed in `conftest.py` instead):
   ```python
   import demo_project
   assert_is_loaded_from_source(SRC_DIR, demo_project)
   ```

3. **Standard Test Functions**:
   ```python
   def test_pass():
       assert demo_project.add_numbers(1,1) == 2
   
   def test_fail():  # Intentionally fails for demonstration
       assert demo_project.add_numbers(1,1) != 2
   ```

4. **Thread Cleanup Testing**:
   ```python
   def test_threads_cleanup():
       assert await_thread_cleanup(timeout=2)
   ```

### `DemoProject/demo_project.py`
A minimal Python module containing a simple function to demonstrate testing:
```python
def add_numbers(a, b):
    return a+b
```

This represents your actual source code that you want to test - it could be any Python module or package.


## Running the Tests

You can execute the tests in two different ways:

### Method 1: Standard pytest
```bash
cd docs/Usage
pytest test_demo.py
```

This runs pytest normally with all its standard features and output.

### Method 2: Standalone Python script
```bash
cd docs/Usage
python test_demo.py
```

This automatically reruns the file using emtest's custom `run_pytest` function.

### Minimal Output

To get minimal, clean output with colored symbols, set the `PRINT_ERRORS` environment variable:
```sh
PRINT_ERRORS=False
python test_demo.py
```

```
✓ test_pass
✗ test_fail  
✗ test_error
✓ test_threads_cleanup
```

You can change the default behaviour in conftest.py in the line:
```py
PRINT_ERRORS = env_vars.bool("PRINT_ERRORS", default=True)
```


### Enable Breakpoints

To enable python-debugger breakpoints on test failures, pass the `--pdb` option:
```sh
python test_demo.py -pdb
```

### Enable Print Statements

Pytest disables all output from print commands in your test code.
To enable them, pass the `-s` option:
```sh
python test_demo.py -s
```

```
Running tests for test_demo

✓ test_pass
✗ test_fail
✗ test_error
✓ test_threads_cleanup                                                                                                             

Finished tests for test_demo
```
