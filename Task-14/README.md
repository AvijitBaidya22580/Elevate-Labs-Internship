# Task 14: Network Intrusion Detection & Threat Monitoring

## Objective
To understand network threat behaviors, configure rules for identifying malicious traffic pattern indicators, and simulate an Intrusion Detection System (IDS) that processes network logs to raise security alerts.

---

## Intrusion Detection System (IDS) Concepts

### 1. Types of IDS
* **Signature-Based (Pattern Matching):** Compares network traffic packets or log events against known patterns of malicious activities (e.g., standard SQL injection keywords like `UNION SELECT`).
* **Anomaly-Based (Behavioral):** Builds a baseline model of normal network traffic and raises alarms when activities deviate significantly from the baseline (e.g., high traffic volumes or rare protocol usage).

### 2. Common Network Threats Monitored
* **Port Scanning:** Reconnaissance activity where an attacker probes target IP addresses to see what services and port numbers are active and listening.
* **Brute-Force Attack:** An attacker systematically submits multiple passwords or passphrases to gain unauthorized access to accounts.
* **Injection Exploitations:** Web-application attacks attempting to run illegal SQL or operating system commands through incoming request payloads.

---

## Implementation Details

A custom Python script `ids_simulator.py` was implemented to monitor network request logs and trigger alerts based on signature-based and behavioral security rules.

### Defined Detection Rules

| Rule Name | Severity | Condition |
| --- | --- | --- |
| **Port Scanning Detection** | `MEDIUM` | Connection attempts to $\ge 5$ distinct ports from the same IP address in $\le 10$ seconds. |
| **Brute-Force Detection** | `HIGH` | $\ge 5$ failed authentication login events from the same source IP in $\le 10$ seconds. |
| **SQL Injection Detection** | `CRITICAL` | Text pattern matching of SQL database characters (`UNION SELECT`, `' OR '`, etc.) inside HTTP query string payloads. |

### Running the Simulator
You can execute the log analyzer using:
```bash
python ids_simulator.py
```

### Analysis & Simulation Output
```text
Initializing Simulated Intrusion Detection System (IDS)...
Reading network packets & log files stream...

[MEDIUM] ALERT: Port Scanning Detected - Host 192.168.1.50 attempted connections to multiple ports: [22, 80, 443, 3389, 8080]
[HIGH] ALERT: Brute-Force Authentication Attempt - Host 203.0.113.5 triggered 5 failed login attempts within 10 seconds. Targeted accounts: root
[CRITICAL] ALERT: SQL Injection Payload Detected - Host 198.51.100.12 sent request with SQLi pattern: GET /search?q=1'%20UNION%20SELECT%20null,username,password%20FROM%20users-- HTTP/1.1

==================================================
          IDS ENGINE DETECTION SUMMARY
==================================================
Total Log Events Analyzed: 14
Alerts Triggered: 3

Severity Breakdown:
  - MEDIUM: 1
  - HIGH: 1
  - CRITICAL: 1
```

---

## Defensive Strategies & Recommendations

1. **Implement IP Rate Limiting:** Apply firewalls or reverse proxy configuration to drop requests from IPs showing high frequency connection attempts (mitigating port scans and brute-force).
2. **Deploy Snort/Suricata rules:** Transition signature matching to enterprise-grade tools.
3. **Automate Account Lockouts:** Temporarily lock accounts after consecutive unsuccessful login attempts to prevent brute-force exploitation.
