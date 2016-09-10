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
### Renaming labels

```
(napalm-tooling) ➜  tooling git:(master) ✗ ./gh-tools.py label hackhation2016 rename hackhaton2016
Couldn't find label `hackhation2016` in repo `napalm`.
Couldn't find label `hackhation2016` in repo `napalm-ansible`.
Label `hackhation2016` exists in repo `napalm-base`. Renaming.
Label `hackhation2016` exists in repo `napalm-eos`. Renaming.
Label `hackhation2016` exists in repo `napalm-junos`. Renaming.
Label `hackhation2016` exists in repo `napalm-ios`. Renaming.
Label `hackhation2016` exists in repo `napalm-iosxr`. Renaming.
Label `hackhation2016` exists in repo `napalm-fortios`. Renaming.
Label `hackhation2016` exists in repo `napalm-pluribus`. Renaming.
Label `hackhation2016` exists in repo `napalm-nxos`. Renaming.
Label `hackhation2016` exists in repo `napalm-ibm`. Renaming.
Couldn't find label `hackhation2016` in repo `napalm-salt`.
Couldn't find label `hackhation2016` in repo `napalm-skeleton`.
Label `hackhation2016` exists in repo `napalm-panos`. Renaming.
Label `hackhation2016` exists in repo `napalm-ros`. Renaming.
Label `hackhation2016` exists in repo `napalm-snmp`. Renaming.
Label `hackhation2016` exists in repo `napalm-iosxr-rpc`. Renaming.
Label `hackhation2016` exists in repo `iosxr-ez`. Renaming.
Couldn't find label `hackhation2016` in repo `tooling`.
```
