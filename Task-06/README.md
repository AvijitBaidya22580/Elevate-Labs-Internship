# Task-6-Introduction-to-Cryptography

## Project Overview

This repository documents the practical implementation of fundamental cryptographic concepts as part of Task 6. The project focuses on securing data through encryption, ensuring data integrity via hashing, and validating authenticity using digital signatures.

By utilizing industry-standard tools such as OpenSSL, this project simulates real-world security scenarios to demonstrate how sensitive information is protected during storage and transmission.

## Objectives

The primary objectives of this project are:

* To distinguish between symmetric and asymmetric encryption methodologies.
* To implement the Advanced Encryption Standard (AES) for data confidentiality.
* To generate and utilize Rivest–Shamir–Adleman (RSA) key pairs for secure key exchange.
* To verify file integrity using cryptographic hash functions.
* To apply digital signatures for non-repudiation and authentication.

## Tools & Technologies

* **OpenSSL:** The primary command-line tool used for generating keys, certificates, and performing encryption/decryption operations.
* **CyberChef:** Utilized as a secondary tool for visualizing data transformation and verification (optional/alternative method).
* **Linux/Unix Terminal:** Environment for executing cryptographic commands.

## Concepts Covered

This project explores the following core cryptographic pillars:

1. **Symmetric Encryption:** Using a single shared key for both encryption and decryption (AES-256-CBC).
2. **Asymmetric Encryption:** Using a public-private key pair (RSA-2048) where the public key encrypts and the private key decrypts.
3. **Hashing:** One-way transformation of data into a fixed-size string to verify integrity (SHA-256).
4. **Digital Signatures:** Signing data with a private key to verify its origin and integrity using the corresponding public key.

## Implementation Steps

### 1. Symmetric Encryption (AES)

Symmetric encryption was implemented using the AES-256-CBC algorithm. This method is efficient for encrypting large amounts of data but requires a secure method to share the secret key.

**Process:**

1. Created a plaintext file containing sensitive data.
2. Encrypted the file using a password-derived key.
3. Decrypted the file to verify the restoration of original data.

### 2. Asymmetric Encryption (RSA)

Asymmetric encryption was used to demonstrate secure key exchange mechanisms.

**Process:**

1. Generated a 2048-bit RSA private key.
2. Extracted the public key from the private key.
3. Encrypted a file using the public key (simulating a sender).
4. Decrypted the file using the private key (simulating the receiver).

### 3. Hashing and Integrity

Cryptographic hashing was applied to ensure that data had not been tampered with.

**Process:**

1. Calculated the SHA-256 hash of a file.
2. Modified the file content slightly.
3. Recalculated the hash to observe the "avalanche effect," proving the file integrity was compromised.

### 4. Digital Signatures

Digital signatures were implemented to provide authentication and non-repudiation.

**Process:**

1. Created a cryptographic signature of a file using the RSA private key.
2. Verified the signature using the RSA public key to confirm the file came from the holder of the private key and was not altered.

## Sample Commands

The following OpenSSL commands were used to execute the project tasks.

### AES Encryption/Decryption

```bash
# Encrypt 'data.txt' using AES-256-CBC
openssl enc -aes-256-cbc -salt -in data.txt -out data.enc

# Decrypt 'data.enc' back to plaintext
openssl enc -d -aes-256-cbc -in data.enc -out data_decrypted.txt

```

### RSA Key Generation & Operations

```bash
# Generate Private Key
openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048

# Extract Public Key
openssl rsa -pubout -in private_key.pem -out public_key.pem

# Encrypt using Public Key
openssl pkeyutl -encrypt -in secret.txt -pubin -inkey public_key.pem -out secret.enc

# Decrypt using Private Key
openssl pkeyutl -decrypt -in secret.enc -inkey private_key.pem -out secret.dec

```

### Digital Signing & Verification

```bash
# Sign the file (Create a digest, then sign the digest)
openssl dgst -sha256 -sign private_key.pem -out signature.bin data.txt

# Verify the signature
openssl dgst -sha256 -verify public_key.pem -signature signature.bin data.txt

```

## Results & Findings

* **Performance:** Symmetric encryption (AES) proved significantly faster than asymmetric encryption (RSA), highlighting why AES is preferred for bulk data encryption.
* **Key Management:** Asymmetric encryption resolves the key distribution problem inherent in symmetric systems but introduces higher computational overhead.
* **Integrity Checks:** Hashing provided a reliable method for detecting even single-bit changes in files.
* **Trust:** Digital signatures successfully linked the data to a specific private key, establishing trust without exchanging the private key itself.

## Real-World Applications

The concepts demonstrated in this project are foundational to modern internet security:

* **HTTPS (SSL/TLS):** Uses a hybrid approach. Asymmetric encryption (RSA/ECC) is used during the handshake to exchange a symmetric key. Symmetric encryption (AES) is then used to encrypt the actual web traffic.
* **VPNs:** Utilize these protocols to create secure tunnels, encapsulating and encrypting data packets to ensure privacy over public networks.
* **Software Distribution:** Developers sign software packages with their private keys. Operating systems use the public key to verify the software hasn't been tampered with before installation.

## Project Structure

```text
/
├── data/
│   ├── plaintext.txt       # Original data
│   ├── encrypted.bin       # Encrypted data files
│   └── decrypted.txt       # Restored data
├── keys/
│   ├── private_key.pem     # RSA Private Key (Do not commit in real scenarios)
│   └── public_key.pem      # RSA Public Key
├── signatures/
│   └── file.sig            # Digital signature output
└── README.md               # Project documentation

```

## How to Run / Reproduce

To reproduce the experiments in this repository:

1. **Prerequisites:** Ensure `openssl` is installed on your system.
* Linux: `sudo apt-get install openssl`
* macOS: `brew install openssl`
* Windows: Install via Win32 OpenSSL or use Git Bash.


2. **Clone the Repository:**
```bash
git clone https://github.com/username/intro-to-cryptography.git
cd intro-to-cryptography

```


3. **Execute Commands:** Follow the commands listed in the "Sample Commands" section to generate keys and process files.

## Conclusion

This project provided a comprehensive overview of cryptographic primitives. Understanding the distinction between symmetric and asymmetric algorithms, along with the application of hashing and signatures, is essential for designing secure software systems. These mechanisms form the underlying architecture of secure communications in distributed systems.

