#!/usr/bin/env python3
"""
sqlmap_tool.py — Wrapper for SQLMap SQL injection tool.

SQLMap is the leading open source tool for detecting and exploiting
SQL injection vulnerabilities. It automates:
- Detection of injectable parameters
- Database fingerprinting
- Data extraction

⚠️  ONLY use on applications you own or have permission to test.

Install: sudo apt install sqlmap  |  pip install sqlmap
"""

from tools.base import BaseTool


class SQLMapTool(BaseTool):
    name         = "sqlmap"
    display_name = "SQLMap — SQL Injection Scanner"
    binary       = "sqlmap"
    install_hint = "sudo apt install sqlmap  OR  pip install sqlmap"

    def run(self, url: str) -> str:
        if not self.require_installed():
            return ""
        # --batch = don't prompt for user input; --level=1 = basic detection
        cmd = ["sqlmap", "-u", url, "--batch", "--level=1", "--risk=1"]
        return self.run_command(cmd)

    def interactive(self):
        print("\n  [SQLMap] SQL Injection Scanner")
        print("  ⚠️  Only use on systems you own or are authorized to test!")
        url = input("  Target URL (e.g. http://site.com/page?id=1): ").strip()
        self.run(url=url)

    def run_from_args(self, args):
        self.run(url=args.url)
