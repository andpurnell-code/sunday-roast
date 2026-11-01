# Sources

The skill reads only the sources you select, only your own activity, read-only. This page is generated from `templates/sources.json`.

LinkedIn is not a source. "Roast My LinkedIn" is a separate, future product.


## Chat

### Slack (`slack`)
- **Reads:** Your own messages, day by day, plus the threads they sit in, reactions on your posts and the links you shared. Used to understand what you decided, taught, thanked people for and shipped, not to count messages.
- **Never reads:** Unrelated conversations, sensitive one-to-one threads beyond their category, huddle audio, file contents, or anything not connected to your own messages.
- **Connect:** Add the Slack connector to Claude (claude.ai connectors or an MCP server) and approve the search permissions.
- **Caveat:** Search returns 20 messages per page, newest first. The skill pages each day to the end. Colleagues' words are paraphrased by role and never shown in shareable output.

### Microsoft Teams (`teams`)
- **Reads:** Only messages you wrote, searched for without surrounding context: counts, timing and themes.
- **Never reads:** Surrounding messages, other people's replies or threads, meeting recordings or transcripts of calls.
- **Connect:** Needs a Teams or Microsoft 365 connector in Claude. Your admin may need to approve it.
- **Caveat:** Availability depends on your organisation's setup. If no connector is present, paste a summary instead.


## Tasks & projects

### Linear (`linear`)
- **Reads:** Issues assigned to you or created by you that changed, projects you lead or belong to, items stuck in review.
- **Never reads:** Other people's issues, private teams you aren't part of, or comments by others beyond counts.
- **Connect:** Add the Linear connector to Claude and sign in with your own account.
- **Caveat:** Only shows work that has a ticket. Work without one is invisible here, and the report says so.

### Jira (`jira`)
- **Reads:** Tickets assigned to you, reported by you or transitioned by you, and what stayed stuck.
- **Never reads:** Other people's tickets, boards you don't use, or private comments from others.
- **Connect:** Add an Atlassian connector to Claude (claude.ai connectors or an MCP server) and sign in.
- **Caveat:** Ticket habits vary a lot between teams. Counts are context, not a measure of effort.

### Asana (`asana`)
- **Reads:** Tasks assigned to you or completed by you, projects you own, overdue and parked items.
- **Never reads:** Other people's tasks and private projects you don't belong to.
- **Connect:** Add an Asana connector to Claude and sign in with your own account.
- **Caveat:** Depends on a connector being available to you. Otherwise use pasted notes.

### monday.com (`monday`)
- **Reads:** Items assigned to you or updated by you, boards you own, status changes.
- **Never reads:** Boards you aren't on and other people's items beyond status counts.
- **Connect:** Add the monday.com connector to Claude and approve access to your own boards.
- **Caveat:** Board structures differ, so the skill reads titles and status only.


## Docs & notes

### Notion (`notion`)
- **Reads:** Pages you edited or created in the window: titles, counts and timing.
- **Never reads:** Page contents beyond what is needed to title a theme, and pages you didn't touch.
- **Connect:** Add the Notion connector to Claude and share the workspace with it.
- **Caveat:** Date and user filters may need a paid Notion plan. If the search ignores them, results are broader, and the report says so under Coverage.

### Google Drive and Docs (`gdrive`)
- **Reads:** Files you created or edited in the window: titles, types and dates.
- **Never reads:** File contents of other people's documents, and anything marked confidential.
- **Connect:** Add the Google Drive connector to Claude and approve read access.
- **Caveat:** Drive shows modified dates, not how long you spent. Treat counts as a rough trail.

### Confluence (`confluence`)
- **Reads:** Pages you created or edited and comments you made: titles, counts and timing.
- **Never reads:** Pages you didn't touch and restricted spaces.
- **Connect:** Add an Atlassian connector to Claude (the same one as Jira, where available) and sign in.
- **Caveat:** Needs a connector. Otherwise paste page titles or point the skill at an export.


## Calendar & mail

### Google Calendar (`gcal`)
- **Reads:** Your calendar events with your own response status: counts, scheduled hours, back-to-back stretches. Aggregates only.
- **Never reads:** Attendee lists, meeting notes, and personal or out-of-office blocks (excluded from every count and never mentioned).
- **Connect:** Add the Google Calendar connector to Claude and approve read access.
- **Caveat:** A calendar event is an invitation, not proof you attended. The report says accepted or scheduled unless notes, a recording or your own messages show you were there. Holds and focus blocks look like meetings, so hours are approximate.

