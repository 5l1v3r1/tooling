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
    prs = ghm.pr_stats(days)

    _print_sum_stats('User', prs['summary_user'])
    _print_sum_stats('Repo', prs['summary_repo'])

    iss = ghm.issue_stats(days)
    click.secho("Issues Stats", fg="green")
    click.secho("============", fg="green")
    total = 0
    for repo, count in iss['stats'].items():
        if count['count']:
            total += count['count']
            l = 20 - len(repo)
            click.secho("{}{}{}".format(repo, " " * l, count['count']))
    l = 20 - len("Total")
    click.secho("Total{}{}".format(" " * l, total), fg="green")


stats.add_command(gather)


def _print_sum_stats(title, stats):
    click.secho("{} Stats".format(title), fg="green")
    l = 20 - len(title)
    click.secho("{}{}PRs\tcommits\tadditions\tdeletions".format(title, " " * l), fg="blue")
    total = {'count': 0, 'commits': 0, 'additions': 0, 'deletions': 0}
    for user, metrics in stats.items():
        l = 20 - len(user)
        click.secho("{}{}{}\t{}\t{}\t\t{}".format(user, " " * l, metrics['count'],
                                                  metrics['commits'], metrics['additions'],
                                                  metrics['deletions']))
        total['count'] += metrics['count']
        total['commits'] += metrics['commits']
        total['additions'] += metrics['additions']
        total['deletions'] += metrics['deletions']
    click.secho("Total{}{}\t{}\t{}\t\t{}".format(" " * 15, total['count'],
                                                 total['commits'], total['additions'],
                                                 total['deletions']), fg="green")
    click.secho("")
