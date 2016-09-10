# tooling
Some useful tools to manage the project


## gh-tools.py

Tool that allows you to easily operate on a multi-repo project.

### Moving issues

```
(napalm-tooling) ➜  tooling git:(master) ✗ ./gh-tools.py issue 000 move --help
Usage: gh-tools.py issue move [OPTIONS] SOURCE_REPO DEST_REPO

  Move an issue with ISSUE_ID from SOURCE_REPO to DEST_REPO.

  Options:
    --help  Show this message and exit.
(napalm-tooling) ➜  tooling git:(master) ✗ ./gh-tools.py issue 215 move napalm napalm-ios
Issue moved, new ID is #176173635 - https://api.github.com/repos/napalm-automation/napalm-ios/issues/27
```
