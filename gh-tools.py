#!/usr/bin/env python
"""Some tools for managing multiple repos on GitHub."""

import click

import os

from gh_tools import label
from gh_tools import issue

EXCLUDE = ['napalm', 'napalm-salt', 'napalm-ansible', 'napalm-skeleton', 'iosxr-ez', 'tooling']


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.option('--organization', default="napalm-automation",
              help="Which org you want to operate on. Defaults to 'napalm-automation'")
@click.option('--token', default=os.getenv("GITHUB_TOKEN"),
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
    ctx.obj['token'] = token
    ctx.obj['exclude'] = exclude

cli.add_command(label.label)
cli.add_command(label.synch_labels)
cli.add_command(issue.issue)


if __name__ == '__main__':
    cli(obj={})
