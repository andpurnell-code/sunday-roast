#!/usr/bin/env python3
"""Generate the static site in site/ from the skill's own source list and brand assets.
Run from the repo root: python3 tools/build_site.py
Brand SVGs are the author's own (Chick.svg lockup, ChickHead.svg). No new illustrations are made here."""
import html, json, pathlib, re, shutil
ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL = ROOT / "plugins/sunday-roast/skills/sunday-roast"
SITE = ROOT / "site"
A = SITE / "assets"
REPO = "https://github.com/andpurnell-code/sunday-roast"
ZIP = REPO + "/releases/latest/download/sunday-roast-skill.zip"
URL = "https://sundayroast.me"
e = html.escape

sources = json.loads((SKILL / "templates/sources.json").read_text())["sources"]
report = json.loads((SKILL / "tests/fixtures/report.json").read_text())

groups = {}
for s in sources:
    groups.setdefault(s["group"], []).append(s)
src_html = ""
for g, items in groups.items():
    src_html += f'<h3>{e(g)}</h3><div class="srcs">'
    for s in items:
        src_html += (f'<details class="src"><summary>{e(s["label"])}</summary>'
                     f'<p><b>Reads</b> {e(s["reads"])}</p><p><b>Never reads</b> {e(s["never_reads"])}</p></details>')
    src_html += "</div>"

sec = {s["key"]: s for s in report["sections"]}
def paras(k, n=None):
    ps = sec[k]["paragraphs"][:n]
    return "".join(f"<p>{e(p)}</p>" for p in ps)
dis = sec["starter"]["disclosure"]

PAGE = f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Sunday Roast | Your week, served with a side of sarcasm</title>
<meta name="description" content="A Claude skill that looks back over your own week in the tools you choose and writes a funny, kind, evidence-based review, narrated by Chef the chicken. Private by default. Free and open source.">
<link rel="canonical" href="{URL}/">
<meta name="theme-color" content="#ffffff">
<meta property="og:type" content="website">
<meta property="og:site_name" content="The Sunday Roast">
<meta property="og:title" content="The Sunday Roast">
<meta property="og:description" content="Your week, served with a side of sarcasm. A free Claude skill that roasts your own week, with receipts.">
<meta property="og:url" content="{URL}/">
<meta property="og:image" content="{URL}/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Chef, a chicken in a tall hat and apron, beside the words the sunday roast">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="The Sunday Roast">
<meta name="twitter:description" content="Your week, served with a side of sarcasm.">
<meta name="twitter:image" content="{URL}/assets/og.png">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/favicon.ico" sizes="48x48">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Caprasimo&family=Figtree:wght@400;600;700&display=swap">
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <a class="brand" href="/" aria-label="The Sunday Roast, home"><img src="/assets/chick-logo.svg" alt="The Sunday Roast" width="1245" height="496"></a>
  <nav aria-label="Main">
    <a href="#example">Example</a><a href="#sources">Sources</a><a href="#safe">Privacy</a><a href="#install">Install</a><a class="gh" href="{REPO}">GitHub</a>
  </nav>
</header>

<main id="main">
<section class="hero" aria-labelledby="h1">
  <img class="hero-art" src="/assets/chick-logo.svg" alt="The Sunday Roast: Chef, a wide-eyed chicken in a tall white chef's hat, beside the words the sunday roast" width="1245" height="496" fetchpriority="high">
  <p class="kicker">A free Claude skill</p>
  <h1 id="h1">Another week. What on earth happened?</h1>
  <p class="lede">Celebrate the wins. Laugh at what went sideways. Start next week a little wiser.</p>
  <p class="sub">Chef, a chicken in an alarmingly tall hat, looks back over your own week in the tools you choose and writes it up. Funny, kind, and backed by receipts.</p>
  <p class="cta"><a class="btn" href="#install">Get Roasted</a><a class="btn ghost" href="{REPO}">Read the source</a></p>
  <p class="fine">Your week, served with a side of sarcasm.</p>
</section>