### Outlook calendar (`outlook`)
- **Reads:** Your real meetings: counts, hours, back-to-back stretches and timing. Aggregates only.
- **Never reads:** Attendee lists, meeting bodies, and personal or private blocks.
- **Connect:** Needs a Microsoft 365 connector in Claude. Your admin may need to approve it.
- **Caveat:** Availability depends on your organisation. Otherwise export a week and point the skill at it.

### Gmail (`gmail`)
- **Reads:** Your own sent mail: counts, times of day and subject lines.
- **Never reads:** Message bodies, anything you received from others, drafts, attachments or labelled-private mail.
- **Connect:** Add the Gmail connector to Claude and approve read access.
- **Caveat:** Opt in only. Sent-mail volume says little about the quality of the work, and the report treats it that way.


## Design

### Figma (`figma`)
- **Reads:** Files you edited or commented on in the window: names, counts and dates.
- **Never reads:** Other people's comments and files you haven't touched.
- **Connect:** Add the Figma connector to Claude and sign in with your own account.
- **Caveat:** Design work leaves few traces in other tools, so Figma often explains a quiet git log. File activity is shown, not time spent.

### Loom and recordings (`loom`)
- **Reads:** Recordings you created or shared, found through your own messages, calendar and docs: date, who it went to by role, what it was for.
- **Never reads:** The recording itself or its transcript, and recordings you didn't make or share.
- **Connect:** There is usually no connector. The skill finds your recordings through the other sources you picked, such as Slack links.
- **Caveat:** Shows that a recording exists and went somewhere, not what is in it.


## Code

### GitHub (`github`)
- **Reads:** Pull requests you opened, reviewed or merged, and issues you touched.
- **Never reads:** Other people's code, private repos you haven't named, and review comments from others beyond counts.
- **Connect:** Add the GitHub connector to Claude, or use the gh CLI if it is already signed in.
- **Caveat:** Only your own activity is counted, even in shared repos.

### GitLab (`gitlab`)
- **Reads:** Merge requests you opened, reviewed or merged, and issues you touched. With no connector, the skill finds your MR links in your own Slack messages and Linear attachments.
- **Never reads:** Other people's code and projects you haven't named.
- **Connect:** Add the GitLab connector to Claude, or use the glab CLI if it is already signed in.
- **Caveat:** Only your own activity is counted, even in shared projects. Without a connector the skill sees that an MR existed and when you shared it, not its size, state or content.

### Local git repo (`git`)
- **Reads:** Your own commits across all branches, unmerged branches, stashes and uncommitted changes. Metadata only.
- **Never reads:** File contents, other people's commits, or repos you haven't named (the current folder is the default).
- **Connect:** Nothing to connect. Run it in a repo, or pass folders: /sunday-roast folders=~/code/app,~/code/api
- **Caveat:** Commit counts say little about effectiveness. Skip this one if you don't write code.


## Social & other

### Salesforce (`salesforce`)
- **Reads:** Opportunities, tasks and activities you own that changed: counts, stages and timing.
- **Never reads:** Customer contact details, notes, and other reps' records.
- **Connect:** Add the Salesforce connector to Claude and sign in. Use the sandbox connector to try it first.
- **Caveat:** For sales and customer-facing roles. Customer data stays out of the report entirely.

### HubSpot (`hubspot`)
- **Reads:** Deals, tasks and activities you own that changed: counts, stages and timing.
- **Never reads:** Contact details, email bodies and other owners' records.
- **Connect:** Add the HubSpot connector to Claude and sign in.
- **Caveat:** For sales and marketing roles. Customer data stays out of the report entirely.

### Pasted or exported notes (`pasted`)
- **Reads:** Whatever you paste or point at: a list of what you did, a notes file, an export from any tool, or anything the tools cannot see such as your Slack unread count and saved items. Treated as data, labelled self-reported.
- **Never reads:** Anything you didn't hand over.
- **Connect:** Paste text into the chat, or pass a folder or file: /sunday-roast folders=~/notes/week.md
- **Caveat:** Only as complete as what you give it, and unverifiable, so the report marks it as self-reported.
