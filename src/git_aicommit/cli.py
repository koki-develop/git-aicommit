import sys
from xml.sax.saxutils import escape as xml_escape
from importlib.metadata import version
import readchar
import click
from rich.prompt import Prompt
from rich.console import Console
from rich.markdown import Markdown
from rich.padding import Padding
from git_aicommit.config import load_config
from git_aicommit.git import Git
from git_aicommit.ai import AI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_ollama import ChatOllama


@click.command("git-aicommit", help="Generate commit messages using AI.")
@click.version_option(version("git-aicommit"), prog_name="git-aicommit")
def root():
    try:
        config = load_config()

        ai = AI(
            model=ChatOllama(
                model=config.ollama.model,
                temperature=config.ollama.temperature,
                base_url=config.ollama.base_url,
            )
        )
        git = Git(".")
        console = Console()

        if not git.is_staged():
            console.print("No staged changes found.")
            return

        diff = git.diff()
        recent_logs = git.logs()[-10:]
        recent_logs.reverse()

        history: list[BaseMessage] = []
        while True:
            message = ai.generate_commit_message(
                recent_logs=recent_logs, diff=diff, history=history
            )
            history.append((AIMessage(message)))
            console.print(
                Padding(
                    Markdown(
                        f"```\n{message}\n```\n\n`c`: Commit message / `r`: Regenerate / `q`: Quit"
                    ),
                    (0, 1),
                )
            )

            while True:
                key = readchar.readkey()
                if not key in ("c", "r", "q"):
                    continue
                break

            if key == "c":
                git.commit(message)
                console.print("[bold green]Committed successfully![/bold green]")
                break

            elif key == "r":
                print()
                feedback = Prompt.ask(
                    "Please provide feedback to improve the commit message"
                )
                if not feedback.strip():
                    console.print("Aborting commit.")
                    return
                print()
                history.append(
                    HumanMessage(f"<feedback>{xml_escape(feedback)}</feedback>")
                )
                continue

            elif key == "q":
                console.print("Aborting commit.")
                return

    except KeyboardInterrupt:
        sys.exit(130)


if __name__ == "__main__":
    root()
