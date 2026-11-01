# Privacy

The Sunday Roast has no server, no analytics, no accounts and no telemetry. This repository contains instructions and local scripts only.

## What gets read
Only the sources you select when you run it, only your own activity, through connectors you have already given Claude. The reads are performed by Claude under those connectors' permissions. The skill never edits, posts or sends anything. See [docs/SOURCES.md](docs/SOURCES.md) for what each source reads and never reads.

## Where data goes
- Intermediate files (JSON per stage) are written to `~/.claude/sunday-roast/runs/<date>/` or the working folder. They can contain names and work detail. Delete them whenever you like.
- The report is a private page or a local `report.html`. It is not uploaded by the skill.
- Your data is processed by Claude under the terms of your Claude plan and connectors, like any other Claude conversation.

## Network use by the bundled code
- The report page loads two fonts (Caprasimo, Figtree) from Google Fonts. If blocked, it falls back to system fonts.
- "Share on LinkedIn" opens `linkedin.com` in a new tab when you click it, with text you reviewed. Nothing is sent otherwise.
- The Python scripts make no network requests. `workspace_digest.py` only reads local git history.

## Sharing
Sharing is a separate, confirmed export. It contains no colleague names, no quotes, no customer or confidential detail, and nothing from the sensitive categories. You see the exact text before anything leaves. Nothing is posted on your behalf.

## What it does not do
No scoring, ranking, performance assessment, or inference about health, motivation or personal circumstances. Missing data is never counted against you.
