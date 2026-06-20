import socket
import ssl
import urllib.request
import urllib.error
from datetime import datetime
import json
import sys

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    443: "HTTPS",
    3389: "RDP",
    8080: "HTTP-Proxy"
}

SECURITY_HEADERS = [
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Strict-Transport-Security",
    "Referrer-Policy"
]

class AttackSurfaceAnalyzer:
    def __init__(self, target_host):
        self.target_host = target_host
        self.ip_address = None
        self.open_ports = []
        self.header_findings = {}
        self.ssl_info = {}

    def resolve_host(self):
        print(f"[*] Resolving host: {self.target_host}...")
        try:
            self.ip_address = socket.gethostbyname(self.target_host)
            print(f"[+] Target IP resolved: {self.ip_address}")
            return True
        except socket.gaierror:
            print(f"[-] Error: Could not resolve host {self.target_host}")
            return False

    def scan_ports(self):
        print(f"\n[*] Scanning common ports on {self.ip_address}...")
        for port, service in COMMON_PORTS.items():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.0)
            result = s.connect_ex((self.ip_address, port))
            if result == 0:
                print(f"  [+] Port {port} ({service}) is OPEN")
                self.open_ports.append((port, service))
            s.close()

    def audit_http_headers(self):
        url = f"https://{self.target_host}"
        print(f"\n[*] Auditing HTTP Security Headers at {url}...")
        
        try:
            # Use urllib to fetch headers
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AttackSurfaceAnalyzer/1.0'}
            )
            response = urllib.request.urlopen(req, timeout=5.0)
            headers = response.info()
            
            for header in SECURITY_HEADERS:
                value = headers.get(header)
                if value:
                    self.header_findings[header] = {"status": "PRESENT", "value": value}
                else:
                    self.header_findings[header] = {"status": "MISSING", "value": None}
            
            # Check server banner
            server = headers.get("Server")
            if server:
                print(f"  [!] Server Banner Exposed: {server}")
                self.header_findings["Server-Banner"] = {"status": "EXPOSED", "value": server}
                
        except urllib.error.URLError as e:
            print(f"  [-] Failed to connect over HTTPS: {e}. Trying fallback to HTTP...")
            self.audit_http_headers_http_fallback()

    def audit_http_headers_http_fallback(self):
        url = f"http://{self.target_host}"
        try:
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AttackSurfaceAnalyzer/1.0'}
            )
            response = urllib.request.urlopen(req, timeout=5.0)
            headers = response.info()
            
            for header in SECURITY_HEADERS:
                value = headers.get(header)
                if value:
                    self.header_findings[header] = {"status": "PRESENT", "value": value}
                else:
                    self.header_findings[header] = {"status": "MISSING", "value": None}
            
            server = headers.get("Server")
            if server:
                self.header_findings["Server-Banner"] = {"status": "EXPOSED", "value": server}
        except Exception as e:
            print(f"  [-] Failed to connect over HTTP: {e}")

    def inspect_ssl(self):
        print(f"\n[*] Inspecting SSL/TLS Certificate for {self.target_host}...")
        context = ssl.create_default_context()
        try:
            with socket.create_connection((self.target_host, 443), timeout=5.0) as sock:
                with context.wrap_socket(sock, server_hostname=self.target_host) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Parse dates
                    not_after_str = cert.get('notAfter')
                    if not_after_str:
                        expiry_date = datetime.strptime(not_after_str, '%b %d %H:%M:%S %Y %Z')
                        self.ssl_info["expiry"] = expiry_date.strftime('%Y-%m-%d %H:%M:%S')
                        days_left = (expiry_date - datetime.utcnow()).days
                        self.ssl_info["days_left"] = days_left
                        print(f"  [+] Certificate expires in: {days_left} days ({self.ssl_info['expiry']})")
                        
                    self.ssl_info["subject"] = dict(x[0] for x in cert.get('subject', ()))
                    self.ssl_info["issuer"] = dict(x[0] for x in cert.get('issuer', ()))
                    
        except Exception as e:
            print(f"  [-] SSL Inspection failed: {e}")

    def generate_report(self):
        print("\n" + "="*60)
        print(f"        ATTACK SURFACE SUMMARY FOR: {self.target_host}")
        print("="*60)
        
        # Ports Score
        open_port_count = len(self.open_ports)
        print(f"[+] Open Ports Detected: {open_port_count}")
        for port, service in self.open_ports:
            print(f"    - Port {port} running {service}")
            
        # Headers Score
        missing_headers = [h for h, f in self.header_findings.items() if f["status"] == "MISSING"]
        print(f"\n[+] Missing Defensive Security Headers: {len(missing_headers)}/{len(SECURITY_HEADERS)}")
        for header in missing_headers:
            print(f"    - {header} is missing!")
            
        # Risk Evaluation
        risk_score = 0
        risk_score += len(self.open_ports) * 10
        risk_score += len(missing_headers) * 15
        if self.header_findings.get("Server-Banner", {}).get("status") == "EXPOSED":
            risk_score += 10
            
        if risk_score > 60:
            risk_level = "HIGH RISK"
        elif risk_score > 25:
            risk_level = "MEDIUM RISK"
        else:
            risk_level = "LOW RISK"
            
        print("\n" + "-"*60)
        print(f"Calculated Attack Surface Rating: {risk_level} (Score: {risk_score})")
        print("-"*60)
        
        # Basic defensive suggestions
        print("\nDefensive Remediation Suggestions:")
        if open_port_count > 0:
            print("  1. Close unnecessary ports at the firewall layer (e.g. limit SSH to internal VPN only).")
        if missing_headers:
            print("  2. Inject missing security headers (CSP, HSTS, X-Frame-Options) in Web Server configurations (Nginx/Apache).")
        if self.header_findings.get("Server-Banner", {}).get("status") == "EXPOSED":
            print("  3. Disable server signature tokens to prevent version enumeration (e.g. Nginx 'server_tokens off;').")
        print("="*60)

def main():
    # Allow target selection via arguments or default
    target = "example.com"
    if len(sys.argv) > 1:
        target = sys.argv[1]
        
    print(f"Starting Attack Surface Scan on: {target}\n")
    analyzer = AttackSurfaceAnalyzer(target)
    if analyzer.resolve_host():
        analyzer.scan_ports()
        analyzer.audit_http_headers()
        analyzer.inspect_ssl()
        analyzer.generate_report()

if __name__ == "__main__":
    main()