<section id="how" class="band" aria-labelledby="how-h">
  <h2 id="how-h">How it works</h2>
  <ol class="steps">
    <li><span class="n">1</span><div><h3>You choose the sources</h3><p>Slack, Linear, GitHub or GitLab, Notion, Google Drive, Calendar and more. Nothing you do not tick is read.</p></div></li>
    <li><span class="n">2</span><div><h3>Chef investigates your week</h3><p>Only your own activity, read-only. It checks threads, tickets, docs and meetings for what you built, decided, taught and unblocked.</p></div></li>
    <li><span class="n">3</span><div><h3>You get a private report</h3><p>A short roast with a verdict, then the receipts for every claim. Sharing is optional, and you review exactly what leaves.</p></div></li>
  </ol>
  <p class="note">Chef can also ask, "Anything I can't see?" Unread counts and saved items are invisible to the tools, so you can tell Chef about them. Open loops, such as tags with no visible reply, are off unless you switch them on.</p>
</section>

<section id="example" aria-labelledby="ex-h">
  <h2 id="ex-h">An example roast</h2>
  <p class="intro">Entirely fictional: an invented person, invented projects and invented colleagues. A real report is private to you.</p>
  <article class="report" aria-label="Example report, fictional">
    <header class="rhead"><img src="/assets/chick-logo.svg" alt="" width="1245" height="496"><div><p class="rlabel">Sunday Roast, {e(report["meta"]["week_label"])}</p><p class="rtag">Fictional example</p></div></header>
    <h3>The verdict</h3>
    <p class="verdict">{e(report["verdict"]["text"])}</p>
    <h3>Starter</h3>
    {paras("starter", 2)}
    <details class="how-chef" open>
      <summary>How Chef knows</summary>
      <dl>
        <dt>Observed</dt><dd>{e("; ".join(dis["observed"]))}.</dd>
        <dt>Inferred</dt><dd>{e("; ".join(dis["inferred"]))}.</dd>
        <dt>Not sure about</dt><dd>{e("; ".join(dis["uncertainty"]))}.</dd>
        <dt>When</dt><dd>{e(dis["dates"])} (fictional)</dd>
      </dl>
    </details>
    <h3>Main</h3>
    {paras("main", 2)}
  </article>
  <p class="note">Every joke traces to something observed. If the evidence does not support a joke, the joke is cut. The facts are sacred. The commentary is not.</p>
</section>

<section id="sources" class="band" aria-labelledby="src-h">
  <h2 id="src-h">Pick your sources</h2>
  <p class="intro">Connect the tools you already use in Claude, then tell Chef which to read. Open a source to see exactly what it reads and what it never reads. You can also pass <code>sources=slack,linear</code> or <code>skip=calendar</code>.</p>
  {src_html}
  <p class="note">The skill can only use connectors you have already added to Claude. If you have none, you can paste notes instead.</p>
</section>

<section id="safe" aria-labelledby="safe-h">
  <h2 id="safe-h">Privacy and safety</h2>
  <ul class="plain">
    <li><b>It is about you, and only you.</b> Your own work only. No scores, no rankings, no manager's dashboard. It will not review a colleague.</li>
    <li><b>Read-only.</b> It never posts, edits or sends anything in your tools.</li>
    <li><b>You choose what it reads.</b> Unselected sources are never queried.</li>
    <li><b>Private by default.</b> The full report is yours. Colleagues appear by role, never by name. Sensitive topics such as hiring, pay, performance, health and legal matters are kept out of anything shareable.</li>
    <li><b>Sharing is a separate step.</b> A share-safe version is built from an allowlist and checked for leaks. You read it, tick a box, then copy it or open LinkedIn with it prefilled. Nothing is posted for you.</li>
    <li><b>This website collects nothing.</b> No accounts, no analytics, no tracking, no cookies. The page loads two fonts from Google Fonts, which means Google sees your IP address when you visit.</li>
  </ul>
  <p class="note">Where your data goes: the skill runs in your own Claude environment and uses the connectors you authorise. Claude and those providers process that data under their own terms, so this is not a promise that nothing leaves your computer. The skill itself uploads nothing and has no server. Read <a href="{REPO}/blob/main/PRIVACY.md">PRIVACY.md</a> and <a href="{REPO}/blob/main/SECURITY.md">SECURITY.md</a>.</p>
</section>

