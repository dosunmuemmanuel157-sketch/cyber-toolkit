"""
Port Scanner
Day 4 of my 10-day Cyber Toolkit challenge.
Checks which ports are open on a computer.
ONLY scan machines you own or have written permission to test.
For educational use only.
"""

import socket
import time

COMMON_PORTS = {
    21: "FTP (file transfer)",
    22: "SSH (remote login)",
    23: "Telnet (old remote login)",
    25: "SMTP (email sending)",
    53: "DNS (name lookup)",
    80: "HTTP (website)",
    110: "POP3 (email)",
    135: "Windows RPC",
    139: "NetBIOS (Windows sharing)",
    443: "HTTPS (secure website)",
    445: "SMB (Windows file sharing)",
    3306: "MySQL (database)",
    3389: "RDP (Windows remote desktop)",
    8000: "HTTP dev server (Python)",
    8080: "HTTP alternate (web server)",
}


def is_port_open(host, port):
    """Return True if the port accepts a connection, otherwise False."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        result = sock.connect_ex((host, port))
    return result == 0


def scan_ports(host, start_port, end_port):
    """Scan a range of ports and return the list of open ones."""
    open_ports = []

    for port in range(start_port, end_port + 1):
        if is_port_open(host, port):
            open_ports.append(port)

    return open_ports


def confirm_permission(host):
    """Only scan your own machine, unless the user confirms permission."""
    if host in ("127.0.0.1", "localhost"):
        return True

    print("\nWARNING: Scanning computers you don't own can be illegal.")
    answer = input("Type YES only if you own this machine or have written permission: ")
    return answer == "YES"


def main():
    print("=" * 40)
    print("   PORT SCANNER")
    print("=" * 40)
    print("Only scan machines you own or have permission to test.\n")

    host = input("Host to scan (press Enter for 127.0.0.1): ").strip()
    if host == "":
        host = "127.0.0.1"

    if not confirm_permission(host):
        print("\nScan cancelled.")
        return

    try:
        start_port = int(input("Start port (e.g. 7990): "))
        end_port = int(input("End port (e.g. 8010): "))
    except ValueError:
        print("\nPorts must be numbers.")
        return

    if start_port < 1 or end_port > 65535 or start_port > end_port:
        print("\nInvalid range. Use ports 1-65535, start before end.")
        return

    print(f"\nScanning {host} ports {start_port}-{end_port}...")
    started = time.time()

    try:
        open_ports = scan_ports(host, start_port, end_port)
    except socket.gaierror:
        print("\nCould not find that host.")
        return

    elapsed = time.time() - started

    print("\n--- RESULTS ---")
    if open_ports:
        for port in open_ports:
            service = COMMON_PORTS.get(port, "unknown service")
            print(f"[OPEN] Port {port}: {service}")
    else:
        print("No open ports found in this range.")

    print(f"\nScanned {end_port - start_port + 1} ports in {elapsed:.1f} seconds.")


if __name__ == "__main__":
    main()