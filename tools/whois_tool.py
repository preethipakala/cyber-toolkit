#!/usr/bin/env python3
"""
whois_tool.py — Built-in WHOIS domain lookup.

WHOIS queries tell you:
- Who owns a domain (registrant info)
- When it was registered / expires
- Name servers (useful for DNS recon)
- Registrar information

This module uses Python's socket library — no external tool needed.
"""

import socket
from tools.base import BaseTool
from utils.reporter import print_section, print_error

WHOIS_PORT = 43
WHOIS_SERVER = "whois.iana.org"


class WhoisTool(BaseTool):
    name         = "whois"
    display_name = "WHOIS — Domain Lookup"
    binary       = "whois"   # May use system whois if available
    install_hint = "sudo apt install whois  (or use built-in Python fallback)"

    def run(self, domain: str) -> str:
        print_section(f"WHOIS lookup: {domain}")
        # Try system whois first, fall back to raw socket
        import shutil
        if shutil.which("whois"):
            return self.run_command(["whois", domain])
        else:
            return self._socket_whois(domain)

    def _socket_whois(self, domain: str) -> str:
        """Raw socket WHOIS query fallback."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(10)
                s.connect((WHOIS_SERVER, WHOIS_PORT))
                s.sendall((domain + "\r\n").encode())
                response = b""
                while True:
                    chunk = s.recv(4096)
                    if not chunk:
                        break
                    response += chunk
            result = response.decode("utf-8", errors="ignore")
            print(result)
            return result
        except Exception as e:
            print_error(f"WHOIS query failed: {e}")
            return ""

    def interactive(self):
        print("\n  [WHOIS] Domain Lookup")
        domain = input("  Domain (e.g. example.com): ").strip()
        self.run(domain=domain)

    def run_from_args(self, args):
        self.run(domain=args.domain)
