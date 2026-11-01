# Stage C: Interpretation

Goal: decide what the week was about, how well each claim is supported, and where the contradictions are. Output `03-interpretation.json`.

## 1. Contribution dimensions
For each workstream, record how it contributes to the six dimensions. These are analytical lenses, not quotas.

| Dimension | Looks like |
|---|---|
| Building | Code changes, prototypes, design work, documentation, experiments, automations, tangible outputs |
| Leadership | Coaching, feedback, recognition, mentoring, creating clarity, resolving ambiguity, helping others work well |
| Collaboration | Cross-functional work, useful questions, unblocking, shared problem-solving, knowledge sharing, constructive challenge |
| Direction | Strategy, prioritisation, decisions, trade-offs, standards, influencing plans, improving how teams operate |
| Learning | Experiments, discoveries, validation, mistakes, changed assumptions, new capabilities |
| Impact | Demonstrable outcomes for users, colleagues, teams, customers or the business |

Impact has two grades. **Evidenced impact** has an observed outcome (a fix confirmed, a plan adopted, a call scheduled because of it). **Plausible impact** is a reasonable guess about the future and is never reported as achieved.

An uneven week stays uneven. Do not require equal representation.

## 2. Classify every claim
Tag each claim you may use as `fact` (directly in a source), `interpretation` (follows from several facts, nothing contradicts it), `hypothesis` (plausible, unchecked) or `unknown`. Only facts and strong interpretations carry a joke. A hypothesis may carry a question. An unknown carries nothing.

## 3. Try to disprove the negatives
Before keeping any unflattering conclusion, look for what contradicts it.

| Tempting conclusion | Check first |
|---|---|
| Built nothing on a build day | MRs, prototypes, recordings, briefs, shared artefacts dated that day |
| A day of meetings, nothing done | What the meetings produced, who organised them, output the same day |
| Work stuck in review | Who the reviewers are, whether review was requested, whether the user chased |
| Late messages | Whether it was a handful of messages, and who the other person was |
| Quiet week | Time away, work outside the tools, long calls |
| Quiet weekend | That is correct, not a gap |

Calendar invitations are not attendance. Timestamps are not hours worked. Never derive hours worked. Drop timing-only observations that do not change the story.

## 4. Find contradictions worth a joke
Look for true tensions: what was said next to what was done, an intention next to an outcome, two things that cannot both be the plan. A contradiction must be observed in sources, be about a decision or a habit, and be something the user would laugh at. If there is none, do not manufacture one.

## 5. Candidate stories for the week
Write at least two competing interpretations of the week's overall story, each with: thesis, supporting workstreams, counter-evidence and the dimensions it draws on. Pick the one the evidence supports best. Say why the others lost. A story that is only the most measurable thing (the MR count) is a weak candidate unless the evidence really says so.

## 6. Check for code bias and tool bias
If the selected stories draw only on the tool with the richest audit trail, ask whether leadership, direction or collaboration work was larger but less measurable. Do not force every connected tool into the report.

## Output
`{contributions:[{workstream_id, dimensions[], evidenced_impact[], plausible_impact[]}], claims:[{text, class, workstream_id, counter_check}], contradictions:[...], week_interpretations:[{id, thesis, supports[], counter[], strength}], selected_interpretation, notes_on_bias}`
