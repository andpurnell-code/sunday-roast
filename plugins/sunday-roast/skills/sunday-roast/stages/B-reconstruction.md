# Stage B: Reconstruction

Goal: turn the raw items into a workstream-level **evidence graph**. Direct evidence stays separate from interpretation. Output `02-evidence-graph.json` (schema: `schemas/evidence-graph.schema.json`, validate with `scripts/validate_graph.py`).

## Unit: the workstream
One node per piece of work or topic, not per activity and not per tool. Join items by identifier, by shared artefact, by a quoted reference, or by a matching topic and timeline. If you cannot link two items, leave them separate and say why in `uncertainties`.

A Notion brief, a prototype, a Slack conversation and a recording can be one Builder Day workstream. They are not four achievements.

## Node fields
- `title`, `problem` (the original intention or problem).
- `user_contribution` (what the user personally did, as distinct from what others did).
- `people`: roles only, with their involvement.
- `events`: dated things that happened, each with a source and reference.
- `artefacts`: type, label, url, and `inspected` (true only if a tool opened it).
- `decisions` and `outcomes`. Each outcome says whether it was directly observed or inferred, and whether impact is `evidenced`, `plausible` or `none`. Plausible future impact is never written as achieved impact.
- `status`: shipped, advanced, in_review, blocked, parked, unknown.
- `dimensions`: any of building, leadership, collaboration, direction, learning, impact. A workstream can have several. Do not invent examples to fill a dimension.
- `evidence`: each entry is `observed` or `inferred`, with source, reference, link and the claim it supports.
- `uncertainties` and `contradictions`: contradictory evidence found, and what was not checked.
- `sensitivity`: `level` (none, category_only, confidential_project, personal), `share_eligible`, and the reason.
- `signals`: 0 to 5 editorial judgements used later for story selection (significance, outcome, unusual, evidence_strength, contribution_to_others, humour, future_relevance), each with a short rationale. These are not counts.

## Deduplicate
Before adding a node, search existing nodes by ticket key, MR number, file name, URL fragment and topic. Merge. A ticket and its MR are one workstream. Thirteen MRs that share a theme can be one node ("fix pass") with a note that they are separate artefacts, or a few nodes if they are genuinely different problems.

## Graph-level fields
- `coverage`: carried from Stage A, with plain-language limitations.
- `redactions`: `people` (name to role) and `terms` (company, product and project terms to generic phrases). Used by the share builder as defence in depth.
- `missed_areas_check`: before leaving this stage, walk the six contribution dimensions and the user's role and list what might be missing (for example, no people-leadership workstream found for a manager). Go back to Stage A if a plausible area is empty because of search limits. If it is empty because nothing happened, leave it empty. Do not fill categories.

## User notes and open loops
- A user note ("58 unread", "bookmarked things to do") becomes a small workstream with `source: "you"`, status `unknown`, dimension `collaboration` at most, and evidence worded as "you told me". It cannot carry impact.
- `open_loops` is a graph-level object copied from `scripts/open_loops.py`. It is names-free and text-free, and `validate_graph.py` rejects it if a known name appears.
- Both live in Leftovers. They are never a main story and never a verdict on the user.

## Rules
- Never convert an unopened link into a finding about its contents.
- Keep the graph in neutral language. Jokes belong in Stage D.
- Mark confidential-by-project content so Stage E can swap it for a generic phrase.