<section id="install" class="band" aria-labelledby="in-h">
  <h2 id="in-h">Get Roasted</h2>
  <p class="intro">Pick the way you use Claude. The skill is free, MIT licensed, and the same in all three.</p>
  <div class="installs">
    <div class="inst">
      <h3>Claude.ai or Cowork</h3>
      <ol>
        <li><a class="btn small" href="{ZIP}">Download the skill (zip)</a></li>
        <li>Open Claude, go to Settings, then Features (the wording may vary) and upload the zip as a skill.</li>
        <li>Make sure code execution is on. Custom skills need a paid plan.</li>
        <li>Connect your tools under Connectors, then say <em>Run my Sunday Roast</em>.</li>
      </ol>
    </div>
    <div class="inst">
      <h3>Claude Code, plugin</h3>
      <div class="cmd"><code>/plugin marketplace add andpurnell-code/sunday-roast</code><button type="button" data-copy="/plugin marketplace add andpurnell-code/sunday-roast">Copy</button></div>
      <div class="cmd"><code>/plugin install sunday-roast@sunday-roast</code><button type="button" data-copy="/plugin install sunday-roast@sunday-roast">Copy</button></div>
      <p>Then run <code>/sunday-roast:sunday-roast</code>.</p>
    </div>
    <div class="inst">
      <h3>Claude Code, plain skill</h3>
      <div class="cmd"><code>git clone {REPO}.git</code><button type="button" data-copy="git clone {REPO}.git">Copy</button></div>
      <div class="cmd"><code>cp -R sunday-roast/plugins/sunday-roast/skills/sunday-roast ~/.claude/skills/</code><button type="button" data-copy="cp -R sunday-roast/plugins/sunday-roast/skills/sunday-roast ~/.claude/skills/">Copy</button></div>
      <p>Then run <code>/sunday-roast</code>.</p>
    </div>
  </div>
  <p class="note">There is no one-click install. The skill needs Python 3.9 or later for its checks. Full steps and troubleshooting are in the <a href="{REPO}/blob/main/docs/INSTALL.md">install guide</a>. PDF export and hosted share links are not available inside the Claude viewer.</p>
</section>

<section id="feedback" aria-labelledby="fb-h">
  <h2 id="fb-h">Tell Chef what you think</h2>
  <p class="intro">It is early. Bugs, missing sources and better jokes are all welcome.</p>
  <p class="links"><a class="btn small" href="{REPO}/issues/new/choose">Report a bug</a><a class="btn small ghost" href="{REPO}/discussions">Join the discussion</a><a class="btn small ghost" href="{REPO}/blob/main/CONTRIBUTING.md">Contribute or fork</a><a class="btn small ghost" href="{REPO}">Source on GitHub</a></p>
  <h3 class="later">Coming later</h3>
  <p>"Roast My LinkedIn" is a separate, future experience. It is not part of the weekly roast or this install, and there is no date.</p>
</section>
</main>

<footer>
  <img class="flogo" src="/assets/chick-logo.svg" alt="The Sunday Roast" width="1245" height="496">
  <p>The Sunday Roast is a personal open-source project by Andrew Purnell. Code and text under the <a href="{REPO}/blob/main/LICENSE">MIT licence</a>. The chicken artwork, logo and name are not covered by it. Not affiliated with or endorsed by Anthropic.</p>
  <p><a href="{REPO}">GitHub</a> <a href="{REPO}/blob/main/PRIVACY.md">Privacy</a> <a href="{REPO}/blob/main/SECURITY.md">Security</a> <a href="{REPO}/releases">Releases</a></p>
