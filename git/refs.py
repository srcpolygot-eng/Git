"""
Git Reference Store (Branches, Tags, HEAD, Reflogs)
"""

from pathlib import Path
from typing import Optional, List, Tuple


class RefStore:
    def __init__(self, repo_path: str = "."):
        self.gitdir = Path(repo_path) / ".git"

    def get_head(self) -> str:
        head_file = self.gitdir / "HEAD"
        if not head_file.exists():
            return ""

        content = head_file.read_text().strip()
        if content.startswith("ref: "):
            return self.read_ref(content[5:])
        return content

    def read_ref(self, ref_path: str) -> str:
        target = self.gitdir / ref_path
        if target.exists():
            return target.read_text().strip()
        return ""

    def write_ref(self, ref_path: str, sha1: str):
        target = self.gitdir / ref_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f"{sha1}\n")
        self.append_reflog(ref_path, sha1)

    def update_head(self, sha1: str):
        head_file = self.gitdir / "HEAD"
        content = head_file.read_text().strip() if head_file.exists() else ""
        if content.startswith("ref: "):
            self.write_ref(content[5:], sha1)
        else:
            head_file.write_text(f"{sha1}\n")
        self.append_reflog("HEAD", sha1)

    def append_reflog(self, ref_name: str, new_sha: str):
        log_file = self.gitdir / "logs" / ref_name
        log_file.parent.mkdir(parents=True, exist_ok=True)
        entry = f"0000000000000000000000000000000000000000 {new_sha} User <dev@pygit.org> 0 +0000\tcommit\n"
        with log_file.open("a") as f:
            f.write(entry)

    def create_branch(self, branch_name: str, sha1: str):
        self.write_ref(f"refs/heads/{branch_name}", sha1)

    def delete_branch(self, branch_name: str):
        target = self.gitdir / "refs" / "heads" / branch_name
        if target.exists():
            target.unlink()

    def list_branches(self) -> List[str]:
        heads_dir = self.gitdir / "refs" / "heads"
        if not heads_dir.exists():
            return []
        return [f.name for f in heads_dir.iterdir() if f.is_file()]

    def list_tags(self) -> List[str]:
        tags_dir = self.gitdir / "refs" / "tags"
        if not tags_dir.exists():
            return []
        return [f.name for f in tags_dir.iterdir() if f.is_file()]
