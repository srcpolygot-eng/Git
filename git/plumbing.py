"""
Git Plumbing Commands Implementation
"""

from typing import Tuple, List
from .repo import Repository
from .objects import Blob, Tree, TreeEntry, Commit


class Plumbing:
    def __init__(self, repo: Repository):
        self.repo = repo

    def hash_object(self, data: bytes, obj_type: str = "blob", write: bool = True) -> str:
        if obj_type == "blob":
            obj = Blob(data)
        elif obj_type == "tree":
            obj = Tree()
        else:
            obj = Blob(data)

        if write:
            return self.repo.write_object(obj)
        return obj.compute_hash()

    def cat_file(self, sha1: str) -> Tuple[str, bytes]:
        obj = self.repo.read_object(sha1)
        return obj.fmt.decode("utf-8"), obj.serialize()

    def write_tree_from_index(self, index_entries: list) -> str:
        tree = Tree()
        for entry in index_entries:
            mode = oct(entry.mode)[2:] if hasattr(entry, 'mode') else "100644"
            tree.entries.append(TreeEntry(mode, entry.path, entry.sha1))
        return self.repo.write_object(tree)

    def commit_tree(self, tree_sha: str, parents: list, message: str, author: str = "Dev <dev@pygit.local>") -> str:
        commit = Commit(
            tree=tree_sha,
            parents=parents,
            author=author,
            committer=author,
            message=message
        )
        return self.repo.write_object(commit)
