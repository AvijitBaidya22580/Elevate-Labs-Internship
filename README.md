# Malware Types & Behavior Analysis (Basic)

## Introduction

Malware (Malicious Software) analysis is a core pillar of cybersecurity. It involves the process of dissecting and understanding how malicious software functions, its origins, and its potential impact. In a landscape where threats evolve daily, the ability to analyze malware allows security professionals to build better defenses, respond to incidents effectively, and protect sensitive data.

This guide provides a foundational overview of malware categories and a safe methodology for analyzing their behaviors using industry-standard, cloud-based tools.

---

## Objectives

By completing this task, you will be able to:

* **Distinguish** between various malware categories based on their propagation and intent.
* **Execute** basic malware analysis using non-intrusive, cloud-based tools.
* **Identify** Indicators of Compromise (IOCs) such as registry changes and network callbacks.
* **Develop** a systematic approach to investigating suspicious files without risking host infection.

---

## Tools Used

For this basic analysis, we will use "Static-Analysis-as-a-Service" platforms. These allow you to study malware behavior without executing it on your local machine.

* **Primary Tool: [VirusTotal**](https://www.virustotal.com/)
* An online service that analyzes files and URLs to detect types of malware using over 70 antivirus scanners and URL/domain blacklisting services.


* **Alternative Tool: [Any.Run](https://any.run/) (Free Tier)**
* An interactive online malware sandbox that allows you to watch malware execution in real-time within a safe, virtualized environment.



---

## Malware Types Overview

Understanding the "who" and "what" of a file starts with its classification:

* **Virus:** A program that attaches itself to a legitimate file or document. It requires human intervention (like opening an attachment) to spread.
* **Worm:** A self-replicating program that spreads across networks automatically by exploiting vulnerabilities, without needing a host file.
* **Trojan:** Software that appears legitimate but performs malicious activity in the background. It does not self-replicate and relies on social engineering.
* **Ransomware:** A type of malware that encrypts a victim's files. The attacker then demands a ransom (usually in cryptocurrency) to provide the decryption key.

---

## Methodology / Step-by-Step Guide

### 1. Uploading Samples to VirusTotal

> **Note:** Never upload sensitive or proprietary documents to VirusTotal, as they become public to the research community.

1. Obtain the **SHA-256 or MD5 hash** of a suspicious file (or the file itself if you are in a safe environment).
2. Navigate to [VirusTotal](https://www.virustotal.com/).
3. Click the **Search** tab to paste a hash, or the **File** tab to upload a sample.
4. Submit the entry for analysis.

### 2. Reading and Analyzing Reports

* **Detection Tab:** View the consensus among AV engines. A high detection ratio (e.g., 50/70) strongly indicates malicious intent.
* **Details Tab:** Examine file metadata, such as the "History" section (creation/submission dates) and "Signature Info."
* **Community Tab:** Read notes from other researchers who may have identified the specific malware family.

### 3. Observing Behavioral Indicators

On the **Behavior** tab (or within an Any.Run session), look for:

* **DNS Requests:** Domains the malware attempts to contact.
* **HTTP Requests:** Specific URLs used to download second-stage payloads.
* **Registry Actions:** Modifications to system settings to disable security tools.

### 4. The Malware Lifecycle

Malware typically follows these stages:

1. **Delivery:** The initial entry (e.g., Phishing email).
2. **Exploitation:** Triggering a vulnerability or tricking the user.
3. **Installation:** Dropping the malicious payload onto the system.
4. **Command & Control (C2):** Establishing a heartbeat with the attacker's server.
5. **Actions on Objectives:** Stealing data, encrypting files, or spreading further.

### 5. Propagation Methods

* **Phishing:** Deceptive emails containing malicious links or attachments.
* **Drive-by Downloads:** Malicious scripts on websites that download malware automatically.
* **Removable Media:** Infected USB drives that run malicious code via "autorun" features.

---

## Behavior Analysis Indicators

When reviewing a report, keep an eye out for these common "Red Flags":

* **File System Changes:** Creation of hidden files in `Temp` folders or modification of system files in `C:\Windows\System32`.
* **Network Communication:** Unusual traffic on ports like 4444, 8080, or connections to known malicious IP addresses.
* **Persistence Mechanisms:** Creating new "Scheduled Tasks" or adding entries to "Run" keys in the Windows Registry to ensure the malware starts after a reboot.
* **Privilege Escalation:** Attempts to bypass User Account Control (UAC) to gain administrative or "SYSTEM" level access.

---

## Prevention & Mitigation Techniques

* **Endpoint Protection:** Use a robust Antivirus/EDR (Endpoint Detection and Response) solution.
* **User Training:** Educate users on identifying phishing attempts and suspicious links.
* **Patch Management:** Regularly update operating systems and software to close known vulnerabilities.
* **Principle of Least Privilege (PoLP):** Ensure users only have the permissions necessary for their roles to limit the "blast radius" of an infection.

---

## Deliverables

To successfully complete this task, you must submit a **Malware Classification Report** including:

1. The **Hash (SHA-256)** of the analyzed sample.
2. The **Classification** (e.g., Trojan/Ransomware).
3. A list of at least **3 Behavioral Indicators** (e.g., a specific IP it contacted).

## Expected Outcome

Learners will emerge with a fundamental understanding of how malware operates and the practical skills to use automated analysis tools to identify and document malicious threats.

## Conclusion

Malware analysis is an essential skill for any cybersecurity professional. By understanding how malware is delivered, how it behaves once inside a system, and how to use tools like VirusTotal and Any.Run, you are better equipped to defend networks and respond to security incidents.
