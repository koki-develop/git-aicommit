from xml.sax.saxutils import escape as xml_escape
import click
from rich.prompt import Confirm, Prompt
from rich.console import Console
from rich.markdown import Markdown
from rich.padding import Padding
from src.lib.config import load_config
from src.lib.git import Git
from src.lib.ai import AI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_ollama import ChatOllama


@click.command()
def root():
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
        console.print(Padding(Markdown(f"```\n{message}\n```"), (0, 1)))

        if not Confirm.ask("Do you want to use this commit message?"):
            feedback = Prompt.ask(
                "Please provide feedback to improve the commit message"
            )
            if not feedback.strip():
                console.print("Aborting commit.")
                return
            history.append(HumanMessage(f"<feedback>{xml_escape(feedback)}</feedback>"))
            continue

        git.commit(message)
        console.print("[bold green]Committed successfully![/bold green]")
        break


if __name__ == "__main__":
    root()
