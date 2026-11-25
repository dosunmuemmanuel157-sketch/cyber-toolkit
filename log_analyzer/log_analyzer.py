"""
Day 7 - Failed-Login Log Analyzer
Part of the Cyber Toolkit (10-day build in public project)

What it does:
    Reads a server log file, counts failed logins per IP address
    and flags IPs that look like brute-force attacks.

Safety:
    Uses a FAKE log file created by this program.
    Only analyze logs from systems you own or have permission to test.
    This tool only reads log files. It never changes them.

Ethical use only. Educational project.
"""

import re

LOG_FILE = "sample_auth.log"

LOG_PATTERN = re.compile(
    r"^\w+ \d+ (?P<time>[\d:]+) .*?: "
    r"(?P<status>Accepted|Failed) password for (?P<user>\S+) from (?P<ip>[\d.]+)"
)

PRIVILEGED_USERS = {"root", "admin", "administrator"}

LEVEL_INFO = {
    "DANGEROUS": ("🔴", "Likely brute-force attack. Block this IP and check if any login succeeded."),
    "SUSPICIOUS": ("🟡", "Unusual activity. Keep watching this IP."),
    "LOW RISK": ("🟢", "Looks like normal behavior or a small typo."),
}


def make_line(time, success, user, ip):
    result = "Accepted" if success else "Failed"
    return f"Nov 25 {time} server sshd[2201]: {result} password for {user} from {ip} port 52344 ssh2"


def create_sample_log():
    lines = [
        make_line("10:15:00", False, "root", "203.0.113.7"),
        make_line("10:15:04", False, "admin", "203.0.113.7"),
        make_line("10:15:08", False, "root", "203.0.113.7"),
    ]

    with open(LOG_FILE, "w") as file:
        for line in lines:
            file.write(line + "\n")

    print(f"✅ Created {LOG_FILE} with {len(lines)} lines\n")


def read_log(filename):
    try:
        with open(filename, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"❌ Could not find {filename}. Create the sample log first.\n")
        return []


def parse_line(line):
    match = LOG_PATTERN.search(line)
    if match is None:
        return None
    return {
        "time": match.group("time"),
        "status": match.group("status"),
        "user": match.group("user"),
        "ip": match.group("ip"),
    }


def parse_log(lines):
    entries = []
    for line in lines:
        entry = parse_line(line)
        if entry:
            entries.append(entry)
    return entries


def group_failures(entries):
    groups = {}

    for entry in entries:
        if entry["status"] != "Failed":
            continue

        ip = entry["ip"]
        if ip not in groups:
            groups[ip] = {"count": 0, "users": set(), "times": []}

        groups[ip]["count"] += 1
        groups[ip]["users"].add(entry["user"])
        groups[ip]["times"].append(entry["time"])

    return groups


def time_to_seconds(time_text):
    hours, minutes, seconds = time_text.split(":")
    return int(hours) * 3600 + int(minutes) * 60 + int(seconds)


def get_level(score):
    if score >= 50:
        return "DANGEROUS"
    if score >= 25:
        return "SUSPICIOUS"
    return "LOW RISK"


def make_bar(score):
    filled = score // 10
    return "█" * filled + "░" * (10 - filled)


def analyze_ip(ip, info):
    count = info["count"]
    users = info["users"]
    duration = time_to_seconds(info["times"][-1]) - time_to_seconds(info["times"][0])
    red_flags = []

    if count >= 10:
        red_flags.append((f"{count} failed logins", 50))
    elif count >= 5:
        red_flags.append((f"{count} failed logins", 30))
    elif count >= 3:
        red_flags.append((f"{count} failed logins", 15))

    if count >= 3:
        per_minute = count / max(duration, 1) * 60
        if per_minute >= 10:
            red_flags.append((f"Machine speed: about {per_minute:.0f} attempts per minute", 30))

    if len(users) >= 2:
        red_flags.append((f"Tried {len(users)} different usernames", 20))

    if users & PRIVILEGED_USERS:
        red_flags.append(("Targeted admin-level accounts", 10))

    score = min(sum(points for _, points in red_flags), 100)

    return {
        "ip": ip,
        "count": count,
        "users": sorted(users),
        "duration": duration,
        "score": score,
        "level": get_level(score),
        "red_flags": red_flags,
    }


def analyze_all(groups):
    results = [analyze_ip(ip, info) for ip, info in groups.items()]
    results.sort(key=lambda result: result["score"], reverse=True)
    return results


def show_report(results, total_lines, total_entries):
    print()
    print("=" * 56)
    print("🕵️  LOGIN LOG REPORT")
    print("=" * 56)
    print(f"📄 Lines read: {total_lines} | Login attempts understood: {total_entries}")

    if not results:
        print("✅ No failed logins found.")
        print("=" * 56 + "\n")
        return

    dangerous = sum(1 for result in results if result["level"] == "DANGEROUS")
    print(f"🌐 IPs with failed logins: {len(results)} | 🔴 Dangerous: {dangerous}")

    for result in results:
        emoji, meaning = LEVEL_INFO[result["level"]]
        users = ", ".join(result["users"])
        print("-" * 56)
        print(f"{emoji} {result['ip']}   {result['score']}/100   {result['level']}")
        print(f"   [{make_bar(result['score'])}]")
        print(f"   {meaning}")
        print(f"   Failed: {result['count']} | Users tried: {users} | Over: {result['duration']}s")

        if result["red_flags"]:
            for text, points in result["red_flags"]:
                print(f"   🚩 {text} (+{points})")
        else:
            print("   ✅ No red flags")

    print("=" * 56)

    if dangerous:
        print("💡 What a defender would do next:")
        print("   - Block the dangerous IP(s) at the firewall")
        print("   - Check if any login from that IP was Accepted")
        print("   - Use strong passwords or key-based login")
        print("   - Add automatic blocking (for example fail2ban)")
    print()


def analyze_file(filename):
    lines = read_log(filename)
    if not lines:
        return
    entries = parse_log(lines)
    results = analyze_all(group_failures(entries))
    show_report(results, len(lines), len(entries))


def confirm_permission():
    print("⚠️  Only analyze logs from systems you own or have permission to test.")
    answer = input("Type YES to confirm you have permission: ").strip()
    return answer == "YES"


def main():
    print("🕵️  FAILED-LOGIN LOG ANALYZER")
    print("Finds brute-force attacks in server logs.")
    print("This tool only reads log files. It never changes them.\n")

    while True:
        print("1. 📄 Create fake sample log")
        print("2. 🔍 Analyze the sample log")
        print("3. 📂 Analyze my own log file")
        print("4. 🚪 Quit")
        choice = input("Choose 1-4: ").strip()

        if choice == "1":
            create_sample_log()
        elif choice == "2":
            analyze_file(LOG_FILE)
        elif choice == "3":
            if confirm_permission():
                filename = input("Log file path: ").strip().strip('"')
                analyze_file(filename)
            else:
                print("Cancelled. Permission not confirmed.\n")
        elif choice == "4":
            print("Stay safe out there! 🛡️")
            break
        else:
            print("Please choose 1, 2, 3 or 4.\n")


if __name__ == "__main__":
    main()