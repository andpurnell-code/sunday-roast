#!/usr/bin/env python3
"""Build the share-safe export from an allowlisted schema.

Usage:
  python3 build_share.py --graph G.json --report R.json [--options O.json] --out DIR

Writes DIR/share.json (the only payload that may ever be published), DIR/share.html
(a standalone page built from that payload alone) and DIR/share.txt.

Options JSON (all optional):
  {"remove_names": true, "remove_company": true,
   "drop": ["burnt"],                      # section keys to drop
   "edits": {"main": "replacement text"}}  # edited passages, applied before the leak check

Allowlist (nothing else is copied): chef.state, meta.tagline, meta.week_label,
verdict.share.text, sections[].title, sections[].share.text. No evidence, links,
coverage, workstream ids or private metadata. The build fails if any redaction
term, link, email or @mention survives.
"""
import argparse
import html
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import schema_lite  # noqa: E402

ASSETS = HERE.parent / "assets" / "brand"
LEAK = re.compile(r"https?://|www\.|\b[\w.+-]+@[\w-]+\.[\w.]+\b|(?<!\w)@\w+")


def apply_redactions(text, redactions, names=True, company=True):
    """Replace names with roles and company terms with generic phrases. Longest first."""
    pairs = []
    if names:
        pairs += [(p["name"], p["role"]) for p in redactions.get("people", [])]
        # first names too
        for p in redactions.get("people", []):
            first = p["name"].split()[0]
            if len(first) > 2:
                pairs.append((first, p["role"]))
    if company:
        pairs += [(t["term"], t["generic"]) for t in redactions.get("terms", [])]
    pairs.sort(key=lambda x: len(x[0]), reverse=True)
    for term, repl in pairs:
        if term:
            text = re.sub(r"(?<![\w])" + re.escape(term) + r"(?![\w])", repl, text, flags=re.I)
    return text


def build(graph, report, options=None):
    options = options or {}
    names = options.get("remove_names", True)
    company = options.get("remove_company", True)
    drop = set(options.get("drop", []))
    edits = options.get("edits", {})
    red = graph["redactions"]
    wsmap = {w["id"]: w for w in graph["workstreams"]}

    def clean(t):
        return apply_redactions(t, red, names, company).strip()

    payload = {
        "chef": {"state": report["chef"]["state"]},
        "tagline": report["meta"]["tagline"],
        "week_label": report["meta"]["week_label"],
        "verdict": clean(edits.get("verdict", report["verdict"]["share"]["text"])) if report["verdict"]["share"]["include"] else "",
        "sections": [],
    }
    skipped = []
    for s in report["sections"]:
        if s["key"] in drop or not s["share"]["include"]:
            skipped.append((s["key"], "excluded"))
            continue
        if any(not wsmap.get(w, {}).get("sensitivity", {}).get("share_eligible", False) for w in s.get("workstream_ids", [])):
            skipped.append((s["key"], "workstream not share_eligible"))
            continue
        text = clean(edits.get(s["key"], s["share"]["text"]))
        if text:
            payload["sections"].append({"title": s["title"], "text": text})

    # leak check: fail rather than publish
    blob = json.dumps(payload, ensure_ascii=False)
    problems = []
    if LEAK.search(blob):
        problems.append("link, email or @mention present")
    for p in red.get("people", []):
        if re.search(re.escape(p["name"]), blob, re.I) and names:
            problems.append(f"name '{p['name']}' present")
    for t in red.get("terms", []):
        if re.search(r"(?<![\w])" + re.escape(t["term"]) + r"(?![\w])", blob, re.I) and company:
            problems.append(f"term '{t['term']}' present")
    if "—" in blob:
        problems.append("em dash present")
    if problems:
        raise ValueError("share build blocked: " + "; ".join(problems))
    return payload, skipped


def text_version(p):
    out = [p["verdict"]] if p["verdict"] else []
    for s in p["sections"]:
        out.append(f"{s['title']}\n{s['text']}")
    out.append(f"{p['tagline']}  sundayroast.me")
    return "\n\n".join(out)


