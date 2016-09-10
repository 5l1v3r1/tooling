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
    ghm = GitHubMux(ctx.obj['organization'], ctx.obj['token'], ctx.obj['exclde'])
    ghm.set_label(ctx.obj['name'], color)


@click.command()
@click.pass_context
def unset_label(ctx):
    """Deal with unsetting labels."""
    ghm = GitHubMux(ctx.obj['organization'], ctx.obj['token'], ctx.obj['exclde'])
    ghm.unset_label(ctx.obj['name'])


@click.command()
@click.argument('new_name')
@click.pass_context
def rename(ctx, new_name):
    """Rename a label."""
    ghm = GitHubMux(ctx.obj['organization'], ctx.obj['token'], ctx.obj['exclde'])
    ghm.rename_label(ctx.obj['name'], new_name)


@click.command()
@click.argument('repo')
@click.pass_context
def synch_labels(ctx, repo):
    """Synch all the repos' labels using the specified repo as the source of truth."""
    ghm = GitHubMux(ctx.obj['organization'], ctx.obj['token'], ctx.obj['exclde'])
    ghm.synch_from_repo(repo)


label.add_command(set_label, name="set")
label.add_command(unset_label, name="unset")
label.add_command(rename)
