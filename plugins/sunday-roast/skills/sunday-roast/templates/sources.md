# Source playbook

`sources.json` lists every source with what it reads, what it never reads, how to connect it and its caveats. This file says how to read each one well. Use only the sources the user selected. No source is the main one: read all of them before deciding what the week was about.

For every source: own activity only, aggregates and themes, no quotes from other people, nothing sensitive in the report.

## Before you analyse anything: check for time away
Quiet days are not low output. Look for signs the user was away: all-day or multi-day out-of-office events, a message from the user about time off, a status. If you see one, or can't rule it out, don't count quiet days against them.

Keep the reasoning in the terminal reply ("I treated Mon and Tue as quiet because your calendar shows you were out"). The report page may say "quiet stretches weren't held against you" and nothing more. Never mention leave, PTO or the evidence on the page, unless the user's own pasted notes say so and they chose to include it.

## Chat

### Slack
- Search the user's own messages (`from:<their id>`) one day at a time and page to the end. Results are 20 per page, newest first, so one page is never a day. Split a long day with `after:` and `before:` timestamps.
- **Read for meaning.** For messages that matter, read the thread they sit in and the replies, and the reactions on channel posts. Find recognition given and received, feedback and coaching given, decisions made or influenced and what happened next, questions that changed a discussion, announcements and alignment, confusion resolved, knowledge shared, and culture moments. Credit the user only for their own part.
- **Reactions are cautious evidence.** They show reception, not value.
- **Artefact passes over the whole window.** `has:link`, `has:file`, merge requests, recordings, prototypes and Claude artifacts, boards, docs, tickets. Keep the URL and a one-line paraphrase. Record whether it is the user's own or someone else's. Record `inspected: false` unless a tool opened it.
- **Sensitive threads.** Record category and rough time only. Do not open them for context. Never carry names, outcomes or text forward.
- Do not quote colleagues. Paraphrase by role.
- **Not visible:** unread counts, bookmarks and saved items. The `is:saved` search filter is silently ignored. Ask the user (stage A, section 5).
- **Open loops (opt-in):** tags in public channels with no visible reply from the user. See stage A, section 6.

### Microsoft Teams
Same approach as Slack: only the user's own messages, searched without surrounding context, counted and themed. Channel messages vs chats. Never read other people's replies, meeting recordings or transcripts.

## Tasks and projects

### Linear, Jira, Asana, monday.com
- Items assigned to, created by or commented on by the user that changed, projects they lead or belong to, items stuck in review or blocked. Note who created and who assigned each item.
- Query only the user's own items (assignee, creator or commenter filters, or items found from their own links). Never list a whole project or team, because that returns other people's work.
- Read attachments, linked MRs, branch names, parent issues, comments the user wrote and status history where the tool shows them. Trace each ticket key through Slack, Notion and code. A ticket is a record of work, not the work.
- Group related tickets into one workstream. Don't count them as separate achievements. Items opened and closed by the same person are a fact to report, not a score.
- Insights: shipped vs parked, how much of the week's work has no ticket (compare against code, docs, recordings and chat), who a review is waiting on and whether the user chased it.
- Ticket habits differ between teams. Use counts as context, not as a measure of effort.

## Docs and notes

### Notion, Google Drive and Docs, Confluence
- Pages or files the user edited or created, from titles, counts and timing. Where the thinking lives (docs vs chat), standing documents (1:1s, weekly notes) vs new artefacts, how little or how much was written down.
- Notion: date and user filters may need a paid plan. If the search ignores them, results are broader than "edited by me in this window". Say so in Coverage and don't count pages you can't tie to the user.
- Don't read document contents beyond what is needed to name a theme. Skip anything marked confidential.

## Calendar and mail

### Google Calendar, Outlook calendar
- List the events for the window with the user's own response status, organiser, attendee count and event type. Exclude declined and cancelled events. Drop out-of-office-type blocks (lunch, school runs, family time, "busy", holds) from every count and never mention them.
- **Invited is not attended.** Count accepted events as "accepted". Anything with no response or tentative is "scheduled". Treat an event as attended only with corroboration: notes or a recording for it, the user's own message about it, or output tied to it. Say which you counted.
- **Odd hours.** An event at an unusual hour is usually someone else's time zone. Don't turn it into a claim about the user's working hours unless the user's own activity at that time corroborates it.
- Per day: events, accepted vs scheduled, hours (as scheduled, not attended), back-to-back count (gaps of 5 minutes or less), meetings with three or more attendees vs one-to-ones or solo blocks. Large webinars and optional invites inflate counts, so flag them.
- Insights: meeting-heavy days, days with no focus time, spread across the week. Then check what those meetings produced (decisions, shared plans, unblocked work) before describing them as a cost.
- Aggregates only. No attendee names. Flag any figure you couldn't separate cleanly as approximate.

