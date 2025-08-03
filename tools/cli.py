import click

from .commands import save_changes, push_commits, squash_commits, stash_changes, pop_stashed_changes, \
  clear_stashed_changes, reset_commits, pull_commits


@click.group()
def cli():
  """Git Buddy - Simplified git operations"""
  pass


@cli.command()
@click.argument('message', required=False)
def gsave(message):
  """Save changes with auto-generated or custom commit message"""
  save_changes(message)


@cli.command()
def gpush():
  """Push commits to remote repository"""
  push_commits()


@cli.command()
@click.argument('message', required=False)
@click.option('--count', '-c', type=int, help='Number of commits to squash')
def gsquash(message, count):
  """Squash multiple commits into one"""
  squash_commits(message, count)


@cli.command()
def gstash():
  """Stash current changes"""
  stash_changes()


@cli.command()
def gpop():
  """Pop most recent stash"""
  pop_stashed_changes()


@cli.command()
def gclear():
  """Clear all stash entries"""
  clear_stashed_changes()


@cli.command()
@click.argument('count_arg', type=int, default=1, required=False)
@click.option('--count', '-c', type=int, help='Number of commits to reset')
@click.option('--hard', "-h", is_flag=True, help='Perform hard reset instead of soft reset')
def greset(count_arg, count, hard):
  """Reset commits (soft by default, hard with --hard flag)"""
  reset_commits(count_arg, count, hard)


@cli.command()
def gpull():
  """Stash changes, pull from remote, then restore stashed changes"""
  pull_commits()


if __name__ == '__main__':
  cli()
