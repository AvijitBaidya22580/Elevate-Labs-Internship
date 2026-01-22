# 🛡️ Malware Types & Behavior Analysis (Basic)

## 📂 Repository Structure

This repository is organized to document the analysis process, findings, and theoretical understanding of basic malware behaviors.

```text
├── README.md
├── reports/
│   └── malware_classification_report.md
├── samples/
│   └── sample_hashes.txt
├── screenshots/
│   └── virustotal_analysis.png
└── notes/
    └── behavior_analysis_notes.md

```

> **Note:** The `samples/` directory contains **file hashes only**. No live malware samples or executable code are hosted in this repository to ensure safety and compliance with GitHub policies.

---

## 1️⃣ Project Overview

This project focuses on the fundamental principles of **Malware Analysis**. It documents the classification, behavioral patterns, and detection mechanisms of common malicious software types.

In the modern cybersecurity landscape, defensive operations rely heavily on understanding the "Anatomy of an Attack." By analyzing how malware operates within a sandbox environment, we can identify **Indicators of Compromise (IOCs)** and implement stronger detection rules (SIEM/EDR) to protect enterprise infrastructure.

---

## 2️⃣ Objectives

* **Differentiate** between core malware categories (Virus, Worm, Trojan, Ransomware).
* **Analyze** suspicious file hashes using industry-standard Threat Intelligence (TI) platforms.
* **Identify** behavioral indicators such as persistence mechanisms and Command & Control (C2) traffic.
* **Document** findings in a structured, professional format suitable for incident response.

---

## 3️⃣ Tools & Platforms Used

### 🟢 Primary Tool: [VirusTotal](https://www.virustotal.com/)

* **Purpose:** Static analysis, hash reputation, AV vendor consensus, and crowdsourced threat intelligence.

### 🟠 Alternative Tool: [Any.Run](https://app.any.run/) (Free Tier)

* **Purpose:** Interactive sandbox analysis to observe process execution and network requests in real-time.

---

## 4️⃣ Malware Types Studied

This project explores the four pillars of basic malware:

### 🦠 Virus

A program that infects legitimate files (hosts) and requires user interaction to execute.

* **Behavior:** Appends its code to `.exe` or `.doc` files. Spreads when the infected file is shared and opened.

### 🪱 Worm

A standalone program that replicates itself to spread to other computers.

* **Behavior:** exploits network vulnerabilities (e.g., SMB) to move laterally across a network **without** user interaction or a host file.

### 🐴 Trojan (Trojan Horse)

Malicious code disguised as legitimate software.

* **Behavior:** Users are socially engineered into downloading it (e.g., "Free Antivirus" or "Game Crack"). Once installed, it creates a backdoor for attackers.

### 🔒 Ransomware

Malware designed to deny access to a computer system or data until a ransom is paid.

* **Behavior:** Rapidly encrypts files (AES/RSA), deletes shadow volume backups, and displays a ransom note.

---

## 5️⃣ Methodology

The analysis was conducted using a safe, non-execution approach relying on file hashes.

### 🔹 Step 1: Hash Retrieval & Lookup

Suspicious file hashes (MD5/SHA256) were obtained from educational repositories (e.g., TheZoo or specific lab exercises) and queried in **VirusTotal**.

### 🔹 Step 2: Interpreting Detection Reports

We analyzed the **Detection Ratio** (e.g., 55/70 vendors) and reviewed the **Community Score** to understand the context of the threat (e.g., specific APT groups or campaigns).

### 🔹 Step 3: Lifecycle Analysis

We mapped the malware's behavior to the standard kill chain:

1. **Delivery:** How it arrives (Email, Drive-by Download).
2. **Exploitation:** Executing code on the endpoint.
3. **Installation:** Establishing persistence.
4. **C2:** Contacting the attacker.

### 🔹 Step 4: Propagation Techniques

We documented how the sample attempts to spread, such as:

* **Email Spam:** Sending copies of itself to the victim's address book.
* **Network Shares:** Copying to open shared folders.

---

## 6️⃣ Behavior Indicators Observed

During the analysis of the reports, the following **Indicators of Compromise (IOCs)** were noted:

### 📁 File System Activity

* Creation of executables in temporary folders (`%TEMP%`, `AppData`).
* Modification of system files (`hosts` file, critical DLLs).

### ⚙️ Registry Changes & Persistence

* **Run Keys:** Entries added to `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`.
* **Services:** Creation of new malicious services to ensure the malware survives a reboot.

### 📡 Network Traffic Patterns

* **DNS Requests:** Queries to randomly generated domain names (DGA).
* **HTTP/HTTPS:** Connections to non-standard ports or known malicious IP addresses for C2 instructions.

---

## 7️⃣ Prevention & Mitigation Techniques

Based on the analysis, the following defense mechanisms are recommended:

* **User Awareness:** Training to recognize phishing emails and avoid downloading "cracked" software.
* **System Hardening:** Disabling unnecessary services (e.g., SMBv1) and restricting macro execution in Office documents.
* **Endpoint Protection:** Utilizing EDR solutions that detect behavior (heuristics) rather than just signatures.
* **Network Security:** Implementing firewalls and blocking communication to known malicious IPs/Domains.

---

## 8️⃣ Deliverables

This repository contains the following outputs:

* 📄 **Malware Classification Report:** A detailed breakdown of the analyzed hashes.
* 📝 **Behavior Analysis Notes:** Raw observations regarding registry and network anomalies.
* 🖼️ **Screenshots:** Visual evidence of the VirusTotal detection graphs and behavior trees.

---

## 9️⃣ Final Outcome

Completing this task has enhanced the following skills:

1. **Threat Intelligence Gathering:** Proficiency in using OSINT tools to validate threats.
2. **IOC Extraction:** The ability to pull actionable data (IPs, Hashes) from analysis reports.
3. **Technical Documentation:** Translating technical findings into clear, structured reports.

---

## 🔐 Ethical & Legal Disclaimer

> **⚠️ WARNING:**
> This repository is for **EDUCATIONAL PURPOSES ONLY**.
> * **Do not** attempt to download, execute, or distribute real malware samples on personal or production networks.
> * All analysis was performed using **file hashes** and **cloud-based sandboxes**.
> * The author is not responsible for any damage caused by the misuse of the information provided herein.
> * Always follow the "Safe Harbor" principles of cybersecurity research.
