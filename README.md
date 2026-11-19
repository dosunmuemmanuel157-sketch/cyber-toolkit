# 🔐 Cyber Toolkit

A 10-day challenge: building one ethical security tool in Python every day.

## Progress

| Day | Tool | Status |
|-----|------|--------|
| 1 | Password Strength Checker | ✅ Done |
| 2 | Breach Checker | ⏳ Coming soon |

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

## ⚠️ Ethical use
This project is for **educational purposes only**. Only test passwords you own, and never use real passwords in screenshots.

## Author
Built by [@dosunmuemmanuel157-sketch](https://github.com/dosunmuemmanuel157-sketch) while studying cybersecurity.