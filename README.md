# Nebius AI kit

A local work assistant for Claude Code and Codex: understand your role, find the
right sources and work through tickets with evidence. The kit ships generic
workflows; your company data stays in the systems where it belongs.

**Workspace edition: 2.0.0-dev — local candidate, not a published release.**
The existing `v1.1` release installs global skills only. Its download link does
not contain this new workspace installer. See [release checks](docs/RELEASING.md)
before sharing an updated public link.

## Start in this folder

1. Obtain the reviewed kit folder from your colleague. Keep hidden folders when
   copying or extracting it; do not copy only the visible Markdown files.
2. Open that folder as a project in **Claude Code or Codex**.
3. Start a new session and say **“Get started”** (or **“Empezar”**).

The folder already includes `AGENTS.md`, `CLAUDE.md`, both products' project
skills, an entry page and an offline installation check. No global configuration,
Git initialization or extra Python packages are needed. Python **3.9+** runs the
installer/checker, and Git must be available for the repository privacy checks.
If Python is absent, the assistant can still read the skills;
ask whoever manages your computer to provide Python before running the checks.
Do not describe an unchecked install as verified.

The assistant checks the files, discovers available company connections and
helps with one real question. Each person still signs in to their own company
accounts. Installation cannot grant access or operational authorization.

## Add it to another repository or folder

Open the destination folder in your assistant and paste this:

```text
Set up the Nebius AI workspace here using my downloaded, reviewed kit folder.
Locate that folder or ask me for its path. Read its README and installer.
Run the bootstrap preview for this destination, show me the exact files it will
create or change, then apply after my confirmation. Preserve my existing files.
Verify the installation, then follow START_HERE.md and help me get started.
Do not initialize Git, change global settings or publish anything.
```

If you prefer a terminal, from the downloaded kit folder:

```bash
python3 scripts/bootstrap.py init --workspace "/path/to/my-workspace"
```

This is a **preview**: it writes nothing. After reviewing it, apply that plan:

```bash
python3 scripts/bootstrap.py init --workspace "/path/to/my-workspace" --apply
```

Then open **the destination folder** in Claude Code or Codex, start a new session
and say **“Get started”**. The copied workspace continues working if the source
kit is moved or removed.

### If you already have instructions

A different `AGENTS.md` or `CLAUDE.md` stops the default install before any write.
To preserve their contents and append the kit instructions, preview explicitly:

```bash
python3 scripts/bootstrap.py init --workspace "/path/to/my-workspace" --integrate
```

Read the existing rules alongside the proposed kit rules. If compatible, rerun
with `--integrate --apply`. Fresh workspaces get a one-line `CLAUDE.md` import;
existing Claude instructions keep their original text plus that import.
Conflicts in other files, hand-edited managed files or `AGENTS.override.md`
require manual review. Using a dedicated empty workspace is also supported.
The installer never resolves conflicting instructions by deleting yours.

## What gets installed

| Location | Purpose |
|---|---|
| `AGENTS.md` | Shared instructions and request routing. |
| `CLAUDE.md` | Imports `AGENTS.md` for Claude. |
| `START_HERE.md` | First use, everyday prompts and recovery. |
| `.agents/skills/nebius-*/SKILL.md` | Codex project skills. |
| `.claude/skills/nebius-*/SKILL.md` | Identical Claude project skills. |
| `.nebius-kit/WORKFLOWS.md` | Daily, weekly and handover guidance. |
| `.nebius-kit/doctor.py` | Offline file/ignore checks. |
| `.nebius-kit/install.json` | Version, first initialization date and file hashes. |
| `.gitignore` | Appends a rule excluding `/.nebius-local/`. |

`.nebius-local/` is reserved for approved private context. Installation creates
no personal role map and does not mark onboarding complete. Setup can save
`.nebius-local/ROLE-MAP.md` only after showing you the contents and getting approval.
Closure can similarly save a sanitized `STATE.md`. Your corrections survive
role-map rebuilds. Legacy home-folder maps are never silently imported.

