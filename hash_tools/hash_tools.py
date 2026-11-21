"""
Hash Generator + File Integrity Checker
Day 3 of my 10-day Cyber Toolkit Challenge.
Create SHA-256 fingerprints of text and files, and detects 
when a file has been changed. 
For educational use only.
"""

import hashlib
import json
import os

BASELINE_FILE = "baseline.json"


def hash_text(text):
    #Return the SHA-256 hash of a piece of text
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def hash_file(path):
    #Return the SHA-256 hash of a file, read in small blocks.
    sha256 = hashlib.sha256()

    with open(path, "rb") as file:
        while True:
            block = file.read(4096)
            if not block:
                break
            sha256.update(block)

    return sha256.hexdigest()


def create_baseline(folder):
    #Fingerprint every file in a folder and save the results.
    baseline = {}

    for name in os.listdir(folder):
        path = os.path.join(folder, name)
        if os.path.isfile(path):
            baseline[path] = hash_file(path)

    with open(BASELINE_FILE, "w") as file:
        json.dump(baseline, file, indent=2)

    return baseline


def check_integrity(folder):
    #Compare a folder's files against the saved baseline.
    try:
        with open(BASELINE_FILE, "r") as file:
            baseline = json.load(file)
    except FileNotFoundError:
        return None

    current = {}
    for name in os.listdir(folder):
        path = os.path.join(folder, name)
        if os.path.isfile(path):
            current[path] = hash_file(path)

    modified = []
    deleted = []
    added = []

    for path, old_hash in baseline.items():
        if path not in current:
            deleted.append(path)
        elif current[path] != old_hash:
            modified.append(path)

    for path in current:
        if path not in baseline:
            added.append(path)

    return modified, deleted, added


def main():
    print("=" * 40)
    print("   HASH TOOLS + INTEGRITY CHECK")
    print("=" * 40)
    print("1. Hash some text")
    print("2. Hash a file")
    print("3. Create a baseline of a folder")
    print("4. Check a folder for changes")

    choice = input("\nChoose 1-4: ")

    if choice == "1":
        text = input("Enter text: ")
        print(f"\nSHA-256: {hash_text(text)}")

    elif choice == "2":
        path = input("Enter file path: ").strip('"')
        try:
            print(f"\nSHA-256: {hash_file(path)}")
        except FileNotFoundError:
            print("\nFile not found.")

    elif choice == "3":
        folder = input("Enter folder path: ").strip('"')
        try:
            baseline = create_baseline(folder)
            print(f"\nBaseline saved for {len(baseline)} files.")
        except FileNotFoundError:
            print("\nFolder not found.")

    elif choice == "4":
        folder = input("Enter folder path: ").strip('"')
        try:
            result = check_integrity(folder)
        except FileNotFoundError:
            print("\nFolder not found.")
            return

        if result is None:
            print("\nNo baseline found. Run option 3 first.")
            return

        modified, deleted, added = result
        if not (modified or deleted or added):
            print("\n[OK] No changes. All files match the baseline.")
        else:
            for path in modified:
                print(f"[!] MODIFIED: {path}")
            for path in deleted:
                print(f"[!] DELETED:  {path}")
            for path in added:
                print(f"[+] NEW FILE: {path}")

    else:
        print("\nInvalid choice.")


if __name__ == "__main__":
    main()
