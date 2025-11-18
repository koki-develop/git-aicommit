import sys
from pathlib import Path
from functools import wraps
from rich.console import Console

console = Console(highlight=False)


def error_handle(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AbortCommitError as e:
            console.print(str(e))
            sys.exit(1)
        except KeyboardInterrupt:
            sys.exit(130)
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")
            sys.exit(1)

    return wrapper


class AbortCommitError(Exception):
    def __init__(self):
        super().__init__("Aborted commit.")


class ConfigurationAlreadyExistsError(Exception):
    def __init__(self, filepath: Path):
        self.filepath = filepath
        super().__init__(f"Configuration file already exists: {self.filepath}")


class InvalidConfigurationError(Exception):
    def __init__(self, error_message: str):
        super().__init__(f"Invalid configuration: {error_message}")
