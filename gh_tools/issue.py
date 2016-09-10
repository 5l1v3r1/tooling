"""Tasks related to issues."""
import click

from .github_helpers import GitHubMux


def _read_body():
    body = []
    print("Enter Body. Type EOF when you are done:")

    while True:
        body.append(raw_input())
        if body[-1] == "EOF":
            break

    return '\n'.join(body[:-1])


@click.group()
@click.argument('issue_id', type=click.INT)
@click.pass_context
def issue(ctx, issue_id):
    """Manipulate issues."""
    ctx.obj['issue_id'] = issue_id


@click.command()
@click.argument('source_repo')
@click.argument('dest_repo')
@click.pass_context
def move(ctx, source_repo, dest_repo):
    """Move an issue with ISSUE_ID from SOURCE_REPO to DEST_REPO."""
    ghm = GitHubMux(ctx.obj['organization'], ctx.obj['token'], ctx.obj['exclude'])
    ghm.move_issue(ctx.obj['issue_id'], source_repo, dest_repo)


@click.command()
@click.argument('source_repo')
@click.pass_context
def spread(ctx, source_repo):
    """Spread an issue with ISSUE_ID from SOURCE_REPO to the rest of the repos."""
    ghm = GitHubMux(ctx.obj['organization'], ctx.obj['token'], ctx.obj['exclude'])
    ghm.spread_issue(ctx.obj['issue_id'], source_repo)

issue.add_command(move)
issue.add_command(spread)
