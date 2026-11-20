"""
Breach Checker 
Day 2 of my 10-day Cyber Toolkit challenge.
Checks if a password has appeared in a known data breach using 
the Have I Been Pwned API. Your password is never sent.
For educational use only.
"""

import hashlib
import urllib.request
import urllib.error

API_URL = "https://api.pwnedpasswords.com/range/"


def hash_password(password):
    #Return the SHA-1 hash of a password as uppercase text.
    return hashlib.sha1(password.encode("utf-8")).hexdigest().upper()

def get_matching_hashes(prefix):
    #Ask the API for all hash endings that start with these 5 characters.
    url = API_URL + prefix
    request = urllib.request.Request(
        url, headers={"User-Agent": "cyber-toolkit-breach-checker"}
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return response.read().decode("utf-8")
    except urllib.error.URLError:
        return None

def check_password_breach(password):
    #Return how many times a password was found in breaches.
    full_hash = hash_password(password)
    prefix = full_hash[:5]
    suffix = full_hash[5:]

    response_text = get_matching_hashes(prefix)
    if response_text is None:
        return None

    for line in response_text.splitlines():
        hash_ending, count = line.split(":")
        if hash_ending == suffix:
            return int(count)

    return 0


def main():
    print("=" * 40)
    print("   BREACH CHECKER")
    print("=" * 40)

    password = input("Enter a password to check: ")
    times_found = check_password_breach(password)

    if times_found is None:
        print("\nCould not connect. Check your internet and try again.")
    elif times_found > 0:
        print(f"\n[!]BREACHED Found {times_found:,} times in data breaches.")
        print("Never use this password anywhere.")
    else:
        print("\n[OK] Not found in known breaches.")
        print("Still use a unique password for every account.")

if __name__ == "__main__":
    main()