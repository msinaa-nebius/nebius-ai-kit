---
# nebius-ai-kit 2.0.0 — workspace-managed copies; local edits are preserved as conflicts
name: nebius-setup
description: Set up a Nebius employee's role buddy and on-demand work assistant in this workspace. Check local installation and live connections, confirm scope, offer private memory and help with one real task. Use for first use, get started, empezar, onboarding, or checking a setup after changing computer or assistant.
---

# Setup

Success means the employee can get useful, source-backed help for their actual job
and resume later. Onboarding is complete when the checks below are addressed or explicitly deferred by the employee; a first work task is optional. Keep messages brief, in their
language, with one question at a time. Do not ask them to understand skills or Git.
No scheduled jobs, background scans or notifications. Follow workspace AGENTS.md.

## 1. Establish the workspace and person

Find the nearest root containing `.nebius-kit/install.json`; read START_HERE.md.
Run `python3 .nebius-kit/doctor.py` there if Python 3.9+ is available. If absent,
explain the unchecked installation and offer the organization-approved Python installation route, without installing anything silently; offer
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

Explain the product before probing, in three short sentences: this folder contains
shared instructions for a role buddy and an on-demand work assistant; connections
belong to the current app and still need checking; private preferences are saved
only if the employee chooses. Distinguish installing files from configuring a person.
Read each needed instruction file completely; split reads if output is truncated.

## 2. Check useful connections, then help close gaps

Briefly announce that you will check the account and small read-only samples of
work systems. Inventory tools by capability in THIS session, including deferred
tool discovery where available. Names and identifiers differ across laptops.
Do not assume ChatGPT, Codex, Claude web and Claude Code expose the same tools.

Check separately: Jira, Confluence, Slack channel search, Outlook mail, Calendar,
SharePoint, Zoom recordings and Granola notes separately. Include every service the employee named; report unavailable or not tested explicitly. Other role-specific systems
are optional. No universal requirement to install every connector.

Use a profile lookup for account identity where supported, then the smallest useful
read for each relevant available capability. Reuse successful reads from this
session instead of probing twice. Examples: one assigned Jira issue, one relevant
Confluence page, one public channel search result, one recent mail, today's calendar,
one accessible library, a short personal-meeting list. Keep payloads in-session.
Prefer metadata and minimal selected fields for connection probes, not full email HTML or document bodies. Use body reads for relevant role research. No DMs or broad staff activity searches. Respect connector-specific consent rules.
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

Only make claims backed by actual results. Prioritize connections needed for role discovery or an already requested task. If they want help, guide ONE supported step at a time:

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

## 3. Personalize before inviting the first task

Use verified directory fields as leads and ask the employee to confirm missing
role, team and site. Do not ask them to write their own job description. Discover
responsibilities using `nebius-role-map`: current internal role/team sources first,
with an official public job advert as an optional candidate baseline. Cross-check
the available responsibility headings with internal sources, distinguish confirmed
scope from candidates and gaps, and present a brief summary for correction. Recent
tickets are examples, not the whole job. Never assume a site, seniority or access.
Research must work without the maintainer's global memories or private bookmarks.

Ask about experience and preferred explanations unless already answered. For example:
“What parts of your work do you know well, where would you like guidance, and how
would you like me to explain things?” Tailor examples to their role; do not give a
logistics employee a Linux questionnaire. Preserve their self-assessment by topic;
strong experience in one area does not imply it in others or prove authorization.
Default to short plain-language explanations; provide technical detail when useful.

Ask only the next missing question, reuse all answers, and let the employee defer
personalization. Do not jump to “What would you like help with first?” while these
items or the memory choice are still unaddressed. If they already asked for urgent
work, help immediately and name the deferred setup items without blocking that work.
Keep the map in chat until step 4; no duplicate save approval.

## 4. Offer memory, including when no connector works

Follow “Private memory” in `.nebius-kit/WORKFLOWS.md`. Ask once whether this employee
wants safe preferences, confirmed corrections and source pointers remembered.
Record owner, choice, date and consent provenance only if the local privacy checks
pass. Consent applies to this employee/workspace, not every colleague using the kit.
A decline remains useful and must not trigger repeated pressure. Existing valid
consent need not be requested again. Unknown interpretations still need confirmation.

## 5. Verify hooks and continuity, then offer useful work

Read `.nebius-kit/HOOKS.md` and guide its activation in the current assistant,
one plain-language step at a time. The employee reviews whatever trust the product
requires; never approve it through a bypass. Check fresh hook delivery before tools,
then ownership and actual preference retrieval/application separately. Repeat in
the other assistant only if the employee uses it. Explicitly deferred or blocked
activation means manual retrieval, not automatically working memory. A fresh chat
is justified here to test actual delivery; ordinary skill discovery alone is not.
Do not repeat role questions or consent already confirmed for this employee.


If a work task was requested, route it: company questions and tickets to `nebius-ask`; role
scope to `nebius-role-map`; daily planning, meeting prep, guided work, drafts and
handover to the relevant mode of WORKFLOWS.md. Give the answer, its evidence and
one next step. Without live access, provide clearly provisional help or a concrete
connection step, never an invented internal answer.

With memory consent, save the topic-specific experience and explanation preference
in STATE.md and the responsibility-to-source mapping in ROLE-MAP.md. Preserve each
discovered responsibility as a sanitized category, source link and qualification;
a source index alone loses the map. Reread the saved sections against the in-chat
map and confirmed preferences, then report what was remembered. Do not save source payloads or ticket status.
If a map was declined but memory was accepted, future sessions can use STATE.md;
absence of a map is not a reason to repeat the consent question or discard scope.

Before closing, check: plain-language product explanation; local file check;
current-product capability results and gaps; confirmed role/team/site; sourced
responsibility map with uncertainties; experience and explanation preferences;
memory choice and verified save or session-only use; hook delivery and behavioral
continuity results, or explicit manual fallback. Each must be addressed or
explicitly deferred, not silently omitted. Recording a failure does not make a check verified. When
sources remain blocked, describe “initial setup with source verification pending”,
not a complete or validated role map. No connectors or a memory decline need
not block setup: explain what remains provisional.

Close in a few lines with configured, deferred and blocked items. Say “ready here”
only for the tested assistant; file parity does not prove another app is connected.
Offer one example relevant to their role and invite the first task, without making
it a completion requirement. Never claim “nothing left to install” across products.
Continue in this session by reading local skills directly. Only request a new
session if the target cannot actually be used here, explaining the observed reason.
Never equate onboarding with operational authorization.
