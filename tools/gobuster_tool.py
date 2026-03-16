#!/usr/bin/env python3
"""
gobuster_tool.py — Wrapper for Gobuster directory brute-forcer.

Gobuster brute-forces URIs (directories and files) on web servers
and DNS subdomain names. It's written in Go and very fast.

Common use:
  gobuster dir -u http://target -w /usr/share/wordlists/dirb/common.txt

Install: sudo apt install gobuster  |  brew install gobuster
"""

from tools.base import BaseTool


class GobusterTool(BaseTool):
    name         = "gobuster"
    display_name = "Gobuster — Directory Brute-Forcer"
    binary       = "gobuster"
    install_hint = "sudo apt install gobuster  OR  brew install gobuster"

    def run(self, url: str, wordlist: str = "data/wordlist.txt") -> str:
        if not self.require_installed():
            return ""
        cmd = ["gobuster", "dir", "-u", url, "-w", wordlist, "--no-error"]
        return self.run_command(cmd)

    def interactive(self):
        print("\n  [Gobuster] Directory Brute-Forcer")
        url      = input("  Target URL (e.g. http://localhost): ").strip()
        wordlist = input("  Wordlist path [data/wordlist.txt]: ").strip() or "data/wordlist.txt"
        self.run(url=url, wordlist=wordlist)

    def run_from_args(self, args):
        self.run(url=args.url, wordlist=args.wordlist)
