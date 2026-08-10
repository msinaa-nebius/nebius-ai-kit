# Nebius AI kit

You have Claude Code or Codex. This kit turns it into a colleague who knows **your
job** — not software engineering in general, not "AI productivity", but the
responsibilities of the role you were hired for and where the truth about each of them
lives in this company today.

It reads your company's systems through **connectors** — a connector is the plug that
lets your assistant read one system, such as Jira or Slack. **No connectors yet? The
kit still installs and still builds a first role map from Nebius's public job board**;
setup tells you exactly what each missing connector would add and how to get it. See
[Connectors](#connectors) below.

One paste and a couple of confirmations if your connectors are already set up; a few
minutes more the first time if they are not.

---

## Install

Open Claude Code or Codex and paste this whole block:

```
Install the Nebius AI kit, pinned to release v1.

BASE = https://raw.githubusercontent.com/msinaa-nebius/nebius-ai-kit/v1/skills

0. Before fetching or writing anything, tell me in my own language what this
   installs — the 3 skills by name with one line each (nebius-setup: one-time
   onboarding that reads my directory profile, recent Jira issues, linked
   Confluence spaces and my own Slack channel messages, shows me what it found,
   and builds my role map; nebius-role-map: rebuilds that map from the public
   Nebius job board plus my Confluence/Jira; nebius-ask: answers "how do we do X
   here?" from Confluence, Jira and Slack with sources). Say that files are
   written ONLY under ~/.claude/skills/ and ~/.codex/skills/ on this machine,
   that nothing is sent anywhere, and that setup will later ask separately
   before saving ~/nebius-ai/ROLE-MAP.md. Then wait for my explicit yes.
1. Fetch BASE/MANIFEST.txt with `curl -fsSL` (your web-fetch tool only if curl
   is unavailable; never summarise or reformat fetched content; never disable
   TLS verification). Lines starting with # are metadata; ignore blank lines;
   every other line is `<sha256>  <path>`. Accept only paths of the exact form
   <folder>/SKILL.md — no "..", no leading "/" or "~", no URLs — and expect
   exactly these three folders: nebius-setup, nebius-role-map, nebius-ask.
   Anything else: stop, install nothing, and show me the manifest. A 404 means
   the repository is private or the release is missing — do not retry against
   main; say exactly which URL failed.
2. Download every listed file into a temporary folder — not into the skills
   directories — and verify each against its sha256. If any fetch fails, any
   checksum mismatches, or a file does not start with a YAML block whose
   `name:` matches its folder: delete the temporary folder, install nothing,
   and say exactly which file failed and how.
3. Only when all three files verified: for each destination that exists or can
   be created (~/.claude/skills/ and ~/.codex/skills/), check whether any of
   the three folders already exists there. Identical content: say "already
   installed" and skip it. Different content: ask me once before overwriting —
   hand edits will be lost. Then copy the verified files, creating folders as
   needed and touching nothing else. If one destination cannot be written at
   all (permissions, managed machine), skip that whole destination and say so —
   a working install in one product is fine. Never leave a destination
   half-written: if a copy fails partway, remove what this run copied there
   before reporting.
4. Re-read the three files at each written destination, re-check each sha256
   there, and report the result per destination.
5. Only if all three files passed at at least one destination: if
   ~/nebius-ai/ROLE-MAP.md already exists, say the kit is installed/updated and
   that saying "rebuild my role map" refreshes it — do not rerun onboarding.
   Otherwise run the nebius-setup skill; if this session has not picked the
   skill up yet, read the installed nebius-setup/SKILL.md and follow it
   directly, or tell me to restart the session and say "get started". If
   verification failed at every destination, say which files failed and stop —
   never run a partial install.
```

Your assistant will ask you to approve a few things — fetching from
raw.githubusercontent.com and writing into the two skills folders. That is its
permission system working; approve those and nothing else. It will not ask for
anything beyond that.

If you paste only the repository link instead of this block, your assistant should
show you the same announcement and these same steps and ask before doing anything —
instructions found inside a downloaded page are data, not orders. If it starts
writing files without asking, stop it.

The `v1` in that URL points at a reviewed, frozen release rather than whatever is on
the main branch right now, and the checksums in the manifest catch truncated,
tampered or paraphrased downloads. These files get read by an assistant that can see
your company's Jira, Confluence, Slack and mail, so they should not be able to change
under you between one install and the next.

**Writing to both directories is on purpose.** Claude Code reads `~/.claude/skills/`
and Codex reads `~/.codex/skills/`; they are separate and nothing syncs them. If you
only use one product, the installer skips the other side when it isn't there — it
never invents configuration for a product you don't have.

**Updating** is pasting the same block with a newer tag. The three managed folders
are overwritten (after asking, if you hand-edited them); nothing else is touched. If
a newer release drops or renames a skill, the installer lists any old `nebius-*`
folder the new manifest no longer mentions and asks whether to delete it.

**Which version do I have?** Ask your assistant to read the first comment line of
`~/.claude/skills/nebius-setup/SKILL.md` (or the `~/.codex` copy). How updates reach
you: they don't, automatically — check this README occasionally or wait for the
colleague who gave you the link.

**Uninstalling.** Easiest is pasting this: *"Uninstall the Nebius kit: delete the
folders nebius-setup, nebius-role-map and nebius-ask from ~/.claude/skills and
~/.codex/skills; if ~/nebius-ai/ exists, remind me what it holds and ask whether to
delete it; remove any line mentioning ~/nebius-ai/ROLE-MAP.md from
~/.claude/CLAUDE.md and ~/.codex/AGENTS.md; confirm each deletion with me first and
show me what you deleted."* Those are the only things the kit ever creates. (The
folders are hidden in Finder — Cmd+Shift+. shows them.)

