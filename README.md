# Nebius AI kit

Your **role buddy and personal work assistant** in Codex or Claude Code. Understand
how work is done here, prepare your day and meetings, and draft replies. It adapts
to your role, team and site, and helps **when you ask**.

**Workspace edition · 2.0.0.** Use the current `main` branch for this complete
workspace setup. The historical v1.1 release installs global skills only and is
not the installation route below. [Validation scope](docs/ACCEPTANCE.md).

## Install by asking your assistant

Open a local project in Codex or Claude Code and say:

> Install or update https://github.com/msinaa-nebius/nebius-ai-kit from main in
> my Nebius work folder. Update the kit, preserve my private notes and unrelated
> settings, guide any hook approval, and verify memory retrieval in a fresh chat.

The assistant follows the installation contract below. You choose the destination
if it is not clear, sign in to your own company accounts, confirm your role and
choose whether it may remember safe context. It asks about experience and preferred
explanations, maps your responsibilities, then offers a first work question.
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
   discovery has not refreshed, read the local skill directly and continue onboarding
   in the same session. Restart only for an observed inability to use that target.
   Follow `.nebius-kit/HOOKS.md` for hook review and fresh-chat verification.
   Report files, hooks, current-product connections, personalization and memory separately.
   Check each command's exit status; a later success cannot erase an earlier failure.
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

Use the current **main** source archive in a separate source folder, not an old
release ZIP or a `git pull` over someone's working notes. Preview and apply to the
**existing work folder**; do not extract over it. This updates kit-managed files in
place and preserves `.nebius-local/`, unrelated files and other hook/settings keys.
Repeat installation is a no-op. The installer accepts the older workspace install
record and upgrades it. Never delete the record to bypass a conflict.

**v1 / v1.1 global-only installation:** those versions installed skills, not a
complete workspace. Install the current workspace as above. Then, from the reviewed
source folder, run `python3 scripts/legacy.py` to preview existing legacy Nebius
skills in both assistants (including the older `.agents/skills` location). Apply
with `--apply` within the employee's explicit install/update authorization. This
replaces only existing recognized Nebius skills; it never touches other skills,
authentication or global settings. Unknown edits stop the whole migration for
review. It does not automatically import old personal context. Both assistants
must follow the new folder's local instructions; global discovery may need a new
session. Keep the source folder until workspace and legacy migration both pass.

**Modified kit files:** the preview names conflicts and writes nothing. Inspect
those exact files and preserve useful employee rules before replacing obsolete kit
content with `--replace-file PATH` (repeat per reviewed file). This flag cannot
replace private notes or settings. For edited global skills, `legacy.py
--replace-skill NAME` is the equivalent explicit, reviewed replacement. Do not
blindly pass every file. Existing non-kit instructions can instead use `--integrate`.
Hook settings are merged; edited Nebius handlers require a scoped manual review.

**Hooks:** installation prepares both apps; each laptop/product must complete its
own trust review. The assistant follows [this short guide](templates/HOOKS.md),
checks a fresh chat and a subsequent message, then tests a real saved preference.
A pending approval or company restriction is reported as pending, never passed.
The hooks deliver a retrieval reminder; the assistant reads private preferences
only after confirming their owner. No login, approval database or private memory
is copied from the maintainer's laptop.

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
