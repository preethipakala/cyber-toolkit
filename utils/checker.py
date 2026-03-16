#!/usr/bin/env python3
"""
checker.py — Check which security tools are installed on the system.
"""

import shutil

GREEN = "\033[92m"
RED   = "\033[91m"
CYAN  = "\033[96m"
RESET = "\033[0m"
BOLD  = "\033[1m"

PENTEST_TOOLS = [
    ("nmap",      "sudo apt install nmap"),
    ("nikto",     "sudo apt install nikto"),
    ("sqlmap",    "sudo apt install sqlmap"),
    ("hashcat",   "sudo apt install hashcat"),
    ("gobuster",  "sudo apt install gobuster"),
    ("whois",     "sudo apt install whois"),
    ("openssl",   "sudo apt install openssl"),
]

SIEM_TOOLS = [
    ("wazuh-control", "https://documentation.wazuh.com/current/installation-guide/"),
    ("suricata",      "sudo apt install suricata && sudo suricata-update"),
    ("zeek",          "sudo apt install zeek"),
    ("elasticsearch", "https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html"),
    ("filebeat",      "sudo apt install filebeat"),
]


def _print_group(title: str, tools: list):
    print(f"\n  {BOLD}{CYAN}{title}{RESET}")
    print(f"  {'Tool':<18} {'Status':<14} {'Install':<50}")
    print(f"  {'─'*18} {'─'*14} {'─'*50}")
    for binary, hint in tools:
        found  = shutil.which(binary) is not None
        status = f"{GREEN}✓ installed{RESET}" if found else f"{RED}✗ missing  {RESET}"
        install = "" if found else hint
        print(f"  {BOLD}{binary:<18}{RESET} {status}  {install}")


def check_all_tools():
    """Print a grouped table showing installed vs missing tools."""
    _print_group("Penetration Testing Tools", PENTEST_TOOLS)
    _print_group("SIEM / Monitoring Tools",   SIEM_TOOLS)
    print()
