#!/usr/bin/env python3
"""
zeek_tool.py — Wrapper for Zeek Network Security Monitor.

Zeek (formerly Bro) is a powerful open source network analysis framework.
Unlike Suricata (which is signature-based), Zeek is:
  - Script-driven — you define what to look for using Zeek's own language
  - Protocol-aware — deeply understands HTTP, DNS, SSL, SMB, FTP, etc.
  - Log-centric    — generates detailed structured logs for every connection

Zeek log types (written to /usr/local/zeek/logs/current/):
  conn.log     — every network connection (IP, port, bytes, duration)
  dns.log      — all DNS queries and responses
  http.log     — full HTTP request/response metadata
  ssl.log      — TLS handshake details, certificates
  files.log    — file transfers detected on the wire
  notice.log   — Zeek's own security notices / alerts
  weird.log    — unusual or anomalous protocol behavior

Install:
  sudo apt install zeek  OR  https://zeek.org/get-zeek/
"""

import os
from tools.base import BaseTool
from utils.reporter import print_section, print_warning

LOG_DIR = "/usr/local/zeek/logs/current"

LOG_FILES = {
    "conn":   "conn.log",
    "dns":    "dns.log",
    "http":   "http.log",
    "ssl":    "ssl.log",
    "files":  "files.log",
    "notice": "notice.log",
    "weird":  "weird.log",
}


class ZeekTool(BaseTool):
    name         = "zeek"
    display_name = "Zeek — Network Analysis Framework"
    binary       = "zeek"
    install_hint = "sudo apt install zeek  OR  https://zeek.org/get-zeek/"

    def run(self, action: str = "status", iface: str = "eth0",
            pcap: str = "", log_type: str = "conn") -> str:
        if action == "status":
            return self._service_status()
        if action == "live":
            return self._live_capture(iface)
        if action == "pcap" and pcap:
            return self._analyze_pcap(pcap)
        if action == "log":
            return self._show_log(log_type)
        if action == "logs":
            return self._list_logs()
        return ""

    def _service_status(self) -> str:
        return self.run_command(["zeekctl", "status"])

    def _live_capture(self, iface: str) -> str:
        """Start Zeek capturing live traffic on an interface."""
        print_section(f"Zeek Live Capture on {iface}")
        return self.run_command(["sudo", "zeek", "-i", iface, "local"])

    def _analyze_pcap(self, pcap_file: str) -> str:
        """Run Zeek analysis on a PCAP file."""
        print_section(f"Zeek PCAP Analysis: {pcap_file}")
        return self.run_command(["zeek", "-r", pcap_file, "local"])

    def _show_log(self, log_type: str) -> str:
        """Tail a specific Zeek log file."""
        filename = LOG_FILES.get(log_type)
        if not filename:
            print_warning(f"Unknown log type: {log_type}. Choose: {', '.join(LOG_FILES.keys())}")
            return ""
        path = os.path.join(LOG_DIR, filename)
        print_section(f"Zeek {log_type.upper()} Log")
        return self.run_command(["tail", "-n", "30", path])

    def _list_logs(self) -> str:
        """List available Zeek log files in the current log directory."""
        print_section(f"Zeek Logs in {LOG_DIR}")
        return self.run_command(["ls", "-lh", LOG_DIR])

    def interactive(self):
        print("\n  [Zeek] Network Analysis Framework")
        print("  Actions: status | live | pcap | log | logs")
        action = input("  Action [status]: ").strip() or "status"
        iface    = ""
        pcap     = ""
        log_type = "conn"
        if action == "live":
            iface = input("  Interface [eth0]: ").strip() or "eth0"
        elif action == "pcap":
            pcap = input("  PCAP file path: ").strip()
        elif action == "log":
            print(f"  Log types: {', '.join(LOG_FILES.keys())}")
            log_type = input("  Log type [conn]: ").strip() or "conn"
        self.run(action=action, iface=iface, pcap=pcap, log_type=log_type)

    def run_from_args(self, args):
        self.run(
            action=getattr(args, "action", "status"),
            iface=getattr(args, "iface", "eth0"),
            pcap=getattr(args, "pcap", ""),
            log_type=getattr(args, "log_type", "conn")
        )
