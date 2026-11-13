#!/usr/bin/env python3
"""
backup_configs.py — Lab project: automated config backup with Netmiko.

What it does: connects to each Cisco IOS device in an inventory YAML over SSH,
runs `show running-config`, and saves the output to backups/<hostname>_<date>.txt.

Status: built 2026-11-12 for lab study ahead of the Vandis technical
interview. Run it against Packet Tracer / GNS3 / a lab switch, or against
Cisco's DevNet always-on IOS XE sandbox, then it becomes a real project
you can defend in an interview.

Requirements on the machine that runs it:
    pip install netmiko pyyaml

Usage:
    python backup_configs.py
    python backup_configs.py --inventory inventory-sandbox.yaml
    # you will be prompted for the SSH password (never stored in a file)

Safety notes:
- No credentials are stored in this repo. Username comes from the inventory
  file, password is prompted at runtime with getpass.
- Read-only commands only: `show running-config` and `show version`.
  Nothing is written to any device.
- inventory.yaml ships with lab-only placeholder addresses (192.168.1.x).
  Replace them with your lab devices before running.
"""

import argparse
import getpass
import sys
from datetime import date
from pathlib import Path

import yaml
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException

BASE_DIR = Path(__file__).resolve().parent
INVENTORY = BASE_DIR / "inventory.yaml"
BACKUP_DIR = BASE_DIR / "backups"


def load_inventory(path=INVENTORY):
    """Read the device list from an inventory YAML file."""
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    devices = data.get("devices", [])
    if not devices:
        print(f"No devices in {path} — add your lab devices and re-run.")
        sys.exit(1)
    return devices


def backup_device(device, password):
    """SSH to one device, grab the running config, save it locally.

    Returns (hostname, ok, message).
    """
    conn_info = {
        "device_type": device["device_type"],  # e.g. "cisco_ios"
        "host": device["host"],
        "username": device["username"],
        "password": password,
        # The DevNet always-on sandbox is shared and slow; Netmiko's
        # 10s default connect timeout is too tight for it.
        "timeout": 60,
        "auth_timeout": 30,
        "conn_timeout": 30,
    }
    try:
        with ConnectHandler(**conn_info) as conn:
            # Confirm what we connected to before trusting the output.
            version = conn.send_command("show version | include uptime")
            hostname = conn.find_prompt().strip("#>")
            running = conn.send_command("show running-config")
    except NetmikoAuthenticationException:
        return device["host"], False, "auth failed — check username/password"
    except NetmikoTimeoutException:
        return device["host"], False, "timeout — device unreachable or SSH off"
    except Exception as exc:  # keep one bad device from killing the whole run
        return device["host"], False, f"error: {exc}"

    today = date.today().isoformat()
    BACKUP_DIR.mkdir(exist_ok=True)
    out_file = BACKUP_DIR / f"{hostname}_{today}.txt"
    out_file.write_text(
        f"! Backup of {hostname} ({device['host']}) on {today}\n"
        f"! {version.strip()}\n{running}\n",
        encoding="utf-8",
    )
    return hostname, True, f"saved to {out_file.name}"


def main():
    parser = argparse.ArgumentParser(
        description="Back up Cisco IOS running configs with Netmiko."
    )
    parser.add_argument(
        "--inventory",
        default=str(INVENTORY),
        help="inventory YAML to use (default: inventory.yaml)",
    )
    args = parser.parse_args()

    devices = load_inventory(args.inventory)
    password = getpass.getpass("SSH password for lab devices: ")
    print(f"Backing up {len(devices)} device(s)...\n")
    for device in devices:
        name, ok, msg = backup_device(device, password)
        status = "OK  " if ok else "FAIL"
        print(f"[{status}] {name}: {msg}")
    print("\nDone. Compare two backups with: diff backups/<old>.txt backups/<new>.txt")


if __name__ == "__main__":
    main()
