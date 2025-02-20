# Port Scanner

## Overview
This project is a simple port scanner written in Python. It allows users to:
- Scan a target IP or an IP range.
- Scan specific ports or all common ports.
- Indicate open ports and running services (HTTP, SSH, etc.).
- Include response times to detect firewalls/filters.
- Support fast and detailed scans.

The scanner utilizes the `socket` module for network communication and enhances output readability using `colorama`.

## Features
- Scan a target IP for open ports within a given range.
- Detect running services on open ports.
- Provide response times to help identify firewalls and filters.
- User-friendly colored output using `colorama`.
- Supports both fast and detailed scans.
- Handles exceptions and timeouts gracefully.

## Installation
### Prerequisites
Ensure you have Python installed on your system. You can check by running:
```sh
python --version
```

### Setup
Clone the repository and create a virtual environment:
```sh
git clone https://github.com/Santiago-Olivera/port-scanner.git
cd port-scanner
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

## Usage
Run the scanner by specifying the target IP and port range:
```sh
python src/scanner.py <target_ip> <start_port> <end_port>
```
Example:
```sh
python src/scanner.py scanme.nmap.org 20 100
```

## File Structure
```
port-scanner/
│── src/
│   ├── scanner.py         # Core scanning logic
│   ├── utils.py           # Utility functions
│   ├── __init__.py        # Marks it as a package
│── tests/                 # Future unit tests
│── docs/                  # Documentation
│── README.md              # Project overview
│── requirements.txt       # Dependencies
│── .gitignore             # Ignored files
```



