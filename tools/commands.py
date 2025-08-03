import os
import subprocess
from typing import Optional


def save_changes(message: Optional[str] = None):
  try:
    subprocess.run(['git', 'add', '.'], check=True, cwd=os.getcwd())

    if message is None:
      result = subprocess.run(
        ['git', 'diff', '--cached'],
        capture_output=True,
        text=True,
        cwd=os.getcwd()
      )

      diff_lines = result.stdout.strip().split('\n')
      changed_lines = []
      for line in diff_lines:
        if line.startswith("+") or line.startswith("-"):
          changed_lines.append(line)
      changed_message = "\n".join(changed_lines)
      trailing = "..." if len(changed_message) > 200 else ""
      commit_message = f"\n{changed_message[:200]}{trailing}" if changed_message else "Saved Changes"
    else:
      commit_message = message

    subprocess.run(['git', 'commit', '-m', commit_message], check=True, cwd=os.getcwd())

    print(f"[gsave] Committed changes with message: '{commit_message}'")
  except subprocess.CalledProcessError as e:
    print(f"[gsave] Git operation failed: {e}")
  except Exception as e:
    print(f"[gsave] Error during save changes: {e}")


def push_commits():
  try:
    result = subprocess.run(
      ['git', 'branch', '--show-current'],
      capture_output=True,
      text=True,
      cwd=os.getcwd()
    )
    current_branch = result.stdout.strip()

    if not current_branch:
      print("[gpush] Could not determine current branch")
      return

    subprocess.run(['git', 'push', 'origin', current_branch], check=True, cwd=os.getcwd())
    print(f"[gpush] Successfully pushed to origin/{current_branch}")

  except subprocess.CalledProcessError as e:
    print(f"[gpush] Git operation failed: {e}")
  except Exception as e:
    print(f"[gpush] Error during push operation: {e}")


def squash_commits(message: Optional[str] = None, commit_count_to_squash: Optional[int] = None):
  try:
    # Check if message is a number and count is not set
    if message is not None and commit_count_to_squash is None and message.isdigit():
      commit_count_to_squash = int(message)
      message = None

    branch_result = subprocess.run(
      ['git', 'branch', '--show-current'],
      capture_output=True,
      text=True,
      cwd=os.getcwd()
    )
    current_branch = branch_result.stdout.strip()

    if not current_branch:
      print("[gsquash] Could not determine current branch")
      return

    result = subprocess.run(
      ['git', 'rev-list', 'HEAD', f'origin/{current_branch}..HEAD'],
      capture_output=True,
      text=True,
      cwd=os.getcwd()
    )
    local_commits_count = len(result.stdout.strip().split('\n'))

    if local_commits_count == 0:
      print("[gsquash] No unpushed commit to squash")
      return

    if commit_count_to_squash is None:
      commits_to_squash = local_commits_count
    else:
      commits_to_squash = min(commit_count_to_squash, local_commits_count)

    subprocess.run(['git', 'reset', '--soft', f'HEAD~{commits_to_squash}'], check=True, cwd=os.getcwd())

    if message is None:
      result = subprocess.run(
        ['git', 'diff', '--cached'],
        capture_output=True,
        text=True,
        cwd=os.getcwd()
      )

      diff_lines = result.stdout.strip().split('\n')
      changed_lines = []
      for line in diff_lines:
        if line.startswith("+") or line.startswith("-"):
          changed_lines.append(line)
      changed_message = "\n".join(changed_lines)
      trailing = "..." if len(changed_message) > 200 else ""
      squash_message = f"\n{changed_message[:200]}{trailing}" if changed_message else "Squashed commits"
    else:
      squash_message = message

    subprocess.run(['git', 'commit', '-m', squash_message], check=True, cwd=os.getcwd())

    print(f"[gsquash] Successfully squashed {commits_to_squash} unpushed commits with message: '{squash_message}'")

  except subprocess.CalledProcessError as e:
    print(f"[gsquash] Git operation failed: {e}")
  except Exception as e:
    print(f"[gsquash] Error during squash operation: {e}")


