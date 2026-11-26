"""
Day 8 - Port Scanner v2: Threading + Banner Grabbing
Part of the Cyber Toolkit (10-day build in public project)

What it does:
    Scans ports much faster using threads, and reads the "banner"
    (the greeting) that open ports send back.

Safety:
    Only scan your own computer (127.0.0.1) or systems you have
    written permission to test.

Ethical use only. Educational project.
"""

import socket
import time
from concurrent.futures import ThreadPoolExecutor

CONNECT_TIMEOUT = 0.5
BANNER_TIMEOUT = 1.0
MAX_THREADS = 200

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 135: "RPC", 139: "NetBIOS", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP",
    2121: "FTP-Alt", 2222: "SSH-Alt", 8080: "HTTP-Alt",
}

OLD_VERSION_HINTS = {
    "OpenSSH_7": "OpenSSH 7.x is an older version. Check CVE databases for known weaknesses.",
    "Apache/2.4.41": "Apache 2.4.41 is an older version. Check CVE databases for known weaknesses.",
}


def clean_banner(data):
    text = data.decode("utf-8", errors="ignore")
    text = text.strip().replace("\r\n", " | ").replace("\n", " | ")
    return text[:100]


def grab_banner(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(BANNER_TIMEOUT)
            sock.connect((host, port))

            try:
                data = sock.recv(1024)
            except socket.timeout:
                sock.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
                data = sock.recv(1024)

        return clean_banner(data)
    except OSError:
        return ""


def version_hint(banner):
    for text, hint in OLD_VERSION_HINTS.items():
        if text in banner:
            return hint
    return ""


def is_port_open(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(CONNECT_TIMEOUT)
        return sock.connect_ex((host, port)) == 0


def check_port(host, port):
    if is_port_open(host, port):
        return {
            "port": port,
            "service": COMMON_PORTS.get(port, "unknown"),
            "banner": grab_banner(host, port),
        }
    return None


def scan_ports_threaded(host, start, end):
    ports = range(start, end + 1)
    open_ports = []

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as pool:
        results = pool.map(lambda port: check_port(host, port), ports)
        for result in results:
            if result:
                open_ports.append(result)

    return open_ports


def scan_ports_slow(host, start, end):
    open_ports = []

    for port in range(start, end + 1):
        result = check_port(host, port)
        if result:
            open_ports.append(result)

    return open_ports


def compare_speed(host, start, end):
    total = end - start + 1

    print(f"🐢 Slow scan (one port at a time) of {total} ports...")
    begin = time.time()
    scan_ports_slow(host, start, end)
    slow_time = time.time() - begin
    print(f"   Done in {slow_time:.1f}s\n")

    print(f"⚡ Fast scan ({MAX_THREADS} workers at once) of {total} ports...")
    begin = time.time()
    scan_ports_threaded(host, start, end)
    fast_time = time.time() - begin
    print(f"   Done in {fast_time:.1f}s\n")

    speedup = slow_time / max(fast_time, 0.01)
    print(f"🚀 Threading was about {speedup:.0f}x faster\n")


def show_report(host, found, elapsed, start, end):
    print()
    print("=" * 56)
    print("🔎 PORT SCAN REPORT")
    print("=" * 56)
    print(f"🎯 Target: {host} | Ports: {start}-{end} | Time: {elapsed:.1f}s")

    if not found:
        print("✅ No open ports found in this range.")
    else:
        print(f"🚪 Open ports: {len(found)}\n")
        for item in found:
            print(f"🟢 Port {item['port']} ({item['service']})")
            print(f"   🏷️  Banner: {item['banner'] or '(none)'}")
            hint = version_hint(item["banner"])
            if hint:
                print(f"   🚩 {hint}")

    print("=" * 56)
    print("💡 Banners can reveal software versions. Defenders can hide or update them.\n")


def confirm_permission():
    print("⚠️  Only scan systems you own or have written permission to test.")
    answer = input("Type YES to confirm you have permission: ").strip()
    return answer == "YES"


def ask_number(text, low, high):
    while True:
        try:
            value = int(input(text).strip())
        except ValueError:
            print("Please type a number.")
            continue

        if low <= value <= high:
            return value
        print(f"Please choose a number from {low} to {high}.")


def run_scan():
    host = input("Target (press Enter for 127.0.0.1): ").strip() or "127.0.0.1"

    if host not in ("127.0.0.1", "localhost") and not confirm_permission():
        print("Cancelled. Permission not confirmed.\n")
        return

    try:
        socket.gethostbyname(host)
    except socket.gaierror:
        print("❌ Could not find that host.\n")
        return

    start = ask_number("Start port (1-65535): ", 1, 65535)
    end = ask_number("End port (1-65535): ", start, 65535)

    print(f"\n⚡ Scanning {host} ports {start}-{end} with {MAX_THREADS} workers...")
    begin = time.time()
    found = scan_ports_threaded(host, start, end)
    show_report(host, found, time.time() - begin, start, end)


def main():
    print("⚡ PORT SCANNER v2 (Threads + Banner Grabbing)")
    print("Tip: run fake_service.py in another terminal to practise safely.\n")

    while True:
        print("1. 🔎 Scan ports (fast, with banners)")
        print("2. ⏱️  Speed test: slow vs fast (localhost only)")
        print("3. 🚪 Quit")
        choice = input("Choose 1-3: ").strip()

        if choice == "1":
            run_scan()
        elif choice == "2":
            print("This takes about a minute because the slow scan is slow on purpose.\n")
            compare_speed("127.0.0.1", 2100, 2250)
        elif choice == "3":
            print("Stay safe out there! 🛡️")
            break
        else:
            print("Please choose 1, 2 or 3.\n")


if __name__ == "__main__":
    main()