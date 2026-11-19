# Network Config Backup (Netmiko)

Simple, reliable Cisco IOS/IOS-XE running-config backup tool built with Netmiko.

Point it at an inventory of devices and it:
- Connects over SSH
- Verifies the device is reachable
- Pulls `show running-config`
- Saves a timestamped backup per device
- Continues on failure (one bad device doesn’t stop the rest)

**Read-only** — it only runs `show` commands. Nothing is written to the devices.

---

## Features

- Inventory-driven (YAML)
- Password prompted at runtime (never stored)
- Per-device timeout handling
- Failure isolation
- Works with Cisco DevNet always-on sandbox out of the box
- Easy to extend for other platforms (Juniper, Arista, etc.)

---

## Quick Start

### 1. Install dependencies
```bash
pip install netmiko pyyaml
```

### 2. Configure inventory
Edit `inventory.yaml`:

```yaml
devices:
  - host: 192.168.1.10
    device_type: cisco_ios
    username: admin
  - host: 192.168.1.11
    device_type: cisco_ios
    username: admin
```

### 3. Run the backup
```bash
python backup_configs.py
```

You will be prompted for the SSH password once. Backups are saved in the `backups/` folder as:

```
<hostname>_YYYY-MM-DD.txt
```

---

## Try It Instantly (No Lab Required)

Use Cisco’s free always-on IOS-XE sandbox:

```bash
python backup_configs.py --inventory inventory-sandbox.yaml
```

Credentials are already in the sandbox inventory file (`admin` / `C1sco12345`).

---

## Example Output

```
[+] Connecting to Cat8kv (sandbox-iosxe-latest-1.cisco.com)...
[+] Backup saved: backups/Cat8kv_2026-11-13.txt (183 lines)
[+] Done. 1 device succeeded, 0 failed.
```

---

## Project Structure

```
backup_configs.py          # Main script
inventory.yaml             # Your devices
inventory-sandbox.yaml     # Cisco DevNet sandbox
backups/                   # Generated backups (git-ignored)
```

---

## Roadmap

- [ ] Ansible version of the same backup workflow
- [ ] Multi-vendor support (Arista, Fortinet, Juniper)
- [ ] Basic compliance checks (NTP, AAA, logging)
- [ ] Optional NetBox inventory source

---

## Author

Antonio Bowden  
Network Engineer | Orlando, FL  
[GitHub](https://github.com/abowden101) · [Portfolio](https://abowden101.github.io/antonio-bowden-portfolio/)