</footer>
<script src="/assets/site.js" defer></script>
</body>
</html>
"""

NOTFOUND = """<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found | The Sunday Roast</title><meta name="robots" content="noindex"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Caprasimo&family=Figtree:wght@400;600;700&display=swap"><link rel="stylesheet" href="/assets/site.css"></head>
<body><main id="main" class="nf"><img class="nflogo" src="/assets/chick-logo.svg" alt="The Sunday Roast" width="1245" height="496"><h1>Overdone. This page is not here.</h1><p class="lede">Chef checked the oven, the pantry and the bin. Nothing.</p><p class="cta"><a class="btn" href="/">Back to the kitchen</a></p></main></body></html>
"""

CSS = r"""
:root{--bg:#fff;--head:#473628;--ink:#302A29;--muted:#6B605B;--yolk:#D5A03D;--roast:#BA5845;--oat:#F4F0E8;--line:#DDD6CA;--on-yolk:#2E2118;--roast-ink:#9C4637;
--display:'Caprasimo','SR Slab',Georgia,'Cambria',serif;--body:'Figtree',system-ui,-apple-system,'Segoe UI',sans-serif;color-scheme:light}
*{box-sizing:border-box}html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important}}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--body);font-size:18px;line-height:1.65}
img{max-width:100%;height:auto}a{color:var(--roast-ink);text-underline-offset:3px}
:focus-visible{outline:3px solid var(--ink);outline-offset:3px;border-radius:4px}
.skip{position:absolute;left:12px;top:-60px;background:var(--ink);color:#fff;padding:10px 14px;border-radius:8px;z-index:10}.skip:focus{top:12px}
h1,h2{font-family:var(--display);font-weight:400;color:var(--head);line-height:1.08;text-wrap:balance;margin:0}
h2{font-size:clamp(30px,5vw,40px);text-decoration:underline;text-decoration-color:var(--yolk);text-decoration-thickness:6px;text-underline-offset:7px;text-decoration-skip-ink:none;margin-bottom:18px}
h3{font-size:19px;margin:22px 0 6px;color:var(--head)}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.88em}
.top{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;max-width:1080px;margin:0 auto;padding:16px 20px}
.brand{display:block;line-height:0}.brand img{height:46px;width:auto}
.top nav{display:flex;gap:4px 18px;flex-wrap:wrap;font-size:16px}.top nav a{color:var(--ink);text-decoration:none;padding:6px 2px}.top nav a:hover{text-decoration:underline;text-decoration-color:var(--yolk);text-decoration-thickness:3px}
main>section{max-width:1080px;margin:0 auto;padding:56px 20px}
.band{max-width:none!important;background:var(--oat);padding-inline:0!important}.band>*{max-width:1040px;margin-inline:auto;padding-inline:20px}
.hero{text-align:center;padding-top:20px!important}.hero>*{margin-inline:auto}
.kicker{font-weight:700;font-size:14px;letter-spacing:.08em;text-transform:uppercase;color:var(--roast-ink);margin:0 0 10px}
h1{font-size:clamp(38px,7vw,64px);margin-bottom:18px}
.lede{font-size:clamp(20px,3vw,24px);color:var(--head);font-weight:600;line-height:1.35;margin:0 0 12px}.sub{margin:0 0 24px;max-width:36em}
.cta,.links{display:flex;flex-wrap:wrap;gap:12px;margin:0}.hero .cta{justify-content:center}
.btn{display:inline-block;background:var(--yolk);color:var(--on-yolk);font-weight:700;text-decoration:none;padding:14px 24px;border-radius:999px;border:2px solid var(--on-yolk);transition:transform .12s}
.btn:hover{transform:translateY(-2px)}.btn.ghost{background:transparent;color:var(--ink);border-color:var(--ink)}.btn.small{padding:10px 18px;font-size:16px}
.fine{color:var(--muted);font-size:15px;margin:18px 0 0}
.hero-art{display:block;width:min(560px,86vw);height:auto;margin-bottom:26px}.hero .sub,.hero .lede{max-width:36em}.flogo{height:44px;width:auto}.nflogo{width:min(320px,70vw);height:auto}
.intro{max-width:44em;color:var(--ink)}.note{max-width:44em;color:var(--muted);font-size:16px;margin-top:22px}
.steps{list-style:none;padding:0;margin:20px 0;display:grid;gap:22px;grid-template-columns:repeat(3,1fr)}
.steps li{display:flex;gap:14px}.steps h3{margin-top:0}.steps p{margin:0}
.n{flex:none;width:38px;height:38px;border-radius:50%;background:var(--yolk);color:var(--on-yolk);font-family:var(--display);display:grid;place-items:center;font-size:20px}
.band .steps+.note{max-width:44em}
.report{max-width:720px;border:2px solid var(--line);border-radius:18px;padding:26px clamp(18px,4vw,34px);margin:22px 0;background:#fff}
.rhead{display:flex;gap:16px;align-items:center;margin-bottom:6px;flex-wrap:wrap}.rhead img{height:44px;width:auto}.rlabel{font-family:var(--display);font-size:22px;color:var(--head);margin:0;line-height:1.1}.rtag{margin:2px 0 0;color:var(--roast-ink);font-weight:700;font-size:14px}
.report h3{font-family:var(--display);font-weight:400;font-size:24px;margin:24px 0 6px;text-decoration:underline;text-decoration-color:var(--yolk);text-decoration-thickness:5px;text-underline-offset:5px;text-decoration-skip-ink:none}
.report p{margin:0 0 12px}.verdict{font-size:20px;line-height:1.5;font-weight:600;color:var(--head)}
.how-chef{background:var(--oat);border-radius:12px;padding:12px 16px;margin:14px 0}.how-chef summary{cursor:pointer;font-weight:700}
.how-chef dl{margin:10px 0 0;font-size:16px}.how-chef dt{font-weight:700;margin-top:8px}.how-chef dd{margin:0}
.srcs{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:10px;margin:8px 0 6px}
.src{background:#fff;border:2px solid var(--line);border-radius:12px;padding:10px 14px;font-size:16px}.src summary{cursor:pointer;font-weight:700}.src p{margin:8px 0 0;font-size:15px;line-height:1.5}
.plain{padding-left:20px;max-width:46em}.plain li{margin:10px 0}
.installs{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin:18px 0}
.inst{background:#fff;border:2px solid var(--line);border-radius:16px;padding:18px 20px;min-width:0}.inst h3{margin-top:0;font-family:var(--display);font-weight:400;font-size:22px}
.inst ol{padding-left:20px;margin:0}.inst li{margin:8px 0}.inst p{margin:10px 0 0;font-size:16px}
.cmd{display:flex;gap:8px;align-items:stretch;margin:8px 0}.cmd code{flex:1;min-width:0;background:var(--oat);border-radius:8px;padding:9px 10px;overflow-wrap:anywhere;font-size:13.5px;line-height:1.45}
.cmd button{flex:none;font:inherit;font-size:14px;font-weight:700;background:#fff;color:var(--ink);border:2px solid var(--ink);border-radius:8px;padding:0 12px;cursor:pointer}
.later{margin-top:34px}
footer{max-width:1080px;margin:0 auto;padding:30px 20px 56px;border-top:2px solid var(--line);font-size:15px;color:var(--muted);display:grid;gap:8px;justify-items:start}
footer p{margin:0;max-width:52em}footer a{margin-right:14px}
.nf{max-width:560px;margin:12vh auto;padding:20px;text-align:center}.nf .cta{justify-content:center}.nf h1{font-size:clamp(32px,8vw,48px);margin:16px 0}
@media (max-width:860px){.steps,.installs{grid-template-columns:1fr}.top nav a.gh{display:none}.brand img{height:38px}}
"""
JS = """(function(){var b=document.querySelectorAll('[data-copy]');for(var i=0;i<b.length;i++){b[i].addEventListener('click',function(e){var t=e.currentTarget,x=t.getAttribute('data-copy');function ok(){t.textContent='Copied';setTimeout(function(){t.textContent='Copy'},1600)}
if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(x).then(ok,function(){sel(t)})}else{sel(t)}})}
function sel(t){var c=t.previousElementSibling,r=document.createRange();r.selectNodeContents(c);var s=getSelection();s.removeAllRanges();s.addRange(r);t.textContent='Press Ctrl or Cmd+C';setTimeout(function(){t.textContent='Copy'},2500)}})();
"""
(SITE / "index.html").write_text(PAGE, encoding="utf-8")
(SITE / "404.html").write_text(NOTFOUND, encoding="utf-8")
(A / "site.css").write_text(CSS.strip() + "\n", encoding="utf-8")
(A / "site.js").write_text(JS, encoding="utf-8")
(SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {URL}/sitemap.xml\n")
(SITE / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{URL}/</loc></url></urlset>\n')
(SITE / "vercel.json").write_text(json.dumps({
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "cleanUrls": True, "trailingSlash": False,
  "redirects": [{"source": "/:path(.*)", "has": [{"type": "host", "value": "www.sundayroast.me"}], "destination": "https://sundayroast.me/:path", "permanent": True}],
  "headers": [
    {"source": "/(.*)", "headers": [
      {"key": "X-Content-Type-Options", "value": "nosniff"},
      {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
      {"key": "X-Frame-Options", "value": "DENY"},
      {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()"},
      {"key": "Content-Security-Policy", "value": "default-src 'self'; img-src 'self' data:; style-src 'self' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; script-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'"}]},
    {"source": "/assets/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]}
  ]}, indent=2) + "\n")
print("site built")
