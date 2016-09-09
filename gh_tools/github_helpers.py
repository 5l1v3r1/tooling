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
            self.org = self.gh.get_organization(organization)
        except UnknownObjectException:
            raise Exception("Looks like organization `{}` doesn't exist.".format(organization))
        self.exclude = []

    def repos(self):
        """Return repos to process."""
        for repo in self.org.get_repos():
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
        repo = self.org.get_repo(repo)

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

    def search_issue_by_title(self, title, org, repo):
        """Search for an issue with `title` in org/repo."""
        query = "{} in:Title repo:{}/{}".format(title, org, repo)
        issues = self.gh.search_issues(query)

        count = 0
        i = None
        for i in issues:
            if count:
                raise Exception("Found too many issues, please make sure the title is unique")
            count += 1
        return i

    def move_issue(self, issue_id, src_repo, dst_repo):
        """Given an issue ID, moves it from src_repo to dst_repo."""
        src_repo = self.org.get_repo(src_repo)
        dst_repo = self.org.get_repo(dst_repo)

        issue = src_repo.get_issue(issue_id)

        new_body = "Original issue {}/{}#{} created by @{}\n\n{}".format(
                                                            src_repo.organization.name,
                                                            src_repo.name,
                                                            issue.number,
                                                            issue.user.login,
                                                            issue.body)

        issue.edit(state="closed")
        new_issue = dst_repo.create_issue(title=issue.title, body=new_body, labels=issue.labels)
        click.echo("Issue moved, new ID is #{} - {}".format(new_issue.id, new_issue.url),
                   fg="yellow")

    def spread_issue(self, issue):
        """
        Spread an issue to multiple repos.

        Given a issue_id from a source repo it will create issues in the rest of the repos
        linking back to the original one.
        """
        self.exclude = self.exclude + (issue.repository.name, )
        body = "See details in the parent issue {}/{}#{}\n\n".format(
                                                            issue.repository.organization.name,
                                                            issue.repository.name,
                                                            issue.number)
        for repo in self.repos():
            new_issue = self.search_issue_by_title(issue.title, repo.organization.name, repo.name)
            if new_issue:
                click.secho("Issue already exists, ID is {}/{}#{} - {}".format(
                                                             new_issue.repository.organization.name,
                                                             new_issue.repository.name,
                                                             new_issue.number,
                                                             new_issue.url),
                            fg="green")
            else:
                new_issue = repo.create_issue(title=issue.title, body=body, labels=issue.labels)
                click.secho("Issue created, ID is {}/{}#{} - {}".format(
                                                             new_issue.repository.organization.name,
                                                             new_issue.repository.name,
                                                             new_issue.number,
                                                             new_issue.url),
                            fg="yellow")
