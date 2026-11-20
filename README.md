# network-config-backup

Automated Cisco IOS running-config backup over SSH with Netmiko. Point it at an inventory of devices and it pulls `show running-config` (plus a `show version` uptime check) and saves a dated backup per device.

**Read-only on the device** — it runs `show` commands only and writes nothing to any switch.

---

## Requirements

- Python 3.10+
- `pip install -r requirements.txt` (netmiko, pyyaml)

## Usage

1. Edit `inventory.yaml` — one entry per device:

```yaml
devices:
  - host: 192.168.1.10
    device_type: cisco_ios
    username: admin
```

2. Run it and type the SSH password when prompted (it is never written to a file):

```bash
python backup_configs.py [--inventory inventory.yaml]
```

3. Check `backups/` — one file per device, named `<hostname>_<date>.txt`. Run it again after a config change and `diff` the two files to see drift:

```bash
diff backups/Cat8kv_2026-11-12.txt backups/Cat8kv_2026-11-13.txt
```

## Try it without hardware

`inventory-sandbox.yaml` points at Cisco's free DevNet always-on IOS XE sandbox (`sandbox-iosxe-latest-1.cisco.com`, Catalyst 8000v). The published demo login is `admin` / `C1sco12345`:

```bash
python backup_configs.py --inventory inventory-sandbox.yaml
```

Verified 2026-11-13 against the sandbox (IOS XE 17.15): a 183-line running-config backup saved for `Cat8kv`.

## How it works

- One SSH session per device via Netmiko (`cisco_ios`)
- Verifies the connection first with `show version | include uptime` and the device prompt before trusting the output
- Timeouts tuned for slow or shared devices (30s connect, 60s command)
- A failure on one device is reported and the run continues with the rest
- Credentials are never stored: username from inventory, password prompted at runtime with `getpass`

## Project structure

```
backup_configs.py       # the backup script
inventory.yaml          # your lab devices (placeholder addresses)
inventory-sandbox.yaml  # Cisco DevNet always-on IOS XE sandbox
requirements.txt        # pinned dependencies
backups/                # generated backups (git-ignored)
LICENSE                 # MIT
```

## Roadmap

- Ansible version of the same backup (`cisco.ios.ios_config` with `backup: yes`) against the same inventory — see also [ansible-network-baseline](https://github.com/abowden101/ansible-network-baseline)

## Author

Antonio Bowden  
Network Engineer · Orlando, FL  
[GitHub](https://github.com/abowden101) · [Portfolio](https://abowden101.github.io/antonio-bowden-portfolio/)