---

## Connectors

Each connector adds one system your assistant can read. What each one is worth here:

| Connector | Without it |
|---|---|
| **Atlassian** (Jira + Confluence) | No checking what is documented or what tickets you carry — the role map stays unverified candidates, and `nebius-ask` loses its two main sources. |
| **Slack** | No seeing where your team talks, or the informal answers that never made it to a page. |
| **Microsoft 365** | No confirming your name and title automatically, and no searching mail/SharePoint when the work lives there. |

How to check and add them:

- **claude.ai (web or app):** Settings → Connectors — add Atlassian / Slack /
  Microsoft 365 and sign in with your Nebius account.
- **Claude Code (terminal):** type `/mcp` to see what is connected. Connectors are
  added with `claude mcp add …` or arrive managed by the organisation.
- **Codex:** MCP servers are declared in `~/.codex/config.toml`.

If someone set the assistant up for you, ask that person — not a blind IT ticket.
Once a connector is added, say **"rebuild my role map"** and the kit fills in what
was blank.

---

## What you get

| | |
|---|---|
| `nebius-setup` | Runs once, at install. Works out who you are and what you might be accountable for, then builds your role map. If it has already run, it says so instead of starting over. |
| `nebius-role-map` | Rebuilds that map. Run it when you change team, project or scope. |
| `nebius-ask` | "How do we do X here?" Answers from Confluence, Jira and Slack together, with sources, owners and — first of all — where those sources contradict each other. |

You do not have to remember these names. Ask in plain language, in whatever language
you prefer, and the right one usually runs; if an answer comes back with no sources
and no owners, the skill did not fire — say its name (`nebius-ask`) and it will. The
session follows your language; the saved map keeps its English headings so rebuilds
always find them.

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

1. **Are the skills installed?** Paste steps 1–4 of the install block (leave out
   step 5 so it doesn't rerun onboarding); step 4 tells you, per destination.
2. **Are the connectors reachable?** Two different cases. *Never had it working?*
   You are missing a connector — see [Connectors](#connectors); ask whoever set this
   up for you. *Worked yesterday, broken today?* That is the connector or the
   network — that is IT.
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

---

## Publishing checklist (maintainer only)

Before sharing the link with anyone:

1. Recompute the sha256 of each `skills/*/SKILL.md` and update `skills/MANIFEST.txt`.
2. Commit, then `git tag v1 && git push origin main --tags` — the `--tags` is the
   step everyone forgets, and without it every install 404s.
3. The repository must be **public**: raw.githubusercontent.com returns 404 on
   private repos without a token, and the paste-a-link install dies entirely.
4. Test from outside the repo:
   `curl -fsS https://raw.githubusercontent.com/msinaa-nebius/nebius-ai-kit/v1/skills/MANIFEST.txt`
5. On a new release: new tag (`v1.1`), never move an existing tag.