A bare `.skills/` folder is not the documented project discovery path. Codex uses
[`.agents/skills`](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills),
Claude uses [`.claude/skills`](https://code.claude.com/docs/en/skills#where-skills-live),
and Claude's [`@AGENTS.md` import](https://code.claude.com/docs/en/memory#agentsmd)
keeps the common rules in one place. No `.codex/config.toml`, credential files,
hooks or permission overrides are copied to colleagues.

## What you can ask

| Say | Result |
|---|---|
| “Get started” | Confirm identity/scope, inspect connections and answer one real question. |
| “What do I have today?” | Open assigned work and requests you reported, plus recent changes and one next action. |
| “Explain this ticket” | Meaning, recorded history, relevant precedents and the next owner. |
| “How do we do this here?” | Reconcile documentation, tickets and Slack, with sources and uncertainties. |
| “Rebuild my role map” | Refresh a routing map without losing your reserved corrections. |
| “Close the day” / “Prepare a handover” | A concise draft separating confirmed facts, assumptions and open questions. |

The three core skills remain `nebius-setup`, `nebius-role-map` and `nebius-ask`.
The [optional Jira dashboard skill](optional-skills/jira-personal-dashboard/)
is not installed automatically and its shared-system actions need approval.

## Connections and first use

The assistant inventories **Jira, Confluence, Slack channels, Outlook mail,
Calendar, SharePoint and relevant meeting tools separately**. Having Outlook
working does not establish SharePoint access. Seeing a tool does not prove that
its account or permissions are correct.

Use the connection/plugin settings available in your product, or `/mcp` where
supported, to inspect your setup. If your organization manages connections, ask
the person/team who configured your assistant. The installer neither installs
connectors nor copies another person's login, machine-specific IDs or settings.

No company connections yet? Setup asks for title, team and site and can make a
provisional role map from a public role posting. If that source is unavailable,
it produces scope questions. “Not searched” never becomes “no procedure exists”.
A role posting is a candidate baseline, not your contract or operating authority.

## Verify, update and recover

From your installed workspace:

```bash
python3 .nebius-kit/doctor.py
```

A pass covers local file integrity and privacy checks only. Confirm in a fresh
assistant session that instructions and skills load, then test a real scoped
read with your own account. Product/organization policies can disable local
customizations; the checker cannot inspect those policies.

- **Repeat installation:** same command; identical files and the original
  initialization date stay unchanged.
- **Update:** use a newly reviewed kit folder, preview, then apply. Only unchanged
  files recorded as kit-managed can be updated automatically.
- **Hand edits:** preserved, reported as conflicts. There is no force-overwrite flag.
- **Missing managed file:** rerun installation to restore it; private context stays.
- **Old global skills:** the checker warns when it finds the same names. In Claude,
  a personal skill can take precedence; ask the assistant to read the workspace's
  exact skill path. Global uninstall/migration is a separate reviewed action.
- **Wrong instructions:** inspect an `AGENTS.override.md`, parent instructions and
  product settings. Open the destination root, not an unrelated parent folder.
- **Failed write:** ordinary errors trigger rollback of this run. Do not run two
  installations concurrently. Process termination/power loss is not a guaranteed
  multi-file rollback; after interruption run the checker and review before retrying.
- **Remove:** ask for a removal plan listing the exact recorded kit paths and any
  appended instruction blocks. Preserve private notes and unrelated settings.
  There is no broad wildcard-delete or automatic global cleanup.

The SHA-256 manifests detect corruption and mismatched package files; they are
not a cryptographic signature proving who published the package. Use a reviewed,
fixed release/commit from a trusted source. Never pipe a moving download into a shell.

## Privacy and limits

Company systems stay read-only by default. Communications are drafted in the
chat for you to send. A closed ticket, delivered key, reachable port or completed
course does not prove access, repair success or readiness to operate.

Only approved preferences, sanitized patterns and source links belong in private
context. Credentials, hostnames, IPs, serials, asset IDs, customer data, topology,
ticket bodies, logs and transcripts stay in live systems. `.gitignore` prevents
ordinary staging; it is not encryption and does not protect already tracked files
or forced adds. Verify privacy checks before saving.

Validated locally with Python 3.9 on macOS and synthetic filesystem tests. Fresh
Claude/Codex discovery on a colleague's machine, account sign-in and Windows/Linux
execution still need the [acceptance walkthrough](docs/ACCEPTANCE.md).
See the [sanitized audit](docs/AUDIT.md) for findings and scope.
