"""
Git Packfile Index (.idx v2) lookup parser
"""

import struct


class IdxFile:
    def __init__(self, idx_path: str):
        self.idx_path = idx_path

    def parse(self, data: bytes):
        if data[:4] != b"\xfftOc":
            raise ValueError("Not a v2 Git Index file")
        version, = struct.unpack(">I", data[4:8])
        fanout = []
        for i in range(256):
            count, = struct.unpack(">I", data[8 + i * 4: 12 + i * 4])
            fanout.append(count)
        return version, fanout[255]
