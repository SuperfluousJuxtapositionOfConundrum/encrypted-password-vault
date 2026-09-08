# Cryptographic Command-Line Password Vault

A lightweight, production-grade local password vault built in pure Python as a Command-Line Interface (CLI) with **zero external dependencies**. This project was engineered to explore low-level memory handling, bitwise cryptographic operations, and defensive filesystem architectures.

## 🛡️ Core Security Architecture

The application implements a dual-layer security perimeter to isolate authentication from local data storage:

1. **Master Authentication Gate:** Master passwords are treated using a one-way **SHA-256 cryptographic hash** (`hashlib`). Plain-text master keys are never stored on disk.
2. **Local Database Encryption:** Account credentials are encrypted at the bit level using a custom **Bitwise XOR Cipher** before being structured into relational storage.

---

## 🔄 Low-Level Data Pipeline

To prevent database format corruption from raw non-alphanumeric system bytes, data undergoes a strict multi-stage transformation lifecycle during execution:

### 🔒 Encryption Pipeline (Adding Credentials)
Plain Text String ("hi") 
  -> UTF-8 Encoding (b'\x68\x69')
        -> Strict 8-bit Alignment (01101000 01101001) via :08b
              -> Bitwise XOR Inversion Loop (10010111 10010110)
                    -> Base-2 to Base-16 Integer Translation
                          -> Prefix-Free Hexadecimal String ("9796")
                                -> Relational JSON Stream Write (vault.json)

### 🔓 Decryption Pipeline (Retrieving Credentials)
Read Hex String ("9796")
  -> Base-16 to Base-2 Binary Bit Extension
        -> Left-Zero Bit Alignment (.zfill())
              -> Reverse Bitwise XOR Inversion Loop
                    -> 8-bit Step Byte Slicing (range(0, len, 8))
                          -> Universal Unicode Mapping (chr())
                                -> Decoded Alphanumeric Plain Text ("hi")

---

## 🛠️ Defensive Engineering & Robustness

* **Short-Circuit Filesystem Gates:** Startup sequences utilize multi-layered `os.path` and explicit `os.path.getsize()` logic to verify target file states. This proactively shields the application from fatal runtime crashes like `FileNotFoundError` and `JSONDecodeError`.
* **State Isolation:** Session tracking layers (`passwd_list`) are kept strictly separated from disk persistence layers (`vault.json`) to isolate local memory states from hard drive access.
* **Pure Python Constraints:** Built entirely using native system libraries (`os`, `json`, `hashlib`), proving platform-agnostic compilation.

## 🚀 How to Run

Ensure you have Python 3.10+ installed. Execute the CLI engine from your terminal environment:

```bash
python password_manager/passwd_manager.py
```
