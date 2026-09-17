---
# nebius-ai-kit 2.0.0-dev — workspace-managed copies; local edits are preserved as conflicts
name: nebius-setup
description: Set up a Nebius employee's role buddy and on-demand work assistant in this workspace. Check local installation and live connections, confirm scope, offer private memory and help with one real task. Use for first use, get started, empezar, onboarding, or checking a setup after changing computer or assistant.
---

# Setup

Success means the employee can get useful, source-backed help for their actual job
and resume later. A role map alone is not success. Keep messages brief, in their
language, with one question at a time. Do not ask them to understand skills or Git.
No scheduled jobs, background scans or notifications. Follow workspace AGENTS.md.

## 1. Establish the workspace and person

Find the nearest root containing `.nebius-kit/install.json`; read START_HERE.md.
Run `python3 .nebius-kit/doctor.py` there if Python 3.9+ is available. If absent,
explain the unchecked installation and follow README's dependency path; offer
read-only help meanwhile. Do not silently install tools, change global config,
initialize Git or relax permissions. A failed checker is not proof all help fails.
With no marker, follow the source checkout README installation route; do not choose
a home-folder memory path. Existing instructions and private files must survive.

Establish the current product (Codex or Claude Code), account and current employee
before using saved private contents. Inspect only ownership metadata first, not
another person's notes. Cross-check account profiles where available; conflicting
accounts are excluded until resolved. If identity cannot be checked, ask the user
to confirm ownership of this workspace. A name match alone is weak evidence.
A copied colleague's role map or consent must never be inherited: offer a new,
clean workspace without reading out, migrating or deleting their private notes.

A saved map or install record does not skip connection checks in a new assistant,
new laptop or requested setup check. For the same confirmed owner, reuse established
preferences and scope, asking only about missing or changed information. Do not
repeat the entire onboarding for an ordinary question.

## 2. Check useful connections, then help close gaps

Briefly announce that you will check the account and small read-only samples of
work systems. Inventory tools by capability in THIS session, including deferred
tool discovery where available. Names and identifiers differ across laptops.
Do not assume ChatGPT, Codex, Claude web and Claude Code expose the same tools.

Check separately: Jira, Confluence, Slack channel search, Outlook mail, Calendar,
SharePoint, and meeting notes/recordings when relevant. Other role-specific systems
are optional. No universal requirement to install every connector.

Use a profile lookup for account identity where supported, then the smallest useful
read for each relevant available capability. Reuse successful reads from this
session instead of probing twice. Examples: one assigned Jira issue, one relevant
Confluence page, one public channel search result, one recent mail, today's calendar,
one accessible library, a short personal-meeting list. Keep payloads in-session.
No DMs or broad staff activity searches. Respect connector-specific consent rules.
Do not open sensitive or unrelated records merely to make a test green.

A small successful query with zero results is **connected; no results in this
sample**, not missing access. A profile or library listing proves only that scope,
not access to every document. A tool missing from the session is **unavailable
here**, not proof that the app is uninstalled. Track available, identity confirmed,
read worked (including empty), denied, failed and not tested distinctly.

Show a short result in everyday language, for example:

> I can read Confluence and your calendar. Slack is available but needs sign-in.
> SharePoint is not available in this session, so I cannot look up its documents.
> Shall we connect Slack first, or continue with what works?

Only make claims backed by actual results. Prioritize the connection needed for the
employee's first task. If they want help, guide ONE supported step at a time:

- **Codex:** inspect the current product's plugin/connection surface or tools.
  Use the supported connection flow and the employee's own corporate account.
  Confirm the installed app's actual tools appear in this session, then retry the
  small read. If the control is unavailable, consult current official documentation
  rather than inventing a menu, endpoint or command.
- **Claude Code:** start with `/mcp` to inspect the session's connections; `/status`
  helps identify the active login. Some claude.ai connectors are inherited with a
  subscription login; other authentication modes or organization policies differ.
  Follow the current official connection path for that service, then verify in
  Claude Code itself. Do not remove authentication settings or duplicate servers
  without a separately explained and authorized change.
- An organization-managed restriction needs the responsible admin, not a bypass.
  Say the precise capability/error to ask about; draft the request if useful.

Reference current [Codex plugins](https://learn.chatgpt.com/docs/plugins) and
[Claude Code connections](https://code.claude.com/docs/en/mcp) when a repair is
needed. These are entry points, not a promise of identical UI on every version.
Never request passwords or tokens in chat or copy the maintainer's config.
After one repair attempt, retest; if blocked, report it and continue with accessible
sources. Let the user choose whether to troubleshoot further. No sign-in loop.

## 3. Confirm enough scope to help

Use verified directory fields and current internal role/team sources first. Recent
assigned work provides vocabulary, not the employee's whole job. Do not list every
visible project or space. Site access varies even within the same organization.
Ask for role, team and site only where missing; offer a short discovered summary
for correction. Never assume Madrid, IT infrastructure, seniority or permissions.
No activity is normal for a new joiner; managers may work mostly in meetings/mail.

Ask the one question that brings value: “What would you like help with first?”
Use a task they already named rather than asking again. Default to plain language;
ask about explanation depth only if it materially changes the help.

Use `nebius-role-map` for a compact in-chat first pass: confirmed responsibilities
and source pointers, with unknowns labelled. In this step draft only; defer saving
the map until the memory choice in step 4, so the employee is asked only once. A public job advert is optional fallback, never a
prerequisite. Do not audit every responsibility before answering the first task.

## 4. Offer memory, including when no connector works

Follow “Private memory” in `.nebius-kit/WORKFLOWS.md`. Ask once whether this employee
wants safe preferences, confirmed corrections and source pointers remembered.
Record owner, choice, date and consent provenance only if the local privacy checks
pass. Consent applies to this employee/workspace, not every colleague using the kit.
A decline remains useful and must not trigger repeated pressure. Existing valid
consent need not be requested again. Unknown interpretations still need confirmation.

## 5. Do useful work and verify continuity

Route the actual request: company questions and tickets to `nebius-ask`; role
scope to `nebius-role-map`; daily planning, meeting prep, guided work, drafts and
handover to the relevant mode of WORKFLOWS.md. Give the answer, its evidence and
one next step. Without live access, provide clearly provisional help or a concrete
connection step, never an invented internal answer.

With memory consent, save only the minimal reusable context, reread the scoped
change and say what was remembered. Do not save source payloads or ticket status.
If a map was declined but memory was accepted, future sessions can use STATE.md;
absence of a map is not a reason to repeat the consent question or discard scope.

Close in a few lines: files checked or unchecked; reads actually tested and remaining
gaps; useful task completed or blocked; private context saved or session-only.
If the assistant cannot load local instructions automatically yet, say exactly which
folder to open and start a fresh session there. Never call onboarding finished just
because files exist, and never call the employee operationally authorized.
