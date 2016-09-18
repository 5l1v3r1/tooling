"""Tasks related to stats."""
import click

from .github_helpers import GitHubMux


@click.group()
@click.pass_context
def stats(ctx):
    """Gather stats."""
    pass


@click.command()
@click.argument('days', type=click.INT)
@click.pass_context
def gather(ctx, days):
    """Gather PR stats for the past N days."""
    ghm = GitHubMux(ctx.obj['organization'], ctx.obj['token'], ctx.obj['exclude'])
    ghm.stats(days)

stats.add_command(gather)
