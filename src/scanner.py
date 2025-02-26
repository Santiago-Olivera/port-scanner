import socket
import time
import concurrent.futures
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils import print_status

COMMON_PORTS = [22, 80, 443, 3389, 445, 8080, 8443, 53, 25, 110, 143, 587, 993, 995]

def get_service(port):
    """Returns the service name for a given port using the socket library."""
    try:
        return socket.getservbyport(port, "tcp")
    except OSError:
        return "Unknown"

def scan_port(target, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        start_time = time.time()
        result = s.connect_ex((target, port))
        response_time = (time.time() - start_time) * 1000  # Convert to ms
        service = get_service(port)

        if result == 0:
            return f"\033[92m[OPEN] Port {port} ({service}) is open - Response Time: {response_time:.2f}ms\033[0m"
        else:
            return (port, response_time, service)

def scan_ports(target, start_port, end_port, quick_scan):
    closed_ports = []
    results = []
    
    ports_to_scan = COMMON_PORTS if quick_scan else list(range(start_port, end_port + 1))
    
    with ThreadPoolExecutor(max_workers=100) as executor:
        future_to_port = {executor.submit(scan_port, target, port): port for port in ports_to_scan}
        for future in as_completed(future_to_port):
            result = future.result()
            if isinstance(result, tuple):  # Closed port
                closed_ports.append(result)
            else:
                results.append(result)
    
    # Sort open ports
    results.sort()
    
    # Identify potential filtering
    if closed_ports:
        closed_ports.sort()  # Ensure closed ports are in order
        closed_response_times = [rt for _, rt, _ in closed_ports]
        if all(rt > 1000 for rt in closed_response_times):
            results.append("\033[93m\n[WARNING] All closed ports have response times >1000ms. This may indicate a firewall or filtering.\033[0m")
        
        # Show all closed ports after the warning
        for port, rt, service in closed_ports:
            if rt > 1000:
                results.append(f"\033[94m[FILTERED?] Port {port} ({service}) is possibly filtered - Response Time: {rt:.2f}ms\033[0m")
            else:
                results.append(f"\033[93m[CLOSED] Port {port} ({service}) is closed - Response Time: {rt:.2f}ms\033[0m")
    
    return "\n".join(results)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Port Scanner")
    parser.add_argument("target", help="Target IP address to scan")
    parser.add_argument("start_port", type=int, nargs='?', default=1, help="Start of port range")
    parser.add_argument("end_port", type=int, nargs='?', default=1024, help="End of port range (default: 1024)")
    parser.add_argument("--quick", action="store_true", help="Perform a quick scan of common ports")
    parser.add_argument("--full-scan", action="store_true", help="Scan the full range of 65535 ports")
    
    args = parser.parse_args()
    
    if args.full_scan:
        start_port, end_port = 1, 65535
    else:
        start_port, end_port = args.start_port, args.end_port
    
    if args.quick:
        print_status(f"Performing a quick scan on {args.target} for common ports...", "info")
        print(scan_ports(args.target, None, None, quick_scan=True))
    else:
        print_status(f"Scanning {args.target} from port {start_port} to {end_port}...", "info")
        print(scan_ports(args.target, start_port, end_port, quick_scan=False))
