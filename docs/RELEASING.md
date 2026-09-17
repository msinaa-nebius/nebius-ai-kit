# Maintainer release checks

Working version: `2.0.0-dev`. The normal repository URL serves the default branch;
local edits and another branch do not update it. Do not move the old v1.1 tag.

Canonical sources: `skills/`, `templates/`, `scripts/`. Generated root instructions,
`.agents/skills/`, `.claude/skills/` and `.nebius-kit/` make extracted copies usable
without a global install. Update canonical files, then:

```bash
python3 scripts/bootstrap.py manifest
python3 scripts/bootstrap.py init --workspace .
python3 scripts/bootstrap.py init --workspace . --apply
python3 -m unittest discover -s tests -v
python3 scripts/bootstrap.py verify
git diff --check
python3 scripts/package.py --output dist/nebius-ai-kit-candidate.zip
```

Choose a new archive name rather than overwriting a previous candidate. The packager
uses an explicit file allowlist: hidden project folders are included, private memory,
credentials, caches and Git history are excluded. Review the archive inventory;
extract those actual bytes into a clean workspace and run its verify and doctor.
Checksums detect inconsistency, not publisher identity. Never regenerate a manifest
as a workaround for a downloaded checksum mismatch.

Record the separate gates in ACCEPTANCE.md: deterministic installer tests,
independent scenario runs, actual product discovery/authentication and colleague
first use. Do not turn a simulation into a “tested on another laptop” statement.
A Claude CLI without login is a blocked product test, not a failed kit install.

Before requesting publication, prepare the exact scope/diff, validation and known
limits. Publication needs explicit user authorization; do not infer it from tests.
With authorization, preserve existing work, commit the reviewed files, integrate the
intended branch into main and push without force. Confirm the remote commit, fetch
its actual source archive, verify its files and recheck the README install path.
Update the README's distribution status truthfully as part of the release. A tagged
stable release requires completed product acceptance, not only a green unit suite.
Never distribute an employee's working folder, which may contain ignored data.
