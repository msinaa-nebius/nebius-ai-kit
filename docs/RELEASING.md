# Maintainer release checks

The working version is `2.0.0-dev`. No v2 tag or public installer URL exists as a
result of local edits. Do not move the existing v1.1 tag.

Canonical source lives in `skills/`, `templates/` and `scripts/`. Root AGENTS.md,
CLAUDE.md, START_HERE.md, `.agents/skills/`, `.claude/skills/` and `.nebius-kit/`
are generated so an extracted checkout can be opened immediately. Both products
receive identical skills; no hand-maintained third copy or symlink is required.

After an authorized source edit:

```bash
python3 scripts/bootstrap.py manifest
python3 scripts/bootstrap.py init --workspace .
python3 scripts/bootstrap.py init --workspace . --apply
python3 -m unittest discover -s tests -v
python3 scripts/bootstrap.py verify
git diff --check
```

The manifest command intentionally rewrites checksums: use it only after reviewing
source edits, never as an automatic repair for a downloaded checksum mismatch.
The installer does not fetch, execute downloads, install dependencies or initialize
Git. Ordinary write errors roll back; a forced termination or power loss needs a
doctor run and review. Do not run installers concurrently.

Before publishing, complete ACCEPTANCE.md in both assistants, set the intended
version consistently in the installer and core skill headers, regenerate and
verify, and review the exact file inventory. Exclude `.nebius-local/`, caches and
any corporate payloads. Include dot folders: omitting them recreates the original
installation failure. Keep optional-skills separate from the core manifest.

Publishing requires explicit approval for the exact commit/tag or PR. Once
approved, publish a new fixed release, download its actual archive to a clean
location and repeat the checks on those bytes. Update README's release status and
distribution link to that verified release. Never label local tests as proof that
an unchanged remote v1.1 installer works differently.
