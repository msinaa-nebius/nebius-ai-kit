# Nebius AI kit

Your **role buddy and personal work assistant** in Codex or Claude Code. Understand
how work is done here, prepare your day and meetings, and draft replies. It adapts
to your role, team and site, and helps **when you ask**.

**Workspace edition · 2.0.0-dev.** Use the current `main` branch for this complete
workspace setup. The historical v1.1 release installs global skills only and is
not the installation route below. [Validation scope](docs/ACCEPTANCE.md).

## Install by asking your assistant

Open a local project in Codex or Claude Code and say:

> Install https://github.com/msinaa-nebius/nebius-ai-kit as my Nebius work assistant.
> Follow the repository's current README. Preserve anything I already have, then
> help me get started.

The assistant follows the installation contract below. You choose the destination
if it is not clear, sign in to your own company accounts, confirm your role and
choose whether it may remember safe context. Then you work on one real question.
No need to create AGENTS.md, CLAUDE.md or hidden skill folders yourself.

**Already downloaded?** Open the extracted folder as the project and say “Empezar”
or “Get started”. Keep the whole folder, including hidden files.

## Installation contract for the assistant

1. Inspect the current destination and its instructions. A request to install the
   kit authorizes that scoped local setup; honor the person's actual approval rules.
   Ask for the destination only if unclear. Prefer a dedicated work folder when an
   existing project has conflicting instructions. Never overwrite their work.
2. Obtain the **complete source archive from the user's GitHub repository/ref**,
   resolving the ref to a commit where possible. Use the product's trusted download
   or browser tools, or GitHub **Code → Download ZIP** if no download tool exists.
   Do not copy just three skills or visible Markdown files. Do not use the old v1.1
   global-skill installer. No Git clone is required. Explain the exact destination
   and preserve an existing download rather than extracting over it.
3. Read the downloaded README and scripts before executing them. Python **3.9+**
   runs the installer and checker; no pip, Node.js, Homebrew or Git is needed for a
   standalone extracted workspace. Git is needed for tracking checks only when the
   destination is inside an existing Git repository. If Python is missing, do not
   pretend the check passed: the prebuilt instructions can still provide read-only
   help. Offer the organization's approved Python installation route, explain it,
   and obtain any needed installation authorization. Do not install a toolchain.
4. From the source folder, preview the target and inspect its plan:
   `python3 scripts/bootstrap.py init --workspace "/chosen/workspace"`.
   For an extracted folder used directly, run `python3 .nebius-kit/doctor.py` first;
   no copying is needed if it passes. A source checksum mismatch stops execution;
   never regenerate downloaded manifests to make the error disappear.
5. Apply the reviewed plan with the same command plus `--apply`, within the user's
   installation authorization. If it conflicts, show the exact files and offer a
   new folder or a reviewed `--integrate` preview. Integration appends instructions;
   it cannot resolve contradictory rules automatically. No silent global changes,
   git initialization, commits, permissions changes or publication.
6. Run the target's `.nebius-kit/doctor.py`, open **that target folder** in the
   assistant, then read START_HERE.md and its `nebius-setup` skill. If automatic
   discovery has not refreshed, start a fresh session there. Report file checks,
   current account/connectivity, saved context and first useful answer separately.
   Do not promise the download or login is complete until it is verified.

For reproducible distribution, share a reviewed fixed commit/release after the
[release checks](docs/RELEASING.md). The normal repo link follows its default branch;
local changes do not change what a colleague downloads.

## What it does

| Ask | Help you get |
|---|---|
| “What do I have today?” | Open work, meetings, things waiting on others, one next focus. |
| “How do we do this here?” | Current sources, ownership and unresolved conflicts. |
| “Explain this ticket; walk me through it” | Context, comparable precedents and one step at a time. |
| “Prepare this meeting” | Relevant context, decisions and questions. |
| “Draft a reply” | Concise message for you to send. |
| “Close the day” / “Prepare a handover” | Verified outcomes, uncertainty and next actions. |
| “What do you remember?” / “Correct this” / “Stop remembering” | Visible, controllable private context. |

Setup checks available capabilities **in the current assistant**, tests small reads,
and helps connect what the first task needs. Mail, Calendar and SharePoint are
separate capabilities. Tools may be visible but signed out, blocked or using the
wrong account. Your colleague's access does not establish yours. No connections?
You can still confirm your scope and get provisional help.

A role map starts from your confirmed responsibilities and current internal sources.
Public job descriptions can help but are never required. Your recent tickets are
only part of your work; the kit is not specific to one role or site.

## Private continuity, shared instructions

During setup you choose once whether to remember safe preferences, confirmed
corrections, source pointers and general lessons in `.nebius-local/`. Both assistants
read the same files. The kit shows what changed, preserves your notes and lets you
stop saving. It does not share chat history or logins between products.

Company records stay in company systems: no ticket bodies, transcripts, credentials,
asset identifiers or operational logs in the kit. Source links are rechecked when
used. `.gitignore` prevents ordinary staging, not forced publication or disclosure;
never share an employee's working folder as an installation package.

| Included | Purpose |
|---|---|
| `AGENTS.md` and `CLAUDE.md` | Common rules; Claude imports AGENTS.md. |
| `.agents/skills/` and `.claude/skills/` | Same local skills for both assistants. |
| `START_HERE.md` and `.nebius-kit/WORKFLOWS.md` | Onboarding and everyday work. |
| `.nebius-kit/doctor.py` and `install.json` | File checks and managed-file hashes. |

No scheduled activity, external writes or global configuration changes are enabled
by onboarding or memory consent. Shared actions need specific authorization.

## Update or recover

Use a newly reviewed source bundle, preview the existing destination and apply.
Unchanged kit files update; private context and edited files are preserved. Repeat
installation is a no-op. A missing managed file can be restored; a modified one
needs review. There is no force-overwrite option.

Run `python3 .nebius-kit/doctor.py` for installation problems. An
`AGENTS.override.md`, conflicting parent instructions or old global skills may
change what an assistant follows; the checker cannot prove actual discovery or
organization policy. Never remove global configuration automatically.

Ordinary installation errors roll back this run. After power loss or termination,
rerun the checker and review the result. Do not install concurrently. Hash manifests
check consistency, not publisher identity; use the intended trusted repository.

[Acceptance cases](docs/ACCEPTANCE.md) · [Maintainer release steps](docs/RELEASING.md)
· [Optional Jira dashboard](optional-skills/jira-personal-dashboard/)

Local discovery reference: [Codex skills](https://learn.chatgpt.com/docs/build-skills),
[Claude skills](https://code.claude.com/docs/en/skills),
[Claude imports](https://code.claude.com/docs/en/memory#agentsmd).
The small source-linked context approach is inspired by
[AIS-OS](https://github.com/nateherkai/AIS-OS), adapted to corporate roles and privacy.
