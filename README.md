# Pure Python Git Client (`pygit`)

A comprehensive, zero-dependency implementation of a Git client in Python. Supports **75 Git Bash commands** for repository management, object storage, index manipulation, ref tracking, diffing, and networking.

## Supported 75 Git Commands

### Core Porcelain Commands (User-Facing)
1. `init` - Initialize repository structure
2. `add` - Stage files into index
3. `commit` - Record changes to repository history
4. `status` - Working tree & staging status
5. `log` - Commit history log
6. `show` - Display commit & object details
7. `diff` - Unified file & commit diff engine
8. `branch` - List, create, or delete branches
9. `checkout` - Switch branches or restore files
10. `switch` - Fast branch switching
11. `restore` - Restore working directory paths
12. `reset` - Soft, mixed, or hard state resets
13. `rm` - Remove paths from index and working tree
14. `mv` - Move or rename files/directories
15. `tag` - Lightweight and annotated tags
16. `stash` - Save modified working state
17. `stash-pop` - Restore and remove stashed state
18. `stash-list` - List stashed modifications
19. `stash-drop` - Remove specific stash
20. `stash-clear` - Clear all stashed states
21. `clean` - Remove untracked files
22. `merge` - Fast-forward and 3-way merge
23. `rebase` - Reapply commits on top of another base
24. `cherry-pick` - Apply specific commit patch
25. `revert` - Revert existing commit
26. `bisect` - Binary search for bug-introducing commits
27. `blame` - Line-by-line modification tracking
28. `grep` - Search text in tracked files
29. `reflog` - Inspect reference update logs
30. `remote` - Manage tracked remote repositories
31. `fetch` - Download objects/refs from remote
32. `pull` - Fetch and merge remote changes
33. `push` - Push commits to remote branch
34. `clone` - Clone remote repository locally
35. `shortlog` - Summarize commit history by author
36. `count-objects` - Count object database statistics
37. `fsck` - Verify object database connectivity
38. `gc` - Prune and optimize object store
39. `prune` - Prune unreachable loose objects
40. `archive` - Zip/Tar archive of repository tree

### Low-Level Plumbing Commands
41. `hash-object` - Compute object SHA-1
42. `cat-file` - Print raw object content/type
43. `ls-files` - Inspect staged index files
44. `ls-tree` - Inspect tree object entries
45. `write-tree` - Create tree from index
46. `read-tree` - Read tree object into index
47. `commit-tree` - Create raw commit from tree
48. `update-ref` - Safely update ref pointers
49. `rev-parse` - Parse git revision parameters
50. `symbolic-ref` - Read/write symbolic references
51. `check-ignore` - Test .gitignore patterns
52. `config` - Read/write repository options
53. `version` - Print git client version
54. `help` - Show command help docs
55. `merge-base` - Find common commit ancestor
56. `patch-id` - Compute unique patch identifier
57. `apply` - Apply diff patch to working tree
58. `format-patch` - Generate patch series from commits
59. `am` - Apply email mailbox patch series
60. `worktree` - Manage attached working trees
61. `describe` - Describe commit using nearest tag
62. `name-rev` - Find symbolic name for revision
63. `verify-pack` - Validate binary packfile index
64. `unpack-objects` - Extract loose objects from pack
65. `pack-objects` - Package objects into binary archive
66. `index-pack` - Create .idx file for packfile
67. `var` - Query git logical variables
68. `ls-remote` - List references on remote server
69. `check-ref-format` - Validate reference names
70. `column` - Display data in formatted columns
71. `stripspace` - Clean up whitespace and comments
72. `mktree` - Create tree object from text format
73. `notes` - Manage object metadata notes
74. `whatchanged` - Commit logs with patch details
75. `verify-commit` - Validate commit signatures

## Usage

```bash
python -m git.cli init .
python -m git.cli status
python -m git.cli add .
python -m git.cli commit -m "Initial repository commit"
python -m git.cli log
```
