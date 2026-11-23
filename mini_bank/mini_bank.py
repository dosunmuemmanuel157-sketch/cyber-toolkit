"""
Secure Mini Bank (simulation)
Day 5 of my 10-day Cyber Toolkit challenge.
Practises secure PIN storage: salted hashes and login lockout.
FAKE MONEY ONLY. Never use a real PIN or real bank details.
For educational use only.
"""

import getpass
import hashlib
import hmac
import json
import secrets
from datetime import datetime

try:
    import msvcrt
except ImportError:
    msvcrt = None

MAX_ATTEMPTS = 3
BANK_FILE = "bank_data.json"

accounts = {}


def money(amount):
    """Format a whole-dollar amount like $5,000."""
    return f"${amount:,}"


def generate_salt():
    """Return a random salt as text."""
    return secrets.token_hex(16)


def hash_pin(pin, salt):
    """Return a salted hash of a PIN."""
    pin_bytes = pin.encode("utf-8")
    salt_bytes = bytes.fromhex(salt)
    hashed = hashlib.pbkdf2_hmac("sha256", pin_bytes, salt_bytes, 100_000)
    return hashed.hex()


def create_account(account_number, name, pin):
    """Create a new account with a hashed PIN."""
    if account_number in accounts:
        return False, "Account already exists."

    if not (pin.isdigit() and len(pin) == 4):
        return False, "PIN must be exactly 4 digits."

    salt = generate_salt()
    accounts[account_number] = {
        "name": name,
        "salt": salt,
        "pin_hash": hash_pin(pin, salt),
        "balance": 0,
        "failed_attempts": 0,
        "locked": False,
        "history": [],
    }
    return True, "Account created."


def login(account_number, pin):
    """Check a PIN. Lock the account after too many wrong tries."""
    account = accounts.get(account_number)
    if account is None:
        return False, "Account not found."

    if account["locked"]:
        return False, "Account is locked. Contact the bank."

    attempt = hash_pin(pin, account["salt"])
    if hmac.compare_digest(attempt, account["pin_hash"]):
        account["failed_attempts"] = 0
        return True, f"Welcome, {account['name']}!"

    account["failed_attempts"] += 1
    if account["failed_attempts"] >= MAX_ATTEMPTS:
        account["locked"] = True
        return False, "Too many wrong PINs. Account locked."

    remaining = MAX_ATTEMPTS - account["failed_attempts"]
    return False, f"Wrong PIN. {remaining} attempt(s) left."


def add_history(account, description, amount):
    """Record a transaction with the date and time."""
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    account["history"].append(f"{time_now} | {description}: {money(amount)}")


def get_balance(account_number):
    """Return an account's balance."""
    return accounts[account_number]["balance"]


def deposit(account_number, amount):
    """Add money to an account."""
    if amount <= 0:
        return False, "Amount must be greater than $0."

    account = accounts[account_number]
    account["balance"] += amount
    add_history(account, "DEPOSIT", amount)
    return True, f"Deposited {money(amount)}. New balance: {money(account['balance'])}"


def withdraw(account_number, amount):
    """Take money out of an account."""
    if amount <= 0:
        return False, "Amount must be greater than $0."

    account = accounts[account_number]
    if amount > account["balance"]:
        return False, "Insufficient funds."

    account["balance"] -= amount
    add_history(account, "WITHDRAW", amount)
    return True, f"Withdrew {money(amount)}. New balance: {money(account['balance'])}"


def transfer(from_account, to_account, amount, pin):
    """Send money to another account. Needs the PIN again."""
    ok, message = login(from_account, pin)
    if not ok:
        return False, message

    if to_account not in accounts:
        return False, "Receiving account not found."

    if to_account == from_account:
        return False, "You can't transfer to the same account."

    if amount <= 0:
        return False, "Amount must be greater than $0."

    sender = accounts[from_account]
    receiver = accounts[to_account]

    if amount > sender["balance"]:
        return False, "Insufficient funds."

    sender["balance"] -= amount
    receiver["balance"] += amount
    add_history(sender, f"TRANSFER OUT to {to_account}", amount)
    add_history(receiver, f"TRANSFER IN from {from_account}", amount)
    return True, (
        f"Transferred {money(amount)} to {receiver['name']}. "
        f"New balance: {money(sender['balance'])}"
    )


