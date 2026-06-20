# Task 5: Malware Types & Behavior Analysis (Basic)

## 📖 1️⃣ Introduction

**Malware Analysis** is the art and science of dissecting malicious software to understand its origin, functionality, and potential impact. In the current cybersecurity landscape, relying solely on signature-based detection (matching file fingerprints) is no longer sufficient. Threat actors continuously evolve their tactics, employing polymorphism and obfuscation to evade traditional defenses.

This project focuses on **Behavioral Analysis**—a methodology that looks beyond *static code* to observe *dynamic actions*. By analyzing how a file interacts with the file system, registry, and network, analysts can identify **Indicators of Compromise (IOCs)** regardless of the file's signature. This repository documents the classification and behavioral study of fundamental malware types using industry-standard threat intelligence tools.

---

## 🎯 2️⃣ Project Objectives

The primary goal of this project is to bridge the gap between theoretical knowledge of malware and practical identification skills.

1. **To differentiate between core malware categories:** I aim to clearly distinguish the operational differences between Viruses, Worms, Trojans, and Ransomware based on their infection vectors and payloads.
2. **To interpret Threat Intelligence reports:** I will develop the skill to read and analyze automated sandbox reports from tools like VirusTotal to separate false positives from true threats.
3. **To identify behavioral Indicators of Compromise (IOCs):** I will learn to recognize specific "red flags" such as registry persistence keys, suspicious network callbacks, and file system modifications.
4. **To understand the Malware Lifecycle:** I will map observed behaviors to the Cyber Kill Chain, identifying how malware establishes a foothold and executes its objectives.

---

## 🛠️ 3️⃣ Tools & Platforms Used

### 🟢 VirusTotal (Primary Analysis Engine)

* **Purpose:** VirusTotal is a premier threat intelligence platform that aggregates over 70 antivirus scanners and URL/domain blocklisting services.
* **Usage:** In this project, VirusTotal was used to perform **Static Analysis** (identifying file metadata, compilation dates, and signatures) and to review crowdsourced detection ratios. It serves as the initial "triage" point for any suspicious file.

### 🟠 Any.Run (Alternative / Behavioral Reference)

* **Purpose:** An interactive, cloud-based sandbox that allows users to watch malware execute in real-time.
* **Usage:** While the free tier has limitations, it provides a crucial visual representation of process trees (e.g., a Word document spawning a PowerShell script), which is essential for understanding **Dynamic Behavior**.

---

## 🦠 4️⃣ Malware Types Explained in Depth

This section details the four malware categories analyzed in this project.

### 1. Virus

* **Definition:** A piece of code that is capable of copying itself and has a detrimental effect, such as corrupting the system or destroying data.
* **Key Behavior:** A virus is **parasitic**; it requires a host file (like an `.exe` or `.doc`) to live. It cannot run on its own.
* **Infection Method:** It spreads when the user unknowingly transfers and executes the infected host file (e.g., sharing a USB drive or email attachment).
* **Real-World Impact:** Data corruption, system slowdowns, and unauthorized application behavior.

### 2. Worm

* **Definition:** A standalone malware computer program that replicates itself in order to spread to other computers.
* **Key Behavior:** Unlike a virus, a worm is **autonomous**. It does not need a host file or user interaction to spread.
* **Infection Method:** Worms exploit network vulnerabilities (such as unpatched SMB ports) to move laterally across a network.
* **Real-World Impact:** Massive network congestion (DoS), rapid infection of enterprise networks, and delivery of secondary payloads (like ransomware).

### 3. Trojan (Trojan Horse)

* **Definition:** A type of malware that is often disguised as legitimate software.
* **Key Behavior:** Trojans rely on **social engineering**. They look like useful tools (cracked games, PDF converters) but execute malicious code in the background.
* **Infection Method:** The user is tricked into downloading and installing the file manually.
* **Real-World Impact:** Installation of backdoors (Remote Access Trojans), theft of sensitive data (banking info), and turning the machine into a botnet zombie.

### 4. Ransomware

* **Definition:** Malware that employs encryption to hold a victim's information at ransom.
* **Key Behavior:** It rapidly traverses the file system, encrypts user files using strong cryptographic algorithms (AES/RSA), and deletes shadow volume backups to prevent recovery.
* **Infection Method:** Often delivered via Phishing emails or dropped by other malware (like Trojans).
* **Real-World Impact:** Catastrophic data loss, operational downtime, and financial extortion.

