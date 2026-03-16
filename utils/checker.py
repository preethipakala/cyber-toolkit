#!/usr/bin/env python3
"""
checker.py — Check which security tools are installed on the system.
"""

import shutil

GREEN = "\033[92m"
RED   = "\033[91m"
RESET = "\033[0m"
BOLD  = "\033[1m"

TOOLS = [
    ("nmap",      "sudo apt install nmap"),
    ("nikto",     "sudo apt install nikto"),
    ("sqlmap",    "sudo apt install sqlmap  OR  pip install sqlmap"),
    ("hashcat",   "sudo apt install hashcat"),
    ("gobuster",  "sudo apt install gobuster"),
    ("whois",     "sudo apt install whois  (optional — Python fallback available)"),
    ("openssl",   "sudo apt install openssl  (optional — Python built-in used)"),
]


def check_all_tools():
    """Print a table showing which tools are installed vs missing."""
    print(f"\n  {'Tool':<12} {'Status':<12} {'Install':<45}")
    print(f"  {'─'*12} {'─'*12} {'─'*45}")
    for binary, hint in TOOLS:
        found = shutil.which(binary) is not None
        status = f"{GREEN}✓ installed{RESET}" if found else f"{RED}✗ missing  {RESET}"
        install = "" if found else hint
        print(f"  {BOLD}{binary:<12}{RESET} {status}  {install}")
    print()
