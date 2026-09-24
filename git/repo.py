"""
Git Repository operations and database management
"""

import os
import zlib
from pathlib import Path
from typing import Optional, List
from .objects import GitObject, Blob, Tree, Commit, Tag


class Repository:
    def __init__(self, path: str = "."):
        self.worktree = Path(path).resolve()
        self.gitdir = self.worktree / ".git"
        self.objects_dir = self.gitdir / "objects"
        self.refs_dir = self.gitdir / "refs"

    @classmethod
    def init(cls, path: str = ".") -> "Repository":
        repo = cls(path)
        repo.gitdir.mkdir(parents=True, exist_ok=True)
        repo.objects_dir.mkdir(parents=True, exist_ok=True)
        (repo.objects_dir / "info").mkdir(exist_ok=True)
        (repo.objects_dir / "pack").mkdir(exist_ok=True)
        (repo.refs_dir / "heads").mkdir(parents=True, exist_ok=True)
        (repo.refs_dir / "tags").mkdir(parents=True, exist_ok=True)

        head_file = repo.gitdir / "HEAD"
        if not head_file.exists():
            head_file.write_text("ref: refs/heads/main\n")

        config_file = repo.gitdir / "config"
        if not config_file.exists():
            config_file.write_text(
                "[core]\n"
                "\trepositoryformatversion = 0\n"
                "\tfilemode = true\n"
                "\tbare = false\n"
            )
        return repo

    def write_object(self, obj: GitObject) -> str:
        raw_data = obj.encode()
        sha1 = obj.compute_hash()
        
        dir_name = sha1[:2]
        file_name = sha1[2:]
        obj_dir = self.objects_dir / dir_name
        obj_dir.mkdir(exist_ok=True)
        
        obj_path = obj_dir / file_name
        if not obj_path.exists():
            compressed = zlib.compress(raw_data)
            obj_path.write_bytes(compressed)
        return sha1

    def read_object(self, sha1: str) -> GitObject:
        dir_name = sha1[:2]
        file_name = sha1[2:]
        obj_path = self.objects_dir / dir_name / file_name

        if not obj_path.exists():
            raise FileNotFoundError(f"Git object {sha1} not found in {self.objects_dir}")

        compressed = obj_path.read_bytes()
        raw = zlib.decompress(compressed)

        null_idx = raw.find(b"\x00")
        header = raw[:null_idx]
        payload = raw[null_idx + 1:]

        fmt, _ = header.split(b" ")
        
        if fmt == b"blob":
            obj = Blob()
        elif fmt == b"tree":
            obj = Tree()
        elif fmt == b"commit":
            obj = Commit()
        elif fmt == b"tag":
            obj = Tag()
        else:
            raise ValueError(f"Unknown object type: {fmt}")

        obj.deserialize(payload)
        return obj

    def list_all_objects(self) -> List[str]:
        objects = []
        if not self.objects_dir.exists():
            return objects
        for sub in self.objects_dir.iterdir():
            if sub.is_dir() and len(sub.name) == 2:
                for obj_file in sub.iterdir():
                    objects.append(sub.name + obj_file.name)
        return objects
