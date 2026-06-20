# Task 13: Secure API Testing, Authorization, and Validation

## Objective
To identify, test, and document security vulnerabilities within Web APIs, focusing on authentication mechanisms, object-level authorization control (BOLA/IDOR), and input validation.

---

## Key Security Concepts Analyzed

### 1. Broken Object Level Authorization (BOLA / IDOR)
* **What it is:** BOLA occurs when an application exposes a resource identifier (such as `/api/v1/invoices/999`) in the API and fails to validate whether the requester owns or is authorized to view that resource.
* **Impact:** Unauthorized data exposure, data tampering, account takeover.
* **Mitigation:** Implement strict access control lists (ACLs) that check if the authenticated user has rights to the specific object ID requested, rather than relying on the client-supplied ID alone.

### 2. Broken User Authentication
* **What it is:** APIs often expose login and token validation endpoints. If authorization headers are optional or poorly validated, unauthorized clients can access restricted data.
* **Impact:** Complete system access, impersonation of other users.
* **Mitigation:** Enforce token authentication (JWT, OAuth2) on all private endpoints, validate tokens server-side, and reject anonymous requests.

### 3. Input Validation & Injection
* **What it is:** API inputs (query strings, JSON body variables) that are not sanitized before being executed in database queries can lead to SQL Injection (SQLi), Cross-Site Scripting (XSS), or Command Injection.
* **Impact:** Sensitive database leakage, administrative access bypass.
* **Mitigation:** Use parameterized queries (Prepared Statements), perform input schema validation, and sanitize inputs.

---

## API Testing Methodology

This task includes a custom security scanner script (`api_security_scanner.py`) designed to test three simulated endpoints:
1. `/api/v1/user/settings` (Tests for authentication token checks)
2. `/api/v1/invoices/<id>` (Tests for BOLA by trying to access another user's invoice)
3. `/api/v1/products?category=<input>` (Tests for SQL Injection vulnerability)

### How to Run the Scanner
Run the scanner script locally using Python:
```bash
python api_security_scanner.py
```

### Mock API Testing Results
```text
[*] Testing for Broken Authentication (Missing Tokens)...
[-] FAIL: Vulnerability detected! API allowed access to settings without authentication.

[*] Testing for Broken Object Level Authorization (BOLA/IDOR)...
[-] FAIL: Vulnerability detected! User token allowed retrieval of admin invoice data (BOLA).

[*] Testing for SQL Injection (SQLi) in input parameters...
[-] FAIL: Vulnerability detected! SQL syntax error returned in database response.

==================================================
          API SECURITY SCAN REPORT
==================================================
Total findings: 3

[1] HIGH - Broken User Authentication
    Endpoint: /api/v1/user/settings
    Description: Endpoint accessible without token
--------------------------------------------------
[2] HIGH - Broken Object Level Authorization
    Endpoint: /api/v1/invoices/999
    Description: User token allowed viewing another user's invoice (BOLA/IDOR)
--------------------------------------------------
[3] CRITICAL - SQL Injection
    Endpoint: /api/v1/products
    Description: SQL error triggered by input payload: electronics' OR '1'='1. Query: SELECT * FROM products WHERE category = 'electronics' OR '1'='1'
--------------------------------------------------
```

---

## Remediation Recommendations

1. **Authentication:** Implement standard JWT validation filters. Reject any request to `/api/v1/user/settings` that does not contain a valid `Authorization: Bearer <token>` header.
2. **Access Control:** Map user identities to resources. When a request for `/api/v1/invoices/<id>` is received, fetch the owner from the database and verify that it matches the user ID encoded in the Bearer token.
3. **Prepared Statements:** Avoid direct string concatenation in queries. Change query logic to use prepared statements:
   ```python
   # Secure implementation using parameterized query:
   cursor.execute("SELECT * FROM products WHERE category = %s", (category_param,))
   ```
