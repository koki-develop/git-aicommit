import os
import warnings


# Suppress Pydantic V1 compatibility warning on Python 3.14+ (except in debug mode)
if os.getenv("DEBUG") != "true":
    warnings.filterwarnings(
        "ignore",
        category=UserWarning,
        module="langchain_core._api.deprecation",
        message="Core Pydantic V1 functionality isn't compatible with Python 3.14 or greater.",
    )


DEFAULT_EXCLUDE_FILES = ["package-lock.json", "pnpm-lock.yaml", "bun.lockb", "*.lock"]
