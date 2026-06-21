# 🛡️ Cybersecurity & Automation Framework — Elevate Labs Internship

Welcome! This repository documents the consolidated deliverables, tools, and methodologies completed during my **Cybersecurity & Security Automation Internship** at **Elevate Labs** (*January 1, 2026 – April 30, 2026*). 

The internship comprised **16 consecutive modules** progressing from core infrastructure mapping to advanced application testing, SIEM log monitoring, threat modeling, API vulnerability discovery, and incident response playbook design.

---

## 📊 Comprehensive Task Dashboard

| Module | Task Name | Core Technical Focus | Tools & Tech Stack | Primary Deliverable |
| :---: | :--- | :--- | :--- | :--- |
| **01** | [Attack Surface Analysis](./Task-01) | Reconnaissance & Threat Modeling | `Python`, `sockets`, `ssl`, `urllib` | Zero-dependency port/header scanner |
| **02** | [OS Security & Hardening](./Task-02) | Linux/Windows System Hardening | `Bash`, `PowerShell`, `UFW`, Access Audits | Automated access policy configuration |
| **03** | [Network Traffic Forensics](./Task-03) | Packet Ingestion & Deep Analysis | `Wireshark`, `tshark`, HTTP/DNS Filters | Exploit packet PCAP & payload trace |
| **04** | [Password & Auth Auditing](./Task-04) | Hash Validation & Auth Security | `Hashcat`, `John the Ripper`, `bcrypt` | Cryptographic hash cracking logs |
| **05** | [Malware Behavior Analysis](./Task-05) | Dynamic Sandboxing & Registry Auditing | `Cuckoo Sandbox`, `Procmon`, PE analysis | Dynamic behavior report & IOC list |
| **06** | [Introduction to Cryptography](./Task-06) | PKI, Encryption, & Signatures | `OpenSSL`, `AES-256`, `RSA-4096`, Hashing | Validated encrypted files & signature certs |
| **07** | [Web App Vulnerability Testing](./Task-07) | Offensive Pentesting & Dashboard | `Flask`, `Python`, SQLi/XSS Injectors | Modular scanner with web dashboard |
| **08** | [SQL Injection Exploitation](./Task-08) | Backend DB Exfiltration & Injection | `DVWA`, `SQLMap`, SQL payloads | Documented manual/automated DB dump |
| **09** | [Vulnerability Scanning](./Task-09) | Port Auditing & Risk Prioritization | `Nmap`, `Nikto`, CVSS v3 Matrix | Full-network vulnerability report |
| **10** | [Firewall Config & Testing](./Task-10) | Host Defense Rules & Rules Auditing | `UFW`, `iptables`, `Windows Defender` | Hardened rule scripts & bypass testing |
| **11** | [Phishing Vector Analysis](./Task-11) | Header Forensics & Threat Assessment | `Simulations`, Phishing Analyzers | Flagged indicators & simulation report |
| **12** | [Log Monitoring & SIEM](./Task-12) | Security Analytics & Dashboards | `Splunk SIEM`, Log Parsers | Ingested events correlation dashboards |
| **13** | [Secure API Testing](./Task-13) | BOLA, IDOR, & Auth Validation | `Python API Client`, custom test harness | Custom API auth & scanner script |
| **14** | [Network Intrusion Detection](./Task-14) | Signature/Anomaly Traffic Auditing | `Python IDS Simulator`, Snort-like rules | Real-time traffic alerts simulator |
| **15** | [Risk Prioritization Matrix](./Task-15) | Prioritizing Patches & Vulnerabilities | CVSS v3 framework, exploit indicators | Score-based priority patching roadmap |
| **16** | [Incident Response Playbooks](./Task-16) | Threat Containment & Timeline Auditing | NIST SP 800-61, Forensic Logs | Timeline correlation & incident playbooks |

---

## 🔍 Task-by-Task Details

### [Task 1: Cyber Security Fundamentals & Attack Surface Analysis](./Task-01)
*   **Focus**: Reconnaissance and threat modeling using the CIA Triad and OWASP principles.
*   **Implementation**: Built a custom network scanner in Python using zero third-party packages to map open ports, audit HTTP security headers (CSP, HSTS), and verify SSL/TLS certificates.
*   **Outcome**: Enabled lightweight system checks with zero setup dependencies.

### [Task 2: Operating System Security & Hardening](./Task-02)
*   **Focus**: Operating system configuration hardening.
*   **Implementation**: Configured secure environment settings, local access privileges, file permission monitoring, and firewall enforcement scripts on Linux/Windows hosts.
*   **Outcome**: Reduced system vulnerability area by disabling legacy services and accounts.

### [Task 3: Network Traffic Analysis & Packet Forensics](./Task-03)
*   **Focus**: Deep packet inspection (DPI) and capture analysis.
*   **Implementation**: Used Wireshark and custom filters to inspect traffic, trace HTTP/DNS protocols, flag cleartext credentials, and isolate malicious packets.
*   **Outcome**: Documented key indicators of network compromise from captured PCAP streams.

