"""Some useful functions to deal with GitHub."""

from github import Github
from github import UnknownObjectException

import click


class GitHubMux:
    """Class that let's you operate in multiple repos of the same org at the same time."""

    def __init__(self, organization, token):
        """Instantiate class."""
        self.token = token
        self.gh = Github(self.token)
        try:
            self.organization = self.gh.get_organization(organization)
        except UnknownObjectException:
            raise Exception("Looks like organization `{}` doesn't exist.".format(organization))
        self.exclude = []

    def repos(self):
        """Return repos to process."""
        for repo in self.organization.get_repos():
            if repo.name in self.exclude:
                click.secho("Skipping repo `{}`.".format(repo.name), fg="blue")
            else:
                yield repo

    def set_label(self, name, color):
        """Ensure a label with `name` and `color` exists in all repos."""
        for repo in self.repos():
            try:
                label = repo.get_label(name)

                if label.color == color:
                    click.secho("Label `{}` already exists in repo `{}`. ".format(name,
                                                                                  repo.name),
                                fg='green')
                else:
                    click.secho("Label `{}` already exists in repo `{}` "
                                "but has a different color. Fixing.".format(name,
                                                                            repo.name),
                                fg='yellow')
                    label.edit(name, color)

            except UnknownObjectException:
                click.secho("Label `{}` doesn't exist in repo `{}`. Creating.".format(name,
                                                                                      repo.name),
                            fg='yellow')
                repo.create_label(name, color)

    def unset_label(self, name):
        """Delete label with `name` in all the repos."""
        for repo in self.repos():
            try:
                label = repo.get_label(name)
                click.secho("Label `{}` exists in repo `{}`. Deleting.".format(name,
                                                                               repo.name),
                            fg='yellow')
                label.delete()
            except UnknownObjectException:
                click.secho("Label `{}` is already missing in repo `{}`.".format(name,
                                                                                 repo.name),
                            fg='green')
