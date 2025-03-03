# Port Scanner

## Overview

This project is a **Python-based port scanner** designed for security testing and network diagnostics. It supports multiple scanning modes, detects open ports, and identifies running services. The scanner also measures **response times** to help detect firewalls or filtering mechanisms.

### 🔹 **Key Features**
- **Quick Scan, Full Scan, Custom Scan, and Default Scan** ([Wiki Explanation](https://github.com/Santiago-Olivera/port-scanner/wiki/Quick-Scan-,-Full-Scan,-Custom-Scan,-Default-Scan))
- **Parallel Port Scanning** for speed optimization ([Wiki Explanation](https://github.com/Santiago-Olivera/port-scanner/wiki/Parallel-Port-Scanning))
- **Response Time Analysis & Port Classification** ([Wiki Explanation](https://github.com/Santiago-Olivera/port-scanner/wiki/Response-Time-and-Port-Classification))
- **Running Services Detection** using Python’s built-in socket module ([Wiki Explanation](https://github.com/Santiago-Olivera/port-scanner/wiki/Running-Services-Detection))
- **Export Results** in JSON or CSV ([Wiki Explanation](https://github.com/Santiago-Olivera/port-scanner/wiki/Quick-Scan-,-Full-Scan,-Custom-Scan,-Default-Scan#exporting-results))
- **Exception Handling** for better stability

For more details about **what ports are, why to scan them, and a breakdown of the project**, visit the **[Home Wiki Page](https://github.com/Santiago-Olivera/port-scanner/wiki)**.

---

## 🛠 Installation

### Prerequisites
Ensure **Python 3** is installed. Check using:
```sh
python --version
```

### Setup
Clone the repository and install dependencies:
```sh
git clone https://github.com/Santiago-Olivera/port-scanner.git
cd port-scanner
python -m venv venv
source venv/bin/activate  # Windows: `venv\Scripts\activate`
pip install -r requirements.txt
```

---

## 🚀 Usage

Run the scanner using different scanning modes:

### **1️⃣ Quick Scan (Common Ports)**
```
Usage: python src/scanner.py <target_ip> --quick
Example: python src/scanner.py scanme.nmap.org --quick
```
Scans common ports only.

### **2️⃣ Full Scan (All Ports)**
```
Usage: python src/scanner.py <target_ip> 1 65535
Example: python src/scanner.py scanme.nmap.org 1 65535
```
Scans **all** 65,535 ports.

### **3️⃣ Custom Scan (Defined Port Range)**
```
Usage: python src/scanner.py <target_ip> <start_port> <end_port>
Example: python src/scanner.py scanme.nmap.org 20 100
```
Scans ports **20 to 100**.

### **4️⃣ Default Scan**
```
Usage: python src/scanner.py <target_ip>
Example: python src/scanner.py scanme.nmap.org
```
Runs a **default scan** using a standard port list.

### **5️⃣ Parallel Port Scanning**
Uses threading to **speed up scanning**. Enabled by default.

### **6️⃣ Exporting Results**
Save scan results as JSON or CSV:
```
Usage: python src/scanner.py <target_ip> <start_port> <end_port> --json <filename>
Example: python src/scanner.py scanme.nmap.org 20 100 --json results.json

Usage: python src/scanner.py <target_ip> <start_port> <end_port> --csv <filename>
Example: python src/scanner.py scanme.nmap.org 20 100 --csv results.csv
```

---


## 📌 Future Enhancements
- [ ] Implementation of a **Web UI** for easier interaction


For more details, check the **[Wiki](https://github.com/Santiago-Olivera/port-scanner/wiki)**.
