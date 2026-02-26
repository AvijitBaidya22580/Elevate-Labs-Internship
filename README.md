# Web-Application-Vulnerability-Scanner

<p align="center">
  <img src="https://img.shields.io/badge/Web%20Security-Vulnerability%20Scanner-red?style=for-the-badge&logo=shield&logoColor=white" alt="Web Security Vulnerability Scanner" />
</p>

<h1 align="center">🛡️ Web Application Vulnerability Scanner</h1>

<p align="center">
  <strong>Internship Project – ELEVATS LAB</strong><br>
  NATTO MUNI CHAKMA | Andhra University
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Flask-Web%20Framework-black?logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/OWASP%20Top%2010-2025-orange?logo=owasp&logoColor=white" alt="OWASP Top 10" />
  <img src="https://img.shields.io/badge/Security-Penetration%20Testing-critical" alt="Penetration Testing" />
</p>

---

## 📌 Project Overview

This project is a **Python-based automated Web Application Vulnerability Scanner** developed during an internship at **ELEVATS LAB**.

The tool focuses on detecting prevalent web security issues aligned with the **OWASP Top 10 (2025)**, with special emphasis on:

- **A03:2025 Injection** (SQL Injection, XSS)
- **A01:2025 Broken Access Control** (CSRF, missing tokens)
- Basic **Security Misconfigurations** (A02:2025)

Key features include:
- Dynamic crawling & form/input discovery
- Intelligent payload injection
- Response analysis & pattern-based detection
- Severity classification
- Structured logging
- JSON/HTML report generation
- User-friendly Flask web dashboard

The scanner was designed and tested in **controlled lab environments only**.

---

## 🎯 Objectives

- Build a modular, extensible vulnerability scanning engine
- Automate reconnaissance, payload testing, and detection
- Implement reliable pattern-based vulnerability identification
- Assign realistic severity levels based on impact
- Generate clear, actionable reports
- Provide an intuitive web interface for scan control and results viewing

---

## 🧠 Methodology

1. **Reconnaissance** — Crawling & input parameter discovery  
2. **Payload Injection** — Targeted test payloads for each vulnerability class  
3. **Response Analysis** — Monitoring for error messages, reflected payloads, behavioral changes  
4. **Detection** — Regex + keyword pattern matching  
5. **Severity Assignment** — Based on potential impact & exploitability  
6. **Reporting** — Structured JSON + readable HTML output  
7. **OWASP Classification** — Mapping findings to current OWASP Top 10 categories

**Test environments (authorized only):**
- DVWA (Damn Vulnerable Web Application)
- Custom localhost applications with intentional vulnerabilities

---

## 🧰 Technology Stack

| Component              | Technology                  |
|------------------------|-----------------------------|
| Language               | Python 3.x                  |
| HTTP Client            | requests                    |
| HTML/XML Parsing       | BeautifulSoup4              |
| Web Interface          | Flask                       |
| Pattern Matching       | re (Regular Expressions)    |
| Logging                | Python logging module       |
| Report Formats         | JSON, HTML                  |
| Security Framework     | OWASP Top 10 (2025)         |

---

## 🔗 Related Resources

- DVWA Lab Setup Guide → [GitHub – DVWA Installation Processes](https://github.com/NATTOMR/DVWA-Installation-Processes/blob/main/README.md)

---

## 🏗 Project Structure

```text
web-vulnerability-scanner/
├── app.py                  # Flask application entry point
├── scanner/
│   ├── crawler.py          # Web crawler & link/form extractor
│   ├── injector.py         # Payload delivery logic
│   ├── detector.py         # Vulnerability detection engine
│   ├── payloads.py         # Payload lists (SQLi, XSS, etc.)
│   ├── reporter.py         # Report generation module
│   └── utils.py            # Helper functions
├── templates/
│   ├── index.html          # Dashboard / scan initiation
│   ├── results.html        # Live / completed scan overview
│   └── report.html         # Detailed vulnerability report
├── static/
│   └── style.css           # Custom styling
├── reports/
│   └── scan_results.json   # Latest JSON report (example)
├── logs/
│   └── scanner.log         # Scan activity logs
├── requirements.txt
└── README.md
```



# 🔬 Vulnerability Detection Capabilities



## 1️⃣ SQL Injection (A03: Injection)



Detection via:

- Database error pattern matching

- Logical condition bypass

- Union-based injection attempts



Example Payload:

sql



`' OR '1'='1`



## 2️⃣ Cross-Site Scripting (A03: Injection)



- Detection via:



- Reflected payload presence



- Script tag injection



- Unescaped output detection



- Example Payload:



 ` <script>alert(1)</script>`

  

## 3️⃣ CSRF (A01: Broken Access Control)



 - Detection via:

 - Missing CSRF token fields

 - Absence of hidden security inputs



## 📊 Severity Classification Model

Vulnerability Severity

- SQL Injection 🔴 Critical

- XSS 🟠 High

- CSRF 🟡 Medium



## 📸 Screenshots

🔹 Scanner Dashboard


![image](https://github.com/NATTOMR/Web-Application-Vulnerability-Scanner/blob/main/images/scanner%20dashboard.png)

🔹 SQL Injection Detection
![image](https://github.com/NATTOMR/Web-Application-Vulnerability-Scanner/blob/main/images/SQL%20dashboard.png)

🔹 XSS Detection
![image](https://github.com/NATTOMR/Web-Application-Vulnerability-Scanner/blob/main/images/XSS%20dashboard.png)

## 🧪 Testing Environment



## Tested Against:



- DVWA (Damn Vulnerable Web Application)



- Controlled lab environments



- Localhost deployments



## ⚠ Authorized testing environments only.



## 📈 Sample Output (JSON)

```[

  {

    "url": "http://target/login.php",

    "parameter": "username",

    "payload": "' OR '1'='1",

    "evidence": "SQL syntax error near...",

    "severity": "Critical"

  }

]

```



## 📚 OWASP Mapping

- Vulnerability OWASP Category

- SQLi A03: Injection

- XSS A03: Injection

- CSRF A01: Broken Access Control



## 🔮 Future Enhancements (Research Scope)



- Multi-threaded scanning



- Authentication session handling



- CVSS scoring integration



- Automated PDF reporting



- Header & cookie analysis



- CI/CD pipeline integration



- Machine learning–based anomaly detection



## 🧠 Research Contributions



- This project demonstrates:



- Practical implementation of vulnerability scanning logic



- Secure software design principles



- Modular architecture for extensibility



- Applied OWASP security methodology



Research-driven penetration testing workflow



## 🔐 Ethical Statement



- This tool is strictly developed for:



- Academic research



- Internship training



- Authorized penetration testing



- Controlled lab environments



- Unauthorized usage is illegal and unethical.



## 🏁 Conclusion

This project reflects professional-level implementation of automated web security testing aligned with industry standards. It bridges academic research and real-world cybersecurity practice.

## Connect with Me 🔗

<p align="left">
  <a href="https://www.linkedin.com/in/natto-muni-chakma-4b19b4259/">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/>
  </a>
  <a href="https://github.com/NATTOMR">
    <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/>
  </a>
</p>

Intern @ **ELEVATS LAB**  

