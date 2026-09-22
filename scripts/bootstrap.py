#!/usr/bin/env python3
"""Install the local Nebius workspace. Preview by default; --apply writes the plan."""
import argparse
import datetime
import json
import os
import re
import sys
import tempfile
from pathlib import Path
import hook_config

from doctor import EXPECTED, IGNORE, RECORD, SKILLS, check, digest, prerequisites, read_record, safe_path

ROOT = Path(__file__).absolute().parent.parent
VERSION = "2.0.0"
SOURCES = {"scripts/bootstrap.py", "scripts/doctor.py", "scripts/hook_config.py", "scripts/memory_hook.py", "scripts/legacy.py", "scripts/legacy-hashes.json"} | {
    f"templates/{name}" for name in ("AGENTS.md", "CLAUDE.md", "START_HERE.md", "WORKFLOWS.md", "HOOKS.md")
} | {f"skills/{name}/SKILL.md" for name in SKILLS}


def manifest_text(root):
    return "# nebius-ai-kit " + VERSION + "\n" + "".join(
        f"{digest(safe_path(root, name).read_bytes())}  {name}\n" for name in sorted(SOURCES))


def verify_bundle(root):
    raw = safe_path(root, "MANIFEST.sha256").read_text(encoding="utf-8")
    entries = {}
    for line in raw.splitlines():
        if not line or line.startswith("#"):
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  ([A-Za-z0-9_./-]+)", line)
        if not match or match[2] not in SOURCES or match[2] in entries:
            raise ValueError("Invalid bundle manifest; nothing installed")
        entries[match[2]] = match[1]
    if set(entries) != SOURCES:
        raise ValueError("Incomplete bundle manifest; nothing installed")
    for rel, wanted in entries.items():
        if digest(safe_path(root, rel).read_bytes()) != wanted:
            raise ValueError(f"Bundle checksum mismatch: {rel}")
    for name in SKILLS:
        content = (root / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
        parts = content.split("---", 2)
        if (not content.startswith("---\n") or len(parts) != 3
                or f"name: {name}" not in parts[1].splitlines()
                or not any(line.startswith("description: ") for line in parts[1].splitlines())):
            raise ValueError(f"Invalid skill frontmatter: {name}")


def payload(root):
    result = {name: (root / "templates" / name).read_bytes()
              for name in ("AGENTS.md", "CLAUDE.md", "START_HERE.md")}
    result[".nebius-kit/WORKFLOWS.md"] = (root / "templates/WORKFLOWS.md").read_bytes()
    result[".nebius-kit/doctor.py"] = (root / "scripts/doctor.py").read_bytes()
    for name in ("hook_config.py", "memory_hook.py"):
        result[".nebius-kit/" + name] = (root / "scripts" / name).read_bytes()
    result[".nebius-kit/HOOKS.md"] = (root / "templates/HOOKS.md").read_bytes()
    for name in SKILLS:
        data = (root / "skills" / name / "SKILL.md").read_bytes()
        for base in (".claude/skills", ".agents/skills"):
            result[f"{base}/{name}/SKILL.md"] = data
    assert set(result) == EXPECTED
    return result


def plan(root, target, integrate=False, replace_files=()):
    verify_bundle(root)
    prerequisites(target)
    override = safe_path(target, "AGENTS.override.md")
    if override.exists() and override.stat().st_size:
        raise ValueError("AGENTS.override.md shadows AGENTS.md; review integration manually; nothing written")
    previous = read_record(target)
    wanted = payload(root)
    if set(replace_files) - set(wanted):
        raise ValueError("--replace-file accepts only managed kit files, never private notes or settings")
    changes, before, conflicts = {}, {}, []
    for rel, data in wanted.items():
        path = safe_path(target, rel)
        old = path.read_bytes() if path.exists() else None
        if old == data:
            continue
        if old is not None:
            known = previous and previous["files"].get(rel) == digest(old)
            if known:
                # Integrated instructions keep their pre-existing prefix on upgrades.
                marker = b"\n<!-- nebius-ai-kit:start -->\n"
                if rel in ("AGENTS.md", "CLAUDE.md") and marker in old:
                    data = old.split(marker, 1)[0] + marker + data + b"<!-- nebius-ai-kit:end -->\n"
            elif rel in replace_files:
                pass  # Exact reviewed replacement, explicitly requested on CLI.
            elif integrate and not previous and rel in ("AGENTS.md", "CLAUDE.md"):
                if b"<!-- nebius-ai-kit:" in old:
                    conflicts.append(rel)
                    continue
                data = old + b"\n<!-- nebius-ai-kit:start -->\n" + data + b"<!-- nebius-ai-kit:end -->\n"
            else:
                conflicts.append(rel)
                continue
        wanted[rel] = data
        if old != data:
            changes[rel], before[rel] = data, old
    if conflicts:
        raise ValueError("Conflicts preserved; nothing written: " + ", ".join(conflicts)
                         + ". Use a new workspace, or review --integrate for existing instruction files.")
    hook_hashes = {}
    for rel in hook_config.FILES:
        path = safe_path(target, rel)
        old = path.read_bytes() if path.exists() else None
        new = hook_config.merge(old, codex=rel.startswith(".codex/"))
        prior = (previous or {}).get("hook_files", {}).get(rel)
        if (old and hook_config.owned(hook_config.parse(old)) and new != old
                and hook_config.fingerprint(old) != prior):
            raise ValueError("Edited Nebius hooks preserved; review manually: " + rel)
        hook_hashes[rel] = hook_config.fingerprint(new)
        if new != old:
            changes[rel], before[rel] = new, old
    for rel in (".nebius-local/ROLE-MAP.md", ".nebius-local/STATE.md"):
        safe_path(target, rel)
    ignore_path = safe_path(target, ".gitignore")
    old_ignore = ignore_path.read_bytes() if ignore_path.exists() else None
    if old_ignore is None or IGNORE.encode() not in old_ignore.splitlines():
        # Append so prior root-level negations cannot undo this rule.
        changes[".gitignore"] = (old_ignore or b"") + b"\n# Private Nebius AI context\n" + IGNORE.encode() + b"\n"
        before[".gitignore"] = old_ignore
    record = {"schema": 1, "version": VERSION, "hook_files": hook_hashes,
              "installed_at": previous["installed_at"] if previous else
              datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "bundle_sha256": digest((root / "MANIFEST.sha256").read_bytes()),
              "files": {rel: digest(data) for rel, data in sorted(wanted.items())}}
    new_record = (json.dumps(record, indent=2, sort_keys=True) + "\n").encode()
    path = safe_path(target, RECORD)
    old_record = path.read_bytes() if path.exists() else None
    if old_record != new_record:
        changes[RECORD], before[RECORD] = new_record, old_record
    return changes, before


def atomic_write(path, data):
    mode = path.stat().st_mode & 0o777 if path.exists() else 0o644
    fd, temporary = tempfile.mkstemp(prefix=".nebius-write-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def apply_plan(target, changes, before):
    """Rollback ordinary errors; never overwrite changes made since preview."""
    made_dirs, written = [], []
    try:
        for rel in changes:
            path = safe_path(target, rel)
            now = path.read_bytes() if path.exists() else None
            if now != before[rel]:
                raise ValueError(f"Changed during install: {rel}")
        for rel, data in changes.items():
            path = safe_path(target, rel)
            missing = []
            parent = path.parent
            while not parent.exists():
                missing.append(parent)
                parent = parent.parent
            for directory in reversed(missing):
                directory.mkdir()
                made_dirs.append(directory)
            # Recheck each destination immediately before writing.
            current = path.read_bytes() if path.exists() else None
            if current != before[rel]:
                raise ValueError(f"Changed during install: {rel}")
            atomic_write(path, data)
            written.append(rel)
        errors, _ = check(target)
        if errors:
            raise ValueError("Post-install check failed: " + "; ".join(errors))
    except BaseException:
        for rel in reversed(written):
            path = target / rel
            if before[rel] is None:
                path.unlink(missing_ok=True)
            else:
                path.write_bytes(before[rel])
        for directory in reversed(made_dirs):
            directory.rmdir()
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init", help="preview installation; add --apply to write")
    init.add_argument("--workspace", type=Path, required=True)
    init.add_argument("--apply", action="store_true")
    init.add_argument("--integrate", action="store_true", help="append kit rules to existing instruction files")
    init.add_argument("--replace-file", action="append", default=[], help="replace this exact reviewed managed file; repeat per conflict")
    sub.add_parser("verify", help="verify source bundle and generated local installation")
    sub.add_parser("manifest", help="maintainer: regenerate checksums after reviewed source edits")
    args = parser.parse_args()
    try:
        if args.command == "manifest":
            (ROOT / "MANIFEST.sha256").write_text(manifest_text(ROOT), encoding="utf-8")
            text = "# nebius-ai-kit " + VERSION + "\n" + "".join(
                f"{digest((ROOT / 'skills' / name / 'SKILL.md').read_bytes())}  {name}/SKILL.md\n"
                for name in SKILLS)
            (ROOT / "skills/MANIFEST.txt").write_text(text, encoding="utf-8")
            print("Updated source manifests. This does not publish a release.")
        elif args.command == "verify":
            verify_bundle(ROOT)
            errors, _ = check(ROOT)
            if errors:
                raise ValueError("; ".join(errors))
            actual = payload(ROOT)
            if any((ROOT / name).read_bytes() != data for name, data in actual.items()):
                raise ValueError("Generated workspace copies differ from canonical source")
            print("PASS: bundle integrity and generated workspace parity")
        else:
            target = Path(os.path.abspath(args.workspace.expanduser()))
            if target == Path.home() or target == Path(target.anchor):
                raise ValueError("Choose a project folder, not your home or filesystem root")
            if any(folder == target or folder in target.parents for folder in
                   (Path.home() / name for name in (".claude", ".codex", ".agents"))):
                raise ValueError("Choose a workspace outside global assistant configuration")
            changes, before = plan(ROOT, target, args.integrate, args.replace_file)
            print("Workspace:", target)
            for rel in changes:
                print(("CREATE " if before[rel] is None else "UPDATE ") + rel)
            if not changes:
                errors, notes = check(target)
                if errors:
                    raise ValueError("; ".join(errors))
                print("Already installed; no files changed.")
            elif args.apply:
                apply_plan(target, changes, before)
                print("PASS: files installed and checked. Personal onboarding is next.")
                print("Continue here: read target START_HERE.md and .agents/skills/nebius-setup/SKILL.md (Claude: .claude/skills).")
                print("Next: follow .nebius-kit/HOOKS.md for approval and a fresh-chat delivery test in each assistant.")
                print("Hooks activation, connectors and operational authorization are NOT VERIFIED.")
            else:
                print("PREVIEW ONLY: no files written. Review, then add --apply.")
        return 0
    except (OSError, ValueError, TypeError) as exc:
        print("ERROR:", exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
