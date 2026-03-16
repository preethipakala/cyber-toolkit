#!/usr/bin/env python3
"""
toolkit.py — Cyber Toolkit main CLI entry point.

Provides an interactive menu OR direct subcommand access to each security tool.

Usage:
    python toolkit.py                             # Interactive menu
    python toolkit.py nmap --target 127.0.0.1
    python toolkit.py nikto --target http://localhost
    python toolkit.py whois --domain example.com
    python toolkit.py sslcheck --domain example.com
    python toolkit.py gobuster --url http://localhost --wordlist data/wordlist.txt
    python toolkit.py sqlmap --url "http://site.com/page?id=1"
    python toolkit.py hashcat --hash <hash> --mode 0
"""

import argparse
import sys
from utils.reporter import print_banner, print_menu
from utils.checker import check_all_tools

from tools.nmap_tool     import NmapTool
from tools.nikto_tool    import NiktoTool
from tools.sqlmap_tool   import SQLMapTool
from tools.hashcat_tool  import HashcatTool
from tools.gobuster_tool import GobusterTool
from tools.whois_tool    import WhoisTool
from tools.ssl_tool      import SSLTool

TOOLS = {
    "nmap":      NmapTool,
    "nikto":     NiktoTool,
    "sqlmap":    SQLMapTool,
    "hashcat":   HashcatTool,
    "gobuster":  GobusterTool,
    "whois":     WhoisTool,
    "sslcheck":  SSLTool,
}


def interactive_menu():
    """Show an interactive numbered menu to select and run a tool."""
    print_banner()
    check_all_tools()

    menu_items = list(TOOLS.items())
    print_menu(menu_items)

    try:
        choice = int(input("\n  Select a tool [1-{}]: ".format(len(menu_items)))) - 1
        if choice < 0 or choice >= len(menu_items):
            print("[!] Invalid selection.")
            sys.exit(1)
    except (ValueError, KeyboardInterrupt):
        print("\n[!] Exiting.")
        sys.exit(0)

    name, tool_class = menu_items[choice]
    tool = tool_class()
    tool.interactive()


def run_subcommand(args):
    """Run a specific tool from CLI subcommand."""
    tool_class = TOOLS.get(args.tool)
    if not tool_class:
        print(f"[!] Unknown tool: {args.tool}")
        sys.exit(1)
    tool = tool_class()
    tool.run_from_args(args)


def build_parser():
    parser = argparse.ArgumentParser(
        description="🛡️  Cyber Toolkit — Unified open source security tool launcher"
    )
    subparsers = parser.add_subparsers(dest="tool")

    # nmap
    p = subparsers.add_parser("nmap", help="Network port scanner")
    p.add_argument("--target",  required=True, help="IP address or hostname")
    p.add_argument("--profile", default="standard",
                   choices=["quick", "standard", "full", "vuln"],
                   help="Scan profile (default: standard)")

    # nikto
    p = subparsers.add_parser("nikto", help="Web server vulnerability scanner")
    p.add_argument("--target", required=True, help="Target URL (e.g. http://localhost)")

    # sqlmap
    p = subparsers.add_parser("sqlmap", help="SQL injection scanner")
    p.add_argument("--url", required=True, help="Target URL with parameters")

    # hashcat
    p = subparsers.add_parser("hashcat", help="Password hash cracker")
    p.add_argument("--hash", required=True, help="Hash to crack")
    p.add_argument("--mode", default="0",   help="Hash mode (0=MD5, 100=SHA1, 1800=SHA512)")
    p.add_argument("--wordlist", default="data/wordlist.txt", help="Wordlist file path")

    # gobuster
    p = subparsers.add_parser("gobuster", help="Directory brute-forcer")
    p.add_argument("--url",      required=True, help="Target URL")
    p.add_argument("--wordlist", default="data/wordlist.txt", help="Wordlist file")

    # whois
    p = subparsers.add_parser("whois", help="Domain WHOIS lookup")
    p.add_argument("--domain", required=True, help="Domain name (e.g. example.com)")

    # sslcheck
    p = subparsers.add_parser("sslcheck", help="SSL/TLS certificate analyzer")
    p.add_argument("--domain", required=True, help="Domain to check")

    return parser


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()

    if args.tool:
        run_subcommand(args)
    else:
        interactive_menu()
