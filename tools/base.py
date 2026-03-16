#!/usr/bin/env python3
"""
base.py — Abstract base class for all tool wrappers.
Every tool inherits from this and implements run() and interactive().
"""

import subprocess
import shutil
from abc import ABC, abstractmethod
from utils.reporter import print_section, print_error, print_success


class BaseTool(ABC):
    """Base class for all cybersecurity tool wrappers."""

    name: str = ""           # e.g. "nmap"
    display_name: str = ""   # e.g. "Nmap — Network Scanner"
    binary: str = ""         # CLI binary name to check, e.g. "nmap"
    install_hint: str = ""   # How to install, e.g. "sudo apt install nmap"

    def is_installed(self) -> bool:
        """Return True if the tool's binary is available on PATH."""
        return shutil.which(self.binary) is not None

    def require_installed(self) -> bool:
        """Print an error if not installed. Returns True if OK to proceed."""
        if not self.is_installed():
            print_error(
                f"{self.display_name} is not installed.\n"
                f"  Install with: {self.install_hint}"
            )
            return False
        return True

    def run_command(self, cmd: list[str]) -> str:
        """
        Run a shell command and stream output to the terminal.
        Returns combined stdout+stderr as a string.
        """
        print_section(f"Running: {' '.join(cmd)}")
        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            print(result.stdout)
            return result.stdout
        except FileNotFoundError:
            print_error(f"Command not found: {cmd[0]}")
            return ""
        except KeyboardInterrupt:
            print("\n[!] Interrupted by user.")
            return ""

    @abstractmethod
    def run(self, **kwargs) -> str:
        """Run the tool with given keyword arguments."""

    @abstractmethod
    def interactive(self):
        """Prompt the user for input and run the tool."""

    def run_from_args(self, args):
        """Run from parsed argparse namespace. Override if needed."""
        self.interactive()
