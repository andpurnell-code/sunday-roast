# Install

Pick one. All three install the same skill.

## 1. Claude.ai or Cowork (zip upload)
1. Download `dist/sunday-roast-skill.zip` from this repo (or the latest Release).
2. Open Claude, then **Settings > Features > Skills** (wording may vary) and upload the zip.
3. Make sure **code execution** is on. Custom skills need a paid plan, and are per user.
4. Connect the tools you want reviewed under **Connectors** (Slack, Linear, Notion, Google Drive, Calendar and so on).
5. Start a chat and say: **Run my Sunday Roast.**

The zip contains one folder, `sunday-roast/`, with `SKILL.md` at its top.

## 2. Claude Code, as a plugin
```
/plugin marketplace add andpurnell-code/sunday-roast
/plugin install sunday-roast@sunday-roast
```
Run it with `/sunday-roast:sunday-roast` (or just say "run my Sunday Roast"). To update later: `/plugin marketplace update sunday-roast`.

## 3. Claude Code, as a plain skill
```
git clone https://github.com/andpurnell-code/sunday-roast.git
cp -R sunday-roast/plugins/sunday-roast/skills/sunday-roast ~/.claude/skills/
```
Per project, copy it to `.claude/skills/` instead. Run `/sunday-roast`.

## Requirements
- Python 3.9+ available to the skill (for the bundled scripts).
- At least one connected source, or pasted notes. With nothing connected the skill says so and offers to work from what you paste.
- Optional: the Artifact tool, to publish the report as a private page. Without it the report is saved as `report.html` to open in a browser.

## Uninstall
Remove the skill in Settings, run `/plugin uninstall sunday-roast`, or delete `~/.claude/skills/sunday-roast`. Delete `~/.claude/sunday-roast/` to remove past run files.
