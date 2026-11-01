# The Sunday Roast

*Your week, served with a side of sarcasm.* ([sundayroast.me](https://sundayroast.me))

A Claude skill that looks back over **your own** week in the tools you choose (Slack, Linear, GitHub or GitLab, Notion, Google Drive, Calendar and more) and writes a funny, affectionate, evidence-based review, narrated by Chef, a chicken. The report is private. Sharing is a separate step, and you review exactly what leaves.

**The facts are sacred. The commentary is not.** Every joke traces to something observed. Nothing is invented.

It is a self-reflection tool. It is never a manager's tool, a score or a ranking, and it will not review anyone but you.

## Install

| Where | How |
|---|---|
| **Claude.ai / Cowork** | Download [`dist/sunday-roast-skill.zip`](dist/sunday-roast-skill.zip), then Settings > Features > Skills > Upload. Code execution must be on (paid plans). |
| **Claude Code (plugin)** | `/plugin marketplace add andpurnell-code/sunday-roast` then `/plugin install sunday-roast@sunday-roast` |
| **Claude Code (copy)** | `cp -R plugins/sunday-roast/skills/sunday-roast ~/.claude/skills/` |

Full steps, screenshots-free, in [docs/INSTALL.md](docs/INSTALL.md).

## Use

Say **"Run my Sunday Roast"** (or `/sunday-roast` in Claude Code). Chef asks which connected sources to use, whether there is anything the tools can't see (an unread count, things you are putting off), and whether to switch on open loops. Then you get a private report page.

Options: `7` (days, up to 90), `sources=slack,linear`, `skip=calendar`, `notes="..."`, `loops=on`, `mode=share`, `mode=rerender`.

## What it reads, what it never does

- Reads only the sources **you** select, only **your own** activity, read-only. It never posts, edits or sends.
- No scoring, ranking, performance judgements, or inferences about health, motivation or private life.
- Colleagues appear by role, never by name, never quoted in anything shareable.
- Sensitive topics (hiring, pay, performance, health, legal) are sized by category at most and never shared.
- Nothing is uploaded by the skill. Network use is limited to Google Fonts in the report and the LinkedIn composer link you click yourself. Details in [PRIVACY.md](PRIVACY.md).

## Sharing

The Share button builds an allowlisted, names-free version and runs a leak check. You review it, tick a box, then copy the text or open LinkedIn's composer with it prefilled. Nothing is posted for you. See [docs/SHARING.md](docs/SHARING.md).

## Repository layout

```
.claude-plugin/marketplace.json      plugin marketplace manifest
plugins/sunday-roast/                Claude Code plugin
  skills/sunday-roast/               the one canonical skill (SKILL.md, stages, scripts, templates, tests)
dist/sunday-roast-skill.zip          upload this to Claude.ai
docs/                                install, sources, sharing, architecture, troubleshooting, audit, publishing
examples/sample-roast/               a fictional sample report
tools/                               zip builder and release verifier
```

## Develop

```
python3 plugins/sunday-roast/skills/sunday-roast/tests/run_tests.py
python3 tools/verify_release.py
python3 tools/package.py        # rebuild dist/sunday-roast-skill.zip
```

Python 3.9+ standard library only. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence

MIT for code and text (see [LICENSE](LICENSE)). The logo and name are the author's, see the note in LICENSE.
