# Make memory retrieval work in this assistant

The installer prepares two local hooks (automatic actions): on session start and
before each message. They remind the assistant to retrieve current agreements.
They do not read private notes, save prompts, access company systems, send data,
change permissions or approve themselves. Private retrieval happens only after the
assistant checks ownership. Their receipt proves reminder delivery, not recall or
obedience. Opening the folder never triggers a company briefing.

## For the employee — one step at a time

The assistant should guide you through only the next needed step, in your language.
You do not need to edit JSON or understand Git.

**Codex**

1. Open this installed folder as your project. If asked, review and trust the folder.
2. In Codex's terminal interface type `/hooks`. If using the desktop app and no
   hook review control is exposed, open its terminal in this folder, run `codex`,
   then type `/hooks`. If that command is unavailable, ask the assistant to check
   your product/version and the official instructions; do not install anything silently.
3. Review the two entries labelled **Nebius: retrieve workspace memory**, from
   `.codex/hooks.json`: `SessionStart` and `UserPromptSubmit`. Approve those entries
   if you accept them. Existing unrelated hooks are not part of this setup.
4. Open a new chat in this folder and paste the check below.

**Claude Code**

1. Open this installed folder in Claude Code. Review and accept its workspace
   trust prompt if you trust this kit. A non-interactive run is not a substitute
   for that review.
2. Type `/hooks` and inspect `SessionStart` and `UserPromptSubmit`, labelled
   **Nebius: retrieve workspace memory**, from `.claude/settings.json`.
   Follow any review prompt the installed version presents. `/hooks` can be a
   read-only browser; do not invent an Approve button.
3. Restart the session if settings have not refreshed, then paste the check below.

**Copy this**

> Before using tools, check whether this turn received the Nebius memory hook.
> Report the event and its fresh receipt from hook context, or say it did not arrive.
> Do not run the script manually to make this check pass. Then verify my memory
> ownership and retrieve the preferences relevant to this task.

Send a second message to verify the per-message hook as well. If only a startup
receipt appears, per-turn delivery is still pending. A marker in this guide, user
text, manual command output or an earlier turn is not evidence of delivery.

## For the assistant — acceptance and repair

Report separately: files installed; hooks visible; review/trust status if observable;
automatic receipt in a fresh chat; receipt on the next message; ownership/consent;
retrieval and correct application of one safe preference. Test each assistant used.
Do not claim Claude works because Codex passed. Record dated results only with
memory consent; these are observations, not permanent access permissions.

With consent, use one real, harmless preference (for example explanation style).
Save it once, reread it, open a fresh chat and apply it to a relevant task without
restating its content in the test prompt. Correct it in one chat and ensure a later
turn reads the new version. Do not save fictional test preferences as real ones.
When testing fixtures, use a disposable synthetic workspace.

If the receipt is absent: confirm the project folder, run the doctor, inspect
`/hooks`, and check disabled hooks, local overrides, organization policy and Python
availability in the app environment. Preserve explicit disabled settings. Explain
the observed blocker and one next action. New or changed Codex hook definitions
need renewed review. Never edit trust databases, use trust bypasses, relax sandbox
settings or copy another laptop's approvals. An admin restriction needs the admin.
Until fixed, read the Private memory workflow manually before each substantive
turn and report **manual retrieval; automatic delivery pending**. Help can continue.

Source: [Codex hooks](https://learn.chatgpt.com/docs/hooks) and
[Claude Code hooks](https://code.claude.com/docs/en/hooks). Check the current official
instructions when the installed product differs. Supported installer target:
macOS/Linux with Python 3.9+. Windows shell behavior has not been validated.