def save_accounts():
    """Save all accounts to a file."""
    with open(BANK_FILE, "w") as file:
        json.dump(accounts, file, indent=2)


def load_accounts():
    """Load saved accounts when the program starts."""
    try:
        with open(BANK_FILE, "r") as file:
            accounts.update(json.load(file))
    except FileNotFoundError:
        pass
    except json.JSONDecodeError:
        print("[!] Bank data file is damaged. Starting with no accounts.")


def show_result(ok, message):
    """Print a result with a clear tag."""
    if ok:
        print(f"[OK] {message}")
    else:
        print(f"[!] {message}")


def show_history(account_number):
    """Print an account's transaction history."""
    history = accounts[account_number]["history"]
    if not history:
        print("No transactions yet.")
        return

    for line in history:
        print(f"  {line}")


def prompt_amount(text):
    """Ask for a whole-dollar amount. Accepts input like 500 or $500."""
    raw = input(text).strip().replace("$", "").replace(",", "")
    try:
        return int(raw)
    except ValueError:
        print("[!] Please enter a whole-dollar amount, like 500 or $500.")
        return None


def read_pin(prompt):
    """Read a PIN and show * for each character typed."""
    if msvcrt is None:
        return getpass.getpass(prompt)

    print(prompt, end="", flush=True)
    pin = ""

    while True:
        char = msvcrt.getwch()

        if char in ("\r", "\n"):
            print()
            return pin

        if char == "\x03":
            raise KeyboardInterrupt

        if char == "\b":
            if pin:
                pin = pin[:-1]
                print("\b \b", end="", flush=True)
        elif char in ("\x00", "\xe0"):
            msvcrt.getwch()
        else:
            pin += char
            print("*", end="", flush=True)


def account_menu(account_number):
    """Menu shown after a successful login."""
    while True:
        account = accounts[account_number]
        print(f"\n--- {account['name']} ({account_number}) ---")
        print("1. Check balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Transaction history")
        print("6. Log out")

        choice = input("Choose 1-6: ")

        if choice == "1":
            print(f"Balance: {money(get_balance(account_number))}")

        elif choice == "2":
            amount = prompt_amount("Amount to deposit ($): ")
            if amount is not None:
                ok, message = deposit(account_number, amount)
                show_result(ok, message)

        elif choice == "3":
            amount = prompt_amount("Amount to withdraw ($): ")
            if amount is not None:
                ok, message = withdraw(account_number, amount)
                show_result(ok, message)

        elif choice == "4":
            to_account = input("Send to account number: ").strip()
            amount = prompt_amount("Amount to transfer ($): ")
            if amount is not None:
                pin = read_pin("Confirm your PIN: ")
                ok, message = transfer(account_number, to_account, amount, pin)
                show_result(ok, message)

        elif choice == "5":
            show_history(account_number)

        elif choice == "6":
            save_accounts()
            print("Logged out. Goodbye!")
            return

        else:
            print("[!] Invalid choice.")

        save_accounts()


def main():
    load_accounts()

    print("=" * 40)
    print("   SECURE MINI BANK (SIMULATION)")
    print("=" * 40)
    print("FAKE MONEY ONLY. Never use a real PIN.")

    while True:
        print("\n1. Create account")
        print("2. Log in")
        print("3. Quit")
        choice = input("Choose 1-3: ")

        if choice == "1":
            account_number = input("Choose an account number: ").strip()
            name = input("Your name: ").strip()
            if account_number == "" or name == "":
                print("[!] Account number and name are required.")
                continue

            pin = read_pin("Choose a 4-digit PIN: ")
            ok, message = create_account(account_number, name, pin)
            show_result(ok, message)
            save_accounts()

        elif choice == "2":
            account_number = input("Account number: ").strip()
            pin = read_pin("PIN: ")
            ok, message = login(account_number, pin)
            show_result(ok, message)
            save_accounts()
            if ok:
                account_menu(account_number)

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("[!] Invalid choice.")


if __name__ == "__main__":
    main()