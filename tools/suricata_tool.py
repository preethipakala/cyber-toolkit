#!/usr/bin/env python3
"""
suricata_tool.py — Wrapper for Suricata IDS/IPS/NSM.

Suricata is a high-performance, open source Network Security Monitor
that functions as:
  - IDS  (Intrusion Detection System)  — detects attacks passively
  - IPS  (Intrusion Prevention System) — blocks attacks inline
  - NSM  (Network Security Monitor)    — full packet capture + logging

Key features:
  - Multi-threaded, handles high-speed networks (10+ Gbps)
  - Lua scripting for custom detection logic
  - Outputs: EVE JSON, PCAP, unified2 (compatible with Wazuh/ELK)
  - Compatible with Snort rules (large community ruleset)

Install:
  sudo apt install suricata
  sudo suricata-update   # Download latest threat rules
"""

from tools.base import BaseTool
from utils.reporter import print_section


class SuricataTool(BaseTool):
    name         = "suricata"
    display_name = "Suricata — IDS / IPS / Network Monitor"
    binary       = "suricata"
    install_hint = "sudo apt install suricata && sudo suricata-update"

    EVE_LOG = "/var/log/suricata/eve.json"

    def run(self, action: str = "status", iface: str = "eth0", pcap: str = "") -> str:
        if action == "status":
            return self._service_status()
        if action == "test":
            return self._test_config()
        if action == "update":
            return self._update_rules()
        if action == "live":
            return self._live_capture(iface)
        if action == "pcap" and pcap:
            return self._analyze_pcap(pcap)
        if action == "tail":
            return self._tail_alerts()
        return ""

    def _service_status(self) -> str:
        return self.run_command(["sudo", "systemctl", "status", "suricata"])

    def _test_config(self) -> str:
        """Validate the suricata.yaml config file."""
        print_section("Suricata Config Test")
        return self.run_command(["sudo", "suricata", "-T", "-v"])

    def _update_rules(self) -> str:
        """Download latest Suricata rules via suricata-update."""
        print_section("Updating Suricata Rules")
        return self.run_command(["sudo", "suricata-update"])

    def _live_capture(self, iface: str) -> str:
        """Start Suricata in live capture mode on a network interface."""
        print_section(f"Live Capture on {iface}")
        return self.run_command(["sudo", "suricata", "-i", iface])

    def _analyze_pcap(self, pcap_file: str) -> str:
        """Run Suricata against an existing PCAP file."""
        print_section(f"Analyzing PCAP: {pcap_file}")
        return self.run_command(["sudo", "suricata", "-r", pcap_file, "-l", "/tmp/suricata_out"])

    def _tail_alerts(self) -> str:
        """Show the latest EVE JSON alerts."""
        print_section("Suricata Recent Alerts (EVE JSON)")
        return self.run_command(["sudo", "tail", "-n", "20", self.EVE_LOG])

    def interactive(self):
        print("\n  [Suricata] IDS / IPS / Network Security Monitor")
        print("  Actions: status | test | update | live | pcap | tail")
        action = input("  Action [status]: ").strip() or "status"
        iface  = ""
        pcap   = ""
        if action == "live":
            iface = input("  Interface [eth0]: ").strip() or "eth0"
        if action == "pcap":
            pcap = input("  Path to PCAP file: ").strip()
        self.run(action=action, iface=iface, pcap=pcap)

    def run_from_args(self, args):
        self.run(
            action=getattr(args, "action", "status"),
            iface=getattr(args, "iface", "eth0"),
            pcap=getattr(args, "pcap", "")
        )
