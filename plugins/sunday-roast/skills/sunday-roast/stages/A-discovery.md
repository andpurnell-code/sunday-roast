# Stage A: Discovery

Goal: find the raw material for the week, and record exactly how much of it you could see. No interpretation, no jokes. Output `01-discovery.json`.

## 1. Discover capabilities
List the tools available in the session. For each source in `templates/sources.json` mark: `direct`, `indirect` (no tool, but its outputs can be found in other sources), `awaiting_input` (LinkedIn, pasted notes), `unavailable` or `not_selected`. Never assume an integration. Never infer inactivity from a missing one.

| Source | Direct route | Indirect route |
|---|---|---|
| Slack | search, thread and reaction tools | none |
| Linear | issues, projects, attachments, comments | none |
| GitLab, GitHub | connector or CLI | Linear attachments and branch names; MR links in Slack, Notion and docs |
| Notion | search and fetch | links in Slack and Linear |
| Google Calendar | events with response status | none |
| Google Drive | search and read | links in Slack and calendar attachments |
| Figma | file tools | `figma.com` links in Slack, Linear, Notion |
| Loom | rarely available | `loom.com` links in Slack, calendar, docs |

An indirect source gives existence, date and context. It does not give contents. Mark linked items `inspected: false` unless a tool actually opened them.

## 2. Retrieve exhaustively
- Page every search to the end. Split by day, then by time window, identifier or activity type when a cap is hit. One page is never coverage. Search results are newest first, so one page shows only the end of a day.
- Query only the user's own items in trackers and code hosts. Never list a whole team or project.
- Keep the link, the identifier and a one-line paraphrase. Do not keep message bodies beyond what is needed to understand the contribution.

## 3. Slack: look for meaning, not volume
Search the user's own messages day by day. Then, for messages that matter, read the thread they sit in (replies included) and the reactions on channel posts. Find:

- Recognition and appreciation the user gave.
- Feedback, coaching and constructive challenge the user gave.
- Decisions the user made or influenced, and the outcome visible in the thread.
- Questions that changed the direction of a discussion.
- Announcements and alignment.
- Confusion or disagreement the user helped resolve.
- Recognition the user received. Separate specific thanks (names the work) from routine politeness.
- Shared artefacts: prototypes, docs, MRs, recordings, research, boards.
- Culture and humour moments that show how the user works with people.

Interpret reactions cautiously. A reaction shows reception, not value. Eight hearts on a plan means eight people reacted. Credit the user only for what the user did, not for everything in the channel. Sensitive DMs are recorded by category and rough time only.

## 4. Other sources
- **Linear:** own issues with attachments (linked MRs), status history, parent issues, comments the user wrote.
- **Code hosts:** authored, reviewed and merged changes and linked issues. Without a tool, resolve MRs through attachments and links and record state as unknown.
- **Notion and Drive:** items the user created or meaningfully edited. Read the user's own documents and the notes of meetings they hosted to understand what the work was. Mark confidential-by-project content as such. Distinguish authored from auto-generated files.
- **Calendar:** events with the user's own response status and organiser. Invited is not attended. Do not carry timing-only observations (for example an event at an odd hour that is probably another time zone) into the findings.
- **Figma and Loom:** direct tool if present, otherwise the links the user shared. Contents not seen.

## 5. What the tools cannot see: ask the user
Tools do not expose Slack unread counts, bookmarks or saved items, reminders, or things the user decided to avoid. Ask once, in the source picker, as an optional free-text line: "Anything Chef can't see? Unread count, saved items, things you're putting off." Store the answer as a workstream with `source: "you"`, evidence phrased as "you told me", and treat it as self-reported and unverified. It is the cheapest and most accurate way to roast the pile. Never guess a number the user did not give.

## 6. Open loops (opt-in, off by default)
Only when the user turns it on (`loops=on` or the picker option).
1. Search for mentions of the user in public channels across the window (`<@their id>`), paging to the end (20 a page, newest first).
2. For each, read the thread and note only booleans: was there a direct question, did the user reply, did the user react.
3. Leave out DMs, group chats, private channels and sensitive threads. They are counted as "left out", never read for content.
4. Run `scripts/open_loops.py` on the booleans and timestamps. It accepts no names and no text, and returns counts and age bands.
5. Store the result as `open_loops` in the graph. Say in the report that these are tags where no reply is *visible*.
Never name who asked. Never list the items. A reply in a call, a DM or a reaction is invisible to the tools, so this is always a guess, and the joke is about the size of the pile, not the person.

## 7. Coverage record
For every source: mode, what was read, what was capped and how you got past the cap, what stayed unseen. Keep internal limitations in `coverage`. Only the ones that change the validity of the report reach the page headline.

## Output shape
`{window, sources:[{id, mode, read, limits[]}], items:[{id, source, when, kind, ref, url?, paraphrase, user_contribution, sensitivity, inspected}], threads:[...], reactions:[...], recognition:{given:[], received:[]}}`
