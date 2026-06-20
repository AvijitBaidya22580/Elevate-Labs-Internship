# Task-4-Password-Security-Authentication-Analysis

# Task 4: Password Security & Authentication Analysis

## 1. Introduction

Password-based authentication is the most widely used security mechanism in modern digital systems. From email accounts to banking applications, passwords remain the primary line of defense. However, weak password practices and improper storage techniques make systems vulnerable to cyberattacks. This report analyzes how passwords are stored, attacked, and protected, and provides recommendations for stronger authentication mechanisms.

---

## 2. Password Storage: Hashing vs Encryption

### Hashing

Hashing converts a password into a fixed-length string using a mathematical algorithm. It is a one-way process, meaning the original password cannot be retrieved from the hash.

**Example:**
- Password: myPass123
- Hash: 482c811da5d5b4bc6d497ffa98491e38



**Common hashing algorithms:**

- MD5  
- SHA-1  
- SHA-256  
- bcrypt  
- Argon2  

### Encryption

Encryption is a two-way process. Data can be decrypted back to its original form using a key. Passwords should not be stored using encryption because if the key is compromised, all passwords are exposed.

✔ **Best practice:** Always use hashing with salt.

---

## 3. Types of Password Hashes

| Algorithm | Security Level |
|---------|---------------|
| MD5 | Very Weak |
| SHA-1 | Weak |
| SHA-256 | Moderate |
| bcrypt | Strong |
| Argon2 | Very Strong |

Older algorithms like MD5 and SHA-1 are fast and therefore vulnerable to brute-force attacks. Modern systems prefer bcrypt or Argon2 because they are intentionally slow.

---

## 4. Password Hash Generation

When a user registers:

1. Password is entered.  
2. A salt is added.  
3. The combined value is hashed.  
4. The hash is stored in the database.  

This prevents attackers from using rainbow tables effectively.

---

## 5. Password Cracking Methods

### 5.1 Dictionary Attack  
Uses predefined wordlists to guess passwords.

### 5.2 Brute Force Attack  
Tries every possible character combination.

### 5.3 Hybrid Attack  
Combines dictionary words with numbers or symbols.

### 5.4 Rainbow Table Attack  
Uses precomputed hash databases.

---

## 6. Why Weak Passwords Fail

Weak passwords such as:

- 123456  
- password  
- admin123  
- qwerty  

can be cracked in seconds because they appear in almost every wordlist.

**Common problems:**

- Short length  
- No symbols  
- Predictable patterns  
- Reuse across platforms  

---

## 7. Multi-Factor Authentication (MFA)

MFA adds additional security layers:

- Something you know → Password  
- Something you have → OTP / Phone  
- Something you are → Fingerprint / Face  

Even if a password is stolen, MFA prevents unauthorized access.

---

## 8. Tools Used in Password Security Analysis

- **Hashcat** – GPU-based password recovery tool  
- **John the Ripper** – Password auditing tool  
- **Online Hash Identifiers** – Identify hash types  

These tools are mainly used for security testing and research.

---

## 9. Brute Force vs Dictionary Attack

| Feature | Brute Force | Dictionary |
|-------|------------|------------|
| Speed | Slow | Faster |
| Accuracy | High | Depends on wordlist |
| Practical | Less | More |

---

## 10. Recommendations for Strong Authentication

✔ Use passwords of at least 12 characters  
✔ Combine uppercase, lowercase, numbers, and symbols  
✔ Use unique passwords per platform  
✔ Enable MFA  
✔ Store passwords using bcrypt or Argon2  
✔ Implement account lockout policies  
✔ Educate users about phishing  

---

## 11. Conclusion

Password security is a critical component of cybersecurity. Weak passwords and improper storage methods lead to major data breaches. By using strong hashing algorithms, MFA, and secure password policies, organizations can significantly reduce security risks. Understanding password attack techniques helps defenders build stronger authentication systems.

---

## Final Outcome

This task provides knowledge of password attacks, defenses, hashing techniques, and modern authentication practices.

