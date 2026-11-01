#!/usr/bin/env python3
"""Validate an evidence graph (Stage B output).

Usage: python3 validate_graph.py 02-evidence-graph.json
Exit code 0 when there are no errors. Warnings do not fail the run.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import schema_lite  # noqa: E402

SCHEMA = pathlib.Path(__file__).resolve().parent.parent / "schemas" / "evidence-graph.schema.json"


def check(graph):
    errors = schema_lite.validate(graph, schema_lite.load(SCHEMA))
    warnings = []
    ws = graph.get("workstreams", [])
    ids = [w.get("id") for w in ws]
    if len(ids) != len(set(ids)):
        errors.append("workstream ids are not unique")
    for w in ws:
        wid = w.get("id", "?")
        sens = w.get("sensitivity", {})
        if sens.get("level") in ("category_only", "personal") and sens.get("share_eligible"):
            errors.append(f"{wid}: {sens.get('level')} workstreams cannot be share_eligible")
        for a in w.get("artefacts", []):
            if a.get("inspected") and not a.get("source"):
                errors.append(f"{wid}: artefact '{a.get('label')}' is marked inspected but names no source")
        for o in w.get("outcomes", []):
            if o.get("impact") == "evidenced" and o.get("evidence") != "observed":
                errors.append(f"{wid}: evidenced impact must rest on observed evidence ('{o.get('text')[:40]}')")
        kinds = {e.get("kind") for e in w.get("evidence", [])}
        if w.get("evidence") and "observed" not in kinds:
            warnings.append(f"{wid}: no directly observed evidence, only inferences")
        if not w.get("evidence"):
            errors.append(f"{wid}: no evidence entries")
        sig = w.get("signals", {})
        for k, v in sig.items():
            if k != "rationale" and isinstance(v, (int, float)) and not 0 <= v <= 5:
                errors.append(f"{wid}: signal {k} out of range 0-5")
    dims = [set(w.get("dimensions", [])) for w in ws]
    if ws and all(d <= {"building"} for d in dims):
        warnings.append("every workstream is building-only: check for missed leadership, collaboration or direction work")
    if ws and not any("leadership" in d or "direction" in d or "collaboration" in d for d in dims):
        warnings.append("no leadership, direction or collaboration workstream found: confirm this is real, not a search gap (see missed_areas_check)")
    ol = graph.get("open_loops")
    if ol and ol.get("enabled"):
        names = [p.get("name", "") for p in graph.get("redactions", {}).get("people", [])]
        blob = json.dumps(ol)
        for n in names:
            if n and n.lower() in blob.lower():
                errors.append(f"open_loops mentions a person by name ({n}): it must be names-free")
        if ol.get("no_visible_reply", 0) > ol.get("considered", ol.get("no_visible_reply", 0)):
            errors.append("open_loops: no_visible_reply is larger than considered")
        if not ol.get("caveats"):
            errors.append("open_loops: caveats are required")
    for w in ws:
        if any(e.get("source") == "you" for e in w.get("evidence", [])):
            if w.get("sensitivity", {}).get("share_eligible") and any(e.get("kind") != "observed" for e in w["evidence"] if e.get("source") == "you"):
                warnings.append(f"{w.get('id')}: self-reported notes are marked observed: check they say 'you told me'")
    if not graph.get("missed_areas_check"):
        warnings.append("missed_areas_check is empty")
    for c in graph.get("coverage", []):
        if c.get("mode") == "unavailable" and not c.get("limits"):
            warnings.append(f"coverage: {c.get('source')} unavailable but no limitation recorded")
    return errors, warnings


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    graph = schema_lite.load(argv[1])
    errors, warnings = check(graph)
    for w in warnings:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
