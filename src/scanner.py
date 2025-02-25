import socket
import time
import concurrent.futures
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils import print_status

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

def scan_ports(target, start_port, end_port):
    closed_ports = []
    results = []
    
    with ThreadPoolExecutor(max_workers=100) as executor:
        future_to_port = {executor.submit(scan_port, target, port): port for port in range(start_port, end_port + 1)}
        for future in as_completed(future_to_port):
            result = future.result()
            if isinstance(result, tuple):  # Closed port
                closed_ports.append(result)
            else:
                results.append(result)
    
    # Identify potential filtering
    if closed_ports:
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
    parser.add_argument("start_port", type=int, help="Start of port range")
    parser.add_argument("end_port", type=int, help="End of port range")
    
    args = parser.parse_args()
    print_status(f"Scanning {args.target} from port {args.start_port} to {args.end_port}...", "info")
    print(scan_ports(args.target, args.start_port, args.end_port))
