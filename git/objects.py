"""
Core Git Object primitives: Blob, Tree, Commit, Tag
"""

import hashlib
import zlib
from typing import List, Optional


class GitObject:
    fmt: bytes = b""

    def __init__(self, data: bytes = b""):
        self.data = data

    def serialize(self) -> bytes:
        raise NotImplementedError

    def deserialize(self, data: bytes):
        raise NotImplementedError

    def compute_hash(self) -> str:
        payload = self.serialize()
        header = self.fmt + b" " + str(len(payload)).encode("utf-8") + b"\x00"
        return hashlib.sha1(header + payload).hexdigest()

    def encode(self) -> bytes:
        payload = self.serialize()
        header = self.fmt + b" " + str(len(payload)).encode("utf-8") + b"\x00"
        return header + payload


class Blob(GitObject):
    fmt = b"blob"

    def serialize(self) -> bytes:
        return self.data

    def deserialize(self, data: bytes):
        self.data = data


class TreeEntry:
    def __init__(self, mode: str, path: str, sha1: str):
        self.mode = mode
        self.path = path
        self.sha1 = sha1


class Tree(GitObject):
    fmt = b"tree"

    def __init__(self, entries: Optional[List[TreeEntry]] = None):
        super().__init__()
        self.entries: List[TreeEntry] = entries or []

    def serialize(self) -> bytes:
        res = bytearray()
        sorted_entries = sorted(self.entries, key=lambda e: e.path if not e.mode.startswith("40000") else e.path + "/")
        for entry in sorted_entries:
            mode_path = f"{entry.mode} {entry.path}\x00".encode("utf-8")
            sha_bytes = bytes.fromhex(entry.sha1)
            res.extend(mode_path + sha_bytes)
        return bytes(res)

    def deserialize(self, data: bytes):
        self.entries = []
        pos = 0
        while pos < len(data):
            space_idx = data.find(b" ", pos)
            null_idx = data.find(b"\x00", space_idx)
            mode = data[pos:space_idx].decode("utf-8")
            path = data[space_idx + 1:null_idx].decode("utf-8")
            pos = null_idx + 1
            sha1 = data[pos:pos + 20].hex()
            pos += 20
            self.entries.append(TreeEntry(mode, path, sha1))


class Commit(GitObject):
    fmt = b"commit"

    def __init__(self, tree: str = "", parents: Optional[List[str]] = None,
                 author: str = "", committer: str = "", message: str = ""):
        super().__init__()
        self.tree = tree
        self.parents = parents or []
        self.author = author
        self.committer = committer
        self.message = message

    def serialize(self) -> bytes:
        lines = [f"tree {self.tree}"]
        for p in self.parents:
            lines.append(f"parent {p}")
        lines.append(f"author {self.author}")
        lines.append(f"committer {self.committer}")
        lines.append("")
        lines.append(self.message)
        return "\n".join(lines).encode("utf-8")

    def deserialize(self, data: bytes):
        content = data.decode("utf-8", errors="replace")
        parts = content.split("\n\n", 1)
        header_part = parts[0]
        self.message = parts[1] if len(parts) > 1 else ""
        self.parents = []
        for line in header_part.split("\n"):
            if line.startswith("tree "):
                self.tree = line[5:].strip()
            elif line.startswith("parent "):
                self.parents.append(line[7:].strip())
            elif line.startswith("author "):
                self.author = line[7:].strip()
            elif line.startswith("committer "):
                self.committer = line[10:].strip()


class Tag(GitObject):
    fmt = b"tag"

    def __init__(self, object_sha: str = "", obj_type: str = "commit",
                 tag_name: str = "", tagger: str = "", message: str = ""):
        super().__init__()
        self.object_sha = object_sha
        self.obj_type = obj_type
        self.tag_name = tag_name
        self.tagger = tagger
        self.message = message

    def serialize(self) -> bytes:
        lines = [
            f"object {self.object_sha}",
            f"type {self.obj_type}",
            f"tag {self.tag_name}",
            f"tagger {self.tagger}",
            "",
            self.message
        ]
        return "\n".join(lines).encode("utf-8")

    def deserialize(self, data: bytes):
        content = data.decode("utf-8", errors="replace")
        parts = content.split("\n\n", 1)
        header_part = parts[0]
        self.message = parts[1] if len(parts) > 1 else ""
        for line in header_part.split("\n"):
            if line.startswith("object "):
                self.object_sha = line[7:].strip()
            elif line.startswith("type "):
                self.obj_type = line[5:].strip()
            elif line.startswith("tag "):
                self.tag_name = line[4:].strip()
            elif line.startswith("tagger "):
                self.tagger = line[7:].strip()
