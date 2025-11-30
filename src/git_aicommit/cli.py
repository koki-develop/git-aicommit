import os
from pathlib import Path
from typing import Literal
from xml.sax.saxutils import escape as xml_escape
from importlib.metadata import version
from time import time
import readchar
import click
from halo import Halo
from rich.prompt import Prompt, Confirm
from rich.console import Console
from rich.markdown import Markdown
from rich.padding import Padding
from langsmith import tracing_context
from git_aicommit import DEFAULT_EXCLUDE_FILES
from git_aicommit.provider import provider_from_config
from git_aicommit.config import load_config
from git_aicommit.git import Git
from git_aicommit.ai import AI
from git_aicommit.error import (
    error_handle,
    AbortCommitError,
    ConfigurationAlreadyExistsError,
)
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage


console = Console(highlight=False)


def _preview_message(message: str, elapsed_seconds: float) -> None:
    console.print(
        f"[bold]Generated Commit Message:[/bold] [dim]({elapsed_seconds:.2f}s)[/dim]",
        Padding(
            Markdown(
                f"```\n{message}\n```\n\n"
                + "`c`: Commit message / `r`: Regenerate / `q`: Quit"
            ),
            (1, 1, 0, 1),
        ),
    )


def _read_action() -> Literal["commit", "regenerate", "quit"]:
    while True:
        key = readchar.readkey()
        if key == "c":
            return "commit"
        elif key == "r":
            return "regenerate"
        elif key == "q":
            return "quit"


@click.group("git-aicommit", invoke_without_command=True)
@click.option(
    "--include-lockfiles", is_flag=True, default=False, help="Include lock files."
)
@click.version_option(version("git-aicommit"), prog_name="git-aicommit")
@click.pass_context
@error_handle
def root(ctx: click.Context, include_lockfiles: bool):
    """Generate commit messages using AI."""
    if ctx.invoked_subcommand is not None:
        return

    config = load_config()
    provider = provider_from_config(config)

    ai = AI(model=provider.chat_model)
    git = Git(".")

    exclude_files = DEFAULT_EXCLUDE_FILES if not include_lockfiles else []

    if not git.staged_files(exclude_files=exclude_files):
        console.print("No staged changes found.")
        ignored_files = git.staged_files(exclude_files=[])
        if ignored_files:
            print()
            console.print(
                "[bold yellow]NOTE[/bold yellow]: The following files are staged but ignored:"
            )
            for file in ignored_files:
                console.print(f" - {file}")

            console.print(
                "\nUse [bold green]--include-lockfiles[/bold green] to include them."
            )
        return

    diff = git.diff(exclude_files=exclude_files)
    recent_logs = git.logs(max_count=10)

    history: list[BaseMessage] = []
    while True:
        start_time = time()
        with Halo(
            text=f"Generating commit message... \033[90m({provider.name}/{provider.model_name})\033[0m",
            spinner="dots",
        ):
            with tracing_context(
                enabled=os.getenv("GIT_AICOMMIT_LANGSMITH_PROJECT") is not None,
                project_name=os.getenv("GIT_AICOMMIT_LANGSMITH_PROJECT"),
            ):
                message = ai.generate_commit_message(
                    recent_logs=recent_logs, diff=diff, history=history
                )
        elapsed_seconds = time() - start_time
        history.append(AIMessage(message))
        _preview_message(message, elapsed_seconds)

        action = _read_action()
        print()

        if action == "commit":
            while True:
                try:
                    with Halo(text="Committing changes...", spinner="dots"):
                        git.commit(message)
                    console.print("[bold green]Committed successfully![/bold green]")
                    break
                except Exception as e:
                    console.print(f"[bold red]Commit failed:[/bold red] {e}")
                    print()
                    if not Confirm.ask("Retry?"):
                        raise
            break

        elif action == "regenerate":
            feedback = Prompt.ask(
                "[bold]Provide feedback to refine the commit message[/bold]"
            )
            if not feedback.strip():
                raise AbortCommitError()
            print()
            history.append(HumanMessage(f"<feedback>{xml_escape(feedback)}</feedback>"))
            continue

        elif action == "quit":
            raise AbortCommitError()


@root.command()
@error_handle
def init():
    """Initialize configuration file."""
    filenames = [
        ".aicommit.yml",
        "aicommit.yml",
        ".aicommit.yaml",
        "aicommit.yaml",
    ]
    for filename in filenames:
        config_file = Path.cwd() / filename

        if config_file.exists():
            raise ConfigurationAlreadyExistsError(config_file)

    # Sample configuration with all providers commented out
    sample_config = """# Uncomment and configure one of the providers below

# Amazon Bedrock
# provider: aws-bedrock
# aws-bedrock:
#   model: "<model>" # Required (e.g. "us.anthropic.claude-sonnet-4-20250514-v1:0")
#   region: "<region>" # Required (e.g. "us-west-2", "us-east-1")
#   temperature: 0.0 # Optional (default: 0.0)

# Anthropic
# provider: anthropic
# anthropic:
#   model: "<model>" # Required (e.g. "claude-haiku-4-5-20251001", "claude-sonnet-4-5-20250929")
#   api-key: "<api-key>" # Required
#   temperature: 0.0 # Optional (default: 0.0)

# Google GenAI
# provider: google-genai
# google-genai:
#   model: "<model>" # Required (e.g. "gemini-2.5-flash", "gemini-2.5-pro")
#   api-key: "<api-key>" # Required
#   temperature: 0.0 # Optional (default: 0.0)

# Ollama
# provider: ollama
# ollama:
#   model: "<model>" # Required
#   base-url: "http://localhost:11434" # Optional (default: http://localhost:11434)
#   temperature: 0.0 # Optional (default: 0.0)

# OpenAI
# provider: openai
# openai:
#   model: "<model>" # Required (e.g. "gpt-5", "gpt-4.1")
#   api-key: "<api-key>" # Required
#   temperature: 0.0 # Optional (default: 0.0)
"""

    config_file = Path.cwd() / "aicommit.yml"
    config_file.write_text(sample_config)
    console.print(f"[bold green]Configuration file created:[/bold green] {config_file}")


if __name__ == "__main__":
    root()
