#!/usr/bin/env python3
"""Build a reviewed, allowlisted ZIP locally. Does not publish or overwrite."""
import argparse
import io
import sys
import zipfile
from pathlib import Path

from bootstrap import ROOT, SOURCES, VERSION, payload, verify_bundle
from doctor import EXPECTED, RECORD, check, safe_path

EXTRAS = {
    "README.md", "LICENSE", ".gitattributes", ".gitignore", "MANIFEST.sha256",
    "skills/MANIFEST.txt", RECORD, "scripts/package.py", "tests/test_bootstrap.py",
    "docs/ACCEPTANCE.md", "docs/AUDIT.md", "docs/RELEASING.md",
    "optional-skills/jira-personal-dashboard/SKILL.md",
    "optional-skills/jira-personal-dashboard/REFERENCE.md",
}
FILES = SOURCES | EXPECTED | EXTRAS


def build_archive(root, output):
    """Fail before creating output if sources, generated copies or inventory differ."""
    root, output = root.absolute(), output.absolute()
    try:
        relative = output.relative_to(root)
    except ValueError as exc:
        raise ValueError("Archive output must be inside the kit workspace") from exc
    if ".." in relative.parts or str(relative) in FILES:
        raise ValueError("Choose a new archive path inside dist/")
    safe_path(root, str(relative))
    if output.exists():
        raise ValueError("Archive already exists; choose a new --output path")
    verify_bundle(root)
    errors, _ = check(root)
    if errors:
        raise ValueError("; ".join(errors))
    for rel, data in payload(root).items():
        if safe_path(root, rel).read_bytes() != data:
            raise ValueError("Generated workspace copies differ from canonical source")
    contents = {name: safe_path(root, name).read_bytes() for name in sorted(FILES)}
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in contents.items():
            info = zipfile.ZipInfo(name)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("xb") as stream:
        stream.write(buffer.getvalue())
    return len(contents)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=ROOT / "dist" / f"nebius-ai-kit-{VERSION}.zip")
    args = parser.parse_args()
    try:
        count = build_archive(ROOT, args.output)
    except (OSError, ValueError, TypeError) as exc:
        print("ERROR:", exc, file=sys.stderr)
        return 1
    print(f"PASS: {count} allowlisted files packaged in {args.output}")
    print("Local artifact only; no publication, account access or assistant discovery verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
