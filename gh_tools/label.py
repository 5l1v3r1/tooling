"""Tasks related to tags."""
import click

from .github_helpers import GitHubMux


@click.group()
@click.argument('name')
@click.pass_context
def label(ctx, name):
    """Manipulate labels."""
    ctx.obj['name'] = name


@click.command()
@click.argument('color')
@click.pass_context
def set_label(ctx, color):
    """Deal with setting labels."""
    ghm = GitHubMux(ctx.obj['organization'], ctx.obj['token'])
    ghm.exclude = ctx.obj['exclude']
    ghm.set_label(ctx.obj['name'], color)


@click.command()
@click.pass_context
def unset_label(ctx):
    """Deal with unsetting labels."""
    ghm = GitHubMux(ctx.obj['organization'], ctx.obj['token'])
    ghm.exclude = ctx.obj['exclude']
    ghm.unset_label(ctx.obj['name'])

label.add_command(set_label, name="set")
label.add_command(unset_label, name="unset")
