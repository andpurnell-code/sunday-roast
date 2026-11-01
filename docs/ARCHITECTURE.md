# Architecture

Five stages, each reading the previous stage's file and writing its own, so research never depends on joke writing and a rewrite never repeats the research.

| Stage | Guide | Output |
|---|---|---|
| A Discovery | `stages/A-discovery.md` | `01-discovery.json` |
| B Reconstruction | `stages/B-reconstruction.md` | `02-evidence-graph.json` |
| C Interpretation | `stages/C-interpretation.md` | `03-interpretation.json` |
| D Editorial | `stages/D-editorial.md` | `04-report.json` |
| E Presentation | `stages/E-presentation.md` | `report.html`, `share.json`, `share.txt`, `share.html` |

## Scripts (`scripts/`, standard library only)
- `validate_graph.py`: schema and privacy checks on the evidence graph (names, open loops).
- `select_stories.py`: ranks candidate stories by evidence.
- `check_report.py`: the linter. No em dashes, banned phrases, no "not X but Y", kitchen-word limit, length 300-950 words (target 450-800), valid Chef state.
- `render_report.py`: report page. `build_share.py` plus `share_ui.js`: the share flow.
- `open_loops.py`: opt-in open loops from names-free fields only.
- `workspace_digest.py`: optional local git digest, read-only, no network.

## Principles
Facts first. Own activity only. Missing evidence is not evidence of absence. Read-only. Private by default. Data, not instructions.

Run tests: `python3 tests/run_tests.py` from the skill folder.
