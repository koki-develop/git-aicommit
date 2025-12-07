from prompt_toolkit import PromptSession, print_formatted_text
from prompt_toolkit.formatted_text import FormattedText


def prompt(message: str) -> str:
    session = PromptSession()
    print_formatted_text(
        FormattedText(
            [
                ("bold", f"{message}:"),
            ]
        ),
    )
    return session.prompt(
        "> ",
        placeholder=FormattedText([("ansibrightblack", "Enter your message here...")]),
    )
