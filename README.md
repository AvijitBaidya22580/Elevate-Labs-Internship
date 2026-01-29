# 🛡️ Task 9: Network Vulnerability Scanning & Risk Assessment

## 📌 Executive Summary

**Vulnerability Scanning** is the proactive identification of security flaws in IT infrastructure before they can be exploited by malicious actors. Unlike the passive analysis in Task 3 (Wireshark), this module involves **active engagement** with target systems to solicit responses, identify running services, and map them against known vulnerability databases (CVEs).

This repository documents the methodology, execution, and analysis of a comprehensive vulnerability assessment performed on a controlled laboratory network.

**⚠️ LEGAL DISCLAIMER:**

> *Active scanning of networks without explicit written permission is illegal and punishable under computer misuse laws (e.g., IT Act 2000 in India, CFAA in USA). All scans documented here were performed on a local, isolated virtualization environment (Sandboxed VM Network) owned by the operator.*

---

## 🎯 Objectives

1. **Asset Discovery:** Identify live hosts and network topology.
2. **Service Enumeration:** Determine open ports, protocols, and exact software versions.
3. **Vulnerability Mapping:** Correlate software versions with the **CVE (Common Vulnerabilities and Exposures)** database.
4. **Risk Scoring:** Utilize **CVSS (Common Vulnerability Scoring System)** to prioritize remediation.

---

## 🛠️ Technical Toolkit

### Core Engine

* **Nmap (Network Mapper):**
* *Role:* Reconnaissance, Port Scanning, Service Versioning, OS Fingerprinting.
* *Key Scripting Engine:* `vuln` (NSE - Nmap Scripting Engine).



### Automated Scanners (One of the following)

* **Tenable Nessus (Essentials):** Industry-standard vulnerability scanner.
* **OpenVAS (Greenbone):** Open-source alternative.

### Target Environment

* **Metasploitable 2 / 3:** Intentionally vulnerable Linux virtual machines.
* **Windows 10/11 (Unpatched):** Control target.

---

## ⚙️ Operational Methodology

### Phase 1: Reconnaissance (Nmap)

Before scanning for weaknesses, we must define the attack surface.

**1. Host Discovery (Ping Sweep)**
Identify live hosts in the subnet `192.168.1.0/24`.

```bash
nmap -sn 192.168.1.0/24

```

**2. Service & Version Detection**
We use the `-sV` flag to interrogate open ports for banners to determine the exact service version (e.g., `Apache 2.2.8` vs `Apache 2.4.50`).

```bash
nmap -sV -sC -O 192.168.1.X

```

* `-sC`: Runs default scripts.
* `-O`: Operating System detection.

**3. Targeted NSE Vulnerability Check**
Using Nmap's built-in scripting engine to check for specific vulnerabilities (e.g., SMBGhost, Heartbleed).

```bash
nmap --script vuln 192.168.1.X

```

### Phase 2: Automated Vulnerability Assessment (Nessus)

Manual correlation is inefficient. We leverage automated scanners for depth.

1. **Policy Configuration:**
* Selected Policy: *Basic Network Scan*.
* Port Scan Range: *All ports*.
* Assessment Mode: *Non-credentialed* (External view) vs. *Credentialed* (Insider view).


2. **Execution:**
* Launched scan against Target IP.
* Monitored system load to prevent Denial of Service (DoS) on fragile legacy services.



### Phase 3: Risk Analysis & Reporting

Raw data must be interpreted. Vulnerabilities are categorized by severity.

* **Critical (CVSS 9.0 - 10.0):** Immediate Remote Code Execution (RCE) or Root compromise possible.
* **High (CVSS 7.0 - 8.9):** Significant compromise, difficult to exploit or requires user interaction.
* **Medium (CVSS 4.0 - 6.9):** Information disclosure, DoS, or limited access.

---

## 📂 Repository Contents

| File / Folder | Description |
| --- | --- |
| `/Scans/nmap_results.txt` | Raw output of Nmap service version scans. |
| `/Scans/nessus_report.pdf` | Generated report detailing identified vulnerabilities. |
| `/Analysis/remediation_plan.md` | Strategic recommendations to patch identified flaws. |
| `Methodology.md` | Detailed step-by-step log of commands used. |

---

## 🔍 Key Findings (Sample)

*Example entry for documentation purposes:*

**Vulnerability:** **VSFTPD v2.3.4 Backdoor Command Execution**

* **Host:** `192.168.1.15` (Metasploitable)
* **Port:** 21/TCP
* **Severity:** **CRITICAL (9.8)**
* **Description:** The specific version of VSFTPD contains a backdoor that opens a shell on port 6200 when a username containing a smiley face `:)` is entered.
* **Remediation:** Upgrade VSFTPD to the latest stable version immediately or decommission the service.

---

## 💡 Expert Insights: False Positives vs. Negatives

> **Note on Accuracy:** Vulnerability scanners are not infallible.
> * **False Positive:** The scanner flags a vulnerability (e.g., "Apache Outdated") because it reads a banner, but the system administrator has "backported" security patches without changing the version number. Verification is required.
> * **False Negative:** The scanner misses a vulnerability because a firewall blocked the probe or the vulnerability is a "Zero-Day" (unknown to the scanner's database).
> 
> 

---

## 📚 References

* [Nmap Reference Guide](https://nmap.org/book/man.html)
* [CVSS v3.1 Specification](https://www.first.org/cvss/v3.1/specification-document)
* [Common Vulnerabilities and Exposures (CVE)](https://cve.mitre.org/)

---
