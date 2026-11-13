# Vandis automation lab — Netmiko config backup

Built 2026-11-12, after Max Parks (Vandis / Green Key) said the technical
interviewers will judge Tonio's automation knowledge. The honest route to
claiming Python/Ansible: build one small real thing, run it in the lab, then
list it. This is that thing — step 1 of 3.

## What this is

`backup_configs.py` — a Python script using Netmiko that SSHes to each Cisco
IOS device in `inventory.yaml`, runs `show running-config`, and saves the
output to `backups/<hostname>_<date>.txt`. Read-only on the device: it runs
`show` commands only and writes nothing to any switch.

## Run it (lab only)

1. On your laptop (the one with the lab / Packet Tracer / GNS3):
   `pip install netmiko pyyaml`
2. Edit `inventory.yaml` — replace the placeholder 192.168.1.x addresses
   with your lab devices, and set the right username.
   **Or skip the local lab:** `inventory-sandbox.yaml` points at Cisco's
   free DevNet always-on IOS XE sandbox (`sandbox-iosxe-latest-1.cisco.com`,
   published demo login `admin` / `C1sco12345`) — run with
   `python backup_configs.py --inventory inventory-sandbox.yaml`.
   The script also accepts `--inventory <file>` for any other inventory.
3. `python backup_configs.py` — type the SSH password when prompted.
   It is never written to a file.
4. Check `backups/` for one `.txt` file per device. Run it again after a
   config change and `diff` the two files — that is the drift check.
5. Only after a successful lab run: push this folder to GitHub
   (e.g. `abowden101/network-config-backup`) and only then add a line to
   the resume: "Python (Netmiko) — automated Cisco config backups in a lab,
   version-controlled on GitHub."

> Nov 13 update: first successful run — Nov 13, 2026, against the DevNet
> sandbox (Catalyst 8000v "Cat8kv", IOS XE 17.15), saved as
> `backups/Cat8kv_2026-11-13.txt` (183 lines). Two fixes landed that day:
> the working sandbox login is `admin` (`developer` is rejected on this
> host), and the script's timeouts were raised (30s connect / 60s command)
> because the shared sandbox is slow — Netmiko's 10s default was too
> tight. Run from Muse's VM with Direct network access enabled.

## Honesty gate — do not skip this

- Until step 4 succeeds, this is a draft, not a project. Do **not** list
  Python, Netmiko, Ansible or REST APIs on the resume, and do not claim
  the two invented projects from the rewrite guide (the backup pipeline
  and the API health-check script) — they do not exist yet.
- The Vandis resume already sent to Max (Nov 12) is the honest version:
  NinjaOne, Huntress, PowerShell/Bash, Terraform VNet. This lab adds to
  that story only once it runs.

## Interview prep — the three questions the guide warned about

These are the answers to be able to give cold before the Vandis technical
interview. They are study notes, not resume claims.

**1. How does an Ansible inventory connect to a Cisco switch over SSH?**
An inventory file (e.g. `hosts.yml`) lists each switch under a group with
`ansible_host` (IP), `ansible_user`, and `ansible_network_os: ios` (or
`cisco.ios.ios`). Ansible's network connection plugin opens an SSH session
to that host and drives the device CLI — it does not install an agent on
the switch. Credentials come from variables / vault, never from the
inventory file itself.

**2. Imperative (Python) vs declarative / idempotent (Ansible)?**
A Python script is imperative: it says *how* — "connect, send these
commands, in this order." Run it twice and it does the work twice.
An Ansible playbook is declarative: it says *what the end state should
be* — "this VLAN exists, this config line is present." Ansible checks the
current state first and only changes what is different, so running it
twice is safe — that is idempotency.

**3. How do you parse a JSON response from a REST API in Python?**
With `requests`: `resp = requests.get(url, headers=...)`, then
`data = resp.json()` gives a dict/list you can index like
`data["results"][0]["status"]`. Always check `resp.status_code` (or call
`resp.raise_for_status()`) before parsing, and wrap it in try/except for
bad JSON or a timeout.

## Next step after this script runs

The second honest project, if the interviewers want more: the same backup
idea as an Ansible playbook (`cisco.ios.ios_config` with `backup: yes`),
run against the same lab devices. Build it only after this script works —
one real project beats two claimed ones.
