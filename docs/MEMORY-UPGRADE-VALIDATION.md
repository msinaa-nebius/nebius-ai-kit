# Memory and upgrade acceptance — 2026-09-22

Scope: macOS/Linux, Python 3.9+, Codex and Claude Code project hooks. No model
training, background jobs, direct company access or global approval changes.

## Design

Two read-only command hooks deliver a short, fresh retrieval reminder at session
start/resume/clear/compact and before each prompt. The assistant then verifies the
employee's ownership and retrieves current private agreements. Automatic injection
of private notes was deliberately excluded: a copied workspace must not reveal its
previous owner's notes before identity is established. This differs from the
maintainer's single-owner memory hook. A receipt proves delivery of the public
reminder, not private retrieval, behavioral compliance or future reliability.

One canonical entry per correction, with scope/date/basis/application example;
readback and application check before confirming. No dependency on daily closure.
No new memory database or transcript ingestion. Existing STATE/ROLE-MAP preserved.

## Installation and upgrade cases

- Fresh non-Git folder; spaces, apostrophes, dollar signs and non-ASCII paths.
- Repeated install; repaired missing file; old schema-1 workspace records.
- v1/v1.1 exact historic global skills updated using checked-in historical hashes.
- Unknown/custom files stop before mutation unless individually reviewed/replaced.
- Existing unrelated settings, permissions, hooks and private notes preserved.
- Concurrent edits, broken JSON, links outside workspace and ordinary write failure.
- Bundle verification, archive allowlist and archive install from another directory.
- Hooks emit valid JSON for both events; no prompt, transcript or private canary
  in output; invalid inputs do not echo their payload; root/subdirectory execution.

## Acceptance on each employee's laptop

Follow `.nebius-kit/HOOKS.md`: review trust where required, then check the automatic
receipt before tools in a fresh chat and again on the next message, separately in
each assistant. With consent, retrieve and apply a real safe preference; correct
it and confirm a later turn uses the current version. Do not store fictional tests
as employee preferences. Explicitly report automatic delivery pending if absent.

Offline tests cannot approve hooks, prove accounts/connectors, simulate organization
policy, or guarantee future model obedience. A manual handler run is not a live
app test. Existing real Codex evidence for the personal-workspace hook informed this
design but does not certify this new kit or Claude's live delivery.

References: [Codex hooks](https://learn.chatgpt.com/docs/hooks),
[Claude Code hooks](https://code.claude.com/docs/en/hooks).

## Results on the maintainer laptop

- 42 automated tests passed; independent review reran all 42 successfully.
- Real historical skill contents from aeefe8d (v1) and 4acfae0 (v1.1): both
  assistants' six existing global skills updated in synthetic homes; repeat no-op.
- Real historical installers from 89f6264, d975582 and 1cccd64: installed into
  disposable workspaces, upgraded in place, private canary unchanged, repeat no-op.
- Current Codex app-server `hooks/list` recognized both project events with
  enabled=true, no errors/warnings and trustStatus=untrusted. Human review is
  correctly still required. No trust database or bypass was used.
- Actual new-kit automatic delivery and behavior in authenticated Codex/Claude
  sessions on another laptop are NOT certified by these checks. They are the
  final guided onboarding checks, with honest manual fallback when blocked.
