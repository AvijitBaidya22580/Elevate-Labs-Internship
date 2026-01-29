# 📡 Task 3: Network Traffic Analysis & Packet Forensics

## 📌 Executive Summary

Network Traffic Analysis (NTA) is the core skill required for identifying malicious activity, diagnosing connectivity issues, and understanding application behavior. This module focuses on "Packet Sniffing"—capturing data units flowing across a network interface—and "Deep Packet Inspection" (DPI) to interpret the underlying protocols.

**Objective:** To transition from passive network usage to active analysis, gaining the ability to dissect protocol headers, identify cleartext vulnerabilities, and validate connection integrity via the TCP state machine.

---

## 🛠️ Technical Stack

### Primary Tooling

* **Wireshark:** The industry-standard network protocol analyzer. It captures traffic in real-time and presents it in a human-readable format.

### Alternative / CLI Tools

* **tcpdump:** A powerful command-line packet analyzer (essential for Linux servers with no GUI).
* **Microsoft Network Monitor:** Legacy Windows tool, useful for specific older stack debugging.

### Prerequisites

* Understanding of the **OSI Model** (specifically Layers 3, 4, and 7).
* Knowledge of **IPv4/IPv6** addressing and **Port numbers** (e.g., 80 vs 443).

---

## ⚙️ Operational Procedure

### Phase 1: Environment Setup

1. **Installation:** Install Wireshark.
* *Critical:* During installation on Windows, ensure you install **Npcap** with "Install Npcap in WinPcap API-compatible Mode" checked. On Linux, ensure your user is added to the `wireshark` group to capture packets without root (if configured) or run via `sudo`.


2. **Interface Selection:**
* Launch Wireshark and select the active interface (e.g., `Wi-Fi`, `eth0`, or `Ethernet adapter`).
* *Pro Tip:* Verify you are capturing in **Promiscuous Mode** (default in Wireshark) to see all traffic reaching your NIC, not just traffic addressed to you.



### Phase 2: Capture & Filtering

*Start the capture (Blue Shark Fin icon) and generate some traffic (open a browser, visit `example.com`, ping a server).*

3. **Display Filters:** The stream of data will be overwhelming. Master the use of Display Filters bar at the top:
* `http`: Shows only HTTP traffic (useful for seeing cleartext).
* `dns`: Shows Domain Name System queries.
* `tcp.port == 443`: Shows HTTPS traffic.
* `ip.addr == 192.168.1.5`: Filters traffic to/from a specific host.



### Phase 3: Protocol Deep Dive

#### 4. The TCP 3-Way Handshake

Connection-oriented communication relies on this mechanism to establish a session. You must locate these packets in your capture.

* **Step A (SYN):** Client sends a packet with the **SYN** flag set. (Sequence=0).
* **Step B (SYN-ACK):** Server acknowledges and sends its own SYN. (Ack=1, Sequence=0).
* **Step C (ACK):** Client acknowledges the server. Connection Established.
* *Wireshark Filter:* `tcp.flags.syn == 1 && tcp.flags.ack == 0` (Finds SYN packets).

#### 5. Cleartext vs. Encrypted Traffic

* **HTTP (Cleartext):** Filter for `http`. Select a packet, right-click, and choose **Follow > TCP Stream**. You will see the raw HTML, headers, and potentially credentials in red/blue text. This demonstrates why HTTP is insecure.
* **HTTPS (Encrypted):** Filter for `tcp.port == 443`. If you "Follow TCP Stream" here, you will see random, unintelligible characters (Ciphertext). This is TLS encryption in action.

#### 6. DNS Analysis

* Filter for `dns`.
* Observe the "Standard Query" (A record) asking "Who has https://www.google.com/search?q=google.com?" and the "Standard Query Response" providing the IP address.
* *Security Note:* Malware often uses DNS for "Beaconing" (calling home to a C2 server). Analyzing DNS logs is a primary method for detecting infections.

---

## 📄 Deliverables

You are required to submit a professional technical report titled **"Network Traffic Analysis Report"**.

### Report Structure (PDF):

1. **Executive Summary:** Brief overview of the capture session.
2. **Topology Info:** Your IP address, Gateway IP, and Interface used.
3. **The 3-Way Handshake:**
* *Screenshot:* A successful SYN, SYN-ACK, ACK sequence from Wireshark.
* *Explanation:* Describe the flags and relative sequence numbers.


4. **Protocol Analysis:**
* **DNS:** Screenshot of a query/response. What IP did the URL resolve to?
* **HTTP vs HTTPS:** Compare the payload of an HTTP packet vs. an HTTPS packet. Explain the security implication.


5. **Conclusion:** Summary of findings.

### Artifacts:

* **`.pcapng` File:** Save your capture session (`File > Save As`). *Warning: Do not capture sensitive personal data (passwords/bank info) in this assignment.*

---

## 💡 Expert Insight: Malware Context

> Since you have an interest in **Malware Analysis**, Wireshark is your microscope. When analyzing a malware sample in a sandbox (like the VM from Task 2):
> * You use Wireshark to see who the malware talks to (Command & Control / C2 servers).
> * You look for "Data Exfiltration" (sensitive files leaving your network).
> * **Tip:** Malware often communicates over non-standard ports (e.g., HTTP traffic over port 8080 or raw TCP over port 4444).
> 
> 

---

## 📚 Resources

* [Wireshark Display Filter Reference](https://www.wireshark.org/docs/dfref/)
* [Sample Captures (Wireshark Wiki)](https://wiki.wireshark.org/SampleCaptures) - *Practice files if you can't generate specific traffic.*
* [IETF RFC 793 (TCP Protocol)](https://datatracker.ietf.org/doc/html/rfc793) - *The official definition of TCP.*

---
