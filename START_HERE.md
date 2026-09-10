# Start here

Open **this folder** in Claude Code or Codex and say:

> Get started. Check what is installed and which company systems you can read,
> then help me with one real work question.

Or say it in your own language. You do not need to know skill names.

The assistant follows `AGENTS.md`; Claude imports it through `CLAUDE.md`.
If this session was already open during installation, start a new session in this
folder. If skills do not appear, ask it to read the relevant local `SKILL.md`.

## Three separate checks

1. **Files installed:** `python3 .nebius-kit/doctor.py` checks the local kit.
2. **Company access:** the assistant checks the tools actually available in the
   session and the outcome of scoped reads. Each person signs in themselves.
3. **Useful first answer:** one work question answered with live sources,
   uncertainty and the next step. No connector? Setup still gives a provisional
   role map and explains what could not be verified.

Installation cannot log you in, grant permissions or certify safe operation.
This kit does not replace company onboarding, safety training or approved procedures.

## Everyday use

- “What do I have today?” — full open workload, recent changes and one next action.
- “Explain this ticket” — meaning, recorded history, precedents and ownership.
- “How do we do this here?” — sources, conflicts and what remains unknown.
- “Rebuild my role map” — refresh scope without losing your corrections.
- “Close the day” / “Prepare a handover” — a concise draft with confirmed facts,
  open questions and the next action; saving requires your approval.

Private context belongs in `.nebius-local/`. It is excluded from ordinary Git
staging. Nothing is saved there during setup until you approve its contents.
The assistant never needs your password pasted into the chat.

Your role map is optional. With no saved map, discovery may need repeating in a
future session. Old maps elsewhere are not imported automatically: confirm the
right person, team and destination first.
