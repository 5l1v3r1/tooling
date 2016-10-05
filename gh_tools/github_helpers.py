"""Some useful functions to deal with GitHub."""
import datetime

from github import Github
from github import UnknownObjectException

import click


class GitHubMux:
    """Class that let's you operate in multiple repos of the same org at the same time."""

    def __init__(self, organization, token, exclude):
        """
        Instantiate class.

        Args:
            organization(string): Organization name.
            token(string): Token to interact with GitHub API.
            exclude(tuple): Tuple with all the repo names that have to excluded from processing.
        """
        self.token = token
        self.gh = Github(self.token)
        self.exclude = exclude
        try:
            self.org = self.gh.get_organization(organization)
        except UnknownObjectException:
            raise Exception("Looks like organization `{}` doesn't exist.".format(organization))

    def exclude_repo(self, repo):
        """
        Exclude a repo.

        Args:
            repo(string): Repo of the name to exclude
        """
        self.exclude = self.exclude + (repo, )

    def repos(self):
        """Return repos to process."""
        for repo in self.org.get_repos():
            if repo.name in self.exclude:
                self.exclude_repo
                click.secho("Skipping repo `{}`.".format(repo.name), fg="blue")
            else:
                yield repo

    def _set_label_repo(self, repo, name, color):
        """
        Create a label if it doesn't exist already.

        Args:
            repo(Repository): Repo where you want to create the label
            name(string): Name of the label
            color(string): Color of the label

        Return:
            (Label) Either the label that was created of the existing one.
        """
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
            label = repo.create_label(name, color)
        return label

    def set_label(self, name, color):
        """
        Create a label in all repos if it doesn't exist.

        Args:
            name(string): Name of the label
            color(string): Color of the label
        """
        for repo in self.repos():
            self._set_label_repo(repo, name, color)

    def _unset_label_repo(self, repo, name):
        """
        Delete a label if it exists.

        Args:
            repo(Repository): Repo where you want to create the label
            name(string): Name of the label
        """
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
        """
        Delete a label in all the repos that it exists.

        Args:
            name(string): Name of the label
        """
        for repo in self.repos():
            self._unset_label_repo(repo, name)

    def rename_label(self, name, new_name):
        """
        Rename an existing label in all the repos that it exists.

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

    def _get_labels_from_repo(self, repo):
        """
        Get labels from a repo.

        Args:
            repo(Repository): Repository to process.

        Return:
            list(Label): List of Labels of repo.
        """
        labels = set()
        for label in repo.get_labels():
            labels.add((label.name, label.color))
        return labels

    def synch_from_repo(self, repo):
        """
        Synch labels across repos.

        Ensure that all repos have exactly the same labels as another repo that holds
        the source of truth. If labels exists same color is enforced, if labels don't exist they
        are created and if there are more labels than necessary they are deleted.

        Args:
            repo(str): Name of the repo that holds the truth.
        """
        repo = self.org.get_repo(repo)

        orig_labels = self._get_labels_from_repo(repo)

        for r in self.repos():
            if r.name == repo.name:
                continue
            click.secho("Processing {}".format(r.name), fg="cyan")
            r_labels = self._get_labels_from_repo(r)
            to_update = orig_labels - r_labels

            for l_tuple in to_update:
                self._set_label_repo(r, l_tuple[0], l_tuple[1])

            # We refresh labels as some might have changed color in the previous step
            r_labels = self._get_labels_from_repo(r)
            to_delete = r_labels - orig_labels

            for l_tuple in to_delete:
                self._unset_label_repo(r, l_tuple[0])

    def search_issue_by_title(self, title, org, repo):
        """
        Search for an issue with `title` in org/repo.

        Args:
            title(string): Title of the issue
            org(string): Organization name the issue has to belong to
            repo(string): Repository name the issue has to belong to

        Return:
            (Issue): that matches the criteria or None.

        Raise:
            (Exception): If there is more than one match.
        """
        query = "{} in:Title repo:{}/{}".format(title, org, repo)
        issues = self.gh.search_issues(query)

        for i in issues:
            if i.title == title:
                return i
        return None

    def move_issue(self, issue_id, src_repo, dst_repo):
        """
        Move an issue between different repos.

        Original issue is going to be closed while the new one will reference to the original issue
        and mention the original reporter.

        Args:
            issue_id(int): Issue number
            src_repo(string): Name of the source repo where the issue lives
            dst_repo(string): Name of the repo where you want to move the issue to
        """
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
        click.secho("Issue moved, new ID is #{} - {}".format(new_issue.id, new_issue.url),
                    fg="yellow")
        issue.create_comment("This issue has been 'moved' to {}/{}#{}".format(
                                                                         dst_repo.organization.name,
                                                                         dst_repo.name,
                                                                         new_issue.number))

    def spread_issue(self, issue_id, src_repo):
        """
        Spread an issue to multiple repos.

        Given a issue_id from a source repo it will create issues in the rest of the repos
        linking back to the original one.

        Args:
            issue_id(int): Issue number of the issue you want to spread.
            src_repo(string): Repository name where the issue lives.
        """
        issue = self.org.get_repo(src_repo).get_issue(issue_id)
        self.exclude_repo(issue.repository.name)
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

    def pr_stats(self, days):
        """Gather stats for the past few days."""
        stats = {}
        summary_user = {}
        summary_repo = {}

        for repo in self.repos():
            stats[repo.name] = {}
            summary_repo[repo.name] = {
                 "count": 0,
                 "commits": 0,
                 "additions": 0,
                 "deletions": 0,
            }
            for pr in repo.get_pulls(state="all", sort="created", direction="desc"):
                if pr.created_at < (datetime.datetime.now() - datetime.timedelta(days=days)):
                    break

                summary_repo[repo.name]["count"] += 1
                summary_repo[repo.name]["commits"] += pr.commits
                summary_repo[repo.name]["additions"] += pr.additions
                summary_repo[repo.name]["deletions"] += pr.deletions

                if pr.user.login not in stats[repo.name]:
                    stats[repo.name][pr.user.login] = {
                        "count": 1,
                        "commits": pr.commits,
                        "additions": pr.additions,
                        "deletions": pr.deletions,
                    }
                else:
                    stats[repo.name][pr.user.login]["count"] += 1
                    stats[repo.name][pr.user.login]["commits"] += pr.commits
                    stats[repo.name][pr.user.login]["additions"] += pr.additions
                    stats[repo.name][pr.user.login]["deletions"] += pr.deletions

                if pr.user.login not in summary_user:
                    summary_user[pr.user.login] = {
                        "count": 1,
                        "commits": pr.commits,
                        "additions": pr.additions,
                        "deletions": pr.deletions,
                    }
                else:
                    summary_user[pr.user.login]["count"] += 1
                    summary_user[pr.user.login]["commits"] += pr.commits
                    summary_user[pr.user.login]["additions"] += pr.additions
                    summary_user[pr.user.login]["deletions"] += pr.deletions

        return {
            "stats": stats,
            "summary_user": summary_user,
            "summary_repo": summary_repo
        }

    def issue_stats(self, days):
        """Gather stats for the past few days."""
        stats = {}

        for repo in self.repos():
            stats[repo.name] = {"count": 0}
            for issue in repo.get_issues(state="closed", sort="updated", direction="desc"):
                if issue.updated_at < (datetime.datetime.now() - datetime.timedelta(days=days)):
                    break

                stats[repo.name]["count"] += 1

        return {
            "stats": stats,
        }
