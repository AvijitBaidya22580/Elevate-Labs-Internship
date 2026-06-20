# Task 15: Vulnerability Assessment & Risk Prioritization

## Objective
To perform a vulnerability assessment scan, analyze the severity of security vulnerabilities, and implement a risk-prioritization matrix that incorporates threat intel (exploit availability) and asset value.

---

## Vulnerability Assessment & Scoring Systems

### 1. Common Vulnerability Scoring System (CVSS)
CVSS is an open framework for communicating the characteristics and severity of software vulnerabilities. The base score ranges from $0.0$ to $10.0$:
* **Low:** $0.1 - 3.9$
* **Medium:** $4.0 - 6.9$
* **High:** $7.0 - 8.9$
* **Critical:** $9.0 - 10.0$

### 2. The Risk Formula
Relying solely on CVSS base scores leads to inefficient patching cycles. Real-world risk is calculated using:
$$\text{Risk Score} = \text{CVSS Base Score} \times \text{Asset Criticality Modifier} \times \text{Exploit Threat Modifier}$$

* **Asset Criticality:** Public web servers or payroll databases are high criticality, while development laptops or print servers are low.
* **Exploit Threat:** If an active public exploit exists (e.g., in Metasploit), the likelihood of exploitation is much higher.

---

## Implementation Details

A Python prioritization tool `vulnerability_prioritizer.py` was developed to analyze vulnerabilities, apply asset/threat weights, and generate a prioritized remediation list.

### Running the Prioritizer
Run the script to analyze the sample vulnerabilities:
```bash
python vulnerability_prioritizer.py
```

### Analysis Output & Risk Prioritization Matrix
```text
================================================================================
                 VULNERABILITY RISK PRIORITIZATION REPORT
================================================================================
CVE-ID          | Asset Name                   | CVSS  | Risk Score | Priority    
--------------------------------------------------------------------------------
CVE-2021-44228  | Web Application Server (Pub) | 10.0  | 45.0       | P0 (CRITICAL)
CVE-2020-1472   | Customer Support Dashboard   | 10.0  | 30.0       | P0 (CRITICAL)
CVE-2023-38180  | Internal Payroll Database    | 7.5   | 22.5       | P1 (HIGH)   
CVE-2018-13379  | Development Staging VM       | 9.8   | 14.7       | P2 (MEDIUM) 
CVE-2021-34527  | Office Print Server          | 8.8   | 13.2       | P2 (MEDIUM) 
================================================================================

REMEDIATION TASK LIST:
[1] REMEDIATE IMMEDIATELY: Patch 'Log4j RCE (Remote Code Execution)' on 'Web Application Server (Public)' (Score: 45.0)
[2] REMEDIATE IMMEDIATELY: Patch 'Netlogon Elevation of Privilege (Zerologon)' on 'Customer Support Dashboard' (Score: 30.0)
[3] REMEDIATE IMMEDIATELY: Patch '.NET Denial of Service Vulnerability' on 'Internal Payroll Database' (Score: 22.5)
[4] Scheduled Maintenance: Address 'FortiGate SSL VPN Directory Traversal' on 'Development Staging VM' (Score: 14.7)
[5] Scheduled Maintenance: Address 'Windows Print Spooler RCE (PrintNightmare)' on 'Office Print Server' (Score: 13.2)
```

---

## Security Audit & Prioritization Findings

1. **Strategic Shift:** Although `CVE-2018-13379` has a CVSS of **9.8**, it exists on a low-importance staging VM, making its calculated risk score **14.7** (Priority P2). 
2. **Immediate Action:** `CVE-2021-44228` (Log4j) on the public Web Application Server has a CVSS of **10.0**, an active exploit exists, and it resides on a highly critical asset, resulting in a high risk score of **45.0** (Priority P0).
3. **Recommendation:** Remediation efforts must always target **P0** items first, followed by **P1**, regardless of whether a non-critical asset has a high CVSS rating.
