"""
Pure Python Git Client Package Exports
"""

from .objects import GitObject, Blob, Tree, TreeEntry, Commit, Tag
from .repo import Repository
from .index import Index, IndexEntry
from .refs import RefStore
from .plumbing import Plumbing
from .porcelain import Porcelain

__version__ = "0.2.0"

__all__ = [
    "GitObject", "Blob", "Tree", "TreeEntry", "Commit", "Tag",
    "Repository", "Index", "IndexEntry", "RefStore", "Plumbing", "Porcelain"
]
