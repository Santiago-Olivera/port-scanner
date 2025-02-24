import socket
import argparse
from utils import print_status

# Dictionary mapping common ports to their services
COMMON_PORTS = {
    20: "FTP",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    5900: "VNC",
    8080: "HTTP-Proxy"
}

def get_service(port):
    """Returns the service name for a given port using the socket library."""
    try:
        return socket.getservbyport(port, "tcp")
    except OSError:
        return "Unknown"


def scan_port(ip, port):
    """Attempts to connect to a given port on a target IP."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # Timeout for connection attempt
            result = s.connect_ex((ip, port))  # Returns 0 if open
            service = get_service(port)
            if result == 0:
                print_status(f"[OPEN] Port {port} ({service}) is open", "success")
            else:
                print_status(f"[CLOSED] Port {port} ({service}) is closed", "warning")
    except Exception as e:
        print_status(f"Error scanning port {port}: {e}", "error")

def scan(target, start_port, end_port):
    """Scans ports in the specified range for a given IP."""
    print_status(f"Scanning {target} from port {start_port} to {end_port}...", "info")
    
    for port in range(start_port, end_port + 1):
        scan_port(target, port)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Port Scanner")
    parser.add_argument("target", help="Target IP address to scan")
    parser.add_argument("start_port", type=int, help="Start of port range")
    parser.add_argument("end_port", type=int, help="End of port range")

    args = parser.parse_args()
    scan(args.target, args.start_port, args.end_port)