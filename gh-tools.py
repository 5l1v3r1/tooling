#!/usr/bin/env python
"""Some tools for managing multiple repos on GitHub."""

import click

import os

from gh_tools import label, issue, stats


EXCLUDE = ['napalm', 'napalm-salt', 'napalm-ansible', 'napalm-skeleton', 'iosxr-ez', 'tooling',
           'napalm-utils', 'napalm-yang', 'napalm-cookiecutter']


def validate_token(ctx, param, value):
    """Validate that there is a token."""
    if not value:
        raise click.BadParameter('Either pass a token or set the env variable GITHUB_TOKEN')
    return value


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.option('--organization', default="napalm-automation",
              help="Which org you want to operate on. Defaults to 'napalm-automation'")
@click.option('--token', default=os.getenv("GITHUB_TOKEN"), callback=validate_token,
              help="GitHub Token. Defaults to env variable 'GITHUB_TOKEN'")
@click.option('--exclude', '-e', multiple=True,
              default=EXCLUDE,
              help="Which repos you want to skip. You can pass this argument mulitple times. "
                   "Defaults to {}".format(EXCLUDE))
@click.pass_context
def cli(ctx, debug, organization, token, exclude):
    """Main entry point."""
    ctx.obj['DEBUG'] = debug
    ctx.obj['organization'] = organization
    ctx.obj['exclude'] = exclude
    ctx.obj['token'] = token


cli.add_command(label.label)
cli.add_command(label.synch_labels)
cli.add_command(issue.issue)
cli.add_command(stats.stats)


if __name__ == '__main__':
    cli(obj={})
