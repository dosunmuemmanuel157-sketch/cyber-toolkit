# 🛡️ Cyber Toolkit

A 10-day **build in public** project: one beginner-friendly cybersecurity tool in Python every day.

Built by a cybersecurity student learning ethical hacking, one tool at a time. 🚀

---

## 📅 Progress

| Day | Tool | Status |
|-----|------|--------|
| 1 | Password Strength Checker | ✅ Done |
| 2 | Breach Checker (HIBP) | ✅ Done |
| 3 | Hash Tools + File Integrity | ✅ Done |
| 4 | Port Scanner | ✅ Done |
| 5 | Secure Mini Bank | ✅ Done |
| 6 | Threading + Banner Grabbing | 🔜 Coming soon |
| 7-10 | More tools | 🔜 Coming soon |

---

## 🔐 Day 1: Password Strength Checker
Checks how strong a password is.
- Detects common passwords
- Checks for upper/lowercase, numbers and symbols
- Calculates entropy (how hard it is to guess)

```bash
python password_checker/password_checker.py
```

## 🕵️ Day 2: Breach Checker
Checks if a password has appeared in a known data breach using the Have I Been Pwned API.
- Uses **SHA-1 hashing**
- Uses **k-anonymity**: only the first 5 characters of the hash are sent, so your real password never leaves your computer

```bash
python breach_checker/breach_checker.py
```

## #️⃣ Day 3: Hash Tools
Hash text and files, then detect if a file has been changed.
- Hash text with SHA-256
- Hash any file
- Create a baseline and check file integrity later

```bash
python hash_tools/hash_tools.py
```

## 🔎 Day 4: Port Scanner
Scans a range of ports to see which ones are open.
- Shows common service names (HTTP, SSH, etc.)
- Asks for permission confirmation before scanning anything other than localhost
- Shows how long the scan took

```bash
python port_scanner/port_scanner.py
```

## 🏦 Day 5: Secure Mini Bank
A fake bank that shows how real systems protect PINs. **No real money, no real data.**
- Create accounts and log in with a 4-digit PIN
- PINs are **never stored in plain text**: they are salted and hashed with PBKDF2-HMAC-SHA256
- Account locks after 3 wrong PIN attempts
- PIN shows as `*` while typing
- Deposit, withdraw, transfer and view transaction history in `$`
- Constant-time PIN comparison (`hmac.compare_digest`)
- Data is saved to a local `bank_data.json` (not uploaded to GitHub)

```bash
python mini_bank/mini_bank.py
```

---

## ⚖️ Ethical Use
This project is for **learning and education only**.
- Only scan or test systems you **own** or have **written permission** to test
- Use fake data only. Never enter real passwords or PINs
- The author is not responsible for misuse

---

## 👤 Author
**Dosunmu Emmanuel**, Cybersecurity student at UNILAG

GitHub: [dosunmuemmanuel157-sketch](https://github.com/dosunmuemmanuel157-sketch)

Follow the journey on LinkedIn, X and Instagram. ⭐ Star the repo if it helps you!