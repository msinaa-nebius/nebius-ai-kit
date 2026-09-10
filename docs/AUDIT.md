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
