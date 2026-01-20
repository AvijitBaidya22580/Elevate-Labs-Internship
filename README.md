# Task-4-Password-Security-Authentication-Analysis

# 🔐 Password Security & Authentication Analysis

## 📌 Project Overview
This project explores **password security**, **hashing algorithms**, and **authentication defenses** through both theoretical learning and hands-on attack simulation.  
By acting as an attacker, we evaluate how weak password practices and outdated hashing algorithms can be compromised—and how modern defenses mitigate these risks.

---

## 🎯 Project Objectives
- Understand the difference between **hashing** and **encryption**
- Identify common password hashing algorithms
- Simulate a real-world password database leak
- Perform **dictionary** and **brute-force attacks**
- Analyze failures and recommend secure authentication practices

---

## 🧠 Phase 1: Theoretical Foundation (Learn Phase)

### 1️⃣ Hashing vs. Encryption

| Concept | Description | Use Case |
|------|------------|---------|
| **Encryption** | Two-way process using a key; data can be decrypted | Data in transit (AES, RSA) |
| **Hashing** | One-way irreversible process producing fixed-length output | Password storage |

Passwords **must never** be encrypted—only hashed.

---

### 2️⃣ Identifying Hash Types

| Algorithm | Hash Length | Format | Security Status |
|--------|------------|--------|----------------|
| **MD5** | 128-bit | 32 hex characters | ❌ Broken |
| **SHA-1** | 160-bit | 40 hex characters | ⚠️ Deprecated |
| **bcrypt** | Variable | `$2a$`, `$2b$`, `$2y$` prefix | ✅ Secure |

---

## 🧪 Phase 2: Lab Setup (Do Phase)

### 🗂 Step 1: Generate Hashes

Create a file named:

`hashes.txt`

`5f4dcc3b5aa765d61d8327deb882cf99
e10adc3949ba59abbe56e057f20f883e
$2y$12$R9h/cIPz0gi.URNNX3kh2OPST9/PgBkqquii.V3/dIwdy/x.wM0je`


> These hashes simulate a compromised password database.

---

### ⚔️ Step 2: The Attack

#### A️⃣ Dictionary Attack

A dictionary attack attempts passwords from a known wordlist (e.g., `rockyou.txt`).

##### Using John the Ripper:
``bash
# Auto-detect hash formats and crack
john hashes.txt

# Display cracked passwords
john --show hashes.txt


- B️⃣ Brute Force Attack

- A brute force attack attempts every possible character combination.

### Using Hashcat (Example):
# -m 0 = MD5, -a 3 = brute-force mode
hashcat -m 0 -a 3 hashes.txt


# 🛡 Final Outcome

- This project demonstrates why modern password storage and authentication controls are essential. Weak passwords and outdated algorithms pose critical security risks, while strong hashing and MFA significantly reduce attack success.

# 📚 Tools & Resources

- John the Ripper

- Hashcat

- rockyou.txt wordlist

- OWASP Authentication Guidelines
