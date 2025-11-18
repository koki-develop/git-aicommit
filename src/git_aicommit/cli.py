import sys
from typing import Literal
from xml.sax.saxutils import escape as xml_escape
from importlib.metadata import version
import readchar
import click
from halo import Halo
from rich.prompt import Prompt
from rich.console import Console
from rich.markdown import Markdown
from rich.padding import Padding
from git_aicommit.config import load_config, Config
from git_aicommit.git import Git
from git_aicommit.ai import AI
from git_aicommit.error import AbortCommitError
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.language_models import BaseChatModel
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

console = Console()


def _preview_message(message: str) -> None:
    console.print(
        Markdown("**Generated Commit Message:**\n\n"),
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


def _load_model(config: Config) -> BaseChatModel:
    if config.provider == "ollama":
        if config.ollama is None:
            raise ValueError("Ollama configuration is missing.")
        return ChatOllama(
            model=config.ollama.model,
            temperature=config.ollama.temperature,
            base_url=config.ollama.base_url,
        )

    elif config.provider == "openai":
        if config.openai is None:
            raise ValueError("OpenAI configuration is missing.")
        return ChatOpenAI(
            model=config.openai.model,
            api_key=config.openai.api_key,
            temperature=config.openai.temperature,
        )

    else:
        raise ValueError(f"Unsupported provider: {config.provider}")


@click.command("git-aicommit", help="Generate commit messages using AI.")
@click.version_option(version("git-aicommit"), prog_name="git-aicommit")
def root():
    try:
        config = load_config()
        model = _load_model(config)

        ai = AI(model=model)
        git = Git(".")

        if not git.is_staged():
            console.print("No staged changes found.")
            return

        diff = git.diff()
        recent_logs = git.logs()[-10:]
        recent_logs.reverse()

        history: list[BaseMessage] = []
        while True:
            with Halo(text="Generating commit message...", spinner="dots"):
                message = ai.generate_commit_message(
                    recent_logs=recent_logs, diff=diff, history=history
                )
            history.append(AIMessage(message))
            _preview_message(message)

            action = _read_action()
            print()

            if action == "commit":
                with Halo(text="Committing changes...", spinner="dots"):
                    git.commit(message)
                console.print("[bold green]Committed successfully![/bold green]")
                break

            elif action == "regenerate":
                feedback = Prompt.ask(
                    "[bold]Provide feedback to refine the commit message[/bold]"
                )
                if not feedback.strip():
                    raise AbortCommitError()
                print()
                history.append(
                    HumanMessage(f"<feedback>{xml_escape(feedback)}</feedback>")
                )
                continue

            elif action == "quit":
                raise AbortCommitError()

    except AbortCommitError:
        print("Aborted commit.")
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(130)


if __name__ == "__main__":
    root()
