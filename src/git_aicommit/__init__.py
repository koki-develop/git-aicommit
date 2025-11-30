import os
import warnings


DEBUG_ENABLED = os.getenv("GIT_AICOMMIT_DEBUG") == "true"
DEFAULT_EXCLUDE_FILES = ["package-lock.json", "pnpm-lock.yaml", "bun.lockb", "*.lock"]


# Suppress Pydantic V1 compatibility warning on Python 3.14+ (except in debug mode)
if not DEBUG_ENABLED:
    warnings.filterwarnings(
        "ignore",
        category=UserWarning,
        message="Core Pydantic V1 functionality isn't compatible with Python 3.14 or greater.",
    )
