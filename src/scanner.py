import socket  # Provides low-level networking interface
import time  # Used to measure response times
import concurrent.futures  # Enables concurrent execution
import argparse  # Handles command-line arguments
import json  # Supports exporting results in JSON format
import csv  # Supports exporting results in CSV format
from concurrent.futures import ThreadPoolExecutor, as_completed  # For multithreading
from utils import print_status  # Custom utility function for status messages

# List of common ports for quick scanning
COMMON_PORTS = [22, 80, 443, 3389, 445, 8080, 8443, 53, 25, 110, 143, 587, 993, 995]

def get_service(port):
    """Returns the service name for a given port using the socket library."""
    try:
        return socket.getservbyport(port, "tcp")  # Get service name for the port
    except OSError:
        return "Unknown"  # If not found, return "Unknown"

def scan_port(target, port):
    """Attempts to connect to a specific port and determine if it is open or closed."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # Create a TCP socket
        s.settimeout(1)  # Set timeout to 1 second to avoid long waits
        start_time = time.time()  # Record start time for response time calculation
        result = s.connect_ex((target, port))  # Try to connect; returns 0 if successful
        response_time = (time.time() - start_time) * 1000  # Calculate response time in ms
        service = get_service(port)  # Get the service running on this port

        if result == 0:
            return {"port": port, "status": "open", "service": service, "response_time": response_time}
        else:
            return {"port": port, "status": "closed", "service": service, "response_time": response_time}

def scan_ports(target, start_port, end_port, quick_scan):
    """Scans multiple ports concurrently and returns results."""
    results = []  # Store scan results
    ports_to_scan = COMMON_PORTS if quick_scan else list(range(start_port, end_port + 1))  # Choose ports to scan
    
    with ThreadPoolExecutor(max_workers=100) as executor:  # Use 100 threads for parallel scanning
        future_to_port = {executor.submit(scan_port, target, port): port for port in ports_to_scan}  # Submit tasks
        for future in as_completed(future_to_port):  # Process results as they complete
            results.append(future.result())  # Store result in the list
    
    results.sort(key=lambda x: x["port"])  # Ensure results are sorted by port number
    return results  # Return the list of scanned ports

def export_results(results, file_format, filename):
    """Exports scan results to a file in JSON or CSV format."""
    if file_format == "json":
        with open(filename, "w") as f:
            json.dump(results, f, indent=4)  # Write results to JSON file
    elif file_format == "csv":
        with open(filename, "w", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["port", "status", "service", "response_time"])
            writer.writeheader()  # Write CSV header
            writer.writerows(results)  # Write scan results

if __name__ == "__main__":
    """Main entry point: Parses arguments and executes the scan."""
    parser = argparse.ArgumentParser(description="Simple Port Scanner")
    parser.add_argument("target", help="Target IP address to scan")  # Target IP or hostname
    parser.add_argument("start_port", type=int, nargs='?', default=1, help="Start of port range")  # Start port (default: 1)
    parser.add_argument("end_port", type=int, nargs='?', default=65535, help="End of port range")  # End port (default: 65535)
    parser.add_argument("--quick", action="store_true", help="Perform a quick scan of common ports")  # Quick scan flag
    parser.add_argument("--json", type=str, help="Export results to a JSON file")  # JSON export flag
    parser.add_argument("--csv", type=str, help="Export results to a CSV file")  # CSV export flag
    
    args = parser.parse_args()  # Parse command-line arguments
    
    if args.quick:
        print_status(f"Performing a quick scan on {args.target} for common ports...", "info")  # Notify user
        scan_results = scan_ports(args.target, None, None, quick_scan=True)  # Run quick scan
    else:
        print_status(f"Scanning {args.target} from port {args.start_port} to {args.end_port}...", "info")  # Notify user
        scan_results = scan_ports(args.target, args.start_port, args.end_port, quick_scan=False)  # Run full scan
    
    for result in scan_results:  # Loop through scan results
        status_color = "\033[92m" if result["status"] == "open" else "\033[93m"  # Green for open, yellow for closed
        print(f"{status_color}[{result['status'].upper()}] Port {result['port']} ({result['service']}) - Response Time: {result['response_time']:.2f}ms\033[0m")  # Print result
    
    if args.json:
        export_results(scan_results, "json", args.json)  # Save results to JSON file
        print(f"\033[94mResults saved to {args.json} (JSON format)\033[0m")  # Notify user
    if args.csv:
        export_results(scan_results, "csv", args.csv)  # Save results to CSV file
        print(f"\033[94mResults saved to {args.csv} (CSV format)\033[0m")  # Notify user
