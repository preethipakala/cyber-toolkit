#!/usr/bin/env python3
"""
nmap_tool.py — Wrapper for Nmap network scanner.

Nmap is the most widely used network discovery and security auditing tool.
It scans hosts, discovers open ports, detects OS/service versions, and can
run vulnerability scripts via the Nmap Scripting Engine (NSE).

Install: sudo apt install nmap  |  brew install nmap
"""

from tools.base import BaseTool

# Nmap scan profiles — each maps to a set of CLI flags
PROFILES = {
    "quick":    ["-F", "--open"],                          # Top 100 ports, fast
    "standard": ["-sV", "--open", "--top-ports", "1000"], # Top 1000 + service versions
    "full":     ["-sV", "-p-", "--open"],                  # All 65535 ports
    "vuln":     ["-sV", "--script=vuln"],                  # NSE vulnerability scripts
}


class NmapTool(BaseTool):
    name         = "nmap"
    display_name = "Nmap — Network Scanner"
    binary       = "nmap"
    install_hint = "sudo apt install nmap  OR  brew install nmap"

    def run(self, target: str, profile: str = "standard") -> str:
        if not self.require_installed():
            return ""
        flags = PROFILES.get(profile, PROFILES["standard"])
        cmd = ["nmap"] + flags + [target]
        return self.run_command(cmd)

    def interactive(self):
        print("\n  [Nmap] Network Scanner")
        target  = input("  Target IP or hostname: ").strip()
        print("  Profiles: quick | standard | full | vuln")
        profile = input("  Profile [standard]: ").strip() or "standard"
        self.run(target=target, profile=profile)

    def run_from_args(self, args):
        self.run(target=args.target, profile=args.profile)
