"""Utilities for parsing and executing shell-command references."""

import re
import subprocess


_COMMAND_REFERENCE = re.compile(r"@(cmd|command)\((.*?)\)", re.DOTALL)


def parse_commands(text):
    """Return command references found in a prompt, preserving their order."""
    return [
        match.group(2)
        for match in _COMMAND_REFERENCE.finditer(text)
    ]


def run_command(command, timeout=30):
    """Execute a shell command and return its standard output."""
    result = subprocess.run(
        command,
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
    )
    if result.returncode:
        output = result.stdout.strip()
        raise RuntimeError(f"Command failed: {output}")
    return result.stdout.strip()
