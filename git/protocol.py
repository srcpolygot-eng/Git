"""
Git Smart HTTP / PKT-LINE network protocol encoder
"""


class PktLine:
    @staticmethod
    def encode(data: bytes) -> bytes:
        if not data:
            return b"0000"
        length = len(data) + 4
        return f"{length:04x}".encode("ascii") + data

    @staticmethod
    def decode_stream(stream: bytes):
        pos = 0
        while pos < len(stream):
            len_hex = stream[pos:pos + 4]
            pos += 4
            if len_hex == b"0000":
                yield None
                continue
            length = int(len_hex, 16)
            payload = stream[pos:pos + length - 4]
            pos += length - 4
            yield payload
