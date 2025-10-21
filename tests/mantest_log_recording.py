import conftest  # noqa
import logging
import emtest.log_recording  # noqa
import traceback

logger = logging.getLogger("my_app")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(handler)

logger.start_recording()
logger.debug("Hello there!")

try:
    logger.start_recording("STEPS")
    logger.debug("step 1")
    logger.debug("step 2")
    raise RuntimeError("Something bad happened!")
except Exception as e:
    recorded = "\n".join(logger.get_recording("STEPS"))
    logger.error(
        f"{e}"
        "\nHere's the log of all steps:\n"
        "-----------------------------------------------"
        # f"\n{recorded}\n"
        f"{traceback.format_exc()}"
        "-----------------------------------------------"
    )
finally:
    logger.stop_recording("STEPS")

logger.stop_recording()
print("\n\n")
print("Full script log:")
print("\n".join(logger.get_recording()))
