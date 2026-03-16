#!/usr/bin/env python3
"""
hashcat_tool.py — Wrapper for Hashcat password hash cracker.

Hashcat is the world's fastest password recovery tool.
It supports 300+ hash types and multiple attack modes:
  Mode 0  = Dictionary attack
  Mode 3  = Brute-force / mask attack
  Mode 6  = Hybrid wordlist + mask

Common hash types:
  -m 0    = MD5
  -m 100  = SHA-1
  -m 1400 = SHA-256
  -m 1800 = SHA-512
  -m 3200 = bcrypt

Install: sudo apt install hashcat  |  https://hashcat.net/hashcat/
"""

from tools.base import BaseTool


class HashcatTool(BaseTool):
    name         = "hashcat"
    display_name = "Hashcat — Password Hash Cracker"
    binary       = "hashcat"
    install_hint = "sudo apt install hashcat  OR  download from hashcat.net"

    def run(self, hash_value: str, mode: str = "0", wordlist: str = "data/wordlist.txt") -> str:
        if not self.require_installed():
            return ""
        cmd = ["hashcat", "-m", mode, "-a", "0", hash_value, wordlist, "--force"]
        return self.run_command(cmd)

    def interactive(self):
        print("\n  [Hashcat] Password Hash Cracker")
        print("  Common modes: 0=MD5  100=SHA1  1400=SHA256  1800=SHA512  3200=bcrypt")
        hash_value = input("  Hash to crack: ").strip()
        mode       = input("  Hash mode [0 for MD5]: ").strip() or "0"
        wordlist   = input("  Wordlist path [data/wordlist.txt]: ").strip() or "data/wordlist.txt"
        self.run(hash_value=hash_value, mode=mode, wordlist=wordlist)

    def run_from_args(self, args):
        self.run(hash_value=args.hash, mode=args.mode, wordlist=args.wordlist)
