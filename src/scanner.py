import socket
import time
import concurrent.futures
import argparse
import json
import csv
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
            return {"port": port, "status": "open", "service": service, "response_time": response_time}
        else:
            return {"port": port, "status": "closed", "service": service, "response_time": response_time}

def scan_ports(target, start_port, end_port, quick_scan):
    results = []
    ports_to_scan = COMMON_PORTS if quick_scan else list(range(start_port, end_port + 1))
    
    with ThreadPoolExecutor(max_workers=100) as executor:
        future_to_port = {executor.submit(scan_port, target, port): port for port in ports_to_scan}
        for future in as_completed(future_to_port):
            results.append(future.result())
    
    results.sort(key=lambda x: x["port"])  # Ensure results are sorted by port number
    return results

def export_results(results, file_format, filename):
    if file_format == "json":
        with open(filename, "w") as f:
            json.dump(results, f, indent=4)
    elif file_format == "csv":
        with open(filename, "w", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["port", "status", "service", "response_time"])
            writer.writeheader()
            writer.writerows(results)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Port Scanner")
    parser.add_argument("target", help="Target IP address to scan")
    parser.add_argument("start_port", type=int, nargs='?', default=1, help="Start of port range")
    parser.add_argument("end_port", type=int, nargs='?', default=65535, help="End of port range")
    parser.add_argument("--quick", action="store_true", help="Perform a quick scan of common ports")
    parser.add_argument("--json", type=str, help="Export results to a JSON file")
    parser.add_argument("--csv", type=str, help="Export results to a CSV file")
    
    args = parser.parse_args()
    
    if args.quick:
        print_status(f"Performing a quick scan on {args.target} for common ports...", "info")
        scan_results = scan_ports(args.target, None, None, quick_scan=True)
    else:
        print_status(f"Scanning {args.target} from port {args.start_port} to {args.end_port}...", "info")
        scan_results = scan_ports(args.target, args.start_port, args.end_port, quick_scan=False)
    
    for result in scan_results:
        status_color = "\033[92m" if result["status"] == "open" else "\033[93m"
        print(f"{status_color}[{result['status'].upper()}] Port {result['port']} ({result['service']}) - Response Time: {result['response_time']:.2f}ms\033[0m")
    
    if args.json:
        export_results(scan_results, "json", args.json)
        print(f"\033[94mResults saved to {args.json} (JSON format)\033[0m")
    if args.csv:
        export_results(scan_results, "csv", args.csv)
        print(f"\033[94mResults saved to {args.csv} (CSV format)\033[0m")
