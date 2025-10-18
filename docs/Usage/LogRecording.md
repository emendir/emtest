# 📜 `emtest.log_recording` — In-memory Log Recorder for Python `logging`

`emtest.log_recording` is a lightweight utility that makes it easy to **capture and access logs in memory** without changing your existing logging configuration.

This is especially useful for:

* Capturing logs during tests
* Including logs in error messages or reports
* Analyzing or asserting on logs programmatically

---

## ✨ Features

* ✅ Record logs in memory with zero file I/O
* 🧪 Ideal for testing or debugging
* 🧭 Fully compatible with the standard `logging` module
* 🪝 Supports multiple independent recorders identified by names
* 🧱 Safe to use alongside existing handlers (e.g., console or file logging)
* ⚡️ Backward compatible: you can use a single default recorder if you don’t need multiple

---

## 🪄 Basic Usage (Single Recorder)

You can record logs without specifying a name — the default recorder will be used.

```python
import logging
import emtest.log_recording  # noqa

logger = logging.getLogger("my_app")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(handler)

# Start recording logs
logger.start_recording()

logger.debug("step 1")
logger.debug("step 2")

# Get the recorded logs as a list of strings
records = logger.get_recording()
print("\n".join(records))

# Stop recording
logger.stop_recording()
```

✅ **Output example:**

```
2025-10-18 12:00:00 [DEBUG] step 1
2025-10-18 12:00:00 [DEBUG] step 2
```

> 💡 Tip: The recorder captures logs **in the same format** as your existing handler.

---

## 🧠 Advanced Usage (Multiple Named Recorders)

You can create multiple independent recorders identified by a string `name`.
This is handy if you want to record different phases of your program separately.

```python
import logging
import emtest.log_recording  # noqa

logger = logging.getLogger("multi")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

# Start recorder for phase 1
logger.start_recording("phase1")
logger.debug("Init step")

# Start another recorder for phase 2 (both are active)
logger.start_recording("phase2")
logger.debug("More work")

# Retrieve logs per recorder
print("Phase 1 logs:")
print("\n".join(logger.get_recording("phase1")))

print("Phase 2 logs:")
print("\n".join(logger.get_recording("phase2")))

# Stop a specific recorder
logger.stop_recording("phase1")
logger.debug("Final step")

# Phase 2 continues recording
print("Phase 2 after more work:")
print("\n".join(logger.get_recording("phase2")))

# Stop phase 2 recorder
logger.stop_recording("phase2")
```

📌 Each recorder only stores logs **after it started**, and is independent of others.

---

## 🧹 API Reference

### `logger.start_recording(name: Optional[str] = None)`

Start recording logs for a given recorder name.
If `name` is `None`, the default recorder (`"__default__"`) is used.

* Creates and attaches an in-memory handler
* No-op if a recorder with the same name already exists

---

### `logger.get_recording(name: Optional[str] = None) -> list[str]`

Return the list of recorded log messages for the given recorder name.

* If `name` is `None`, uses the default recorder
* Returns `[]` if no recorder with that name exists

---

### `logger.stop_recording(name: Optional[str] = None)`

Stop recording logs for the given recorder name.

* Removes the handler from the logger
* Safe to call even if the recorder doesn’t exist

---

## 🧪 Typical Use Case: Capturing Logs on Error

```python
import logging
import traceback
import emtest.log_recording  # noqa

logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

try:
    logger.start_recording()
    logger.info("Starting process")
    logger.warning("Something looks odd...")
    raise RuntimeError("Something bad happened!")

except Exception as e:
    recorded = "\n".join(logger.get_recording())
    logger.error(
        f"{e}\n"
        "Here's the full log:\n"
        "-----------------------------------------------\n"
        f"{recorded}\n"
        f"{traceback.format_exc()}"
        "-----------------------------------------------"
    )
finally:
    logger.stop_recording()
```

✅ Logs recorded in-memory are embedded directly into the error output.

---

## ⚠️ Notes & Tips

* Recorders are **independent**: stopping one doesn’t affect the others.
* Multiple recorders can be active simultaneously.
* The in-memory buffer is not automatically cleared. You can call:

  ```python
  handler = logger._recording_handlers["phase1"]
  handler.clear()
  ```

  *(or just stop and restart the recorder)*.
* The formatter used by the recorder defaults to your logger’s first handler, or a basic fallback if none exist.

