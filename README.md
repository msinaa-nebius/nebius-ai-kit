# Nebius AI kit

You already have Claude Code or Codex and every connector wired: Jira, Confluence,
Slack, Outlook, Zoom, Granola. Most people still use it as a chat window.

This kit turns it into a colleague who knows **your job** — not software engineering in
general, not "AI productivity", but the responsibilities of the role you were hired for
and where the truth about each of them lives in this company today.

It takes one paste, two short confirmations, and a first pass over your own sources.

---

## Install

Open Claude Code or Codex and paste this:

```
Install the Nebius AI kit, pinned to release v1.

BASE = https://raw.githubusercontent.com/msinaa-nebius/nebius-ai-kit/v1/skills

1. Fetch BASE/MANIFEST.txt
2. For every path listed there, fetch BASE/<path> and write it to BOTH
   ~/.claude/skills/<path> and ~/.codex/skills/<path>, creating folders as needed.
3. Do not modify, overwrite or delete any file that is not listed in the manifest.
4. Verify: re-read every manifest path at BOTH destinations and confirm each file
   exists, is not empty, and starts with a YAML block containing "name:" and
   "description:". Report the result per destination.
5. Only if every file passed, run the nebius-setup skill. If any failed, say exactly
   which ones and stop — do not run a partial install.
```

The `v1` in that URL is deliberate: it points at a reviewed, frozen release rather than
whatever is on the main branch right now. These files get read by an assistant that can
see your company's Jira, Confluence, Slack and mail, so they should not be able to change
under you between one install and the next.

Step 4 exists because a half-finished install is worse than a failed one: it looks like
it worked and then behaves oddly a week later.

**Writing to both directories is on purpose.** Claude Code reads `~/.claude/skills/` and
Codex reads `~/.codex/skills/`; they are separate and nothing syncs them. If you only use
one product, the other copy is harmless. If a destination fails — a managed machine, a
permissions prompt — the install reports that destination and carries on with the other.

**Updating** is pasting the same block with a newer tag. The three managed files are
overwritten; nothing else is touched.

**Uninstalling** is deleting these three folders from both directories:
`nebius-setup`, `nebius-role-map`, `nebius-ask`.

---

## What you get

| | |
|---|---|
| `nebius-setup` | Runs once. Works out who you are and what you might be accountable for, then builds your role map. |
| `nebius-role-map` | Rebuilds that map. Run it when you change team, project or scope. |
| `nebius-ask` | "How do we do X here?" Answers from Confluence, Jira and Slack together, with sources, owners and — first of all — where those sources contradict each other. |

You do not have to remember any of these names. Ask in plain language, in whatever
language you prefer, and the right one runs. Typing the name works too.

---

## The one thing worth understanding

Every public Nebius job posting states what its role is expected to do. Your company's
Confluence and Jira state what is actually written down and being worked on. **Nobody has
ever put those two lists side by side.**

`nebius-setup` does exactly that, on your machine. The interesting output is not the part
that matches — it's the part that doesn't: responsibilities that look like yours with no
procedure you can find. Those become questions for your manager, and most people take six
months to work out which questions to ask.

**Read that as questions, not as findings.** A job advert is a recruiting document, not
your job description, and a search that finds nothing has not proved that nothing exists —
the page may be named differently, sit in a space you cannot read, or live in SharePoint.
The kit says *"I did not find this in Confluence or Jira"* and names where it looked. Only
your manager or the owner can turn that into a confirmed gap. Any tool that tells you your
team has undocumented procedures, on the strength of one round of searching, is lying to
you — including this one, if you read it that way.

---

## What this kit does not do

- **It never acts without you saying yes.** No skill here sends a Slack message, creates
  or transitions a Jira issue, publishes a Confluence page or replies to an email on its
  own. It drafts, shows you the draft, and asks. Permission is per action, not per
  session — it asks again next time. Anything other people can see, you approve first.
- **It ships no company knowledge.** Nothing in this repository is internal, which is why
  the repository can be public, which is why you can install it without a terminal or a
  git client. Your *role map*, however, is a different matter — see below.
- **It does not copy procedures.** The role map holds links, titles, owning teams and
  dates: a routing table, never a copy. Procedures, tickets, logs, hostnames, serials,
  capacity figures and customer data stay in the live systems where they belong.

## What it does hold, and where

`~/nebius-ai/ROLE-MAP.md` is a local file on your laptop containing your team's Jira
projects, Confluence spaces, channel names, page titles and internal URLs. None of that
is secret on its own. Together it is a small map of how your team works and where it is
thin, sitting outside every access control your company has.

So: the kit asks before it saves that file, and shows you what is going in. If you would
rather it saved nothing and simply answered in the session, say so — everything still
works.

## Maintenance, honestly

Both inputs are fetched live, so the map reflects today and there is no index to rot.
That is not the same as no maintenance.

Connector tool names change. Confluence gets reorganised. Products move where they look
for skills. When that happens nothing breaks loudly — it degrades quietly, which is
worse. Expect this to need an hour of somebody's attention a few times a year, and treat
a role map older than a few months as a lead rather than as truth.

---

## Support

There isn't a support channel, by design. Three checks cover almost everything:

1. **Are the skills installed?** Paste the install block again; step 4 tells you.
2. **Are the connectors reachable?** If Jira or Confluence is not answering, that is not
   this kit — that is IT.
3. **Did the run finish?** Ask the assistant to say whether it completed or stopped
   early, and where. A bad answer from a complete run is a different problem from a run
   that quietly stopped halfway.

Beyond that: tell the assistant the answer was bad and why. That is the whole debugging
procedure, and it works better than you expect.

---

## Contributing

The kit contains no role-specific content, so there are no role packs to write and none
to maintain. If a step consistently produces a worse answer than doing it by hand, open
an issue saying so. Removals are more welcome than additions.
