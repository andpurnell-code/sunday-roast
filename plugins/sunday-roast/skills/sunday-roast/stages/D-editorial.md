# Stage D: Editorial

Goal: choose the stories, write the report in Chef's voice, choose Chef's illustration. Reads `02-evidence-graph.json` and `03-interpretation.json`. Writes `04-report.json` (schema: `schemas/report.schema.json`). Never calls a source.

## 1. Select stories
Rank by: significance to the user's role, meaningful progress or outcome, unusual or interesting circumstances, strength of evidence, contribution to others, humour potential and relevance to future decisions. `scripts/select_stories.py` gives a transparent first ranking from the graph's editorial signals. It never uses message, MR, meeting or source counts. You make the final call.

- One Main. The week's most substantial achievement, contribution, decision or workstream.
- One or two Sides, ideally different kinds of contribution (not two code stories).
- A Burnt bit only if something really did go sideways or revealed a contradiction. Skip it otherwise.
- Leftovers only for genuinely unfinished work or open questions.
- Compliments are specific and include helping others. No generic praise.
- A Bill only if there is something useful to say about effort or trade-offs. Never an invented estimate.
- Specials: one to three concrete suggestions that follow from the evidence. No generic advice.
- Do not repeat the same achievement in several sections. Do not force each tool to appear.

## 2. Report shape
Default reading length roughly 450 to 800 words of narrative. Funnier writing runs a little longer; never cut a true, important thing to hit a number. Sections, with the cuts allowed:

1. **Chef's verdict.** Two or three sentences on what defined the week, including a win and an interesting observation.
2. **Starter.** An engaging opening story or observation. Not automatically the first event.
3. **Main.**
4. **Sides.** One or two.
5. **Burnt bits.** Optional.
6. **Leftovers.** Optional. The natural home for the user's own pile (unread, bookmarks, tags with no visible reply). Say whose number it is ("you told me") or that it is a visible-reply guess. The joke is the pile, never the person.
7. **Compliments to the chef.** Specific recognition.
8. **The bill.** Optional.
9. **Chef's notes.**

No visible source footnotes, confidence statements or audit-style citations in the narrative. Each story carries a hidden `disclosure` instead: sources and links, what was directly observed, what was inferred, any meaningful uncertainty, dates or measurements. It is shown on demand as "How Chef knows".

There is no "Not on the menu" section. Coverage goes to the Sources and coverage panel. Only when a gap materially affects the validity of the report, add one plain sentence near the verdict.

## 3. Voice
Follow `templates/chef.md`. Short version: natural contemporary British English, dry, observant, properly funny, slightly absurd, occasionally sharp, generous in spirit. Chef is a chicken and may say so, and a few Sunday-lunch puns are welcome. The user must feel recognised, not attacked, and should laugh at themselves. Let some observations be sincere.

## 4. Share text
Every story also carries a `share.text`: a self-contained, share-safe rewrite with no names, no company or project terms, no quotes, no confidential detail and no evidence. It keeps Chef's humour. Stories that are sensitive or cannot be made safe set `share.include` to false.

## 5. Choose the Chef illustration
Pick one state from `schemas/chef-states.json` using its `when` rules, based on the week's selected story, not on surface signals. If nothing fits, use `chef-default`.

## 6. Editorial check
Run `python3 scripts/check_report.py` and then answer these:
1. Are the major deliverables and conversations in the graph?
2. Has linked evidence been followed across tools?
3. Is any activity being mistaken for impact?
4. Was each criticism checked against contradicting evidence?
5. Are calendar invitations and timestamps treated fairly?
6. Is every claim grounded in an accessible source, and is plausible impact kept out of achieved impact?
7. Is every joke funny, or only elaborate? Does any depend on a stretched fact?
8. Does the report fairly reflect what was achieved, including leadership and helping others?
9. Would the user recognise their week? Is there a detail that could not belong to anyone else?
10. Does the user finish amused and informed, not judged?

If the evidence is thin, go back to Stage A or B. If it stays thin, narrow the claim.
