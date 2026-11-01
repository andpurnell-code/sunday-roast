#!/usr/bin/env python3
"""Transparent first-pass story ranking from the graph's editorial signals.

It never uses message, MR, meeting or source counts. The weights below apply
only to the 0-5 judgements recorded in each workstream's `signals`. The output
is a suggestion for Stage D, not the final choice.

Usage: python3 select_stories.py 02-evidence-graph.json
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import schema_lite  # noqa: E402

WEIGHTS = {
    "significance": 3.0,
    "outcome": 2.5,
    "evidence_strength": 2.0,
    "contribution_to_others": 1.5,
    "unusual": 1.5,
    "humour": 1.0,
    "future_relevance": 1.0,
}


def score(ws):
    sig = ws.get("signals", {})
    total = sum(WEIGHTS[k] * float(sig.get(k, 0)) for k in WEIGHTS)
    # weak evidence cannot carry a story however good the joke
    if float(sig.get("evidence_strength", 0)) < 2:
        total *= 0.5
    return round(total / (5 * sum(WEIGHTS.values())) * 100, 1)


def rank(graph):
    rows = []
    for w in graph["workstreams"]:
        rows.append({
            "id": w["id"],
            "title": w["title"],
            "score": score(w),
            "dimensions": w.get("dimensions", []),
            "status": w.get("status"),
            "share_eligible": w.get("sensitivity", {}).get("share_eligible", False),
            "sensitivity": w.get("sensitivity", {}).get("level"),
        })
    rows.sort(key=lambda r: r["score"], reverse=True)
    return rows


def suggest(rows):
    notes = []
    top = rows[:3]
    if top and all(set(r["dimensions"]) <= {"building"} for r in top):
        notes.append("top three are building-only: check whether leadership, direction or collaboration work was larger but less measurable")
    main = rows[0] if rows else None
    if main and main["sensitivity"] in ("category_only", "personal"):
        notes.append("the top story is sensitive: use the next one as Main and keep this category-only")
    sides = [r for r in rows[1:] if r["sensitivity"] not in ("category_only", "personal")][:2]
    dims_seen = set()
    for r in sides:
        dims_seen |= set(r["dimensions"])
    return {
        "suggested_main": main["id"] if main and main["sensitivity"] not in ("category_only", "personal") else next((r["id"] for r in rows if r["sensitivity"] not in ("category_only", "personal")), None),
        "suggested_sides": [r["id"] for r in sides],
        "notes": notes,
    }


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    graph = schema_lite.load(argv[1])
    rows = rank(graph)
    print(json.dumps({"ranking": rows, "suggestion": suggest(rows)}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
