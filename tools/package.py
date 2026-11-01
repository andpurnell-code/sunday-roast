#!/usr/bin/env python3
"""Build dist/sunday-roast-skill.zip from the canonical skill. Deterministic."""
import pathlib, zipfile
ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL = ROOT / "plugins" / "sunday-roast" / "skills" / "sunday-roast"
ZIP = ROOT / "dist" / "sunday-roast-skill.zip"
ZIP.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
    for p in sorted(SKILL.rglob("*")):
        if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc" and p.name != ".DS_Store":
            zi = zipfile.ZipInfo(str(pathlib.Path("sunday-roast") / p.relative_to(SKILL)), date_time=(2026, 11, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, p.read_bytes())
print("built", ZIP, ZIP.stat().st_size, "bytes")
