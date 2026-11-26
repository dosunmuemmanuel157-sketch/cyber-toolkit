"""
Day 8 - Fake services for testing the port scanner.

Runs 3 pretend services on YOUR OWN computer (127.0.0.1 only).
Nothing here is reachable from outside your PC.

Ethical use only. Educational project.
"""

import socket
import threading
import time


FAKE_SERVICES = {
    2222: "SSH-2.0-OpenSSH_7.2 (fake)\r\n",
    2121: "220 FakeFTP 1.0 ready\r\n",
    8080: "HTTP/1.1 200 OK\r\nServer: Apache/2.4.41 (fake)\r\n\r\n",
}

def run_fake_service(port, banner):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", port))
    server.listen()


    while True:
        client, address = server.accept()
        client.sendall(banner.encode())
        client.close()


def main():
    print("🧪 Starting fake services on 127.0.0.1 (your own computer only)")

    for port, banner in FAKE_SERVICES.items():
        thread = threading.Thread(target=run_fake_service, args=(port, banner), daemon=True)
        thread.start()
        print(f"   ✅ Port {port} is now listening")

    print("Leave this window open. Press Ctrl+C to stop.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
            print("\nStopped. Bye!")
    
    
if __name__ == "__main__":
    main()