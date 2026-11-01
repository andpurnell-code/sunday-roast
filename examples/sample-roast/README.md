# Sample roast

A report rendered from the fictional fixtures in `plugins/sunday-roast/skills/sunday-roast/tests/fixtures/`. The persona, projects and colleagues are invented. Open `report.html` in a browser. `share.*` shows the share-safe export.

Regenerate:

```
S=plugins/sunday-roast/skills/sunday-roast
python3 $S/scripts/render_report.py --graph $S/tests/fixtures/graph.json --report $S/tests/fixtures/report.json --out examples/sample-roast/report.html
```
