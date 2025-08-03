# Git Short

A simplified set of CLI commands for using git that I find convenient. Aimed at reducing the toil of using git. Best suited for single developer repos.

If you have any suggestions for new commands or changes, please let me know.

## Installation

```bash
pip install git-short
```

## Commands

### `gsave [message]`

Save changes with auto-generated or custom commit message.

- `gsave` - Auto-generates commit message from diff
- `gsave "Custom commit message"` - Uses your custom message

### `gpush`

Push commits to remote repository on current branch.

### `gsquash [message] [--count,-c]`

Squash unpushed commits into one commit.

- `gsquash` - Squash all unpushed commits
- `gsquash "Squash message"` - Squash with custom message
- `gsquash 3` - Squash only the last 3 unpushed commits
- `gsquash --count 3` - Squash only the last 3 unpushed commits

### `greset [count] [--count,-c] [--hard,-h]`

Reset commits (soft by default).

- `greset` - Soft reset 1 commit
- `greset 3` - Soft reset 3 commits
- `greset --count 5` - Soft reset 5 commits
- `greset --count 2 --hard` - Hard reset 2 commits

### `gstash`

Stash current changes.

### `gpop`

Pop most recent stash.

### `gclear`

Clear all stash entries.

### `gpull`

Stash changes, pull from remote, then restore stashed changes.

## Requirements

- Python 3.7+
- Remote repository set up (origin)