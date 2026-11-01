#!/usr/bin/env python3
"""Editorial lint for a Sunday Roast report (Stage D output).

Usage: python3 check_report.py 04-report.json [--graph 02-evidence-graph.json]

Mechanical checks only. It cannot tell whether a joke is funny. Exit code 1 on
any ERROR, 0 otherwise (warnings do not fail).
"""
import argparse
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import schema_lite  # noqa: E402

SCHEMA = HERE.parent / "schemas" / "report.schema.json"
MANIFEST = HERE.parent / "schemas" / "chef-states.json"

BANNED = ["genuinely", "honestly", "straightforward", "remarkable", "testament", "worth noting", "journey",
          "unlock", "you've got this", "keep going", "delve", "tapestry", "navigate", "it's clear that",
          "game-changer", "leverage", "synergy"]
KITCHEN = ["oven", "cook", "cooked", "cooking", "kitchen", "recipe", "simmer", "boil", "bake", "baked",
           "stew", "sauce", "ingredient", "pan", "hob", "roast", "burnt", "serving", "served", "plate"]
THIRD_PERSON = re.compile(r"\b(chef (thinks|noticed|says|reckons|believes|saw|has noticed)|according to chef)\b", re.I)
NOT_BUT = [re.compile(r"\bnot\s+[^.!?]{1,40}?,?\s+but\b", re.I), re.compile(r"\b(isn't|wasn't|aren't)\s+[^.!?]{1,40},\s+(it's|it was|they're)\b", re.I)]
FOOTNOTE = [re.compile(r"\b(confidence|sources?)\s*:", re.I), re.compile(r"https?://"),
            re.compile(r"\b(Slack|Linear|Notion|GitLab|GitHub|Figma|Loom|Drive|Calendar)\s*:", re.I)]
TRIPLE = re.compile(r"\bthen\b", re.I)


def words(text):
    return re.findall(r"[A-Za-z0-9'’]+", text)


def narrative_text(report):
    parts = [report["verdict"]["text"]]
    for s in report["sections"]:
        parts.extend(s.get("paragraphs", []))
        parts.extend(s.get("items", []))
    return parts


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def check(report, graph=None):
    errors, warnings = [], []
    errors += schema_lite.validate(report, schema_lite.load(SCHEMA))
    if errors:
        return errors, warnings
    parts = narrative_text(report)
    full = "\n".join(parts)
    wc = len(words(full))
    if wc < 300 or wc > 950:
        errors.append(f"narrative is {wc} words, target is roughly 450-800")
    elif wc < 450 or wc > 800:
        warnings.append(f"narrative is {wc} words, target is roughly 450-800")

    if "—" in full:
        errors.append("em dash found")
    if "–" in full:
        warnings.append("en dash found")
    low = full.lower()
    for b in BANNED:
        if b in low:
            errors.append(f"banned phrase: '{b}'")
    tp = THIRD_PERSON.findall(full)
    if len(tp) >= 2:
        errors.append("Chef refers to itself in the third person more than once")
    elif tp:
        warnings.append("Chef refers to itself in the third person once")
    for rx in NOT_BUT:
        if rx.search(full):
            errors.append("'not X but Y' construction found")
            break
    for rx in FOOTNOTE:
        if rx.search(full):
            errors.append(f"audit-style citation or link in the narrative ({rx.pattern})")
            break
    if "?" in full:
        warnings.append("rhetorical question in the narrative")
    thens = sum(1 for p in parts for s in sentences(p) if re.match(r"then\b", s, re.I))
    if thens >= 3:
        warnings.append(f"{thens} sentences start with 'Then' (repetitive 'You did X. Then Y.' pattern)")
    total_k = 0
    for p in parts:
        k = sum(1 for w in words(p.lower()) if w in KITCHEN)
        total_k += k
        if k > 2:
            errors.append(f"kitchen metaphors piling up in one paragraph ({k}): {p[:50]}...")
    if total_k > 6:
        warnings.append(f"{total_k} kitchen words in total")
    nums = len(re.findall(r"\b\d[\d,.:]*\b", full))
    if nums > 14:
        warnings.append(f"{nums} numbers in the narrative (needless precision?)")
    vs = sentences(report["verdict"]["text"])
    if not 2 <= len(vs) <= 3:
        warnings.append(f"verdict has {len(vs)} sentences, target is 2-3")

    # structure
    keys = [s["key"] for s in report["sections"]]
    if keys.count("main") != 1:
        errors.append("exactly one 'main' section is required")
    if keys.count("side") > 2:
        errors.append("at most two 'side' sections")
    for s in report["sections"]:
        if s["key"] == "specials":
            n = len(s.get("items", []))
            if not 1 <= n <= 3:
                errors.append(f"specials must have 1-3 items, has {n}")
        if s["key"] in ("starter", "main", "side", "burnt", "leftovers", "specials") and not s.get("disclosure"):
            warnings.append(f"section '{s['key']}' has no 'How Chef knows' disclosure")
        if s["key"] == "bill" and not s["paragraphs"]:
            errors.append("empty bill section: omit it instead")
    seen = {}
    for s in report["sections"]:
        if s["key"] in ("compliments", "specials"):
            continue
        for wid in s.get("workstream_ids", []):
            if wid in seen:
                warnings.append(f"workstream {wid} appears in both '{seen[wid]}' and '{s['key']}'")
            seen[wid] = s["key"]

    # chef state
    manifest = json.loads(MANIFEST.read_text())
    if report["chef"]["state"] not in manifest["states"]:
        errors.append(f"unknown Chef state '{report['chef']['state']}'")

    # graph cross-checks
    if graph:
        gids = {w["id"] for w in graph["workstreams"]}
        wsmap = {w["id"]: w for w in graph["workstreams"]}
        for s in report["sections"]:
            for wid in s.get("workstream_ids", []):
                if wid not in gids:
                    errors.append(f"section '{s['key']}' cites unknown workstream {wid}")
            if s["share"]["include"]:
                for wid in s.get("workstream_ids", []):
                    w = wsmap.get(wid)
                    if w and not w["sensitivity"]["share_eligible"]:
                        errors.append(f"section '{s['key']}' is shareable but {wid} is not share_eligible")
        terms = [p["name"] for p in graph["redactions"]["people"]] + [t["term"] for t in graph["redactions"]["terms"]]
        shares = [report["verdict"]["share"]] + [s["share"] for s in report["sections"]]
        for sh in shares:
            if not sh["include"]:
                continue
            for t in terms:
                if t and re.search(re.escape(t), sh["text"], re.I):
                    errors.append(f"share text contains redaction term '{t}'")
            if re.search(r"https?://|@\w+|\b\S+@\S+\.\S+", sh["text"]):
                errors.append("share text contains a link, mention or email")
        if "—" in "".join(sh["text"] for sh in shares):
            errors.append("em dash in share text")
    return errors, warnings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("report")
    ap.add_argument("--graph")
    a = ap.parse_args()
    report = schema_lite.load(a.report)
    graph = schema_lite.load(a.graph) if a.graph else None
    errors, warnings = check(report, graph)
    for w in warnings:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
