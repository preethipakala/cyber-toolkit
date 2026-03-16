#!/usr/bin/env python3
"""
wazuh_tool.py — Wrapper for Wazuh SIEM/XDR agent.

Wazuh is a free, open source SIEM and XDR platform that provides:
  - Real-time log analysis and correlation
  - File integrity monitoring (FIM)
  - Vulnerability detection
  - Active response to threats
  - Compliance reporting (PCI-DSS, HIPAA, GDPR)

Architecture:
  Wazuh Manager  <-- receives events from agents
  Wazuh Agent    <-- installed on endpoints, ships logs
  Wazuh Indexer  <-- stores & indexes events (OpenSearch)
  Wazuh Dashboard <-- visualize alerts (Kibana-based)

Install: https://documentation.wazuh.com/current/installation-guide/
  curl -sO https://packages.wazuh.com/4.7/wazuh-install.sh
  sudo bash wazuh-install.sh -a
"""

import subprocess
import shutil
from tools.base import BaseTool
from utils.reporter import print_section, print_error, print_warning


class WazuhTool(BaseTool):
    name         = "wazuh"
    display_name = "Wazuh — SIEM / XDR Platform"
    binary       = "wazuh-control"
    install_hint = "https://documentation.wazuh.com/current/installation-guide/"

    # Common Wazuh log locations
    ALERT_LOG  = "/var/ossec/logs/alerts/alerts.log"
    OSSEC_LOG  = "/var/ossec/logs/ossec.log"
    AGENT_CONF = "/var/ossec/etc/ossec.conf"

    def run(self, action: str = "status") -> str:
        """Control the Wazuh manager service or tail alerts."""
        if action == "tail":
            return self._tail_alerts()
        if action == "agents":
            return self._list_agents()
        if action in ("start", "stop", "status", "restart"):
            return self._service_control(action)
        print_warning(f"Unknown action: {action}. Use: status | start | stop | restart | tail | agents")
        return ""

    def _service_control(self, action: str) -> str:
        if not self.require_installed():
            return ""
        return self.run_command(["sudo", "wazuh-control", action])

    def _tail_alerts(self) -> str:
        """Stream the last 20 lines of the Wazuh alert log."""
        print_section("Wazuh Recent Alerts")
        if not shutil.which("tail"):
            print_error("tail command not found")
            return ""
        try:
            result = subprocess.run(
                ["sudo", "tail", "-n", "40", self.ALERT_LOG],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
            )
            output = result.stdout
            print(output)
            return output
        except Exception as e:
            print_error(f"Could not read alert log: {e}")
            return ""

    def _list_agents(self) -> str:
        """List connected Wazuh agents."""
        return self.run_command(["sudo", "/var/ossec/bin/agent_control", "-l"])

    def interactive(self):
        print("\n  [Wazuh] SIEM / XDR Platform")
        print("  Actions: status | start | stop | restart | tail | agents")
        action = input("  Action [status]: ").strip() or "status"
        self.run(action=action)

    def run_from_args(self, args):
        self.run(action=getattr(args, "action", "status"))
