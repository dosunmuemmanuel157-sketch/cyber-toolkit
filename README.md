# 🔐 Cyber Toolkit

A 10-day challenge: building one ethical security tool in Python every day.

## Progress

| Day | Tool | Status |
|-----|------|--------|
| 1 | Password Strength Checker | ✅ Done |
| 2 | Breach Checker | ✅ Done |
| 3 | Hash Generator + File Integrity Checker | ⏳ Coming soon |

## Day 1: Password Strength Checker

Checks how strong a password is and tells you how to improve it.

### Features
- Detects passwords found in common hacker wordlists
- Checks length and character variety (lowercase, uppercase, numbers, symbols)
- Calculates **entropy** (in bits) to measure how hard it is to guess
- Rates passwords from WEAK to VERY STRONG with improvement tips

### How to run
```bash
python password_checker/password_checker.py
```

### Example
```
========================================
   PASSWORD STRENGTH CHECKER
========================================
Enter a password: hello

Rating:  WEAK
Entropy: 23.5 bits

How to improve:
  - Use at least 8 characters (12+ is better).
  - Add UPPERCASE letters.
  - Add numbers.
  - Add symbols like ! @ # $ %.
```

### What I learned
- How dictionary attacks use common password lists
- What entropy means and how it is calculated
- Python functions, sets, dictionaries and f-strings

## Day 2: Breach Checker

Checks whether a password has appeared in a known data breach, **without sending the password anywhere**.

### How it works
1. Hashes the password with SHA-1
2. Sends only the **first 5 characters** of the hash to the [Have I Been Pwned](https://haveibeenpwned.com/API/v3#PwnedPasswords) API (this technique is called **k-anonymity**)
3. Receives about 800 possible matches
4. Searches those matches **locally** for the rest of the hash
5. Reports how many times the password was found in breaches

### How to run
```bash
python breach_checker/breach_checker.py
```

### Example
```
========================================
   BREACH CHECKER
========================================
Enter a password to check: password

[!] BREACHED! Found <count> times in data breaches.
Never use this password anywhere.
```

### What I learned
- How hashing works (SHA-1) and why hashes can't be reversed
- How k-anonymity protects privacy
- Calling a web API with Python's built-in `urllib`
- Handling errors with `try` / `except`

## ⚠️ Ethical use
This project is for **educational purposes only**. Only test passwords you own, and never use real passwords in screenshots.

## Author
Built by [@dosunmuemmanuel157-sketch](https://github.com/dosunmuemmanuel157-sketch) while studying cybersecurity.