def page(p):
    logo = re.sub(r'^<svg width="[^"]*" height="[^"]*"', '<svg role="img" aria-hidden="true" focusable="false"', (ASSETS / "logo-head.svg").read_text(encoding="utf-8").strip(), count=1)
    secs = "".join(f"<section><h2>{html.escape(s['title'])}</h2><p>{html.escape(s['text'])}</p></section>" for s in p["sections"])
    verdict = f'<section class="verdict"><h2>Chef\'s verdict</h2><p>{html.escape(p["verdict"])}</p></section>' if p["verdict"] else ""
    return f"""<title>Sunday Roast</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Caprasimo&family=Figtree:wght@400;500;600;700&display=swap">
<style>
@font-face{{font-family:'Caprasimo';font-style:normal;font-weight:400;font-display:block;src:url(https://fonts.gstatic.com/s/caprasimo/v6/esDT31JQOPuXIUGBp72klQ.ttf) format('truetype')}}
@font-face{{font-family:'SR Slab';font-weight:400;src:local('Rockwell Bold'),local('Rockwell-Bold'),local('Georgia Bold'),local('Georgia-Bold'),local('Cambria Bold'),local('Cambria-Bold')}}
:root{{--logo-bg:transparent;--logo-inset:0px;--bg:#FFFFFF;--head:#473628;--ink:#302A29;--muted:#6B605B;--oat:#E9E5DD;--roast-ink:#9C4637;--display:'Caprasimo','SR Slab',Georgia,serif;--body:'Figtree',system-ui,-apple-system,'Segoe UI',sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--logo-bg:#FAF7F0;--logo-inset:5px;--bg:#1E1A18;--head:#F3ECDF;--ink:#F3ECDF;--muted:#B5A99D;--oat:#2C2623;--roast-ink:#EFA68B;color-scheme:dark}}}}
:root[data-theme="dark"]{{--logo-bg:#FAF7F0;--logo-inset:5px;--bg:#1E1A18;--head:#F3ECDF;--ink:#F3ECDF;--muted:#B5A99D;--oat:#2C2623;--roast-ink:#EFA68B;color-scheme:dark}}
body{{background:var(--bg);color:var(--ink);font-family:var(--body);font-size:17px;line-height:1.65;padding-block:24px 56px;padding-left:max(18px,env(safe-area-inset-left,0px));padding-right:max(18px,env(safe-area-inset-right,0px))}}
.wrap{{max-width:680px;margin:0 auto;display:flex;flex-direction:column;gap:30px}}
header{{display:flex;gap:18px;align-items:center}}header>div{{min-width:0}}
.plate{{flex:none;line-height:0}}.plate svg{{width:112px;height:112px}}
.k{{margin:0 0 4px;font-size:15px;color:var(--muted)}}
h1{{color:var(--head);font-family:var(--display);font-weight:400;font-size:clamp(30px,6vw,40px);line-height:1.05;margin:0}}
.tag{{margin:2px 0 0;font-size:15.5px;color:var(--muted)}}
h2{{margin:0 0 4px;font-size:18px;font-weight:700;color:var(--head)}}
section p{{margin:0;max-width:62ch}}
.verdict{{background:var(--oat);border-radius:20px;padding:20px 24px}}.verdict h2{{font-size:15px;color:var(--roast-ink)}}.verdict p{{font-size:20px;line-height:1.5;font-weight:500}}
.foot{{margin:0;font-size:14px;color:var(--muted)}}
.logo{{flex:none;height:104px;width:calc(104px*408/496);box-sizing:border-box;padding:var(--logo-inset);border-radius:12px;background:var(--logo-bg);line-height:0}}.logo svg{{width:100%;height:100%;display:block}}
@media (max-width:560px){{body{{font-size:16.5px}}.plate svg{{width:88px;height:88px}}header{{gap:14px}}}}
</style>
<div class="wrap">
<header><span class="logo">{logo}</span><div><p class="k">{html.escape(p['week_label'])}</p><h1>The Sunday Roast</h1><p class="tag">{html.escape(p['tagline'])}</p></div></header>
{verdict}
{secs}
<p class="foot">sundayroast.me</p>
</div>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", required=True)
    ap.add_argument("--report", required=True)
    ap.add_argument("--options")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    graph = schema_lite.load(a.graph)
    report = schema_lite.load(a.report)
    options = schema_lite.load(a.options) if a.options else {}
    try:
        payload, skipped = build(graph, report, options)
    except ValueError as e:
        print("ERROR", e)
        return 1
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "share.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (out / "share.txt").write_text(text_version(payload) + "\n", encoding="utf-8")
    (out / "share.html").write_text(page(payload), encoding="utf-8")
    for k, why in skipped:
        print(f"skipped {k}: {why}")
    print(f"wrote {out}/share.json, share.txt, share.html ({len(payload['sections'])} sections)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
