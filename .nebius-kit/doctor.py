#!/usr/bin/env python3
"""Offline installation checks; no account access, network or mutations."""
import argparse
import hashlib
import json
import os
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
GIT_TIMEOUT = 15
GIT_OVERRIDES = {"GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR",
                 "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES",
                 "GIT_NAMESPACE", "GIT_CEILING_DIRECTORIES", "GIT_CONFIG_PARAMETERS",
                 "GIT_CONFIG_COUNT", "GIT_CONFIG", "GIT_CONFIG_GLOBAL", "GIT_CONFIG_SYSTEM"}


def check_git_environment():
    active = sorted(name for name in os.environ if name in GIT_OVERRIDES
                    or name.startswith(("GIT_CONFIG_KEY_", "GIT_CONFIG_VALUE_")))
    if active:
        raise ValueError("Git environment overrides prevent reliable privacy checks; unset "
                         + ", ".join(active) + " and retry (values are not displayed)")


def run_git(*args):
    """Bound checks, including macOS Git shims without installed developer tools."""
    check_git_environment()
    try:
        return subprocess.run(["git", *args], capture_output=True, text=True,
                              timeout=GIT_TIMEOUT)
    except FileNotFoundError as exc:
        raise ValueError("Git unavailable: ask your IT team to provide Git; nothing can verify repository privacy yet") from exc
    except subprocess.TimeoutExpired as exc:
        raise ValueError("Git did not respond within 15 seconds; resolve the local Git setup and retry") from exc


def repository_present(root):
    return any((p / ".git").exists() or (p / ".git").is_symlink()
               for p in (root, *root.parents))


def prerequisites(root):
    check_git_environment()
    if repository_present(root) and run_git("--version").returncode:
        raise ValueError("Git is present but cannot run; resolve the local Git setup and retry")


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
    check_git_environment()
    if not repository_present(root):
        return []
    probe = run_git("-C", str(root), "rev-parse", "--show-toplevel")
    if probe.returncode:
        return ["Git repository could not be inspected"]
    tracked = run_git("-C", str(root), "ls-files", "--", ".nebius-local")
    if tracked.returncode or tracked.stdout.strip():
        return ["Private context is tracked or tracking could not be checked; resolve before saving"]
    candidates = [".nebius-local/ROLE-MAP.md", ".nebius-local/STATE.md"]
    local = root / ".nebius-local"
    if local.is_symlink():
        return ["Private context directory is a symlink"]
    if local.exists():
        candidates += [str(p.relative_to(root)) for p in local.rglob("*") if p.is_file()]
    for name in candidates:
        result = run_git("-C", str(root), "check-ignore", "-q", "--", name)
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
    local = root / ".nebius-local"
    if local.exists():
        for path in local.rglob("*"):
            if path.is_symlink():
                errors.append("Private context contains a symlink; review before saving")
                break
            if not path.is_dir():
                safe_path(root, str(path.relative_to(root)))
    errors.extend(git_privacy(root))
    notes = ["Assistant discovery: confirm in a new session opened at the workspace root",
             "Connectors/accounts: NOT VERIFIED by this offline check",
             "Operational authorization: NOT VERIFIED by installation"]
    if not repository_present(root):
        notes.append("No Git repository found: ignore rule present; tracking checks are not applicable until a repository is created")
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