---

## 🔬 5️⃣ Step-by-Step Methodology

The analysis was conducted following a strict safe-handling protocol:

1. **Hash Selection:** I selected MD5/SHA256 hashes of well-known educational malware samples (e.g., WannaCry, Emotet) from public security repositories.
2. **Submission & Triage:** These hashes were queried in VirusTotal.
3. **Detection Ratio Analysis:** I evaluated the "Score" (e.g., 65/72 vendors). A high score confirms malicious intent, while specific vendor names (e.g., `Ransom.WannaCry`) help in classification.
4. **Behavioral Observation:** I navigated to the "Behavior" and "Relations" tabs to observe what the file *attempted* to do in the sandbox.
5. **Lifecycle Mapping:** I correlated the observed technical actions (e.g., creating a registry key) with the malware's intent (e.g., Persistence).
6. **Documentation:** All findings were recorded in the project reports.

---

## 🚩 6️⃣ Behavior Analysis Indicators (Detailed)

This project identified specific technical indicators that serve as evidence of malicious activity.

### 📁 File System Modifications

* **Dropping Files:** Malware often writes new executable files to `%TEMP%` or `%APPDATA%`. This allows it to hide deep within the user's directory structure.
* **Extension Spoofing:** Files may be named `document.pdf.exe` to trick Windows into hiding the `.exe` extension.

### ⚙️ Registry Activity & Persistence

* **The "Run" Keys:** The most common behavior observed was malware adding entries to `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`.
* **Why?** This ensures the malicious code executes automatically every time the computer reboots, achieving **Persistence**.

### 🌐 Network Communication

* **C2 Callbacks:** The analysis showed attempts to contact unregistered domains or suspicious IP addresses.
* **Why?** This is the **Command & Control (C2)** phase, where the malware asks the attacker for instructions or exfiltrates stolen data.

### 🛡️ Privilege Escalation

* **UAC Bypass:** Attempts to execute commands with elevated administrative privileges without alerting the user via the User Account Control prompt.

---

## 🔄 7️⃣ Malware Lifecycle Explanation

Understanding the lifecycle helps in disrupting the attack.

1. **Initial Infection:** The delivery mechanism (Phishing email, USB, Drive-by download).
2. **Execution:** The code runs on the endpoint.
3. **Persistence:** The malware modifies the system to survive reboots.
4. **Privilege Escalation:** The malware attempts to gain Admin/Root access.
5. **Command & Control (C2):** The malware communicates with the attacker.
6. **Action on Objectives:** The final payload is executed (Encryption, Theft, Destruction).

---

## 🛡️ 8️⃣ Prevention & Mitigation Strategies

Based on the analysis, the following defense mechanisms are critical:

* **User Awareness:** Training users to recognize phishing attempts and double-check file extensions.
* **Endpoint Protection:** Utilizing EDR (Endpoint Detection & Response) rather than just legacy Antivirus, as EDR can detect *behavior* even if the signature is unknown.
* **Patch Management:** Keeping systems updated to prevent Worms from exploiting vulnerabilities like EternalBlue.
* **Network Segmentation:** Isolating critical systems so that if one machine is infected, the malware cannot spread to the entire network.

---

## 📦 9️⃣ Deliverables

* [x] **Malware Classification Report:** A detailed technical breakdown of findings.
* [x] **Behavior Analysis Notes:** Raw data and observations.
* [x] **Screenshots:** Visual proof of detection and graph analysis.

---

## 🔐 Ethical & Legal Considerations

> **⚠️ DISCLAIMER:**
> * **Educational Use Only:** This repository is intended for academic and professional development in the field of cybersecurity.
> * **No Live Malware:** No executable malware samples are hosted or distributed in this repository. All analysis was performed using **File Hashes**.
> * **Safe Harbor:** All actions complied with standard ethical guidelines for security research. No systems were harmed, and no unauthorized access was attempted.
> 
> 

---

## 🔍 Final Outcome & Skills Gained

By completing this task, I have developed a foundational understanding of **Malware Forensics**. I can now confidently interpret automated sandbox reports, identify the difference between various malware families, and articulate the technical indicators that signal a system compromise. This project has enhanced my ability to contribute to Blue Team operations and Incident Response scenarios.

---

*Author: Avijit Baidya*
*Date: Jan, 2026*
