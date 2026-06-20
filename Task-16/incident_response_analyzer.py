import time
from collections import defaultdict

# Mock timeline of a simulated security breach
LOG_EVENTS = [
    {"timestamp": "2026-06-20T10:00:00", "source": "WebServer-WAF", "severity": "HIGH", "message": "SQL Injection attempt detected and blocked from IP 198.51.100.44"},
    {"timestamp": "2026-06-20T10:05:00", "source": "WebServer-WAF", "severity": "MEDIUM", "message": "File upload attempted: cmd.jsp uploaded by guest user to /uploads/"},
    {"timestamp": "2026-06-20T10:06:00", "source": "WebServer-Runtime", "severity": "CRITICAL", "message": "Process execution: 'whoami' run by user tomcat"},
    {"timestamp": "2026-06-20T10:10:00", "source": "WebServer-OS", "severity": "HIGH", "message": "Outbound TCP connection established to 198.51.100.44 on port 4444 (Reverse Shell)"},
    {"timestamp": "2026-06-20T10:20:00", "source": "Internal-Firewall", "severity": "MEDIUM", "message": "Successful SSH connection from WebServer (192.168.1.10) to DB-Server (192.168.2.50) using credential 'db_backup_admin'"},
    {"timestamp": "2026-06-20T10:25:00", "source": "DB-Server-Database", "severity": "HIGH", "message": "Query Executed: 'SELECT * FROM credit_cards'"},
    {"timestamp": "2026-06-20T10:30:00", "source": "External-Firewall", "severity": "CRITICAL", "message": "Data Exfiltration Alert: 4.8 GB of outbound data transferred to 198.51.100.44 from DB-Server (192.168.2.50) over port 443"},
]

class IncidentResponseAnalyzer:
    def __init__(self, events):
        self.events = events
        self.timeline = []
        self.compromised_hosts = set()
        self.adversary_ips = set()
        self.exfiltrated_data = "0 MB"

    def analyze(self):
        print("[*] Performing Forensic Log Analysis...")
        for event in self.events:
            msg = event["message"]
            source = event["source"]
            timestamp = event["timestamp"]

            # Identify initial compromise
            if "uploaded" in msg or "whoami" in msg:
                self.compromised_hosts.add(source.split("-")[0])
                self.timeline.append((timestamp, "INITIAL COMPROMISE", f"Adversary uploaded/executed shell on {source}"))
                
            # Identify Command & Control (C2) / Reverse Shell
            elif "Reverse Shell" in msg:
                # Extract malicious IP
                ip = msg.split("to ")[1].split(" on")[0]
                self.adversary_ips.add(ip)
                self.timeline.append((timestamp, "COMMAND & CONTROL", f"Reverse shell established to attacker IP {ip}"))
                
            # Identify Lateral Movement
            elif "SSH connection" in msg:
                self.compromised_hosts.add("DB-Server")
                self.timeline.append((timestamp, "LATERAL MOVEMENT", "Adversary moved laterally from WebServer to DB-Server via SSH using stolen credentials"))
                
            # Identify Data Exfiltration
            elif "Exfiltration" in msg:
                self.exfiltrated_data = msg.split("Alert: ")[1].split(" of")[0]
                self.timeline.append((timestamp, "DATA EXFILTRATION", f"Data exfiltrated to attacker server. Volume: {self.exfiltrated_data}"))

    def print_incident_report(self):
        print("\n" + "=" * 80)
        print("                 INCIDENT RESPONSE FORENSIC REPORT")
        print("=" * 80)
        
        print("\nCOMPROMISED INTERNAL ASSETS:")
        for host in self.compromised_hosts:
            print(f"  - [Compromised] {host}")

        print("\nIDENTIFIED ATTACKER IP ADDRESSES:")
        for ip in self.adversary_ips:
            print(f"  - [Attacker C2] {ip}")

        print(f"\nESTIMATED DATA EXFILTRATED: {self.exfiltrated_data}")

        print("\nATTACK TIMELINE OF EVENTS:")
        print(f"{'Timestamp':<20} | {'Phase':<20} | {'Details'}")
        print("-" * 80)
        for ts, phase, details in self.timeline:
            print(f"{ts:<20} | {phase:<20} | {details}")

        print("\nCONTAINMENT & REMEDIATION RECOMMENDATIONS:")
        print("  1. ISOLATE WebServer (192.168.1.10) and DB-Server (192.168.2.50) from the network immediately.")
        print("  2. TERMINATE active outbound TCP connections to attacker IP 198.51.100.44.")
        print("  3. REVOKE 'db_backup_admin' database credentials and rotation credentials across all services.")
        print("  4. PURGE uploaded file 'cmd.jsp' and patch file-upload parameters on the web app.")
        print("=" * 80)

def main():
    analyzer = IncidentResponseAnalyzer(LOG_EVENTS)
    analyzer.analyze()
    analyzer.print_incident_report()

if __name__ == "__main__":
    main()
