# 🔒 Task 2: Operating System Security & Hardening

## 📌 Overview

Operating System (OS) hardening is the process of securing a system by reducing its "surface of vulnerability." This module moves from theoretical concepts to hands-on systems administration. You will configure a secure environment, enforce strict access controls, and minimize the attack surface by eliminating unnecessary vectors.

**Final Outcome:** A production-ready **OS Security Checklist** and practical proficiency in Linux/Windows system defense.

---

## 🛠️ Laboratory Environment

### Primary Tools

* **Virtualization:** Oracle VirtualBox or VMware Workstation Player.
* **Guest OS:** Ubuntu Linux (Server or Desktop) — *Preferred for this task due to granular control.*
* **Host OS Security:** Windows Defender & Firewall (for comparative analysis).

### Prerequisites

* Basic familiarity with the Command Line Interface (CLI).
* Administrator/Root access to your virtual machine.

---

## 📖 Technical Execution Guide

### Phase 1: Environment & Identity Management (IAM)

*Concept: The Principle of Least Privilege (PoLP).*

1. **Virtual Machine Setup:**
* Install Ubuntu on a VM. *Crucial:* Take a "Snapshot" immediately after installation. This allows you to revert changes if you break the system while learning.


2. **User Accounts & Privileges:**
* Understand the "Root" (Superuser) vs. "Standard User" model.
* **Action:** Create a new user with limited privileges. Attempt to install software or modify system files as this user to see the "Permission Denied" errors.
* **Action:** Practice using `sudo` (SuperUser DO) for temporary privilege escalation.



### Phase 2: File System Security & Permissions

*Concept: Discretionary Access Control (DAC).*

3. **Permissions Analysis:**
* Navigate the file system and inspect permissions using `ls -l`.
* Analyze the output: `-rwxr-xr--` (Owner, Group, Others).


4. **Modifying Access:**
* **`chmod` (Change Mode):** Practice changing permissions.
* *Example:* `chmod 700 file.txt` (Only owner can read/write/execute).


* **`chown` (Change Owner):** Transfer ownership of a file to a different user.
* *Why this matters:* Malware often attempts to execute scripts from temporary directories. Restricting execute permissions (`-x`) in these areas is a key hardening step.



### Phase 3: Network Defense & Attack Surface Reduction

*Concept: Defense in Depth.*

5. **Firewall Configuration:**
* **Linux (UFW):** The "Uncomplicated Firewall" is your primary network shield.
* *Command:* `sudo ufw status` (Check status).
* *Command:* `sudo ufw enable` (Turn it on).
* *Command:* `sudo ufw allow ssh` (Allow remote connection).
* *Command:* `sudo ufw deny http` (Block web traffic if not hosting a server).


* **Windows:** Explore "Windows Defender Firewall with Advanced Security" to create Inbound/Outbound rules.


6. **Service Auditing:**
* Every running service is a potential entry point (port).
* **Identify:** Use `systemctl list-units --type=service --state=running` or `ps aux` to see what is running.
* **Harden:** Disable unused services (e.g., if you aren't printing, disable `cups`; if you aren't sharing files, disable `smbd`).



---

## 📋 Deliverable: The OS Security Checklist

You must create a formal document. Below is a template you can use to structure your findings.

### 📄 Template: OS Hardening Standard Operating Procedure (SOP)

| Category | Check | Command / Action Taken | Status |
| --- | --- | --- | --- |
| **Account Security** | [ ] | Password complexity policy enforced? | ✅ Pass |
| **Account Security** | [ ] | Guest account disabled? | ✅ Pass |
| **File Systems** | [ ] | Root ownership verified for `/etc/shadow`? | ⚠️ Review |
| **Network** | [ ] | UFW enabled and blocking all incoming by default? | ✅ Pass |
| **Services** | [ ] | SSH Root Login disabled? (`PermitRootLogin no`) | ❌ Fail |
| **Updates** | [ ] | System is patched (`apt update && apt upgrade`)? | ✅ Pass |

---

## 💡 Expert Hints for Detail

> * **The "Shadow" File:** When exploring permissions, look specifically at `/etc/shadow`. This file contains hashed user passwords. Notice that *only* root can read it. If a standard user can read this file, the system is compromised.
> * **SSH Hardening:** If you are using SSH, never allow login via password; use SSH Keys. Also, strictly disable root login via SSH in the `/etc/ssh/sshd_config` file.
> * **Persistence:** Malware often installs itself as a service to restart when the computer reboots. Monitoring your startup services (`systemctl list-unit-files --state=enabled`) is how you catch this.
> 
> 

---

## 📚 Resources

* [CIS Benchmarks (Center for Internet Security)](https://www.cisecurity.org/cis-benchmarks/) - *The gold standard for hardening.*
* [Ubuntu Security Guide](https://ubuntu.com/security)
* [Microsoft Windows Security Baselines](https://learn.microsoft.com/en-us/windows/security/threat-protection/windows-security-baselines)

---
