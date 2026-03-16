#!/usr/bin/env python3
"""
toolkit.py — Cyber Toolkit main CLI entry point.

Usage:
    python toolkit.py                              # Interactive menu
    python toolkit.py nmap --target 127.0.0.1
    python toolkit.py nikto --target http://localhost
    python toolkit.py whois --domain example.com
    python toolkit.py sslcheck --domain example.com
    python toolkit.py gobuster --url http://localhost --wordlist data/wordlist.txt
    python toolkit.py sqlmap --url "http://site.com/page?id=1"
    python toolkit.py hashcat --hash <hash> --mode 0

    # SIEM tools
    python toolkit.py wazuh --action status
    python toolkit.py suricata --action tail
    python toolkit.py zeek --action log --log-type dns
    python toolkit.py elk --action health
    python toolkit.py elk --action indices
"""

import argparse
import sys
from utils.reporter import print_banner, print_menu
from utils.checker import check_all_tools

from tools.nmap_tool      import NmapTool
from tools.nikto_tool     import NiktoTool
from tools.sqlmap_tool    import SQLMapTool
from tools.hashcat_tool   import HashcatTool
from tools.gobuster_tool  import GobusterTool
from tools.whois_tool     import WhoisTool
from tools.ssl_tool       import SSLTool

# SIEM tools
from tools.wazuh_tool     import WazuhTool
from tools.suricata_tool  import SuricataTool
from tools.zeek_tool      import ZeekTool
from tools.elk_tool       import ELKTool

TOOLS = {
    # --- Penetration Testing ---
    "nmap":      NmapTool,
    "nikto":     NiktoTool,
    "sqlmap":    SQLMapTool,
    "hashcat":   HashcatTool,
    "gobuster":  GobusterTool,
    "whois":     WhoisTool,
    "sslcheck":  SSLTool,
    # --- SIEM / Monitoring ---
    "wazuh":     WazuhTool,
    "suricata":  SuricataTool,
    "zeek":      ZeekTool,
    "elk":       ELKTool,
}

# Group tools for display
TOOL_GROUPS = {
    "🔍 Penetration Testing": ["nmap", "nikto", "sqlmap", "hashcat", "gobuster", "whois", "sslcheck"],
    "🛡️  SIEM / Monitoring":  ["wazuh", "suricata", "zeek", "elk"],
}


def interactive_menu():
    """Show an interactive numbered menu to select and run a tool."""
    print_banner()
    check_all_tools()

    menu_items = list(TOOLS.items())
    print_menu(menu_items, TOOL_GROUPS)

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
        description="🛡️  Cyber Toolkit — Unified open source security + SIEM tool launcher"
    )
    subparsers = parser.add_subparsers(dest="tool")

    # --- Pentest tools ---
    p = subparsers.add_parser("nmap", help="Network port scanner")
    p.add_argument("--target",  required=True)
    p.add_argument("--profile", default="standard", choices=["quick", "standard", "full", "vuln"])

    p = subparsers.add_parser("nikto", help="Web server vulnerability scanner")
    p.add_argument("--target", required=True)

    p = subparsers.add_parser("sqlmap", help="SQL injection scanner")
    p.add_argument("--url", required=True)

    p = subparsers.add_parser("hashcat", help="Password hash cracker")
    p.add_argument("--hash", required=True)
    p.add_argument("--mode", default="0")
    p.add_argument("--wordlist", default="data/wordlist.txt")

    p = subparsers.add_parser("gobuster", help="Directory brute-forcer")
    p.add_argument("--url", required=True)
    p.add_argument("--wordlist", default="data/wordlist.txt")

    p = subparsers.add_parser("whois", help="Domain WHOIS lookup")
    p.add_argument("--domain", required=True)

    p = subparsers.add_parser("sslcheck", help="SSL/TLS certificate analyzer")
    p.add_argument("--domain", required=True)

    # --- SIEM tools ---
    p = subparsers.add_parser("wazuh", help="Wazuh SIEM/XDR platform")
    p.add_argument("--action", default="status",
                   choices=["status", "start", "stop", "restart", "tail", "agents"],
                   help="Wazuh action (default: status)")

    p = subparsers.add_parser("suricata", help="Suricata IDS/IPS/NSM")
    p.add_argument("--action", default="status",
                   choices=["status", "test", "update", "live", "pcap", "tail"],
                   help="Suricata action (default: status)")
    p.add_argument("--iface",  default="eth0", help="Network interface for live capture")
    p.add_argument("--pcap",   default="",     help="PCAP file path for offline analysis")

    p = subparsers.add_parser("zeek", help="Zeek network analysis framework")
    p.add_argument("--action",   default="status",
                   choices=["status", "live", "pcap", "log", "logs"],
                   help="Zeek action (default: status)")
    p.add_argument("--iface",    default="eth0", help="Network interface for live capture")
    p.add_argument("--pcap",     default="",     help="PCAP file for analysis")
    p.add_argument("--log-type", default="conn",
                   choices=["conn", "dns", "http", "ssl", "files", "notice", "weird"],
                   help="Zeek log type to display (default: conn)")

    p = subparsers.add_parser("elk", help="ELK Stack SIEM (Elasticsearch/Logstash/Kibana)")
    p.add_argument("--action", default="health",
                   choices=["health", "indices", "kibana", "ingest", "search"],
                   help="ELK action (default: health)")
    p.add_argument("--es-url", default="http://localhost:9200", help="Elasticsearch URL")
    p.add_argument("--kb-url", default="http://localhost:5601", help="Kibana URL")
    p.add_argument("--index",  default="",  help="Index name for search action")

    return parser


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()

    if args.tool:
        run_subcommand(args)
    else:
        interactive_menu()
