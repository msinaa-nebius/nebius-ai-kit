#!/usr/bin/env python3
"""Offline installation checks; no account access, network or mutations."""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

SKILLS = ("nebius-setup", "nebius-role-map", "nebius-ask")
FIXED = {"AGENTS.md", "CLAUDE.md", "START_HERE.md", ".nebius-kit/WORKFLOWS.md",
         ".nebius-kit/doctor.py"}
EXPECTED = FIXED | {f"{base}/{name}/SKILL.md" for base in
                   (".agents/skills", ".claude/skills") for name in SKILLS}
RECORD = ".nebius-kit/install.json"
IGNORE = "/.nebius-local/"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_path(root, rel):
    """Reject symlinks and non-directory ancestors, including the target root."""
    path = root / rel
    for item in (path, *path.parents):
        if item.is_symlink():
            raise ValueError(f"Symlink refused: {item}")
        if item != path and item.exists() and not item.is_dir():
            raise ValueError(f"Not a directory: {item}")
    if path.exists() and not path.is_file():
        raise ValueError(f"Not a regular file: {path}")
    if path.exists() and path.stat().st_nlink > 1:
        raise ValueError(f"Hard-linked file refused: {path}")
    return path


def read_record(root):
    path = safe_path(root, RECORD)
    if not path.exists():
        return None
    record = json.loads(path.read_text(encoding="utf-8"))
    if (not isinstance(record, dict) or record.get("schema") != 1 or not isinstance(record.get("files"), dict)
            or set(record["files"]) != EXPECTED
            or any(not isinstance(v, str) or not re.fullmatch(r"[0-9a-f]{64}", v)
                   for v in record["files"].values())
            or not isinstance(record.get("installed_at"), str)):
        raise ValueError("Invalid install record; no paths from it will be followed")
    return record


def git_privacy(root):
    """Check both tracked state and effective ignore, including nested overrides."""
    try:
        probe = subprocess.run(["git", "-C", str(root), "rev-parse", "--show-toplevel"],
                               capture_output=True, text=True)
    except FileNotFoundError:
        return ["Git unavailable: tracking and effective ignore NOT VERIFIED"]
    if probe.returncode:
        if any((p / ".git").exists() for p in (root, *root.parents)):
            return ["Git repository could not be inspected"]
        return []
    tracked = subprocess.run(["git", "-C", str(root), "ls-files", "--", ".nebius-local"],
                             capture_output=True, text=True)
    if tracked.returncode or tracked.stdout.strip():
        return ["Private context is tracked or tracking could not be checked; resolve before saving"]
    candidates = [".nebius-local/ROLE-MAP.md", ".nebius-local/STATE.md"]
    local = root / ".nebius-local"
    if local.is_symlink():
        return ["Private context directory is a symlink"]
    if local.exists():
        candidates += [str(p.relative_to(root)) for p in local.rglob("*") if p.is_file()]
    for name in candidates:
        result = subprocess.run(["git", "-C", str(root), "check-ignore", "-q", "--", name],
                                capture_output=True)
        if result.returncode:
            return ["Private context is not effectively ignored; resolve before saving"]
    return []


def check(root):
    errors = []
    override = safe_path(root, "AGENTS.override.md")
    if override.exists() and override.stat().st_size:
        errors.append("AGENTS.override.md shadows AGENTS.md; review integration manually")
    record = read_record(root)
    if record is None:
        return ["Installation record missing; run the kit installer"], []
    for rel, wanted in record["files"].items():
        path = safe_path(root, rel)
        if not path.exists():
            errors.append(f"Missing: {rel}")
        elif digest(path.read_bytes()) != wanted:
            errors.append(f"Changed: {rel} (preserved; review before reinstalling)")
    ignore = safe_path(root, ".gitignore")
    if not ignore.exists() or IGNORE not in ignore.read_text(encoding="utf-8").splitlines():
        errors.append("Private-context ignore rule missing")
    for rel in (".nebius-local/ROLE-MAP.md", ".nebius-local/STATE.md"):
        safe_path(root, rel)
    errors.extend(git_privacy(root))
    notes = ["Assistant discovery: confirm in a new session opened at the workspace root",
             "Connectors/accounts: NOT VERIFIED by this offline check",
             "Operational authorization: NOT VERIFIED by installation"]
    for name in SKILLS:
        # Read only the known legacy skill path, never global configuration/credentials.
        if any((Path.home() / base / "skills" / name / "SKILL.md").is_file()
               for base in (".claude", ".codex", ".agents")):
            notes.append(f"Legacy/global {name} also exists; select this workspace's copy")
    return errors, notes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=Path(__file__).absolute().parent.parent)
    args = parser.parse_args()
    try:
        errors, notes = check(args.workspace.absolute())
    except (OSError, ValueError, TypeError) as exc:
        errors, notes = [str(exc)], []
    for error in errors:
        print("FAIL:", error)
    for note in notes:
        print("NOTE:", note)
    if not errors:
        print("PASS: local files and privacy checks; live onboarding remains separate")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
