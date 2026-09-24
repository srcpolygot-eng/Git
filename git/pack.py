"""
Git Packfile (.pack) binary reader and decompression
"""

import zlib
import struct


class PackFile:
    def __init__(self, pack_path: str):
        self.pack_path = pack_path

    def parse_header(self, data: bytes):
        sig, version, num_objects = struct.unpack(">4sII", data[:12])
        if sig != b"PACK":
            raise ValueError("Invalid packfile signature")
        return version, num_objects

    def unpack_objects(self, data: bytes):
        version, num_objs = self.parse_header(data)
        offset = 12
        objects = []
        for _ in range(num_objs):
            byte = data[offset]
            offset += 1
            obj_type = (byte >> 4) & 7
            size = byte & 15
            shift = 4
            while byte & 0x80:
                byte = data[offset]
                offset += 1
                size |= (byte & 0x7F) << shift
                shift += 7

            decompressor = zlib.decompressobj()
            decompressed = decompressor.decompress(data[offset:])
            offset += len(data[offset:]) - len(decompressor.unconsumed_tail)
            objects.append((obj_type, decompressed))
        return objects
