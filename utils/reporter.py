#!/usr/bin/env python3
"""
reporter.py — Shared terminal output helpers.
"""

GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


def print_banner():
    print(f"\n{BOLD}{CYAN}")
    print("  ╔══════════════════════════════════════════════╗")
    print("  ║         🛡️  Cyber Toolkit  v1.0              ║")
    print("  ║  Unified Open Source Security Tool Launcher  ║")
    print("  ╚══════════════════════════════════════════════╝")
    print(f"{RESET}")
    print(f"  {RED}⚠️  For authorized use only. Never scan systems you don't own.{RESET}\n")


def print_menu(items: list):
    print(f"  {BOLD}Available Tools:{RESET}\n")
    for i, (name, tool_class) in enumerate(items, 1):
        print(f"  [{CYAN}{i}{RESET}] {BOLD}{tool_class.display_name}{RESET}")


def print_section(title: str):
    print(f"\n{CYAN}{'─' * 55}{RESET}")
    print(f"  ▶  {BOLD}{title}{RESET}")
    print(f"{CYAN}{'─' * 55}{RESET}\n")


def print_success(msg: str):
    print(f"  {GREEN}[✓]{RESET} {msg}")


def print_error(msg: str):
    print(f"  {RED}[✗]{RESET} {msg}")


def print_warning(msg: str):
    print(f"  {YELLOW}[!]{RESET} {msg}")
