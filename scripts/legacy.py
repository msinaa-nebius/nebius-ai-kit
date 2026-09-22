#!/usr/bin/env python3
"""Preview/update only existing v1 global Nebius skills. Never edit settings/auth."""
import argparse
import json
from pathlib import Path
import sys

from bootstrap import ROOT, atomic_write, verify_bundle
from doctor import SKILLS, digest, safe_path


def plan(source, home, replace=()):
    verify_bundle(source)
    if set(replace) - set(SKILLS):
        raise ValueError("Unknown Nebius skill")
    known = json.loads((source / "scripts/legacy-hashes.json").read_text())
    changes, conflicts = [], []
    for base in (".codex/skills", ".claude/skills", ".agents/skills"):
        for name in SKILLS:
            rel = f"{base}/{name}/SKILL.md"
            path = safe_path(home, rel)
            if not path.exists():
                continue
            old = path.read_bytes()
            new = (source / "skills" / name / "SKILL.md").read_bytes()
            if old == new:
                continue
            if digest(old) not in known[name] and name not in replace:
                conflicts.append(rel)
            else:
                changes.append((rel, old, new))
    if conflicts:
        raise ValueError("Modified global skills preserved: " + ", ".join(conflicts)
                         + ". Review exact content first; --replace-skill NAME permits that reviewed replacement.")
    return changes


def apply(home, changes):
    for rel, old, _ in changes:
        if safe_path(home, rel).read_bytes() != old:
            raise ValueError("Global skill changed during upgrade: " + rel)
    written = []
    try:
        for rel, old, new in changes:
            path = safe_path(home, rel)
            if path.read_bytes() != old:
                raise ValueError("Global skill changed during upgrade: " + rel)
            atomic_write(path, new)
            written.append((path, old))
    except BaseException:
        for path, old in reversed(written):
            atomic_write(path, old)
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--replace-skill", action="append", default=[])
    args = parser.parse_args()
    try:
        changes = plan(ROOT, Path.home(), args.replace_skill)
        for rel, _, _ in changes:
            print("UPDATE " + rel)
        if args.apply:
            apply(Path.home(), changes)
            print("PASS: existing global Nebius skills updated. Open the installed workspace; follow its local skill.")
        else:
            print("PREVIEW ONLY: no files changed. Add --apply after reviewing these exact replacements.")
        print("Global settings, credentials, other skills and private notes are unchanged.")
    except (OSError, ValueError, TypeError) as exc:
        print("ERROR:", exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
