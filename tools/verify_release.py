#!/usr/bin/env python3
"""Release checks: manifests, one canonical skill, zip layout, links."""
import json, pathlib, re, sys, zipfile
ROOT = pathlib.Path(__file__).resolve().parent.parent
errs = []
def need(c, m):
    if not c: errs.append(m)
mk = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
pj = json.loads((ROOT / "plugins" / "sunday-roast" / ".claude-plugin" / "plugin.json").read_text())
need(mk["plugins"][0]["name"] == pj["name"], "marketplace entry name must equal plugin.json name")
need(not pj["name"].startswith("claude") and "anthropic" not in pj["name"], "reserved name")
need((ROOT / "plugins" / "sunday-roast" / mk["plugins"][0]["source"].replace("./plugins/sunday-roast", "").lstrip("/")).exists(), "plugin source path")
skills = [p for p in ROOT.rglob("SKILL.md") if ".git" not in p.parts]
need(len(skills) == 1, f"exactly one SKILL.md expected, found {len(skills)}")
text = skills[0].read_text()
need(f'version: "{pj["version"]}"' in text, "SKILL.md metadata.version must match plugin.json")
z = zipfile.ZipFile(ROOT / "dist" / "sunday-roast-skill.zip")
names = z.namelist()
need("sunday-roast/SKILL.md" in names, "zip must have sunday-roast/SKILL.md")
need(not any("__pycache__" in n or "/chef/" in n for n in names), "zip has junk")
need(z.read("sunday-roast/SKILL.md").decode() == text, "zip SKILL.md differs from canonical")
for md in ROOT.rglob("*.md"):
    for link in re.findall(r"\]\((?!https?:|#|mailto:)([^)#]+)", md.read_text()):
        need((md.parent / link).exists(), f"broken link in {md.relative_to(ROOT)}: {link}")
for f in ("LICENSE", "README.md", "PRIVACY.md", "SECURITY.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "CHANGELOG.md"):
    need((ROOT / f).exists(), f"missing {f}")
print("FAIL" if errs else "OK")
for e in errs: print(" -", e)
sys.exit(1 if errs else 0)
