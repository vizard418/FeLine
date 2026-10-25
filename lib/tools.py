"""Utilities for parsing and executing shell-command references."""

import re
import subprocess


_COMMAND_REFERENCE = re.compile(r"@(cmd|command)\((.*?)\)", re.DOTALL)


def parse_commands(text: str) -> list[str]:
    """Return command references found in a prompt, preserving their order."""
    return [
        match.group(2)
        for match in _COMMAND_REFERENCE.finditer(text)
    ]


def run_command(command: str, timeout: int = 30) -> str:
    """Execute a local shell command and return its output after user confirmation.

    Args:
        command: The shell command to execute locally.
        timeout: Maximum execution time in seconds.
    """
    print(f"\n[Agent wants to execute command]: {command}")
    confirm = input("Do you want to allow this execution? [Y/n]: ").strip().lower()

    # Si el usuario presiona Enter (vacio) o responde 'y'/'yes', se aprueba.
    # Solo si responde explicitamente 'n' o 'no' se cancela.
    if confirm in ["n", "no"]:
        raise RuntimeError("Command execution cancelled by user.")

    result = subprocess.run(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
    )

    output = result.stdout.decode("utf-8", errors="replace").strip()

    if result.returncode:
        raise RuntimeError(f"Command failed: {output}")

    return output

AVAILABLE_TOOLS = [
    run_command
]
