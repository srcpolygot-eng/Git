"""
Git Text Unified Diff engine
"""

import difflib


class GitDiff:
    @staticmethod
    def diff_texts(text_a: str, text_b: str, from_file: str = "a", to_file: str = "b") -> str:
        lines_a = text_a.splitlines(keepends=True)
        lines_b = text_b.splitlines(keepends=True)
        diff = difflib.unified_diff(lines_a, lines_b, fromfile=from_file, tofile=to_file)
        return "".join(diff)
