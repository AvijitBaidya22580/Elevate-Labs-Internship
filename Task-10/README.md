# 🧱 Task 10: Firewall Configuration & Testing

This repository contains the documentation and practical implementation guide for **Task 10: Firewall Configuration & Testing**. This module focuses on network defense fundamentals, specifically the implementation of host-based firewalls to control incoming and outgoing network traffic.

---

## 📖 Project Overview

Firewalls are the first line of defense in network security. This task demonstrates how to configure, manage, and audit firewall rules using industry-standard tools on both Linux (**UFW**) and Windows (**Windows Defender Firewall**) environments. The goal is to understand how to reduce the attack surface by strictly filtering network traffic based on protocols, ports, and IP addresses.

## 🎯 Objectives

* Understand the difference between **Stateful** and **Stateless** inspection.
* Configure default policies (Fail-Safe defaults).
* Create specific rules to **Allow** or **Deny** traffic for services (SSH, HTTP).
* Block malicious traffic from specific IP addresses.
* Analyze firewall logs to detect potential intrusion attempts.
* Verify rule effectiveness using network scanning tools.

---

## 🛠 Tools Used

* **Linux:** UFW (Uncomplicated Firewall) / iptables
* **Windows:** Windows Defender Firewall with Advanced Security / PowerShell
* **Testing:** Nmap, Ping, Netcat
* **Environment:** Virtual Machines (Kali Linux, Ubuntu Server, Windows 10)

## 📋 Prerequisites

* Basic understanding of TCP/UDP ports and IP addressing.
* Administrative (Root/Administrator) privileges on the target machine.
* A safe lab environment (VirtualBox/VMware).

---

## 📚 Task Overview / Implementation Guide

### Phase 1: Conceptual Understanding

Before applying rules, understand that firewalls operate on a "Default Deny" or "Default Allow" basis.

* **Best Practice:** Adopt a **Default Deny** policy for incoming traffic (block everything unless explicitly allowed).

### Phase 2: Linux Configuration (UFW)

*Uncomplicated Firewall is the standard configuration tool for Ubuntu/Debian.*

1. **Check Status:**
```bash
sudo ufw status verbose

```


2. **Set Defaults (Security Best Practice):**
```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing

```


3. **Allow Essential Services:**
* **SSH (Port 22):** *Critical to prevent locking yourself out!*
```bash
sudo ufw allow ssh
# OR specific port
sudo ufw allow 22/tcp

```


* **HTTP/HTTPS (Web Server):**
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

```




4. **Block Specific Malicious IP:**
```bash
sudo ufw deny from 192.168.1.50 to any

```


5. **Enable Firewall & Logging:**
```bash
sudo ufw logging on
sudo ufw enable

```



### Phase 3: Windows Firewall Configuration

*Using PowerShell for automation and precision.*

1. **View Current Profile:**
```powershell
Get-NetFirewallProfile

```


2. **Create an Allow Rule (e.g., for an RDP connection):**
```powershell
New-NetFirewallRule -DisplayName "Allow RDP" -Direction Inbound -LocalPort 3389 -Protocol TCP -Action Allow

```


3. **Block a Program:**
```powershell
New-NetFirewallRule -DisplayName "Block Calculator" -Direction Outbound -Program "C:\Windows\System32\calc.exe" -Action Block

```



### Phase 4: Testing & Verification

Do not trust; verify. Use a separate machine (Attacker VM) to test the rules.

1. **Test Connectivity (Ping):**
If ICMP is blocked, `ping <target-ip>` should timeout.
2. **Port Scan (Nmap):**
Verify that only intended ports are open.
```bash
nmap -p 22,80,443 <target-ip>

```


*Result should show `FILTERED` for blocked ports and `OPEN` for allowed ports.*

### Phase 5: Log Observation

Analyze logs to see dropped packets.

* **Linux:** `tail -f /var/log/ufw.log`
* **Windows:** Event Viewer > Applications and Services Logs > Microsoft > Windows > Windows Firewall with Advanced Security.

---

## 🛡 Impact Analysis

* **Attack Surface Reduction:** By closing unused ports (e.g., closing Port 23 Telnet), we eliminate vectors for brute-force or exploit attacks.
* **Access Control:** Limiting SSH access to specific trusted IPs prevents unauthorized remote administration.
* **Traffic Visibility:** Logging dropped packets provides early warning signs of network reconnaissance (scanning).

## 📂 Deliverables

* **Rules Table:** A document mapping Port/Service to Action (Allow/Deny).
* **Verification Screenshots:** Nmap results showing "Filtered" ports.
* **Log Extract:** Sample logs showing a blocked connection attempt.

## 🏆 Final Outcome

Upon completion, the user demonstrates competence in **Host-Based Defense**, capable of hardening a server against network-based attacks and managing traffic flow policies effectively.

---
