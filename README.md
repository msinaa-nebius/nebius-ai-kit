# Nebius AI kit

You already have Claude Code (or Codex) and every connector wired: Jira, Confluence,
Slack, Outlook, Zoom, Granola. Most people still use it as a chat window.

This kit turns it into a colleague who knows **your job** — not software engineering
in general, not "AI productivity", but the actual responsibilities of the role you
were hired for, and where the truth about each of them lives in this company today.

It takes about ten minutes and asks you roughly one question.

---

## Install

Open Claude Code or Codex and paste this:

```
Install the Nebius AI kit.

1. Fetch https://raw.githubusercontent.com/REPLACE-ME/nebius-ai-kit/main/skills/MANIFEST.txt
2. For every path listed there, fetch
   https://raw.githubusercontent.com/REPLACE-ME/nebius-ai-kit/main/skills/<path>
   and write it to BOTH ~/.claude/skills/<path> and ~/.codex/skills/<path>,
   creating folders as needed.
3. Do not modify, overwrite or delete any file that is not listed in the manifest.
4. Then run the nebius-setup skill.
```

That is the whole installation. It only ever **adds** folders under
`~/.claude/skills/` and `~/.codex/skills/`. It never edits your settings, your
existing instructions or anything else you have configured — with one exception it
will ask you about out loud, showing you the file first.

**Updating** is pasting the same block again. **Uninstalling** is deleting the
`nebius-*` folders from those two directories.

---

## What you get

| | |
|---|---|
| `nebius-setup` | Runs once. Works out who you are and what you are accountable for, then builds your role map. |
| `nebius-role-map` | Rebuilds that map. Run it when you change team, project or scope — or every few months. |
| `nebius-ask` | "How do we do X here?" Answers from Confluence, Jira and Slack together, with sources, owners and — first of all — where those sources contradict each other. |
| `nebius-loose-ends` | What you promised someone this week that has no ticket behind it. |

You do not have to remember any of these names. Ask in plain language, in whatever
language you prefer, and the right one runs. Typing the name works too if you like
knowing exactly what you're invoking.

---

## The one thing worth understanding

Every public Nebius job posting states what its role is responsible for. Your
company's Confluence and Jira state what is actually written down and being worked
on. **Nobody has ever put those two lists side by side.**

`nebius-setup` does exactly that, on your machine, in ten minutes. The interesting
output is not the part that matches. It's the part that doesn't: the
responsibilities that are yours and have no procedure written anywhere. Those are
your questions for week one, and most people take six months to find them.

---

## What this kit does not do

- **It stores no company knowledge.** Your role map holds links, titles, owners and
  review dates — a routing table, never a copy. Procedures, tickets, logs, hostnames,
  serials and customer data stay in the live systems where they belong. Nothing in
  this repository is internal, which is why the repository can be public, which is
  why you can install it without a terminal or a git client.
- **It never writes to a shared system.** No skill here sends a Slack message,
  creates or transitions a Jira issue, publishes a Confluence page, or replies to
  an email. It will happily draft any of those into a local file for you to paste.
  Anything other people can see, you send yourself.
- **It does not go stale, because it holds nothing that can.** The job posting is
  fetched live. Your sources are fetched live. Rebuild the map whenever you want; it
  costs minutes.

---

## Support

There isn't any, by design.

- Something broken? Paste the install block again.
- A connector failing? That's not this kit. That's IT.
- A bad answer? Tell the assistant it was bad and why. That is the entire debugging
  procedure, and it works better than you expect.

---

## Contributing

The kit contains no role-specific content, so there are no role packs to write and
none to maintain. If you find a step that consistently produces a worse answer than
doing it by hand, open an issue saying so. Removals are more welcome than additions.
