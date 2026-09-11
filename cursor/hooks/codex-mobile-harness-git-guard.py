#!/usr/bin/env python3
"""Fail-closed guard for destructive Git history and workspace commands."""

from __future__ import annotations

import json
import os
import re
import shlex
import sys


FORBIDDEN_SUBCOMMANDS = {"commit", "push", "clean"}


def deny(message: str) -> dict[str, str]:
    return {"permission": "deny", "user_message": message}


def git_token(token: str) -> bool:
    return os.path.basename(token) == "git"


def contains_forbidden_git(command: str) -> bool:
    # Conservative raw checks catch command substitution, shell grouping, and
    # wrappers before token parsing can hide the destructive operation.
    if re.search(r"(?<![A-Za-z0-9_-])git\b[^;&|\n]*\b(commit|push|clean)\b", command):
        return True
    if re.search(r"(?<![A-Za-z0-9_-])git\b[^;&|\n]*\breset\b[^;&|\n]*--hard(?:[=\s]|$)", command):
        return True
    try:
        tokens = shlex.split(command, posix=True)
    except ValueError:
        return True

    for index, token in enumerate(tokens):
        if not git_token(token):
            continue
        cursor = index + 1
        while cursor < len(tokens):
            option = tokens[cursor]
            if option in {"-C", "--git-dir", "--work-tree", "-c"}:
                cursor += 2
                continue
            if option.startswith(("-C", "--git-dir=", "--work-tree=", "-c")):
                cursor += 1
                continue
            break
        if cursor >= len(tokens):
            continue
        subcommand = tokens[cursor]
        if subcommand in FORBIDDEN_SUBCOMMANDS:
            return True
        if subcommand == "reset" and any(
            option == "--hard" or option.startswith("--hard=")
            for option in tokens[cursor + 1 :]
        ):
            return True
    return False


def decision(payload: object) -> dict[str, str]:
    if not isinstance(payload, dict) or not isinstance(payload.get("command"), str):
        return deny("CURSOR_HARNESS_GIT_GUARD: malformed shell input")
    command = payload["command"]
    if contains_forbidden_git(command):
        return deny(
            "CURSOR_HARNESS_GIT_GUARD: git commit, git push, git reset --hard, "
            "and git clean are blocked"
        )
    return {"permission": "allow"}


def main() -> None:
    try:
        output = decision(json.load(sys.stdin))
    except (json.JSONDecodeError, OSError):
        output = deny("CURSOR_HARNESS_GIT_GUARD: invalid hook input")
    print(json.dumps(output))


if __name__ == "__main__":
    main()
