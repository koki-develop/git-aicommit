from git import Repo


class Git:
    def __init__(self, path: str):
        self.repo = Repo(path)

    def logs(self, max_count: int) -> list[str]:
        return [
            (
                commit.message.strip()
                if isinstance(commit.message, str)
                else bytes(commit.message).decode("utf-8").strip()
            )
            for commit in self.repo.iter_commits("HEAD", max_count=max_count)
        ]

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
