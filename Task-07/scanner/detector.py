import re
from bs4 import BeautifulSoup

# Database error regex lists for SQL Injection detection
SQL_ERROR_PATTERNS = {
    "MySQL": [
        r"you have an error in your sql syntax",
        r"warning: mysql_",
        r"mysql_fetch_array",
        r"mysql_num_rows",
        r"mysql_query",
        r"mysql_error\(\)",
        r"MySqlException"
    ],
    "PostgreSQL": [
        r"PostgreSQL.*ERROR",
        r"warning: pg_",
        r"pg_query\(\)",
        r"invalid input syntax for integer",
        r"pg_exec\(\)"
    ],
    "SQLite": [
        r"warning: sqlite_",
        r"sqlite_compile\(\)",
        r"SQLite/JDBC Driver",
        r"SQLite.Exception",
        r"System.Data.SQLite.SQLiteException"
    ],
    "Microsoft SQL Server": [
        r"driver.*sql server",
        r"ole db provider.*sql server",
        r"unclosed quotation mark after the character string",
        r"Microsoft OLE DB Provider for SQL Server"
    ],
    "Oracle": [
        r"ORA-[0-9]{5}",
        r"oracle error",
        r"Oracle Exception",
        r"Oracle class library"
    ]
}

def check_sqli(response_text):
    """
    Checks the HTTP response body for database error messages.
    Returns (is_vulnerable, db_type, evidence) if found, else (False, None, None).
    """
    if not response_text:
        return False, None, None
        
    for db_type, patterns in SQL_ERROR_PATTERNS.items():
        for pattern in patterns:
            # Case insensitive search
            match = re.search(pattern, response_text, re.IGNORECASE)
            if match:
                return True, db_type, match.group(0)
                
    return False, None, None

def check_xss(payload, response_text):
    """
    Checks if the exact payload is reflected unescaped in the response HTML.
    Returns (is_vulnerable, evidence) if vulnerable.
    """
    if not response_text or not payload:
        return False, None

    # Check if the payload is present in the response
    if payload in response_text:
        # To avoid simple string match false positives, we check if the reflected payload 
        # is actually active HTML (not encoded, e.g. &lt;script&gt;)
        # We can search for the unescaped characters like '<script' or '<svg'
        # A simple check: if the characters '<' and '>' of our tag are not escaped in the reflected part
        # If payload contains HTML-like elements:
        if '<' in payload and '>' in payload:
            # Verify it's not HTML entity encoded
            encoded_lt = "&lt;"
            encoded_gt = "&gt;"
            # If the index of the payload is in the text, we check nearby context
            # A strict substring search for the payload is standard for basic XSS detection
            return True, f"Payload reflected unescaped: {payload}"
            
    return False, None

def check_csrf(form):
    """
    Checks if a POST form is missing a CSRF protection token.
    Returns (is_vulnerable, evidence) if missing.
    """
    method = form.get('method', 'get').lower()
    if method != 'post':
        return False, None

    inputs = form.get('inputs', [])
    
    # Common CSRF token input names
    csrf_patterns = [
        r'csrf', r'token', r'xsrf', r'authenticity_token', 
        r'__RequestVerificationToken', r'secure'
    ]
    
    has_csrf_token = False
    
    for inp in inputs:
        name = inp.get('name', '').lower()
        inp_type = inp.get('type', '').lower()
        
        # Typically CSRF tokens are hidden fields
        if inp_type == 'hidden' or inp_type == 'text':
            for pattern in csrf_patterns:
                if re.search(pattern, name):
                    has_csrf_token = True
                    break
            if has_csrf_token:
                break
                
    if not has_csrf_token:
        evidence = f"Form at {form['url']} (POST) does not contain a CSRF token field."
        return True, evidence
        
    return False, None

def check_security_headers(headers):
    """
    Checks response headers for missing security-related headers or info disclosures.
    Returns a list of findings.
    """
    findings = []
    
    # Headers to check for presence
    security_headers = {
        'X-Frame-Options': {
            'description': 'Protects against clickjacking attacks.',
            'owasp': 'A05:2025-Security Misconfiguration',
            'severity': 'Low'
        },
        'X-Content-Type-Options': {
            'description': 'Prevents the browser from MIME-sniffing a response away from the declared content-type.',
            'owasp': 'A05:2025-Security Misconfiguration',
            'severity': 'Low'
        },
        'Content-Security-Policy': {
            'description': 'Restricts resources (such as JavaScript, CSS, Images) that the browser is allowed to load.',
            'owasp': 'A05:2025-Security Misconfiguration',
            'severity': 'Low'
        },
        'Strict-Transport-Security': {
            'description': 'Enforces HTTPS connections to the server.',
            'owasp': 'A05:2025-Security Misconfiguration',
            'severity': 'Low'
        }
    }
    
    for header, info in security_headers.items():
        if header not in headers and header.lower() not in [h.lower() for h in headers.keys()]:
            findings.append({
                'vuln_type': f'Missing {header} Header',
                'severity': info['severity'],
                'evidence': f"Header '{header}' is missing in HTTP response.",
                'description': info['description'],
                'owasp_category': info['owasp']
            })
            
    # Server signature disclosure check
    server_header = headers.get('Server') or headers.get('server')
    if server_header:
        # Check if the header contains version numbers (e.g. Apache/2.4.41, nginx/1.18.0)
        if re.search(r'\d', server_header):
            findings.append({
                'vuln_type': 'Server Information Leakage',
                'severity': 'Info',
                'evidence': f"Server header: {server_header}",
                'description': 'Exposes web server version details, which helps attackers find version-specific exploits.',
                'owasp_category': 'A05:2025-Security Misconfiguration'
            })
            
    x_powered_by = headers.get('X-Powered-By') or headers.get('x-powered-by')
    if x_powered_by:
        findings.append({
            'vuln_type': 'Technology Stack Disclosure',
            'severity': 'Info',
            'evidence': f"X-Powered-By header: {x_powered_by}",
            'description': 'Exposes server-side technologies used (e.g., PHP, ASP.NET, Express).',
            'owasp_category': 'A05:2025-Security Misconfiguration'
        })
        
    return findings
