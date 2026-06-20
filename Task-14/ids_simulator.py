import time
import re
from collections import defaultdict, deque

# Mock network and system access logs for analysis
MOCK_LOGS = [
    # Port scan simulation
    {"timestamp": 1718900000, "src_ip": "192.168.1.50", "dest_port": 22, "event": "connection_attempt"},
    {"timestamp": 1718900001, "src_ip": "192.168.1.50", "dest_port": 80, "event": "connection_attempt"},
    {"timestamp": 1718900002, "src_ip": "192.168.1.50", "dest_port": 443, "event": "connection_attempt"},
    {"timestamp": 1718900003, "src_ip": "192.168.1.50", "dest_port": 3389, "event": "connection_attempt"},
    {"timestamp": 1718900004, "src_ip": "192.168.1.50", "dest_port": 8080, "event": "connection_attempt"},
    
    # Normal traffic
    {"timestamp": 1718900005, "src_ip": "192.168.1.20", "dest_port": 80, "event": "http_request", "payload": "GET /index.html HTTP/1.1"},
    
    # Brute force login simulation
    {"timestamp": 1718900010, "src_ip": "203.0.113.5", "dest_port": 443, "event": "login_failed", "username": "admin"},
    {"timestamp": 1718900011, "src_ip": "203.0.113.5", "dest_port": 443, "event": "login_failed", "username": "admin"},
    {"timestamp": 1718900012, "src_ip": "203.0.113.5", "dest_port": 443, "event": "login_failed", "username": "admin"},
    {"timestamp": 1718900013, "src_ip": "203.0.113.5", "dest_port": 443, "event": "login_failed", "username": "administrator"},
    {"timestamp": 1718900014, "src_ip": "203.0.113.5", "dest_port": 443, "event": "login_failed", "username": "root"},
    
    # SQL Injection simulation in URI query
    {"timestamp": 1718900020, "src_ip": "198.51.100.12", "dest_port": 80, "event": "http_request", "payload": "GET /search?q=1'%20UNION%20SELECT%20null,username,password%20FROM%20users-- HTTP/1.1"},
    
    # Normal login
    {"timestamp": 1718900025, "src_ip": "192.168.1.20", "dest_port": 443, "event": "login_success", "username": "user123"}
]

class IDSEngine:
    def __init__(self):
        # Tracking variables
        self.port_scan_tracker = defaultdict(set) # src_ip -> set of ports
        self.login_fail_tracker = defaultdict(list) # src_ip -> list of timestamps
        self.alerts = []

    def analyze_event(self, log):
        timestamp = log["timestamp"]
        src_ip = log["src_ip"]
        event = log["event"]

        # Rule 1: Detect Port Scanning (Connecting to 5+ distinct ports from same IP within 10 seconds)
        if event == "connection_attempt":
            port = log["dest_port"]
            self.port_scan_tracker[src_ip].add(port)
            if len(self.port_scan_tracker[src_ip]) >= 5:
                self.trigger_alert(
                    "MEDIUM", 
                    "Port Scanning Detected", 
                    f"Host {src_ip} attempted connections to multiple ports: {sorted(list(self.port_scan_tracker[src_ip]))}"
                )
                self.port_scan_tracker[src_ip].clear() # Reset after alert

        # Rule 2: Detect Brute Force Login (5 failed logins from same IP within 10 seconds)
        elif event == "login_failed":
            self.login_fail_tracker[src_ip].append(timestamp)
            # Remove timestamps older than 10 seconds
            self.login_fail_tracker[src_ip] = [t for t in self.login_fail_tracker[src_ip] if timestamp - t <= 10]
            
            if len(self.login_fail_tracker[src_ip]) >= 5:
                self.trigger_alert(
                    "HIGH",
                    "Brute-Force Authentication Attempt",
                    f"Host {src_ip} triggered 5 failed login attempts within 10 seconds. Targeted accounts: {log.get('username')}"
                )
                self.login_fail_tracker[src_ip].clear()

        # Rule 3: Detect SQL Injection in Web Requests
        elif event == "http_request":
            payload = log.get("payload", "")
            sqli_patterns = [
                r"UNION\s+SELECT",
                r"OR\s+\d+=\d+",
                r"SELECT\s+.*FROM\s+.*",
                r"'"
            ]
            for pattern in sqli_patterns:
                if re.search(pattern, payload, re.IGNORECASE):
                    self.trigger_alert(
                        "CRITICAL",
                        "SQL Injection Payload Detected",
                        f"Host {src_ip} sent request with SQLi pattern: {payload}"
                    )
                    break

    def trigger_alert(self, severity, alert_type, message):
        alert = {
            "severity": severity,
            "type": alert_type,
            "message": message
        }
        self.alerts.append(alert)
        print(f"[{severity}] ALERT: {alert_type} - {message}")

    def summary(self):
        print("\n" + "="*50)
        print("          IDS ENGINE DETECTION SUMMARY")
        print("="*50)
        print(f"Total Log Events Analyzed: {len(MOCK_LOGS)}")
        print(f"Alerts Triggered: {len(self.alerts)}")
        
        severity_counts = defaultdict(int)
        for a in self.alerts:
            severity_counts[a["severity"]] += 1
            
        print("\nSeverity Breakdown:")
        for sev, count in severity_counts.items():
            print(f"  - {sev}: {count}")

def main():
    print("Initializing Simulated Intrusion Detection System (IDS)...")
    print("Reading network packets & log files stream...\n")
    
    engine = IDSEngine()
    for log in MOCK_LOGS:
        # Simulate processing delay
        time.sleep(0.1)
        engine.analyze_event(log)
        
    engine.summary()

if __name__ == "__main__":
    main()