### [Task 4: Password Security & Authentication Analysis](./Task-04)
*   **Focus**: Passwords, storage safety, and validation.
*   **Implementation**: Audited cryptographic hashing algorithms (bcrypt, PBKDF2) and ran brute-force dictionary attacks against mock hashes using Hashcat.
*   **Outcome**: Established password complexity policies and secure storage guidelines.

### [Task 5: Malware Types & Behavior Analysis](./Task-05)
*   **Focus**: Dynamic analysis of malicious file behaviors.
*   **Implementation**: Monitored registry modifications, file system mutations, and network attempts made by isolated test payloads inside a sandbox environment.
*   **Outcome**: Compiled indicators of compromise (IOCs) for signature-free threat classification.

### [Task 6: Introduction to Cryptography](./Task-06)
*   **Focus**: Data confidentiality, integrity, and authenticity.
*   **Implementation**: Used OpenSSL to generate private/public keypairs, sign/verify documents, and encrypt payloads using symmetric (AES-256) and asymmetric (RSA-4096) schemes.
*   **Outcome**: Configured a local PKI-style mock environment.

### [Task 7: Web Application Vulnerability Testing](./Task-07)
*   **Focus**: Custom web scanning automation.
*   **Implementation**: Built a complete Flask-based vulnerability scanner that crawls links, maps forms, injects SQLi/XSS payloads, and displays findings on a web dashboard.
*   **Outcome**: Modular python scanning tool for non-destructive local testing.

### [Task 8: SQL Injection Practical Exploitation](./Task-08)
*   **Focus**: Offensive SQLi injection lifecycles.
*   **Implementation**: Conducted manual and automated (SQLMap) SQL injection attacks against vulnerable DVWA pages to exfiltrate tables, bypass auth, and dump DB metadata.
*   **Outcome**: Outlined defensive query sanitization and prepared statement patches.

### [Task 9: Network Vulnerability Scanning & Risk Assessment](./Task-09)
*   **Focus**: Network scans and asset scanning.
*   **Implementation**: Deployed Nmap and Nikto to scan target Virtual Machines, mapped vulnerabilities to CVSS scores, and evaluated system risks.
*   **Outcome**: Identified open ports and service vulnerabilities to design patch pathways.

### [Task 10: Firewall Configuration & Testing](./Task-10)
*   **Focus**: Host-based and network defense controls.
*   **Implementation**: Configured firewall policies (Linux UFW / Windows Firewall) to restrict open ports, block unauthorized traffic, and verified rules using spoofed port queries.
*   **Outcome**: Implemented ingress and egress rule sets to prevent lateral movement.

### [Task 11: Phishing Attack Simulation & Detection](./Task-11)
*   **Focus**: Email forensics and simulation analysis.
*   **Implementation**: Analyzed raw email headers for SPF/DKIM validation errors, parsed mock phishing links, and drafted user training playbooks.
*   **Outcome**: Strengthened organization-wide defensive awareness.

### [Task 12: Log Monitoring & Analysis](./Task-12)
*   **Focus**: SIEM dashboard building.
*   **Implementation**: Ingested and parsed server logs using Splunk to correlation events, track brute force attempts, and map threat trends.
*   **Outcome**: Configured centralized dashboards for security operations centers (SOC).

### [Task 13: Secure API Testing, Authorization, and Validation](./Task-13)
*   **Focus**: API security.
*   **Implementation**: Implemented a custom scanner Python script (`api_security_scanner.py`) to audit endpoints for missing authentication tokens, Broken Object Level Authorization (BOLA/IDOR), and input parameters validation issues.
*   **Outcome**: Secured settings and invoice APIs against unauthorized cross-user queries.

### [Task 14: Network Intrusion Detection & Threat Monitoring](./Task-14)
*   **Focus**: Intrusion detection simulation.
*   **Implementation**: Programmed an IDS simulation engine (`ids_simulator.py`) utilizing signature checks and anomaly alert logic (e.g. tracking suspicious request frequencies or payload spikes).
*   **Outcome**: Triggered real-time security alerts on malicious traffic markers.

### [Task 15: Vulnerability Assessment & Risk Prioritization](./Task-15)
*   **Focus**: Prioritizing software updates and patches.
*   **Implementation**: Developed a prioritization system mapping vulnerability severity, exploit accessibility (threat intelligence), and target business asset values.
*   **Outcome**: Designed a structured patching strategy targeting critical vulnerabilities first.

### [Task 16: Incident Response & Security Breach Simulation](./Task-16)
*   **Focus**: Threat response and containment.
*   **Implementation**: Traced logs to rebuild a breach timeline and drafted containment, eradication, and recovery playbooks following NIST SP 800-61 guidelines.
*   **Outcome**: Prepared action sheets to respond to active intrusion alerts.
