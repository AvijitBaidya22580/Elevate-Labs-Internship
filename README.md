# Task-7-Web-Application-Vulnerability-Testing

A comprehensive cybersecurity project demonstrating manual and automated web application penetration testing. This repository documents the methodology, tools, and findings from testing intentionally vulnerable applications to understand common security flaws and their mitigations.

> **⚠️ DISCLAIMER: Legal & Ethical Use**
> This project is for **educational purposes only**. All testing was conducted on locally hosted, intentionally vulnerable applications (DVWA/OWASP Juice Shop) within an isolated environment.
> * Do not use these techniques on real-world applications without explicit written consent from the owner.
> * Unauthorized access to computer systems is illegal and punishable by law.
> * The author assumes no liability for the misuse of the information contained in this repository.
> 
> 

---

## 📖 Project Overview

This project simulates a real-world Vulnerability Assessment and Penetration Testing (VAPT) engagement. The goal is to identify, analyze, and document security vulnerabilities within web applications using industry-standard tools and methodologies based on the OWASP Top 10.

### 🎯 Objectives

* Understand the mechanics of HTTP requests and responses.
* Learn how to configure and use proxy tools (Burp Suite/OWASP ZAP).
* Identify common web vulnerabilities (SQL Injection, XSS, Broken Access Control).
* Practice documenting findings and providing remediation strategies.

---

## 🛠️ Tools & Technologies

* **Proxy/Analysis:** [Burp Suite Community Edition](https://portswigger.net/burp)
* **Alternative Tool:** [OWASP ZAP (Zed Attack Proxy)](https://www.zaproxy.org/)
* **Target Environments:**
* [DVWA (Damn Vulnerable Web App)](https://github.com/digininja/DVWA)
* [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/)


* **Virtualization:** Docker (Recommended) or VirtualBox

---

## ⚙️ Prerequisites

Before starting, ensure you have the following installed:

1. **Docker Desktop** (For easy deployment of targets)
2. **Firefox Browser** (Recommended for FoxyProxy integration)
3. **FoxyProxy Extension** (To switch traffic to Burp/ZAP easily)

---

## 🚀 Setup Instructions

We will use **Docker** to safely spin up the vulnerable environments.

### Option 1: OWASP Juice Shop (Recommended for Modern Web App Testing)

```bash
# Pull the latest image
docker pull bkimminich/juice-shop

# Run the container on port 3000
docker run --rm -p 3000:3000 bkimminich/juice-shop

```

*Access via:* `http://localhost:3000`

### Option 2: DVWA (Legacy PHP Testing)

```bash
# Run DVWA using a pre-configured Docker image
docker run --rm -it -p 80:80 vulnerables/web-dvwa

```

*Access via:* `http://localhost` (Default creds: `admin` / `password`)

---

## 🔍 Testing Methodology

This project follows a structured approach aligned with the **OWASP Top 10** framework.

### 1. Intercepting Traffic

Using Burp Suite as a proxy to intercept traffic between the browser and the server allows for the manipulation of parameters in real-time.

* **Setup:** Configure Firefox FoxyProxy to `127.0.0.1:8080`.
* **Action:** Turn "Intercept On" in Burp Suite.
* **Goal:** Capture the login request and analyze headers.

### 2. SQL Injection (SQLi)

Attempting to manipulate the backend database query to bypass authentication or extract data.

* **Target Area:** Login forms, Search bars, ID parameters.
* **Test Payload (Authentication Bypass):**
```sql
' OR '1'='1

```


* **Observation:** If the application logs you in without a password, the SQL query was successfully manipulated.

### 3. Cross-Site Scripting (XSS)

Injecting malicious scripts to execute in the victim's browser.

* **Reflected XSS:** The script is reflected off the web server (e.g., search results).
* **Stored XSS:** The script is permanently stored on the server (e.g., comment sections).
* **Test Payload (Safe PoC):**
```html
<script>alert('Vulnerable to XSS')</script>

```


* **Observation:** A pop-up alert box confirms the code execution.

---

## 📊 Sample Findings

*Note: In a real engagement, this would be a detailed PDF report.*

| Vulnerability | Severity | Description | Status |
| --- | --- | --- | --- |
| **SQL Injection** | **Critical** | Login form allows authentication bypass via header manipulation. | 🔴 Open |
| **Reflected XSS** | **High** | Search parameter reflects input without sanitization. | 🔴 Open |
| **Weak Passwords** | **Medium** | Default credentials (`admin`/`password`) were active. | 🟠 Mitigated |

### Example Exploit: SQL Injection

**Location:** `/vulnerabilities/sqli/`
**Payload Used:**

```text
%27+OR+1%3D1+%23

```

**Result:** The database returned all user rows, exposing sensitive user IDs and names.

---

## 🛡️ Mitigation Recommendations

To secure the application against the vulnerabilities found above:

1. **Prevent SQL Injection:**
* Use **Prepared Statements** (Parameterized Queries) for all database access.
* Input validation: Ensure input data matches expected types.


2. **Prevent XSS:**
* **Context-aware encoding:** Encode data before rendering it in the browser (HTML, JavaScript, CSS).
* Implement **Content Security Policy (CSP)** headers to restrict script execution sources.


3. **General Hygiene:**
* Change default credentials immediately upon setup.
* Ensure error messages do not leak system information.



---

## 📂 Deliverables

This repository contains:

* [x] Vulnerability Assessment Checklist
* [x] Sample Penetration Test Report (Mock)
* [x] Screenshots of intercepted requests (in `/evidence` folder)
* [x] List of safe payloads used for testing

---

## 🧠 Learning Outcomes

By completing this project, I have gained proficiency in:

* **Burp Suite Proficiency:** Repeater, Intruder, and Decoder modules.
* **Web Protocol Analysis:** Deep understanding of HTTP/S, Headers, Cookies, and Sessions.
* **Vulnerability Identification:** Recognizing signatures of SQLi, XSS, and Command Injection.
* **Remediation:** Writing developer-friendly fixes for security flaws.

---

### 👤 Author

Avijit Baidya
* **GitHub:** [Your GitHub Profile]

*If you found this project helpful or have suggestions, feel free to open an issue or pull request!*
