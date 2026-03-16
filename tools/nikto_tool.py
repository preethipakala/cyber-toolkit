#!/usr/bin/env python3
"""
nikto_tool.py — Wrapper for Nikto web server scanner.

Nikto is an open source web server scanner that checks for:
- Outdated server software and dangerous files
- Misconfigurations and default credentials
- Interesting/sensitive files (e.g. /admin, /phpinfo.php)
- Over 6700 known vulnerabilities

Install: sudo apt install nikto  |  brew install nikto
"""

from tools.base import BaseTool


class NiktoTool(BaseTool):
    name         = "nikto"
    display_name = "Nikto — Web Server Scanner"
    binary       = "nikto"
    install_hint = "sudo apt install nikto  OR  brew install nikto"

    def run(self, target: str) -> str:
        if not self.require_installed():
            return ""
        cmd = ["nikto", "-h", target]
        return self.run_command(cmd)

    def interactive(self):
        print("\n  [Nikto] Web Server Scanner")
        target = input("  Target URL (e.g. http://localhost): ").strip()
        self.run(target=target)

    def run_from_args(self, args):
        self.run(target=args.target)
