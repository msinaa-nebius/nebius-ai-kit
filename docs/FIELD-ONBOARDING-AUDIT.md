# Field onboarding audit — 2026-09-17

Scope: both conversations titled “Instala nebius-ai-kit” and “Empezar configuración”,
including all six user turns, the asynchronous preference reply, tool calls/results,
validation output, source qualifications and the final saved-context write. The
installation transcript was reviewed directly; a separate agent reviewed the full
onboarding transcript. This report keeps only sanitized product findings, not
company records, identities, role payloads or private context.

## Findings and changes

| Observed behavior | Product correction |
|---|---|
| Installation, doctor and repeat installation succeeded, then the assistant required another conversation. | Continue by reading the installed skill directly; restart only for an observed runtime limitation. |
| The first onboarding response checked tools and asked for a work task before personalizing. | Explicit completion checks for scope, responsibilities, experience, explanation style and memory choice. Urgent work and explicitly deferred questions remain possible. |
| The employee had to ask what had actually been installed. | Start with a three-sentence explanation of local instructions, app connections and optional private context. |
| Experience and preferred explanation depth were omitted until the employee objected. | Ask once when unknown; preserve self-assessment by topic, without inferring qualification. |
| The presented responsibility map became mostly a source index when saved. | Retain every sanitized responsibility-to-source row and its qualification; compare saved rows with the presented map. |
| Role discovery recovered an entry point from maintainer memory. | Discover through confirmed role/team/site and available sources; no hidden dependency on maintainer memory. |
| Meeting services were not all tested until named; later lists returned no results. | Inventory Zoom and Granola separately; distinguish empty successful samples, unavailable tools, failures and untested access. |
| Repeated Confluence failures preceded a successful browser fallback. | Bound retries/alternatives; preserve unresolved coverage and never equate timeouts with denial. |
| Final wording implied nothing remained to install despite only one runtime being exercised. | State readiness only for the tested product; file parity does not establish another assistant's connectivity. |

The previous “first useful task” shortcut was a design error in the kit itself:
it allowed an installation check to replace onboarding. A task is now optional
at the end, not a substitute for personalization or a condition for completing it.

## Retained safeguards

Owner checks, voluntary private memory, scoped file writes, existing-note
preservation, draft/outdated source qualifications and read-only company access
remain in force. Public job adverts provide candidate scope, not local authority.
New joiners and nontechnical roles do not require ticket history or a job advert.

## Validation boundaries

Automated filesystem tests cover installation, preservation, generated parity and
packaging. An independent instruction review and synthetic conversation rehearsal
check the revised flow; they do not establish actual behavior in a signed-in Claude
Code session or a colleague's laptop. The observed field conversations prove the
old installation succeeded and expose the old onboarding defects. A future real
run remains the evidence needed for the revised end-to-end experience.

Independent review confirmed the revised gates and caught one remaining ambiguity:
recording a timeout must not count as verified scope. The skill now distinguishes
initial setup with pending source verification from a validated role map. A
synthetic logistics scenario exercised mixed experience, declined memory, absent
Jira, failed Confluence and an empty Zoom result without inventing responsibilities.