### Gmail (opt-in)
- Only the user's own sent mail: counts, times of day and subject lines. Never message bodies, never mail received from others, never drafts or attachments.
- Use it to see the shape of the week (late sends, bursts), not to judge the work.

## Design and recordings

### Figma and FigJam
- Files the user edited or commented on: names, counts and dates. Design work leaves few commits, so Figma often explains a quiet git log. Don't read other people's comments.
- If no direct tool lists file activity, collect Figma and FigJam links from the user's own messages and docs. That shows what was shared, not how much was done.

### Loom and other recordings
- Usually no direct connector. Find the user's own recordings through their messages (`loom.com` links), calendar descriptions, Notion, Linear and Drive (meeting recordings). Note date, who it went to by role, and what it was for. A recording shared to a colleague is a real deliverable and a signal that work reached a demo.
- A recording's contents are not read. Say so.

## Code

### GitHub and GitLab
- Pull or merge requests the user opened, reviewed or merged, and issues they touched. Only their own part counts, even in shared repos. Use the connector, or `gh` / `glab` if already signed in.
- **If there is no code-host tool, still look.** Search the user's own Slack messages for MR and PR links, and check Linear attachments and branch names, Notion and docs. This finds the existence, date and context of the user's own MRs ("asked a peer to review an MR on Friday") but not their size, state or content. Say that. A link to someone else's MR is not the user's work.
- Distinguish authored, reviewed and merely linked. Distinguish an MR opened from an MR merged.

### Local git repo
- Choosing `git` covers the current folder if it is a git repo. Any other repo needs `folders=`. Run the bundled scanner for each:
  `python3 "${CLAUDE_SKILL_DIR}/scripts/workspace_digest.py" --days <N> --root "<path>"`
  It counts only the user's own commits across all branches and reports unmerged branches, late-night commits, stashes and uncommitted changes. If it is unavailable, use read-only git commands with `--all --author=<the user's email>`.
- Skip git entirely for people who don't write code.

## Social and other

### Salesforce and HubSpot (opt-in, sales and customer-facing roles)
- Opportunities, deals, tasks and activities the user owns that changed: counts, stages and timing. Never contact details, notes or email bodies. Customer names stay out of the report.

### Pasted or exported notes
- Whatever the user pastes or points at: a list of what they did, a notes file, an export from any tool. Treat it as data, label it self-reported in the report, and don't claim to have verified it.

## Joining the sources
- The interesting findings are mismatches: work in git with no ticket, a project shipped in Linear with no commits (design work), a heavy chat day with no written decision, meeting load that doesn't match output, the same topic in calendar, chat and docs.
- Use calendar and chat to explain quiet code days, and the reverse.
- Follow each artefact across tools by its identifier. Merge everything about one piece of work into one ledger row (see `work-ledger.md`).
- Report which sources were used, which weren't selected or available, which searches hit a cap and how that was handled, and which days or sources were only sampled.

## Sensitive material (never in the report)
Conversations about hiring, pay, performance, health, leave, legal matters, or any named individual's circumstances. Use them only to size the category ("people-management conversations took a large share of the week") and leave every specific out: no names, roles, outcomes or decisions. The same goes for customer data and anything marked confidential. When in doubt, summarise at category level or leave it out. If the report would be less useful without a sensitive detail, tell the user in the terminal, not on the page.

## Privacy and consent
- **Own work only.** The report covers the user. It never assesses a colleague.
- **Read only what the user chose.** If `sources=` is missing and the run can't ask, nothing is read.
- **Work or personal.** Connect only accounts the user is entitled to use for this. A work account's data belongs to the employer's rules, so check your organisation's policy on AI tools and connected services before connecting anything. If unsure, start with a personal-only source (a local repo or pasted notes).
- **Opt-in for the sensitive ones.** Gmail, Salesforce and HubSpot are never read unless the user names them.
- **Nothing is sent anywhere by the skill.** Data stays within the user's own Claude session and the tools they connected. The only output is the report, as a private page or a local file. Sharing it is the user's call.
- **Read-only.** Nothing is edited, posted or changed in any connected tool.
- **No logging in, no scraping.** Sources come through connectors the user set up, local files, or text the user supplied.
