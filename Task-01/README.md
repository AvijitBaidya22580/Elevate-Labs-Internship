# 🛡️ Task 1: Cyber Security Fundamentals & Attack Surface Analysis

## 📌 Overview

This module focuses on building a foundational understanding of cybersecurity principles, actor profiling, and attack surface mapping. The objective is to move beyond theoretical definitions and apply core concepts (CIA Triad, OWASP Top 10) to real-world applications and infrastructure.

**Final Outcome:** A strong, documented foundation in threat awareness and architectural vulnerability assessment.

---

## 🛠️ Tools & Prerequisites

### Primary

* **Web Browser:** Chrome or Firefox (latest version recommended for rendering modern web apps).

### Reference Knowledge Bases

* **[OWASP Foundation](https://owasp.org/):** The standard for web application security.
* **Google Cybersecurity Blog:** For current trends and threat intelligence.
* **NIST / ISO Standards (Optional):** For formal definitions of CIA.

---

## 📋 Execution Guide

Follow these steps to complete the module deliverables.

### Phase 1: Conceptual Foundations

1. **CIA Triad Deep Dive:**
* Research **Confidentiality, Integrity, and Availability**.
* *Action:* Define each pillar and provide a real-world failure scenario (e.g., a banking DDoS attack affects *Availability*; a password leak affects *Confidentiality*).


2. **Threat Actor Profiling:**
* Identify and categorize attackers based on motivation and capability:
* **Script Kiddies:** Low skill, use existing tools.
* **Insiders:** High access, trusted status.
* **Hacktivists:** Ideologically motivated.
* **Nation State Actors:** High resource, APT (Advanced Persistent Threat) focus.





### Phase 2: Attack Surface Mapping

3. **Digital Landscape Analysis:**
* Explore the differences between web apps, mobile APIs, network infrastructure, and cloud environments.


4. **Vulnerability Study (OWASP Top 10):**
* Visit the current [OWASP Top 10](https://owasp.org/www-project-top-ten/).
* *Critical:* Don't just memorize the names; understand the *mechanism* (e.g., how Broken Access Control actually happens).


5. **Real-World Mapping:**
* Select daily-use applications (e.g., WhatsApp, Gmail, NetBanking).
* Map their features to potential attack surfaces (e.g., "File Upload" feature = potential malware entry point).



### Phase 3: Data Flow Modeling

6. **Architecture Visualization:**
* Trace the path of data: `User Input` → `Frontend App` → `API/Server` → `Database`.


7. **Threat Injection:**
* Identify where attacks occur in this flow (e.g., Man-in-the-Middle attacks happen between User and Server; SQL Injection happens between Server and Database).



---

## 🛠️ Practical Implementation: Attack Surface Analyzer Tool

To ground these conceptual models in practice, this task includes a Python-based utility: **`attack_surface_analyzer.py`**. This tool programmatically assesses the digital attack surface of any target domain or IP.

### Features
1. **Port Scanning:** Scans standard target ports (SSH, FTP, HTTP, HTTPS, RDP, etc.) to discover open ports.
2. **Security Header Auditing:** Interrogates target HTTP(S) responses to check for defensive security configurations like:
   - `Content-Security-Policy` (CSP)
   - `X-Frame-Options`
   - `X-Content-Type-Options`
   - `Strict-Transport-Security` (HSTS)
   - `Referrer-Policy`
3. **Information Leakage Detection:** Checks for exposed web server signatures (e.g. `Server` banner).
4. **SSL/TLS Auditing:** Inspects active SSL/TLS certificates and calculates expiry window metrics.
5. **Risk Scoring:** Assigns a priority weight and outputs a structured vulnerability rating with defensive suggestions.

### How to Run
Run the tool using standard Python:
```bash
python attack_surface_analyzer.py <target_domain>
```
*Example:* `python attack_surface_analyzer.py google.com`

---

## 📦 Deliverables

Create a single document (PDF or DOCX) structured as follows:

| Section | Content Requirement |
| --- | --- |
| **1. The CIA Triad** | Definitions + Real-world Banking/Social Media examples. |
| **2. Threat Actors** | Table comparing actors by Skill Level and Motivation. |
| **3. Attack Surfaces** | Analysis of Web, Mobile, API, and Cloud vectors. |
| **4. OWASP Summary** | Brief explanation of why the Top 10 are dangerous. |
| **5. Data Flow Diagram** | Visual or descriptive map of User → DB flow with identified attack points. |

---

## 💡 Expert Hints

> * **Think like an attacker:** When looking at a login page, don't just see a form. See an entry point for SQL Injection or Brute Force attacks.
> * **Context matters:** The "Integrity" of data is far more critical to a bank than to a meme page. Adjust your risk assessment accordingly.
> * **Documentation:** Clear documentation is a critical skill in cybersecurity. Use diagrams where possible (Draw.io is a good tool for Step 6).
> 
> 

---

## 📚 Resources

* [OWASP Top 10 Project](https://owasp.org/www-project-top-ten/)
* [Cybersecurity & Infrastructure Security Agency (CISA)](https://www.cisa.gov/)
* [SANS Institute Reading Room](https://www.sans.org/white-papers/)

---
