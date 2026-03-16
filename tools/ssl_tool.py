#!/usr/bin/env python3
"""
ssl_tool.py — Built-in SSL/TLS certificate analyzer.

Checks:
- Certificate validity dates (is it expired?)
- Issuer and subject (who issued it?)
- Subject Alternative Names (what domains does it cover?)
- TLS protocol version supported

Uses Python's built-in ssl and socket modules — no external tool needed.
"""

import ssl
import socket
from datetime import datetime
from tools.base import BaseTool
from utils.reporter import print_section, print_error, print_success


class SSLTool(BaseTool):
    name         = "sslcheck"
    display_name = "SSL Check — Certificate Analyzer"
    binary       = "openssl"  # Optional; we use Python built-in
    install_hint = "No install needed — uses Python built-in ssl module"

    def run(self, domain: str, port: int = 443) -> str:
        print_section(f"SSL/TLS Check: {domain}:{port}")
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    self._print_cert(domain, cert, ssock.version())
                    return str(cert)
        except ssl.SSLCertVerificationError as e:
            print_error(f"Certificate verification failed: {e}")
        except ConnectionRefusedError:
            print_error(f"Connection refused — is port {port} open on {domain}?")
        except Exception as e:
            print_error(f"SSL check failed: {e}")
        return ""

    def _print_cert(self, domain: str, cert: dict, tls_version: str):
        """Display certificate details in a readable format."""
        subject  = dict(x[0] for x in cert.get("subject", []))
        issuer   = dict(x[0] for x in cert.get("issuer", []))
        not_after  = cert.get("notAfter", "")
        not_before = cert.get("notBefore", "")
        sans = [v for t, v in cert.get("subjectAltName", []) if t == "DNS"]

        # Parse expiry
        fmt = "%b %d %H:%M:%S %Y %Z"
        try:
            expiry = datetime.strptime(not_after, fmt)
            days_left = (expiry - datetime.utcnow()).days
            expiry_str = expiry.strftime("%Y-%m-%d")
            status = "✓ Valid" if days_left > 0 else "✗ EXPIRED"
            exp_label = f"{status} — {days_left} days remaining" if days_left > 0 else "EXPIRED"
        except Exception:
            expiry_str = not_after
            exp_label  = "(could not parse expiry)"

        print(f"  Domain      : {domain}")
        print(f"  TLS Version : {tls_version}")
        print(f"  Subject CN  : {subject.get('commonName', 'N/A')}")
        print(f"  Issuer      : {issuer.get('organizationName', 'N/A')}")
        print(f"  Valid From  : {not_before}")
        print(f"  Expires     : {expiry_str}  [{exp_label}]")
        if sans:
            print(f"  SANs        : {', '.join(sans[:5])}{'...' if len(sans) > 5 else ''}")

    def interactive(self):
        print("\n  [SSL Check] Certificate Analyzer")
        domain = input("  Domain (e.g. example.com): ").strip()
        self.run(domain=domain)

    def run_from_args(self, args):
        self.run(domain=args.domain)
