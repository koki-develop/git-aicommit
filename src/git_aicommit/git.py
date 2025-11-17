from git import Repo


class Git:
    def __init__(self, path: str):
        self.repo = Repo(path)

    def logs(self) -> list[str]:
        return [log.message for log in self.repo.head.log()]

    def is_staged(self) -> bool:
        return self.repo.is_dirty(index=True, working_tree=False)

    def diff(self) -> str:
        return self.repo.git.execute(
            ["git", "diff", "--staged"],
            with_extended_output=False,
            as_process=False,
            stdout_as_string=True,
        )

    def commit(self, message: str) -> None:
        # NOTE: `self.repo.index.commit` does not support commit signing
        self.repo.git.execute(["git", "commit", "-m", message], as_process=False)
