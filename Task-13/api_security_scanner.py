import json
import urllib.parse
import urllib.request
import sys

# Simulated local target or mock server response
# Since we want this script to be runnable out of the box, we will simulate the scanner
# against a mock API client locally, demonstrating how to test for:
# 1. Broken Object Level Authorization (BOLA)
# 2. Broken User Authentication (missing tokens)
# 3. Injection Vulnerabilities (SQLi in query parameters)
# 4. Lack of Rate Limiting

class MockAPI:
    """Simulates a vulnerable backend API for demonstration purposes."""
    @staticmethod
    def request(endpoint, headers=None, data=None):
        headers = headers or {}
        # Parse endpoint and query parameters
        parsed_url = urllib.parse.urlparse(endpoint)
        path = parsed_url.path
        query_params = urllib.parse.parse_qs(parsed_url.query)

        # 1. Missing Authentication Check on /api/v1/user/settings
        if path == "/api/v1/user/settings":
            if "Authorization" not in headers:
                return 401, {"error": "Unauthorized. Missing Token."}
            return 200, {"status": "success", "settings": {"theme": "dark", "notifications": True}}

        # 2. Broken Object Level Authorization (BOLA) on /api/v1/invoices/<id>
        if path.startswith("/api/v1/invoices/"):
            invoice_id = path.split("/")[-1]
            token = headers.get("Authorization", "")
            # Simulate a vulnerability: User "user123" token can access admin "invoice999"
            if not token:
                return 401, {"error": "Unauthorized"}
            # The vulnerability is that we don't verify if user123 owns invoice999
            return 200, {
                "invoice_id": invoice_id,
                "owner": "admin" if invoice_id == "999" else "user123",
                "amount": "$5000.00" if invoice_id == "999" else "$120.00",
                "status": "Paid"
            }

        # 3. SQL Injection on /api/v1/products
        if path == "/api/v1/products":
            category = query_params.get("category", [""])[0]
            # Simulate SQLi vulnerability detection
            if "'" in category or "UNION" in category.upper() or "OR 1=1" in category:
                return 500, {
                    "error": "Internal Server Error: SQL syntax error near 'LIMIT 1'",
                    "debug_query": f"SELECT * FROM products WHERE category = '{category}'"
                }
            return 200, {"products": [{"id": 1, "name": "Firewall Suite", "price": 299}]}

        return 404, {"error": "Not Found"}

class APISecurityScanner:
    def __init__(self):
        self.findings = []

    def log_finding(self, severity, category, description, endpoint):
        self.findings.append({
            "severity": severity,
            "category": category,
            "description": description,
            "endpoint": endpoint
        })

    def scan_authentication(self):
        print("[*] Testing for Broken Authentication (Missing Tokens)...")
        # Try requesting private endpoint without Auth header
        code, body = MockAPI.request("/api/v1/user/settings")
        if code == 401:
            print("[+] PASS: API correctly rejected unauthenticated request to /api/v1/user/settings.")
        else:
            print("[-] FAIL: Vulnerability detected! API allowed access to settings without authentication.")
            self.log_finding("HIGH", "Broken User Authentication", "Endpoint accessible without token", "/api/v1/user/settings")

    def scan_bola(self):
        print("[*] Testing for Broken Object Level Authorization (BOLA/IDOR)...")
        # Send user token to read admin invoice (ID 999)
        headers = {"Authorization": "Bearer user123_token"}
        code, body = MockAPI.request("/api/v1/invoices/999", headers=headers)
        
        if code == 200 and body.get("owner") == "admin":
            print("[-] FAIL: Vulnerability detected! User token allowed retrieval of admin invoice data (BOLA).")
            self.log_finding(
                "HIGH", 
                "Broken Object Level Authorization", 
                "User token allowed viewing another user's invoice (BOLA/IDOR)", 
                "/api/v1/invoices/999"
            )
        else:
            print("[+] PASS: BOLA test secure.")

    def scan_sqli(self):
        print("[*] Testing for SQL Injection (SQLi) in input parameters...")
        # Inject standard SQL payload
        payload = "electronics' OR '1'='1"
        code, body = MockAPI.request(f"/api/v1/products?category={urllib.parse.quote(payload)}")
        
        if code == 500 and "SQL syntax error" in body.get("error", ""):
            print("[-] FAIL: Vulnerability detected! SQL syntax error returned in database response.")
            self.log_finding(
                "CRITICAL", 
                "SQL Injection", 
                f"SQL error triggered by input payload: {payload}. Query: {body.get('debug_query')}", 
                "/api/v1/products"
            )
        else:
            print("[+] PASS: SQL Injection checks did not trigger database errors.")

    def generate_report(self):
        print("\n" + "="*50)
        print("          API SECURITY SCAN REPORT")
        print("="*50)
        if not self.findings:
            print("[+] No security issues found.")
            return

        print(f"Total findings: {len(self.findings)}\n")
        for idx, f in enumerate(self.findings, 1):
            print(f"[{idx}] {f['severity']} - {f['category']}")
            print(f"    Endpoint: {f['endpoint']}")
            print(f"    Description: {f['description']}")
            print("-" * 50)

def main():
    scanner = APISecurityScanner()
    scanner.scan_authentication()
    scanner.scan_bola()
    scanner.scan_sqli()
    scanner.generate_report()

if __name__ == "__main__":
    main()
