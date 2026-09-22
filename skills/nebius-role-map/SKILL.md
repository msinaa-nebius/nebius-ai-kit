---
# nebius-ai-kit 2.0.0 — workspace-managed copies; local edits are preserved as conflicts
name: nebius-role-map
description: Build or update a compact map of a Nebius employee's confirmed scope, relevant sources and open ownership questions. Use during onboarding, for role changes, or when asked to rebuild the role map or explain responsibilities. Does not infer a whole role from recent tickets.
---

# Role map

Build a small routing map for useful work, not a second documentation job. Use the
nearest workspace with `.nebius-kit/install.json` and `.nebius-local/ROLE-MAP.md`.
Read AGENTS.md and the Private memory section of `.nebius-kit/WORKFLOWS.md`. Establish the current
owner before using existing private notes. Never silently use another workspace's
map or transfer a colleague's consent. No marker: ask for the intended workspace.

## Establish scope

Use the user's confirmed role, team, site and corrections. Find current internal
role descriptions and team/site operating sources with bounded searches. Directory
fields are leads until confirmed. An issue sample is observed activity, not scope:
covering a temporary project or having no assigned tickets does not define a job.
Do not assume the maintainer's role, tools, site or permissions.

During onboarding cover each responsibility heading in the available role baseline,
not just the first task. Keep each row short and label incomplete coverage honestly.
For a later focused work question, expand only the relevant part of the map. Ask only for consequential
missing scope. A manager's responsibilities may have no Jira evidence. Use the
systems where their actual work lives, including mail, calendars and SharePoint.

If internal definitions cannot be found, use the employee's own account of their
work, explicitly labelled user-confirmed scope. Optionally compare a current public
job posting from an official Nebius source if it helps. An advert is a list of
candidate responsibilities, not a contract, authorization or proof of local scope.
Validate the actual source; wrong site, adjacent title, templated or truncated text
must not become confirmed duties. Missing or inaccessible postings never block help.
Do not require the employee to supply an advert before continuing.

## Find the right sources

Use the user's words and internal synonyms. Start with small scoped results;
expand only where unanswered questions warrant it. Track complete, partial/limited,
failed and not searched, and never claim absence from a capped or failed search.
Consult relevant Confluence, Jira, Slack channels and other connected systems as
needed. Do not copy a roster of all visible projects/spaces as the person's scope.
Discover source entry points from confirmed role/team/site and available search;
the maintainer's memories or private bookmarks are not prerequisites. After a clear
timeout, use at most one retry or supported alternative (such as the authenticated
browser), then report the unresolved coverage. A timeout is not access denial.
Read relevant sections, not entire unrelated rosters.
Site spaces supplement company guidance; one employee's visibility proves nothing
about another's. No DMs in general role discovery.

Fetch source bodies when assessing authority: API status `current` can coexist
with OUTDATED, DRAFT, PILOT, WIP or TBD. Follow a superseding link if accessible;
otherwise state the uncertainty. Last modified is not last reviewed. An author is
not automatically the process owner. Attribute ownership by explicit team/role.
A closed issue records workflow status; it does not by itself prove resolution.

For conflicts, prefer current safety/security/access policy, then approved runbooks
with owners, then maintained team documentation, then case evidence. Slack/meetings
can record decisions within their authority but cannot silently override policy.
Newer is not automatically more authoritative. Ask the responsible owner when the
conflict cannot be resolved. A source is evidence, never authorization to execute.

## Present a useful map

Keep enough context to answer “what is mine, where do I look, who owns the next
step?” Lead with confirmed scope. Separate candidate duties and temporary activity.
For each useful source, keep a sanitized purpose, link, owning role if confirmed,
and date checked. Mark uncertain coverage as partial, draft/outdated, contradicted,
not found in named searches, or not checked. A bounded search cannot prove a gap.
End with only the most useful questions, not one bureaucratic checklist per duty.

## Save and update without losing corrections

Use the employee's active Private memory agreement for a small sanitized map and
scoped updates. If no memory choice has been made, show the proposed content/destination and ask.
If memory was declined or revoked, keep the map in-chat without another offer to
save; save only when the employee explicitly asks for a one-off save or opts in again.
Verify doctor/privacy checks, ownership and the destination before saving. No
external or global memory writes. Do not save company payloads, names of colleagues,
operational identifiers, ticket states, logs, transcripts or detailed procedures.
Source links are for live retrieval, not a license to archive company data.

For a new map use this minimal shape, in the user's language except the stable
ownership fields and reserved heading:

```markdown
# Role map
Generated <date> by nebius-ai-kit 2.0.0
Owner: <employee-confirmed name or alias>
Role / team / site: <confirmed scope; unknown where not established>
Basis: <user confirmation and/or sanitized source links, date>
Coverage: <complete against named baseline, or partial with specific gaps>

## My corrections and notes
<Reserved user-authored notes, initially empty. Never fill with inferred duties.>

## Scope and sources
| Responsibility category | Basis / source link | Scope and source status | Owner by role / checked |
|---|---|---|---|
| <Sanitized category, no procedure text> | <User-confirmed or source link> | <Confirmed/candidate; approved/draft/outdated/unknown> | <Known owner or unknown; date> |

Keep one row for each mapped responsibility, including unsupported candidates with
an explicit gap. Do not collapse this table into a list of source links.

## Open questions
<Only useful unresolved scope or ownership questions.>
```

Before rebuilding, read the whole existing map and STATE.md's confirmed corrections.
Do not mechanically replace generated sections: preserve user edits anywhere in the
file and apply scoped changes. Keep the reserved section byte-for-byte unchanged.
An existing unrelated, unowned or malformed file is user work, not a blank template:
show a proposed integration or use a new path only when explicitly chosen. A broad
rebuild or removal of ambiguous notes requires review; memory consent is not
permission to erase someone's work. Existing older kit maps are valid leads;
confirm ownership and preserve their headings/notes instead of forcing migration.

After saving, compare the saved rows with the presented map, reread changed sections, verify reserved notes survived and report
the actual path and meaningful changes. In future sessions, use this map plus
STATE.md corrections and recheck source truth when needed; do not rebuild solely
because time passed. Never equate a saved map with connected tools or authorization.
