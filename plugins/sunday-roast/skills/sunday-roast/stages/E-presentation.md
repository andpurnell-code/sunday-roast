# Stage E: Presentation

Goal: render the report and the share experience. Reads `04-report.json` and the evidence graph. Writes `report.html`, `share.json`, `share.html`.

```
python3 scripts/render_report.py --graph 02-evidence-graph.json --report 04-report.json --out report.html
python3 scripts/build_share.py  --graph 02-evidence-graph.json --report 04-report.json --options share-options.json --out share
```

## The private report
- Chef illustration at the top, one of the approved assets, shown on a light plate so it keeps its colours in both themes.
- Tagline: "Your week, served with a side of sarcasm." Positioning line: "Celebrate the wins. Laugh at what went sideways. Start next week a little wiser."
- The narrative only. Sections as in Stage D.
- Each story has a "How Chef knows" disclosure (native `details` element). It lists source names, links, what was directly observed, what was inferred, uncertainties, dates and measurements. Links are clearly labelled, and a link that was not opened is marked "not opened".
- A **Sources and coverage** panel opened from the header. It lists each source with its mode (direct, via links, awaiting input, not available, not selected), what was read, and the limitations. Nothing is inferred from a missing source.
- A **Share** button.
- Light and dark themes, phone width, no external data, no download links (the viewer blocks them).

The private page contains the full private data. It is private to its owner until the owner shares it. Do not publish it for others.

## The share flow (in the page)
1. **Preview** the share-safe report. It is built only from allowlisted fields: Chef illustration state, tagline, week label, the verdict's `share` text and each included story's `share.text`.
2. **Remove or edit** any passage. Each passage has an include switch and an editable text box.
3. **Remove names and company details**, on by default. The names and terms to replace come from the graph's `redactions`. The share text is already written without them. This is a second layer, not the first.
4. **Hide evidence links, raw source material and private metadata.** Evidence is never part of the share payload.
5. **Export an image.** The page draws the share card on a canvas. If the viewer blocks downloads, the image opens in an overlay to save by long press or right click.
6. **Copy the share-safe text.** The clipboard may be refused in some viewers, so the text is also selectable.
7. **Create a shareable page.** The page cannot publish by itself. The button explains the safe route: ask Claude to publish the share page, which runs `build_share.py`, shows the exact payload and waits for explicit confirmation. A public link is never created without it.

PDF export is not offered inside the Claude viewer, because printing is blocked there. The standalone `report.html` supports the browser's own print dialog.

## The shared page
`build_share.py` writes `share.json` (the allowlisted payload) and `share.html` built only from that payload. It is a separate document. The private page is never published as the share. Rules it enforces:
- allowlist: `chef.state`, `tagline`, `week_label`, `verdict`, `sections[].title`, `sections[].text`
- sections with `share.include: false`, or from non-share-eligible workstreams, are dropped
- replacement of names and terms from `redactions`
- hard fail if any redaction term, URL, email or `@mention` remains
- no evidence, links, coverage, ids or metadata

Hosting: a hosted share page is a normal private-by-default page that the user then chooses to share. **Revocation** is deleting that page. **Expiry** is not supported and must not be promised.

## Testing
`python3 tests/run_tests.py` checks the assets, the schemas, the story selector, the report linter, the share builder (including a leak test), the renderer output (including a syntax check of its script).
