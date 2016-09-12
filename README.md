# tooling
Some useful tools to manage the project


## gh-tools.py

Tool that allows you to easily operate on a multi-repo project.

### Synching labels

```
(napalm-tooling) ➜  tooling git:(master) ./gh-tools.py synch_labels napalm-base
Skipping repo `napalm`.
Skipping repo `napalm-ansible`.
Processing napalm-eos
Processing napalm-junos
Processing napalm-ios
Label `enhancement` exists in repo `napalm-ios`. Deleting.
Processing napalm-iosxr
Processing napalm-fortios
Label `fortios` exists in repo `napalm-fortios`. Deleting.
Processing napalm-pluribus
Processing napalm-nxos
Processing napalm-ibm
Skipping repo `napalm-salt`.
Skipping repo `napalm-skeleton`.
Processing napalm-panos
Processing napalm-ros
Processing napalm-snmp
Processing napalm-iosxr-rpc
Skipping repo `iosxr-ez`.
Skipping repo `tooling`.
(napalm-tooling) ➜  tooling git:(master) vagrant ssh ios
```

### Spreading issues

```
(napalm-tooling) ➜  tooling git:(master) ./gh-tools.py issue 70 spread napalm-base
Skipping repo `napalm`.
Skipping repo `napalm-ansible`.
Skipping repo `napalm-base`.
Issue created, ID is napalm-automation/napalm-eos#39 - https://api.github.com/repos/napalm-automation/napalm-eos/issues/39
Issue created, ID is napalm-automation/napalm-junos#41 - https://api.github.com/repos/napalm-automation/napalm-junos/issues/41
Issue created, ID is napalm-automation/napalm-ios#35 - https://api.github.com/repos/napalm-automation/napalm-ios/issues/35
Issue created, ID is napalm-automation/napalm-iosxr#40 - https://api.github.com/repos/napalm-automation/napalm-iosxr/issues/40
Issue created, ID is napalm-automation/napalm-fortios#7 - https://api.github.com/repos/napalm-automation/napalm-fortios/issues/7
Issue created, ID is napalm-automation/napalm-pluribus#15 - https://api.github.com/repos/napalm-automation/napalm-pluribus/issues/15
Issue created, ID is napalm-automation/napalm-nxos#25 - https://api.github.com/repos/napalm-automation/napalm-nxos/issues/25
Issue created, ID is napalm-automation/napalm-ibm#4 - https://api.github.com/repos/napalm-automation/napalm-ibm/issues/4
Skipping repo `napalm-salt`.
Skipping repo `napalm-skeleton`.
Issue created, ID is napalm-automation/napalm-panos#8 - https://api.github.com/repos/napalm-automation/napalm-panos/issues/8
Issue created, ID is napalm-automation/napalm-ros#8 - https://api.github.com/repos/napalm-automation/napalm-ros/issues/8
Issue created, ID is napalm-automation/napalm-snmp#4 - https://api.github.com/repos/napalm-automation/napalm-snmp/issues/4
Issue created, ID is napalm-automation/napalm-iosxr-rpc#3 - https://api.github.com/repos/napalm-automation/napalm-iosxr-rpc/issues/3
Skipping repo `iosxr-ez`.
Skipping repo `tooling`.
```

### Moving issues

```
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
