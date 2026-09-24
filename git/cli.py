"""
`pygit` Command-Line Interface exposing 75 Git Bash Commands
"""

import sys
import argparse
from .porcelain import Porcelain


def main():
    p = Porcelain(".")
    
    if len(sys.argv) < 2:
        print("pygit client version 0.2.0 - Supports 75 Git commands")
        print("Usage: python -m git.cli <command> [args]")
        return

    cmd = sys.argv[1]
    args = sys.argv[2:]

    # 75 Git Command CLI Router
    if cmd == "init": p.init(); print("Initialized empty Git repository")
    elif cmd == "add": p.add(args if args else ["."]); print("Staged files")
    elif cmd == "commit":
        msg = args[args.index("-m") + 1] if "-m" in args else "Commit"
        sha = p.commit(msg)
        print(f"[{sha[:7]}] {msg}")
    elif cmd == "status":
        st = p.status()
        print("Staged:", st["staged"])
        print("Untracked:", st["untracked"])
    elif cmd == "log":
        for sha, c in p.log():
            print(f"commit {sha}\nAuthor: {c.author}\n\n    {c.message}\n")
    elif cmd == "show": print(p.show(args[0] if args else p.refs.get_head()))
    elif cmd == "diff": print(p.diff())
    elif cmd == "branch": print("\n".join(p.branch(args[0] if args else None)))
    elif cmd == "checkout": p.checkout(args[0]); print(f"Switched to {args[0]}")
    elif cmd == "switch": p.switch(args[0]); print(f"Switched branch to {args[0]}")
    elif cmd == "restore": p.restore(args[0]); print(f"Restored {args[0]}")
    elif cmd == "reset": p.reset(); print("Reset HEAD")
    elif cmd == "rm": p.rm(args); print(f"Removed {args}")
    elif cmd == "mv": p.mv(args[0], args[1]); print(f"Moved {args[0]} to {args[1]}")
    elif cmd == "tag": print(p.tag(args[0] if args else None))
    elif cmd == "stash": p.stash(); print("Stashed state")
    elif cmd == "stash-pop": print(p.stash_pop())
    elif cmd == "stash-list": print(p.stash_list())
    elif cmd == "stash-drop": p.stash_drop(); print("Dropped stash")
    elif cmd == "stash-clear": p.stash_clear(); print("Cleared stashes")
    elif cmd == "clean": p.clean(); print("Cleaned untracked files")
    elif cmd == "merge": print(p.merge(args[0]))
    elif cmd == "rebase": print(p.rebase(args[0]))
    elif cmd == "cherry-pick": print(p.cherry_pick(args[0]))
    elif cmd == "revert": print(p.revert(args[0]))
    elif cmd == "bisect": print(p.bisect(args[0] if args else "start"))
    elif cmd == "blame": print("\n".join(p.blame(args[0])))
    elif cmd == "grep": print("\n".join(p.grep(args[0])))
    elif cmd == "reflog": print("\n".join(p.reflog()))
    elif cmd == "remote": print(p.remote())
    elif cmd == "fetch": print(p.fetch())
    elif cmd == "pull": print(p.pull())
    elif cmd == "push": print(p.push())
    elif cmd == "clone": p.clone(args[0], args[1]); print("Cloned repo")
    elif cmd == "shortlog": print(p.shortlog())
    elif cmd == "count-objects": print("Object count:", p.count_objects())
    elif cmd == "fsck": print(p.fsck())
    elif cmd == "gc": print(p.gc())
    elif cmd == "prune": print(p.prune())
    elif cmd == "archive": p.archive(args[0] if args else "repo.zip"); print("Archived repo")
    elif cmd == "hash-object": print(p.hash_object(args[0].encode("utf-8") if args else b""))
    elif cmd == "cat-file": print(p.cat_file(args[0]))
    elif cmd == "ls-files": print("\n".join(p.ls_files()))
    elif cmd == "ls-tree": print("\n".join(p.ls_tree(args[0])))
    elif cmd == "write-tree": print(p.write_tree())
    elif cmd == "read-tree": print(p.read_tree(args[0]))
    elif cmd == "commit-tree": print(p.commit_tree(args[0], args[1] if len(args) > 1 else "Commit"))
    elif cmd == "update-ref": p.update_ref(args[0], args[1]); print("Updated ref")
    elif cmd == "rev-parse": print(p.rev_parse(args[0]))
    elif cmd == "symbolic-ref": print(p.symbolic_ref(args[0]))
    elif cmd == "check-ignore": print(p.check_ignore(args[0]))
    elif cmd == "config": print(p.config())
    elif cmd == "version": print(p.version())
    elif cmd == "help": print(p.help())
    elif cmd == "merge-base": print(p.merge_base(args[0], args[1]))
    elif cmd == "patch-id": print(p.patch_id(args[0] if args else ""))
    elif cmd == "apply": print(p.apply_patch(args[0] if args else ""))
    elif cmd == "format-patch": print(p.format_patch())
    elif cmd == "am": print(p.am())
    elif cmd == "worktree": print(p.worktree())
    elif cmd == "describe": print(p.describe())
    elif cmd == "name-rev": print(p.name_rev(args[0]))
    elif cmd == "verify-pack": print(p.verify_pack())
    elif cmd == "unpack-objects": print(p.unpack_objects())
    elif cmd == "pack-objects": print(p.pack_objects())
    elif cmd == "index-pack": print(p.index_pack())
    elif cmd == "var": print(p.var(args[0] if args else "GIT_AUTHOR_IDENT"))
    elif cmd == "ls-remote": print(p.ls_remote())
    elif cmd == "check-ref-format": print(p.check_ref_format(args[0]))
    elif cmd == "column": print(p.column(args))
    elif cmd == "stripspace": print(p.stripspace(args[0] if args else ""))
    elif cmd == "mktree": print(p.mktree())
    elif cmd == "notes": print(p.notes())
    elif cmd == "whatchanged":
        for sha, c in p.whatchanged(): print(f"commit {sha}\n    {c.message}")
    elif cmd == "verify-commit": print(p.verify_commit(args[0] if args else ""))
    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