def stash_changes():
  try:
    subprocess.run(['git', 'add', '.'], check=True, cwd=os.getcwd())
    subprocess.run(['git', 'stash'], check=True, cwd=os.getcwd())
  except subprocess.CalledProcessError as e:
    if "no local changes to save" in str(e).lower():
      print("[gstash] No changes to stash")
    else:
      print(f"[gstash] Git operation failed: {e}")
  except Exception as e:
    print(f"[gstash] Error during stash operation: {e}")


def pop_stashed_changes():
  try:
    subprocess.run(['git', 'stash', 'pop'], check=True, cwd=os.getcwd())
    print("[gpop] Stash successfully popped")
  except subprocess.CalledProcessError as e:
    if "no stash entries found" in str(e).lower():
      print("[gpop] No stash entries to pop")
    else:
      print(f"[gpop] Git operation failed: {e}")
  except Exception as e:
    print(f"[gpop] Error during stash pop operation: {e}")


def clear_stashed_changes():
  try:
    subprocess.run(['git', 'stash', 'clear'], check=True, cwd=os.getcwd())
    print("[gclear] All stash entries cleared")
  except subprocess.CalledProcessError as e:
    print(f"[gclear] Git operation failed: {e}")
  except Exception as e:
    print(f"[gclear] Error during stash clear operation: {e}")


def reset_commits(count_arg: Optional[int] = None, count: int = 1, hard: bool = False):
  try:
    if count_arg is not None:
      count = count_arg

    branch_result = subprocess.run(
      ['git', 'branch', '--show-current'],
      capture_output=True,
      text=True,
      cwd=os.getcwd()
    )
    current_branch = branch_result.stdout.strip()

    if not current_branch:
      print("[greset] Could not determine current branch")
      return

    result = subprocess.run(
      ['git', 'rev-list', 'HEAD', f'origin/{current_branch}..HEAD'],
      capture_output=True,
      text=True,
      cwd=os.getcwd()
    )

    result_text = result.stdout.strip()
    local_commits_count = len(result_text.split('\n'))

    if local_commits_count == 0 or result_text == "":
      print("[greset] No unpushed commits to reset")
      return

    commit_to_reset = min(count, local_commits_count)

    reset_type = '--hard' if hard else '--soft'
    subprocess.run(['git', 'reset', reset_type, f'HEAD~{commit_to_reset}'], check=True, cwd=os.getcwd())

    reset_action = "hard" if hard else "soft"
    print(f"[greset] Successfully performed {reset_action} reset of {commit_to_reset} unpushed commit(s)")

  except subprocess.CalledProcessError as e:
    print(f"[greset] Git operation failed: {e}")
  except Exception as e:
    print(f"[greset] Error during reset operation: {e}")


def pull_commits():
  try:
    branch_result = subprocess.run(
      ['git', 'branch', '--show-current'],
      capture_output=True,
      text=True,
      cwd=os.getcwd()
    )
    current_branch = branch_result.stdout.strip()

    if not current_branch:
      print("[gpull] Could not determine current branch")
      return

    status_result = subprocess.run(
      ['git', 'status', '--porcelain'],
      capture_output=True,
      text=True,
      cwd=os.getcwd()
    )
    has_changes = bool(status_result.stdout.strip())

    if has_changes:
      subprocess.run(['git', 'add', '.'], check=True, cwd=os.getcwd())
      subprocess.run(['git', 'stash'], check=True, cwd=os.getcwd())
      print("[gpull] Changes stashed")

    subprocess.run(['git', 'pull', 'origin', current_branch], check=True, cwd=os.getcwd())
    print(f"[gpull] Successfully pulled from origin/{current_branch}")

    if has_changes:
      try:
        subprocess.run(['git', 'stash', 'pop'], check=True, cwd=os.getcwd())
        print("[gpull] Stashed changes restored")
      except subprocess.CalledProcessError as e:
        print(f"[gpull] Warning: Failed to restore stashed changes. Use 'git stash pop' manually. Error: {e}")

  except subprocess.CalledProcessError as e:
    print(f"[gpull] Git operation failed: {e}")
  except Exception as e:
    print(f"[gpull] Error during pull operation: {e}")
