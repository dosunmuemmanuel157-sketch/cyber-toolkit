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
| 6 | Phishing Link Analyzer | ✅ Done |
| 7 | Failed-Login Log Analyzer | ✅ Done |
| 8 | Port Scanner v2 (Threading + Banner Grabbing) | ✅ Done |
| 9 | Menu UI combining all tools | 🔜 Coming soon |
| 10 | Final README, demo and recap | 🔜 Coming soon |

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

## 🎣 Day 6: Phishing Link Analyzer
Paste a link and get a risk score from 0 to 100, with the reasons.
- Detects lookalike domains like `paypa1.com` and `g00gle.com`
- Flags shortened links, raw IP addresses, the `@` trick, cheap domain endings and scam words
- Shows 🚩 red flags (with points) and ✅ green flags (good signs)
- Gives a clear verdict: 🟢 Low risk, 🟡 Suspicious or 🔴 Dangerous
- **Only reads the text of the link. It never opens it.**

```bash
python phishing_checker/phishing_checker.py
```

> ⚠️ "Low risk" does not mean "safe". It means none of the checks fired. Real tools also check domain age and blocklists.

## 🕵️ Day 7: Failed-Login Log Analyzer
Reads a server login log and finds brute-force attacks, like a SOC analyst would.
- Creates a **fake** log in the style of Linux `sshd`, using reserved example IPs
- Pulls out the time, result, username and IP from each line with regex
- Counts failed logins per IP and measures how fast they happen
- Scores each IP from 0 to 100 using red flags: many failures, machine speed, many usernames tried, and admin accounts targeted
- Prints a report with 🔴 🟡 🟢 levels and defender advice
- Only reads logs. It never changes them.

```bash
python log_analyzer/log_analyzer.py
```

> ⚠️ Only analyze logs from systems you own or have permission to test. The tool currently understands Linux `sshd` log lines only.

## ⚡ Day 8: Port Scanner v2 (Threading + Banner Grabbing)
An upgrade to the Day 4 scanner.
- **Threading:** scans with 200 workers at once. In my test, 151 ports took 75 seconds one by one and 0.6 seconds with threads (about 118x faster)
- **Banner grabbing:** reads the greeting that open ports send back (like `SSH-2.0-OpenSSH_7.2`), which can reveal software versions
- Flags a few known older versions as hints to check CVE databases
- Includes a built-in speed test and a safe **fake service** (`fake_service.py`) that runs only on your own computer (127.0.0.1) for practice
- Asks for permission confirmation before scanning anything other than localhost

```bash
# Terminal 1: start the practice services
python port_scanner/fake_service.py

# Terminal 2: run the scanner
python port_scanner/port_scanner_v2.py
```

> ⚠️ The version hints are a tiny hand-written list. Real pentesters check CVE databases and use tools like Nmap.

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