# Start here

Open **this folder** in Claude Code or Codex and say:

> Get started. Check what is installed and which company systems you can read,
> confirm my role, experience and preferences, and help me get started.

Or say it in your own language. You do not need to know skill names.

The assistant follows `AGENTS.md`; Claude imports it through `CLAUDE.md`.
Continue in the same session by reading the relevant local `SKILL.md` directly if
skills do not appear. Start another session only if this app cannot use the target
folder here. These files supply shared working instructions; connections and logins
belong to each app. Nothing runs in the background.

## Setup in three parts

1. **Files installed:** `python3 .nebius-kit/doctor.py` checks the local kit.
2. **Company access:** the assistant checks the tools actually available in the
   session and the outcome of scoped reads. Each person signs in themselves.
3. **Your buddy configured:** confirm role/team/site, cross-check responsibilities,
   ask about experience and explanation preferences, and offer private memory.
   Then choose a first task if you want. Missing access or skipped questions remain
   visible gaps; neither should be disguised as completed personalization.

If Python 3.9+ is unavailable, the assistant explains the unchecked installation
and the organization's approved installation route. It can still help read-only;
it must not silently install tools.

Installation cannot log you in, grant permissions or certify safe operation.
This kit does not replace company onboarding, safety training or approved procedures.

## Everyday use

Ask whenever you need help. Opening this folder does not start a daily review,
and setup creates no scheduled checks or notifications.

- “What do I have today?” — full open workload, recent changes and one next action.
- “Walk me through this” — one useful step at a time, with an explanation.
- “Prepare this meeting” — context, decisions needed and questions to bring.
- “Draft a reply” — a ready-to-use message, without sending it.
- “Explain this ticket” — meaning, recorded history, precedents and ownership.
- “How do we do this here?” — sources, conflicts and what remains unknown.
- “Rebuild my role map” — refresh scope without losing your corrections.
- “Close the day” / “Prepare a handover” — a concise draft with confirmed facts,
  open questions and the next action; remember safe lessons if you opted in.
- “What do you remember?” / “Correct this” / “Stop remembering” — inspect and
  control the private context used by both assistants.

Private context belongs in `.nebius-local/`. It is excluded from ordinary Git
staging. During onboarding, you choose whether to let the assistant remember safe
preferences and lessons there. With your initial consent it keeps those notes useful
without asking every time, tells you what changed, and lets you correct or stop it.
Uncertain decisions still need confirmation. Company records stay in their sources.
The assistant never needs your password pasted into the chat.

Your role map is optional. With no saved context, discovery may need repeating in a
future session. Old maps elsewhere are not imported automatically: confirm the
right person, team and destination first.
