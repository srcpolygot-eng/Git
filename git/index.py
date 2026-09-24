"""
Git Index (.git/index) Binary Parser and Serializer
"""

import struct
import hashlib
from pathlib import Path
from typing import List


class IndexEntry:
    def __init__(self, ctime: tuple, mtime: tuple, dev: int, ino: int,
                 mode: int, uid: int, gid: int, size: int,
                 sha1: str, flags: int, path: str):
        self.ctime = ctime
        self.mtime = mtime
        self.dev = dev
        self.ino = ino
        self.mode = mode
        self.uid = uid
        self.gid = gid
        self.size = size
        self.sha1 = sha1
        self.flags = flags
        self.path = path


class Index:
    def __init__(self, repo_path: str = "."):
        self.index_file = Path(repo_path) / ".git" / "index"
        self.entries: List[IndexEntry] = []

    def read(self):
        if not self.index_file.exists():
            self.entries = []
            return

        data = self.index_file.read_bytes()
        if len(data) < 12:
            return

        signature, version, num_entries = struct.unpack(">4sII", data[:12])
        if signature != b"DIRC":
            raise ValueError("Invalid Git index file signature")

        pos = 12
        self.entries = []

        for _ in range(num_entries):
            entry_data = data[pos:pos + 62]
            fields = struct.unpack(">LLLLLLLLL20sH", entry_data)
            
            ctime = (fields[0], fields[1])
            mtime = (fields[2], fields[3])
            dev, ino, mode, uid, gid, size = fields[4:10]
            sha1 = fields[10].hex()
            flags = fields[11]

            path_end = data.find(b"\x00", pos + 62)
            path = data[pos + 62:path_end].decode("utf-8", errors="replace")
            
            entry_len = ((62 + len(path) + 1 + 7) // 8) * 8
            pos += entry_len

            self.entries.append(IndexEntry(ctime, mtime, dev, ino, mode, uid, gid, size, sha1, flags, path))

    def write(self):
        out = bytearray()
        out.extend(struct.pack(">4sII", b"DIRC", 2, len(self.entries)))

        for e in self.entries:
            path_bytes = e.path.encode("utf-8")
            sha1_bytes = bytes.fromhex(e.sha1)
            flags = len(path_bytes) & 0xFFF

            entry = struct.pack(
                ">LLLLLLLLL20sH",
                e.ctime[0], e.ctime[1],
                e.mtime[0], e.mtime[1],
                e.dev, e.ino, e.mode, e.uid, e.gid, e.size,
                sha1_bytes, flags
            ) + path_bytes + b"\x00"

            pad_len = ((len(entry) + 7) // 8) * 8 - len(entry)
            entry += b"\x00" * pad_len
            out.extend(entry)

        checksum = hashlib.sha1(out).digest()
        out.extend(checksum)
        self.index_file.write_bytes(bytes(out))

    def add_entry(self, path: str, sha1: str, mode: int = 0o100644, size: int = 0):
        import time
        now = (int(time.time()), 0)
        self.entries = [e for e in self.entries if e.path != path]
        new_entry = IndexEntry(
            ctime=now, mtime=now, dev=0, ino=0, mode=mode,
            uid=0, gid=0, size=size, sha1=sha1, flags=0, path=path
        )
        self.entries.append(new_entry)
        self.entries.sort(key=lambda x: x.path)

    def remove_entry(self, path: str):
        self.entries = [e for e in self.entries if e.path != path]
