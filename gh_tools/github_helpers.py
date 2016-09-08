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

    def _set_label_repo(self, repo, name, color):
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

    def set_label(self, name, color):
        """Ensure a label with `name` and `color` exists in all repos."""
        for repo in self.repos():
            self._set_label_repo(repo, name, color)

    def _unset_label_repo(self, repo, name):
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

    def unset_label(self, name):
        """Delete label with `name` in all the repos."""
        for repo in self.repos():
            self._unset_label_repo(repo, name)

    def rename_label(self, name, new_name):
        """
        Rename an existing label.

        Args:
            name(str): Current name of the label
            new_name(str): New name for the label
        """
        for repo in self.repos():
            try:
                label = repo.get_label(name)
                click.secho("Label `{}` exists in repo `{}`. Renaming.".format(name,
                                                                               repo.name),
                            fg='yellow')
                label.edit(new_name, label.color)
            except UnknownObjectException:
                click.secho("Couldn't find label `{}` in repo `{}`.".format(name,
                                                                            repo.name),
                            fg='green')

    def _extract_label_info(self, repo):
        labels = set()
        for label in repo.get_labels():
            labels.add((label.name, label.color))
        return labels

    def synch_from_repo(self, repo):
        """
        Synch labels across repos.

        Ensure that all repos have exactly the same labels as another repo that hold that holds
        the source of truth.

        Args:
            repo(str): Repo name of the repo that holds the truth.
        """
        repo = self.organization.get_repo(repo)

        orig_labels = self._extract_label_info(repo)

        for r in self.repos():
            if r.name == repo.name:
                continue
            click.secho("Processing {}".format(r.name), fg="cyan")
            r_labels = self._extract_label_info(r)
            to_update = orig_labels - r_labels

            for l_tuple in to_update:
                self._set_label_repo(r, l_tuple[0], l_tuple[1])

            # We refresh labels as some might have changed color in the previous step
            r_labels = self._extract_label_info(r)
            to_delete = r_labels - orig_labels

            for l_tuple in to_delete:
                self._unset_label_repo(r, l_tuple[0])
