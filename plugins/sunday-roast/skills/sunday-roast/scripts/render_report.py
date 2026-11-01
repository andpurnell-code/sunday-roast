#!/usr/bin/env python3
"""Render the private Sunday Roast report page (Stage E).

Usage:
  python3 render_report.py --graph 02-evidence-graph.json --report 04-report.json --out report.html

Output is an artifact-format fragment (no doctype/html/head/body), self-contained
apart from Google Fonts. The page holds the full private data. It is private to
its owner. The share flow inside it only uses allowlisted share text.
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

LOGO = HERE.parent / "assets" / "brand" / "logo-head.svg"


def logo_svg():
    """The supplied chicken-head logo, inlined as is (only size attributes and an accessible name are added)."""
    t = LOGO.read_text(encoding="utf-8").strip()
    t = re.sub(r'^<svg width="[^"]*" height="[^"]*"', '<svg role="img" aria-hidden="true" focusable="false"', t, count=1)
    return t

MODE_LABEL = {
    "direct": "Read directly",
    "indirect": "Found through links only",
    "awaiting_input": "Waiting for your input",
    "unavailable": "Not available",
    "not_selected": "Not selected",
}

CSS = """
@font-face{font-family:'Caprasimo';font-style:normal;font-weight:400;font-display:block;src:url(https://fonts.gstatic.com/s/caprasimo/v6/esDT31JQOPuXIUGBp72klQ.ttf) format('truetype')}
@font-face{font-family:'SR Slab';font-weight:400;src:local('Rockwell Bold'),local('Rockwell-Bold'),local('Georgia Bold'),local('Georgia-Bold'),local('Cambria Bold'),local('Cambria-Bold')}
/* Warm, plain reading page. Caprasimo for the title and two headings (bold system slab as fallback), Figtree for everything else. */
:root{--logo-bg:transparent;--logo-inset:0px;--bg:#FFFFFF;--head:#473628;--ink:#302A29;--muted:#6B605B;--yolk:#D5A03D;--roast:#BA5845;--oat:#E9E5DD;
--yolk-soft:#F6E9CB;--roast-soft:#F3DDD6;--roast-ink:#9C4637;--line:#DDD6CA;--on-yolk:#2E2118;--overlay:rgba(48,42,41,.45);--focus:#302A29;
--display:'Caprasimo','SR Slab',Georgia,serif;--body:'Figtree',system-ui,-apple-system,'Segoe UI',sans-serif}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--logo-bg:#FAF7F0;--logo-inset:5px;--bg:#1E1A18;--head:#F3ECDF;--ink:#F3ECDF;--muted:#B5A99D;--roast:#D98B6E;--oat:#2C2623;--yolk-soft:#3A3020;--roast-soft:#3A2822;--roast-ink:#EFA68B;--line:#3D3531;--overlay:rgba(0,0,0,.6);--focus:#F3ECDF;color-scheme:dark}}
:root[data-theme="dark"]{--logo-bg:#FAF7F0;--logo-inset:5px;--bg:#1E1A18;--head:#F3ECDF;--ink:#F3ECDF;--muted:#B5A99D;--roast:#D98B6E;--oat:#2C2623;--yolk-soft:#3A3020;--roast-soft:#3A2822;--roast-ink:#EFA68B;--line:#3D3531;--overlay:rgba(0,0,0,.6);--focus:#F3ECDF;color-scheme:dark}
body{background:var(--bg);color:var(--ink);font-family:var(--body);font-size:17px;line-height:1.65;padding-block:18px 72px;padding-left:max(18px,env(safe-area-inset-left,0px));padding-right:max(18px,env(safe-area-inset-right,0px))}
body.lock{overflow:hidden}
*:focus-visible{outline:3px solid var(--focus);outline-offset:3px;border-radius:4px}
.wrap{max-width:720px;margin:0 auto;display:flex;flex-direction:column;gap:44px}
.top{display:flex;gap:12px;align-items:center;justify-content:flex-end}
.logo{flex:none;--lh:104px;height:var(--lh);width:calc(var(--lh)*408/496);box-sizing:border-box;padding:var(--logo-inset);border-radius:12px;background:var(--logo-bg);line-height:0}
.logo svg{width:100%;height:100%;display:block}
.btns{display:flex;gap:8px;align-items:center}
button{font:inherit;cursor:pointer}
.btn{background:transparent;color:var(--head);border:1.5px solid var(--head);border-radius:999px;padding:7px 16px;font-size:15px;font-weight:600;line-height:1.3}
.btn.quiet{border-color:transparent;color:var(--head);text-decoration:underline;text-underline-offset:3px;padding-inline:8px}
.btn.primary{background:var(--yolk);color:var(--on-yolk);border-color:var(--yolk)}
.btn:hover{background:var(--yolk-soft)}
.btn.primary:hover{background:var(--yolk);filter:brightness(.94)}
.btn:disabled,.btn.disabled{opacity:.5;cursor:not-allowed}
a.btn{display:inline-block;text-decoration:none}
.hero{display:flex;gap:18px;align-items:center}
.hero .ht{min-width:0}
.hero .tag{margin:2px 0 0}
.hero>div{min-width:0}
.when{margin:0 0 4px;font-size:15px;color:var(--muted)}
h1{color:var(--head);font-family:var(--display);font-weight:400;font-size:clamp(32px,6.4vw,44px);line-height:1.05;margin:0;text-wrap:balance}
.tag{margin:8px 0 0;color:var(--muted);font-size:16px}
.verdict{background:var(--oat);border-radius:22px;padding:24px 28px 26px}
.verdict h2{margin:0 0 6px;font-size:15px;font-weight:700;color:var(--roast-ink)}
.verdict p{margin:0;font-size:21px;line-height:1.5;font-weight:500;text-wrap:pretty}
.gap{font-size:15px;color:var(--muted);margin:-20px 0 0}
.course{display:flex;flex-direction:column;gap:12px}
.course h2{color:var(--head);margin:0;font-size:20px;font-weight:700;line-height:1.3}
.course p{margin:0;max-width:64ch;text-wrap:pretty}
.main{gap:16px}
.main h2{color:var(--head);font-family:var(--display);font-weight:400;font-size:32px;line-height:1.1;text-decoration:underline;text-decoration-color:var(--yolk);text-decoration-thickness:6px;text-underline-offset:6px;text-decoration-skip-ink:none}
.main p{font-size:18.5px;line-height:1.7}
.sides .cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px 32px}
.sides p{font-size:16px;line-height:1.6}
.burnt{background:var(--roast-soft);border-radius:18px;padding:20px 24px 22px;transform:rotate(-.7deg);margin-inline:-6px}
.burnt h2{color:var(--roast-ink)}
.leftovers p{font-size:15.5px;color:var(--muted)}
.leftovers h2{font-size:17px;color:var(--head)}
.kind{background:var(--yolk-soft);border-radius:18px;padding:22px 26px 24px}
.kind p{font-size:17.5px}
ul.notes-list{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:14px}
ul.notes-list li{padding-left:22px;position:relative;max-width:64ch}
ul.notes-list li::before{content:"";position:absolute;left:2px;top:.62em;width:9px;height:9px;border-radius:50%;background:var(--yolk)}
ul.notes-list strong{font-weight:700}
ul.notes-list p{display:inline;margin:0}
.closing{border-top:1.5px solid var(--line);padding-top:30px;gap:16px}
.closing h2{color:var(--head);font-family:var(--display);font-weight:400;font-size:26px;line-height:1.15}
.signoff{display:flex;gap:16px;align-items:center;margin-top:6px}
.signoff p{color:var(--muted);font-size:15.5px;margin-bottom:8px}
.how{font-size:15px;margin-top:2px}
.how summary{cursor:pointer;color:var(--muted);width:max-content;max-width:100%;padding:3px 0;text-decoration:underline;text-decoration-style:dotted;text-underline-offset:4px;list-style-position:inside}
.how[open] summary{color:var(--ink)}
.how-body{margin-top:8px;padding:14px 16px;background:var(--oat);border-radius:12px;display:flex;flex-direction:column;gap:12px;color:var(--ink)}
.how-body h4{margin:0 0 2px;font-size:14px;font-weight:700}
.how-body ul{margin:0;padding-left:18px}
.how-body p{font-size:15px;max-width:none}
.how-body a{color:var(--roast-ink);overflow-wrap:anywhere}
.how-body .tagn{color:var(--muted)}
.foot{margin:0;font-size:14px;color:var(--muted);display:flex;flex-direction:column;gap:2px}
.panel{position:fixed;inset:0;background:var(--overlay);z-index:20;display:flex;justify-content:flex-end;padding-top:env(safe-area-inset-top,0px)}
.panel[hidden]{display:none}
.sheet{background:var(--bg);color:var(--ink);width:min(560px,100%);height:100%;overflow:auto;padding:22px max(18px,env(safe-area-inset-right,0px)) 40px 22px;display:flex;flex-direction:column;gap:16px;font-size:16px}
.sheet h3{color:var(--head);font-family:var(--display);font-weight:400;font-size:26px;margin:0;line-height:1.15}
.sheet .row{display:flex;justify-content:space-between;gap:12px;align-items:flex-start}
.sheet p{margin:0;font-size:15px}
.src{border-top:1.5px solid var(--line);padding-top:12px;display:flex;flex-direction:column;gap:2px}
.src b{font-weight:700}.src .m{font-size:13.5px;color:var(--roast-ink);font-weight:600}
.src ul{margin:4px 0 0;padding-left:18px;font-size:15px;color:var(--muted)}
.opts{display:flex;flex-direction:column;gap:8px;font-size:15px}
.opts label{display:flex;gap:10px;align-items:flex-start}
.opts input{margin-top:.35em;accent-color:var(--roast)}
.passage{display:flex;flex-direction:column;gap:4px}
.passage .ph{font-size:14.5px;font-weight:700;display:flex;gap:8px;align-items:center}
textarea{width:100%;box-sizing:border-box;font:15px/1.5 var(--body);background:var(--oat);color:var(--ink);border:1.5px solid var(--line);border-radius:10px;padding:10px;resize:vertical}
.card{background:var(--oat);color:#302A29;border-radius:16px;padding:18px;display:flex;flex-direction:column;gap:10px}
.card .ch{display:flex;gap:12px;align-items:center}
.card .ch b{font-family:var(--display);font-weight:400;font-size:20px;display:block;color:#473628}
.card .ch span{font-size:13.5px;color:#6B605B}
.card h4{font-size:13.5px;color:#9C4637;margin:6px 0 0;font-weight:700}
.card p{margin:0;font-size:15px;color:#302A29}
.card .ft{font-size:13px;color:#6B605B}
.warn{background:var(--yolk-soft);color:var(--ink);border-radius:10px;padding:10px 12px;font-size:14.5px}
.act{display:flex;gap:8px;flex-wrap:wrap}
.status{font-size:14px;color:var(--muted);min-height:1.3em}
.imgwrap{display:flex;flex-direction:column;gap:8px}
.imgwrap img{max-width:100%;border-radius:10px;border:1.5px solid var(--line)}
.note{font-size:14px;color:var(--muted)}
.edit-h{margin:8px 0 0;font-size:16px;font-weight:700;color:var(--head)}
.copysrc{font-size:14px}
@media (max-width:560px){
body{font-size:16.5px;padding-block:12px 56px}
.wrap{gap:36px}
h1{font-size:26px}
.hero{gap:14px}.logo{--lh:100px}.tag{font-size:14.5px;line-height:1.4}
.verdict{padding:20px 20px 22px;border-radius:18px}
.verdict p{font-size:19px;line-height:1.5}
.main h2{font-size:28px}.main p{font-size:17.5px}
.burnt{transform:none;margin-inline:0;padding:18px 18px 20px}
.kind{padding:18px 18px 20px}
.sheet{padding-left:18px}
.panel{align-items:flex-end}
.sheet{height:92%;border-radius:20px 20px 0 0;width:100%}
}
@media print{.top .btns,.panel{display:none!important}.how:not([open])>.how-body{display:block}body{padding:0}.burnt{transform:none}}
"""


def e(s):
    return html.escape(str(s), quote=True)


def disclosure(d):
    if not d:
        return ""
    parts = []
    if d.get("observed"):
        parts.append("<div><h4>What Chef saw</h4><ul>" + "".join(f"<li>{e(x)}</li>" for x in d["observed"]) + "</ul></div>")
    if d.get("inferred"):
        parts.append("<div><h4>What Chef worked out</h4><ul>" + "".join(f"<li>{e(x)}</li>" for x in d["inferred"]) + "</ul></div>")
    if d.get("uncertainty"):
        parts.append("<div><h4>What Chef is not sure about</h4><ul>" + "".join(f"<li>{e(x)}</li>" for x in d["uncertainty"]) + "</ul></div>")
    if d.get("sources"):
        lis = []
        for s in d["sources"]:
            name = e(s["name"])
            if s.get("url"):
                tag = "" if s.get("opened") else ' <span class="tagn">(link only, not opened)</span>'
                lis.append(f'<li><a href="{e(s["url"])}" target="_blank" rel="noopener noreferrer">{name}</a>{tag}</li>')
            else:
                lis.append(f"<li>{name}</li>")
        parts.append("<div><h4>Where to look</h4><ul>" + "".join(lis) + "</ul></div>")
    if d.get("dates"):
        parts.append(f"<div><h4>When</h4><p>{e(d['dates'])}</p></div>")
    return '<details class="how"><summary>How Chef knows</summary><div class="how-body">' + "".join(parts) + "</div></details>"


def section_html(s, closing_svg=""):
    k = s["key"]
    paras = s.get("paragraphs", [])
    items = s.get("items", [])
    if not paras and not items:
        return ""  # nothing meaningful to say: leave the course off the menu
    title = e(s["title"])
    how = disclosure(s.get("disclosure"))
    p_html = "".join(f"<p>{e(p)}</p>" for p in paras)
    if k == "specials":
        lis = []
        for it in items:
            if " | " in it:
                t, rest = it.split(" | ", 1)
                lis.append(f"<li><strong>{e(t)}.</strong> <p>{e(rest)}</p></li>")
            else:
                lis.append(f"<li><p>{e(it)}</p></li>")
        sign = '<div class="signoff"><div><p>See you next Sunday.</p><button class="btn" data-open-share type="button">Share this roast</button></div></div>'
        return (f'<section class="course closing" id="sec-{k}"><h2>{title}</h2>{p_html}<ul class="notes-list">{"".join(lis)}</ul>'
                f'{how}{sign}</section>')
    ul = ""
    if items:
        ul = '<ul class="notes-list">' + "".join(f"<li><p>{e(i)}</p></li>" for i in items) + "</ul>"
    if k == "side":
        p_html = f'<div class="cols">{p_html}</div>'
    cls = {"main": "main", "side": "sides", "burnt": "burnt", "leftovers": "leftovers", "compliments": "kind"}.get(k, "")
    return f'<section class="course {cls}" id="sec-{k}"><h2>{title}</h2>{p_html}{ul}{how}</section>'


def coverage_html(cov):
    out = []
    for c in cov:
        lim = "".join(f"<li>{e(x)}</li>" for x in c.get("limits", []))
        out.append(f'<div class="src"><span class="m">{e(MODE_LABEL.get(c["mode"], c["mode"]))}</span><b>{e(c["source"])}</b>'
                   f'<p>{e(c["read"])}</p>{"<ul>" + lim + "</ul>" if lim else ""}</div>')
    return "".join(out)


def render(graph, report):
    state = report["chef"]["state"]
    closing_svg = ""  # no mascot illustrations in the report for now
    secs = "".join(section_html(s, closing_svg) for s in report["sections"])
    gap = f'<p class="gap">{e(report["meta"]["gap_note"])}</p>' if report["meta"].get("gap_note") else ""
    share = {
        "verdict": report["verdict"]["share"],
        "sections": [{"key": s["key"], "index": i, "title": s["title"], "text": s["share"]["text"], "include": s["share"]["include"]}
                     for i, s in enumerate(report["sections"])],
    }
    data = {"tagline": report["meta"]["tagline"], "week_label": report["meta"]["week_label"], "share": share,
            "redactions": graph["redactions"]}
    data_json = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    js = (HERE / "share_ui.js").read_text(encoding="utf-8")
    cov = coverage_html(graph["coverage"])
    pos = report["meta"].get("positioning", "")
    return f"""<title>Sunday Roast</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preload" href="https://fonts.gstatic.com/s/caprasimo/v6/esDT31JQOPuXIUGBp72klQ.ttf" as="font" type="font/ttf" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Caprasimo&family=Figtree:wght@400;500;600;700&display=swap">
<style>{CSS}</style>
<div class="wrap" id="top">
<div class="top"><div class="btns"><button class="btn quiet" id="open-cov" type="button">Sources</button><button class="btn primary" id="open-share" data-open-share type="button">Share</button></div></div>
<header class="hero"><span class="logo">{logo_svg()}</span><div class="ht"><p class="when">{e(report['meta']['week_label'])}</p><h1>The Sunday Roast</h1><p class="tag">{e(report['meta']['tagline'])}</p></div></header>
<section class="verdict" aria-labelledby="verdict-h"><h2 id="verdict-h">Chef's verdict</h2><p>{e(report['verdict']['text'])}</p></section>
{gap}
{secs}
<p class="foot"><span>{e(pos)}</span><span>Private report. Only you can see this page.</span></p>
</div>

<div class="panel" id="cov" hidden role="dialog" aria-modal="true" aria-labelledby="cov-t"><div class="sheet">
<div class="row"><h3 id="cov-t">Sources and coverage</h3><button class="btn" type="button" data-close>Close</button></div>
<p>What Chef could see, and what it could not. A missing source is never treated as a quiet week.</p>
{cov}
</div></div>

<div class="panel" id="share" hidden role="dialog" aria-modal="true" aria-labelledby="sh-t"><div class="sheet">
<div class="row"><h3 id="sh-t">Share</h3><button class="btn" type="button" data-close>Close</button></div>
<p>Your report stays private. This builds a separate, share-safe version from short text written for sharing. Evidence, links, sources and private details are never part of it.</p>
<div class="opts">
<label><input type="checkbox" id="opt-names" checked> Remove names (replaced by roles)</label>
<label><input type="checkbox" id="opt-company" checked> Remove company and project details</label>
<label><input type="checkbox" checked disabled> Hide evidence links, raw sources and private metadata (always on)</label>
</div>
<div class="card" id="card"><div class="ch"><div><b>The Sunday Roast</b><span>{e(report['meta']['week_label'])}</span></div></div><div id="card-body"></div><div class="ft">{e(report['meta']['tagline'])} sundayroast.me</div></div>
<div class="warn" id="leak" hidden>A link, email or mention is still in the text. Remove it before sharing.</div>
<div class="opts"><label><input type="checkbox" id="review-ok"> I have reviewed this preview and it is safe to share.</label></div>
<div class="act"><a class="btn primary" id="li-btn" href="#" target="_blank" rel="noopener noreferrer" aria-disabled="true">Share on LinkedIn</a><button class="btn" id="copy-btn" type="button">Copy text</button><button class="btn" id="img-btn" type="button">Make image</button></div>
<p class="note">LinkedIn opens in a new tab with your text filled in. To add the picture, make the image, copy it and paste it into the post.</p>
<p class="status" id="status" role="status" aria-live="polite"></p>
<textarea id="copy-src" class="copysrc" rows="5" readonly aria-label="Share-safe text" hidden></textarea>
<div class="imgwrap" id="img-wrap" hidden><img id="img-out" alt="Share image preview"><div class="act"><button class="btn" id="img-copy" type="button">Copy image</button></div></div>
<p class="note">Want a page with a link instead? Ask Claude to publish your share page. It uses only the text above. Deleting that page removes it.</p>
<h4 class="edit-h">Edit or remove passages</h4>
<div id="passages"></div>
</div></div>

<script type="application/json" id="rr-data">{data_json}</script>
<script>{js}</script>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", required=True)
    ap.add_argument("--report", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    graph = schema_lite.load(a.graph)
    report = schema_lite.load(a.report)
    pathlib.Path(a.out).write_text(render(graph, report), encoding="utf-8")
    print("wrote", a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
