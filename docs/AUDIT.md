# Workspace installation audit

Date: 2026-09-10. Scope: local installer/readiness and a bounded read-only sample
of three previous work conversations, two Jira records, Confluence onboarding
content and related Slack channel messages. This is not a company-wide audit.
No company payloads, identities, topology or transcripts are included here.
Live evidence and exact internal references remain in the requesting conversation.

## Confirmed findings and changes

| Finding | Change |
|---|---|
| The prior installer copied three global skills but no workspace instructions or entry page. | Portable project files and both assistants' discovery directories. |
| Installation depended on an assistant interpreting a long prose script. | Python installer with preview, checksum verification, conflict checks and rollback. |
| Global role maps could override another workspace's context. | Workspace-first private map; legacy migration requires identity/scope confirmation. |
| A saved map, installed files and successful connector use were conflated. | Separate file check, live access result, saved onboarding and useful first answer. |
| Recent activity was used as if it were the full open workload. | Separate complete assigned/reported inventories and recent delta; explicit partial coverage. |
| A user's correction about responsibility was not consistently carried into later advice. | Preserve confirmed scope/corrections; separate role ownership from the team executing a dependency. |
| Connectivity was used too readily as a route to a practice session. | Separate access layers; no example passwords or actively automated practice targets. |
| Source metadata can say a page is current while its body says draft/pilot. | Inspect content status and authority, not only metadata. |
| A completed request does not establish each requested permission was implemented. | Require evidence of the particular outcome before asserting it. |
| Legacy tool claims assumed fixed fields and capability lists. | Discover current capabilities and use explicit ownership evidence. |

These patterns are generic. The kit does not ship the maintainer's job, site,
vendor matrix, assigned issues, internal page inventory or conversation history.

## Validation boundaries

Automated tests exercise fresh installs, preview, parity, repeatability,
instruction integration, updates, missing files, user edits, checksum failures,
manifest validation, symlink/hardlink collisions, write failure, postcheck failure,
concurrent edits detected before writing, ignore behavior and shadowing instructions.
Tests use synthetic local data and never authenticate to company systems.

Checksums establish byte integrity, not publisher authenticity. Instructions guide
behavior; they are not an enforced permissions boundary. Offline checks cannot
prove live skill loading, account access, answer quality or operational readiness.
No fresh session in a second assistant or colleague machine was exercised during
this audit. Follow ACCEPTANCE.md for that final product-level check.
The bundled Python skill validator could not run because PyYAML is not installed.
Core skill frontmatter was parsed independently with the system Ruby YAML parser;
the installer also checks names, descriptions and bundle integrity. No dependency
was installed to perform validation.

## Follow-up proposals

1. Run the same short acceptance flow with a colleague who has no prior global kit.
2. Run it once with an existing v1.1 install to verify the legacy-skill warning and
   explicit local-skill selection in both assistants.
3. Publish a fixed release only after these checks; replace the old install link.
4. If connector onboarding remains the bottleneck, document the organization's
   approved connection route with its owner, kept internally rather than bundled
   with personal settings in this public kit.

## Candidate closure — 2026-09-17

Expanded read-only history inventory found 106 distinct Codex root-session IDs
(including automations/review tasks) and 12 Claude session files under the relevant
work project. Keyword screening covered 779 Codex user-message records; this is
not a claim that every turn, image or tool result was manually audited. Selected
workflow corrections and the earlier colleague-installation report informed the
changes. No transcripts or internal operational examples were copied into the kit.

### Review loops and resulting changes

1. Independent onboarding review: removed the saved-map shortcut that skipped
   current-runtime checks; replaced availability-only claims with bounded live reads;
   added one-at-a-time connection repair and repository-URL installation intake.
   Internal/user-confirmed role scope now precedes optional public job postings.
2. Independent workflow review: added guided work, meeting prep/follow-up and
   drafts; roles with little Jira activity can use mail/calendar/documents. Help is
   on demand. Memory consent is visible, revocable and bound to its employee.
3. Cross-file re-review: eliminated overlapping save prompts and repeated offers
   after refusal. Check ownership of each private file separately. Preserve all
   user edits during map updates, not only a designated section.
4. Independent installer code review: closed false privacy passes from dangling
   Git metadata and environment overrides that select another index/repository.
   Added explicit archive allowlisting, hidden-folder inclusion and leakage canaries.

### Evidence, with limits

- 29 automated tests passed on this Mac using synthetic fixtures, including
  fresh install, repeat/update, conflicts, rollback, missing/broken Git, privacy
  checks and verification of an extracted allowlisted ZIP. The no-Git standalone
  branch uses mocked repository discovery; it is not a new-machine test.
- A copied bundle installed through its CLI from another directory, and the
  installed doctor still worked after the source copy was removed.
- A separate fresh subagent installed verified fixture workspaces and exercised
  synthetic memory recovery, mismatched owner refusal and revocation. New preference
  saving after revocation was checked with an unchanged file hash. This is a model
  behavior exercise inside this environment, not a second laptop or Claude runtime.
- Core skill YAML parsed with Ruby; bundle/parity verification and diff whitespace
  checks passed. The Python skill validator remains unavailable without PyYAML;
  no dependency was installed merely for that validation.
- Actual Claude CLI authentication reports no logged-in account. No authenticated
  Claude discovery or company-connection acceptance is claimed. A Codex CLI smoke
  was not launched under a stricter whole-process no-global-write test constraint:
  ephemeral execution alone does not certify that isolation.

The candidate improves concrete failure cases but cannot guarantee every laptop,
company policy, connector permission or future model response. Publication and a
colleague's own first-use acceptance are still separate gates. No background jobs,
company-system writes or publication were performed by these tests.

### Blind continuity recheck

A second subagent with a fresh context, not given the expected preference, read only
the installed synthetic workspace. It recovered the saved language/role preference,
recognized revoked saving consent and refused a differently owned role map after
owner-only inspection. It changed no files. This adds independent context-recovery
evidence; it still does not prove Claude Code startup or another physical laptop.

The built candidate archive contains 34 allowlisted files. Its actual extracted
bytes passed bundle verification, doctor and an unchanged reinstallation preview.

## Publication decision — 2026-09-17

The maintainer explicitly authorized committing and pushing this workspace edition
to main now, without waiting for additional laptop or authenticated Claude runs.
The limits above remain part of the evidence; publication does not turn them into
passed tests. The current README points to the workspace edition rather than v1.1.
