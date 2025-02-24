import socket
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils import print_status

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
                return (port, f"[OPEN] Port {port} ({service}) is open", "success")
            else:
                return (port, f"[CLOSED] Port {port} ({service}) is closed", "warning")
    except Exception as e:
        return (port, f"Error scanning port {port}: {e}", "error")

def scan(target, start_port, end_port):
    """Scans ports in the specified range for a given IP."""
    print_status(f"Scanning {target} from port {start_port} to {end_port}...", "info")
    
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(scan_port, target, port): port for port in range(start_port, end_port + 1)}
        results = []
        for future in as_completed(futures):
            results.append(future.result())
        
        # Sort results by port number
        results.sort(key=lambda x: x[0])
        
        # Print results in order
        for port, message, status in results:
            print_status(message, status)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Port Scanner")
    parser.add_argument("target", help="Target IP address to scan")
    parser.add_argument("start_port", type=int, help="Start of port range")
    parser.add_argument("end_port", type=int, help="End of port range")

    args = parser.parse_args()
    scan(args.target, args.start_port, args.end_port)