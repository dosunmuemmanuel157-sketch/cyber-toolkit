"""
Password Strength Checker
Day 1 of my 10-day Cyber Toolkit challenge.
Checks how strong a password is and gives tips to improve it.
For educational use only.
"""

import string
import math

# Some of the most common passwords from public breach lists.
# Attackers try these first in a "dictionary attack".
COMMON_PASSWORDS = {
    "123456", "password", "123456789", "12345678", "12345",
    "qwerty", "abc123", "password1", "111111", "123123",
    "admin", "letmein", "welcome", "monkey", "dragon",
    "football", "iloveyou", "sunshine", "princess", "000000",
    "qwerty123", "1q2w3e4r", "passw0rd", "master", "login",
}


def check_character_types(password):
    """Return which kinds of characters the password contains."""
    has_lower = any(char in string.ascii_lowercase for char in password)
    has_upper = any(char in string.ascii_uppercase for char in password)
    has_digit = any(char in string.digits for char in password)
    has_symbol = any(char in string.punctuation for char in password)

    return {
        "lowercase": has_lower,
        "uppercase": has_upper,
        "numbers": has_digit,
        "symbols": has_symbol,
    }


def calculate_entropy(password):
    """Estimate password entropy in bits."""
    types = check_character_types(password)

    pool_size = 0
    if types["lowercase"]:
        pool_size += 26
    if types["uppercase"]:
        pool_size += 26
    if types["numbers"]:
        pool_size += 10
    if types["symbols"]:
        pool_size += len(string.punctuation)

    if pool_size == 0:
        return 0

    return len(password) * math.log2(pool_size)


def analyze_password(password):
    """Analyze a password and return its rating and feedback."""
    tips = []

    # 1. Is it in the common password list?
    if password.lower() in COMMON_PASSWORDS:
        return "VERY WEAK", 0, ["This password is in common hacker wordlists. Never use it."]

    # 2. Check length
    if len(password) < 8:
        tips.append("Use at least 8 characters (12+ is better).")
    elif len(password) < 12:
        tips.append("Make it 12 or more characters for better security.")

    # 3. Check character types
    types = check_character_types(password)
    if not types["lowercase"]:
        tips.append("Add lowercase letters.")
    if not types["uppercase"]:
        tips.append("Add UPPERCASE letters.")
    if not types["numbers"]:
        tips.append("Add numbers.")
    if not types["symbols"]:
        tips.append("Add symbols like ! @ # $ %.")

    # 4. Rate it by entropy
    entropy = calculate_entropy(password)
    if entropy < 40:
        rating = "WEAK"
    elif entropy < 60:
        rating = "MEDIUM"
    elif entropy < 80:
        rating = "STRONG"
    else:
        rating = "VERY STRONG"

    return rating, entropy, tips


def main():
    print("=" * 40)
    print("   PASSWORD STRENGTH CHECKER")
    print("=" * 40)

    password = input("Enter a password: ")
    rating, entropy, tips = analyze_password(password)

    print(f"\nRating:  {rating}")
    print(f"Entropy: {entropy:.1f} bits")

    if tips:
        print("\nHow to improve:")
        for tip in tips:
            print(f"  - {tip}")
    else:
        print("\nGreat password!")


if __name__ == "__main__":
    main()