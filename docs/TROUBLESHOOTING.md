# Troubleshooting

**Claude.ai rejects the zip.** The upload accepts only these frontmatter keys: name, description, license, compatibility, metadata, allowed-tools. This skill uses only those. Re-download the zip and check that `sunday-roast/SKILL.md` is at its top level. Code execution must be enabled.

**The skill does not trigger.** It runs only when you ask for your Sunday Roast or use `/sunday-roast`. In Claude Code as a plugin the command is `/sunday-roast:sunday-roast`.

**"No sources connected."** Add connectors in Claude, or pass notes: `notes="..."`. The skill never opens an unselected source.

**Slack looks thin.** Search returns 20 results per page and does not expose unread counts or saved items. Use `notes=` for those.

**Report has plain fonts.** Google Fonts is blocked on your network. Everything else works.

**The report was not published as a page.** The Artifact tool is not available here, so the skill saved `report.html`. Open it in a browser.

**LinkedIn button does nothing.** Pop-up blocked, or LinkedIn changed its prefill link. Use Copy text.

**Python not found.** Install Python 3.9+. Without it the skill still writes the report but cannot run its checks, and says so.

Still stuck? Open an issue using the bug template. Do not paste private data.
