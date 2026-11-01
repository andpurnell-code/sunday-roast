#!/usr/bin/env python3
"""Sunday Roast tests (stdlib only). Run: python3 tests/run_tests.py

All fixtures are synthetic. No real week's data lives in this folder.
"""
import copy
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

HERE = pathlib.Path(__file__).resolve().parent
SKILL = HERE.parent
sys.path.insert(0, str(SKILL / "scripts"))

import build_share  # noqa: E402
import open_loops  # noqa: E402
import check_report  # noqa: E402
import render_report  # noqa: E402
import schema_lite  # noqa: E402
import select_stories  # noqa: E402
import validate_graph  # noqa: E402
import datetime as dt  # noqa: E402

FIX = HERE / "fixtures"
GRAPH = json.loads((FIX / "graph.json").read_text())
REPORT = json.loads((FIX / "report.json").read_text())


def g():
    return copy.deepcopy(GRAPH)


def r():
    return copy.deepcopy(REPORT)


class Assets(unittest.TestCase):
    def test_chef_states_and_logo(self):
        m = json.loads((SKILL / "schemas" / "chef-states.json").read_text())
        self.assertIn(m["fallback"], m["states"])
        self.assertGreaterEqual(len(m["states"]), 6)
        ET.fromstring((SKILL / "assets" / "brand" / "logo-head.svg").read_text())
        self.assertFalse((SKILL / "assets" / "chef").exists(), "unapproved generated Chef art must not ship")

    def test_no_old_character_system(self):
        self.assertFalse((SKILL / "characters").exists())
        text = (SKILL / "SKILL.md").read_text() + "".join(p.read_text() for p in (SKILL / "stages").glob("*.md"))
        for old in ("Pit Stop", "Magpie", "characters.json", "build_sprites"):
            self.assertNotIn(old, text)


class PublicRelease(unittest.TestCase):
    ALLOWED_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}

    def test_portable_frontmatter(self):
        block = (SKILL / "SKILL.md").read_text().split("---")[1]
        top = re.findall(r"^([A-Za-z-]+):", block, flags=re.M)
        self.assertTrue(set(top) <= self.ALLOWED_KEYS, set(top) - self.ALLOWED_KEYS)
        name = re.search(r"^name:\s*(.+)$", block, flags=re.M).group(1).strip()
        desc = re.search(r"^description:\s*(.+)$", block, flags=re.M).group(1).strip()
        self.assertRegex(name, r"^[a-z0-9-]{1,64}$")
        self.assertTrue(0 < len(desc) <= 1024)
        self.assertIsNone(re.search(r"<[^>]+>", desc))

    def test_referenced_files_exist(self):
        files = list(SKILL.glob("*.md")) + list((SKILL / "stages").glob("*.md")) + list((SKILL / "templates").glob("*.md"))
        missing = [(p.name, ref) for p in files for ref in re.findall(r"`((?:stages|templates|scripts|schemas|assets)/[A-Za-z0-9_./-]+)`", p.read_text()) if not (SKILL / ref).exists()]
        self.assertEqual(missing, [])

    def test_no_private_strings_or_secrets(self):
        bad = re.compile(r"(/Users/|/sessions/|(?<!and)purnell(?!-code)|@remote\.com|xox[bp]-|ghp_|BEGIN (RSA|PRIVATE))", re.I)
        for p in SKILL.rglob("*"):
            if p.is_file() and "__pycache__" not in p.parts and p.suffix in (".py", ".js", ".md", ".json", ".svg") and p.name != "run_tests.py":
                self.assertIsNone(bad.search(p.read_text()), p)

    def test_network_hosts_documented(self):
        ok = ("fonts.googleapis.com", "fonts.gstatic.com", "www.linkedin.com", "www.w3.org", "json-schema.org", "example.com", "sundayroast.me")
        for p in (SKILL / "scripts").glob("*"):
            if p.is_file() and p.suffix in (".py", ".js"):
                for host in re.findall(r"https?://([A-Za-z0-9.-]+)", p.read_text()):
                    self.assertIn(host, ok, f"{p.name}: {host}")


class Schemas(unittest.TestCase):
    def test_fixture_graph_valid(self):
        errors, warnings = validate_graph.check(g())
        self.assertEqual(errors, [], errors)

    def test_missing_field_fails(self):
        bad = g()
        del bad["workstreams"][0]["problem"]
        errors, _ = validate_graph.check(bad)
        self.assertTrue(any("problem" in e for e in errors))

    def test_sensitive_cannot_be_shareable(self):
        bad = g()
        bad["workstreams"][2]["sensitivity"]["share_eligible"] = True
        errors, _ = validate_graph.check(bad)
        self.assertTrue(any("share_eligible" in e for e in errors))

    def test_inspected_requires_source_and_impact_requires_observed(self):
        bad = g()
        bad["workstreams"][0]["artefacts"][0].pop("source")
        bad["workstreams"][0]["outcomes"][0]["evidence"] = "inferred"
        errors, _ = validate_graph.check(bad)
        self.assertTrue(any("inspected" in e for e in errors))
        self.assertTrue(any("evidenced impact" in e for e in errors))

    def test_building_only_warns(self):
        bad = g()
        bad["workstreams"] = [w for w in bad["workstreams"] if w["id"] == "ws-fixes"]
        _, warnings = validate_graph.check(bad)
        self.assertTrue(any("building-only" in w for w in warnings))

    def test_report_schema(self):
        errors, _ = check_report.check(r(), g())
        self.assertEqual(errors, [], errors)


class Selection(unittest.TestCase):
    def test_counts_do_not_decide(self):
        gr = g()
        # pile on artefacts and events for the low-signal workstream
        gr["workstreams"][1]["artefacts"] += [{"type": "mr", "label": f"MR {i}", "inspected": False, "source": "linear"} for i in range(40)]
        gr["workstreams"][1]["events"] += [{"when": "2026-03-03", "what": f"event {i}", "source": "slack"} for i in range(40)]
        rows = select_stories.rank(gr)
        self.assertEqual(rows[0]["id"], "ws-migration")

    def test_weak_evidence_is_discounted(self):
        gr = g()
        gr["workstreams"][1]["signals"].update(significance=5, outcome=5, unusual=5, humour=5, evidence_strength=1)
        rows = {x["id"]: x["score"] for x in select_stories.rank(gr)}
        gr["workstreams"][1]["signals"]["evidence_strength"] = 5
        rows2 = {x["id"]: x["score"] for x in select_stories.rank(gr)}
        self.assertLess(rows["ws-fixes"], rows2["ws-fixes"] * 0.7)

    def test_sensitive_story_not_suggested_as_main(self):
        gr = g()
        gr["workstreams"][2]["signals"].update(significance=5, outcome=5, evidence_strength=5, unusual=5, contribution_to_others=5, humour=5, future_relevance=5)
        s = select_stories.suggest(select_stories.rank(gr))
        self.assertNotEqual(s["suggested_main"], "ws-coaching")


class Lint(unittest.TestCase):
    def errs(self, mutate):
        rep = r()
        mutate(rep)
        e, _ = check_report.check(rep, g())
        return e

    def test_good_report_clean(self):
        e, w = check_report.check(r(), g())
        self.assertEqual(e, [])

    def test_em_dash(self):
        self.assertTrue(any("em dash" in x for x in self.errs(lambda rep: rep["sections"][0]["paragraphs"].__setitem__(0, rep["sections"][0]["paragraphs"][0] + " Fine — really."))))

    def test_banned_phrase(self):
        self.assertTrue(any("banned" in x for x in self.errs(lambda rep: rep["sections"][1]["paragraphs"].append("Honestly, a remarkable week."))))

    def test_third_person_chef(self):
        def m(rep):
            rep["sections"][0]["paragraphs"].append("Chef thinks this was fine. Chef noticed the plan.")
        self.assertTrue(any("third person" in x for x in self.errs(m)))

    def test_not_x_but_y(self):
        self.assertTrue(any("not X but Y" in x for x in self.errs(lambda rep: rep["sections"][1]["paragraphs"].append("It was not a plan, but a manifesto."))))

    def test_footnote_leak(self):
        self.assertTrue(any("citation" in x for x in self.errs(lambda rep: rep["sections"][1]["paragraphs"].append("Confidence: high. Source: Slack."))))

    def test_kitchen_pileup(self):
        self.assertTrue(any("kitchen" in x for x in self.errs(lambda rep: rep["sections"][1]["paragraphs"].append("You cooked in the kitchen, the oven was hot and the sauce simmered."))))

    def test_length(self):
        def m(rep):
            for s in rep["sections"]:
                s["paragraphs"] = ["Short."] if s["paragraphs"] else []
        self.assertTrue(any("words" in x for x in self.errs(m)))

    def test_unknown_chef_state(self):
        self.assertTrue(any("Chef state" in x for x in self.errs(lambda rep: rep["chef"].__setitem__("state", "chef-pixel-owl"))))

    def test_shareable_section_with_ineligible_workstream(self):
        def m(rep):
            rep["sections"][2]["share"]["include"] = True
        self.assertTrue(any("not share_eligible" in x for x in self.errs(m)))

    def test_share_text_with_redaction_term(self):
        self.assertTrue(any("redaction term" in x for x in self.errs(lambda rep: rep["sections"][1]["share"].__setitem__("text", "Priya Shah built a calendar."))))


class Share(unittest.TestCase):
    def test_allowlist_only(self):
        payload, skipped = build_share.build(g(), r())
        self.assertEqual(set(payload), {"chef", "tagline", "week_label", "verdict", "sections"})
        self.assertEqual(set(payload["chef"]), {"state"})
        for s in payload["sections"]:
            self.assertEqual(set(s), {"title", "text"})
        # the section tied to a category-only workstream is dropped
        self.assertTrue(any(k == "side" for k, _ in skipped))
        self.assertNotIn("Sides", [s["title"] for s in payload["sections"]])

    def test_names_and_terms_replaced(self):
        rep = r()
        rep["sections"][1]["share"]["text"] = "Priya Shah rebuilt the Acme Ledger plan for Project Heron."
        payload, _ = build_share.build(g(), rep)
        blob = json.dumps(payload)
        for t in ("Priya", "Shah", "Acme Ledger", "Project Heron"):
            self.assertNotIn(t, blob)
        self.assertIn("platform lead", blob)

    def test_link_blocks_build(self):
        rep = r()
        rep["sections"][1]["share"]["text"] = "See https://example.com/plan for more."
        with self.assertRaises(ValueError):
            build_share.build(g(), rep)

    def test_email_and_mention_block_build(self):
        for bad in ("Ask sam@example.com", "Ping @sam about it"):
            rep = r()
            rep["sections"][1]["share"]["text"] = bad
            with self.assertRaises(ValueError):
                build_share.build(g(), rep)

    def test_options_drop_and_edit(self):
        payload, _ = build_share.build(g(), r(), {"drop": ["burnt"], "edits": {"main": "A plan, quickly agreed."}})
        titles = [s["title"] for s in payload["sections"]]
        self.assertNotIn("Burnt bits", titles)
        self.assertEqual(next(s["text"] for s in payload["sections"] if s["title"] == "Main"), "A plan, quickly agreed.")

    def test_share_html_has_no_private_material(self):
        payload, _ = build_share.build(g(), r())
        page = build_share.page(payload)
        for banned in ("ws-migration", "Priya", "Acme Ledger", "example.com", "How Chef knows", "evidence", "coverage", "rr-data", "<script"):
            self.assertNotIn(banned, page)
        self.assertIn("<svg", page)  # the logo is there

    def test_cli_writes_files(self):
        with tempfile.TemporaryDirectory() as d:
            res = subprocess.run([sys.executable, str(SKILL / "scripts" / "build_share.py"), "--graph", str(FIX / "graph.json"),
                                  "--report", str(FIX / "report.json"), "--out", d], capture_output=True, text=True)
            self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
            for f in ("share.json", "share.txt", "share.html"):
                self.assertTrue((pathlib.Path(d) / f).exists())
            self.assertNotIn("Priya", (pathlib.Path(d) / "share.json").read_text())


class Scope(unittest.TestCase):
    def test_linkedin_out_of_weekly_roast(self):
        sk = (SKILL / "SKILL.md").read_text()
        self.assertIn("Roast My LinkedIn", sk)
        self.assertNotIn("linkedin=", sk)
        self.assertFalse((SKILL / "scripts" / "linkedin_ingest.py").exists())
        ids = [s["id"] for s in json.loads((SKILL / "templates" / "sources.json").read_text())["sources"]]
        self.assertNotIn("linkedin", ids)


class OpenLoops(unittest.TestCase):
    end = dt.date(2026, 10, 31)
    base = {"channel_kind": "public", "thread": True, "direct_question": False, "user_replied": False, "user_reacted": False, "sensitive": False}

    def c(self, **kw):
        d = dict(self.base); d.update(kw); return d

    def test_counts_and_bands(self):
        cands = [self.c(ts="2026-10-30T10:00:00Z", direct_question=True),
                 self.c(ts="2026-10-27T10:00:00Z"),
                 self.c(ts="2026-10-25T10:00:00Z"),
                 self.c(ts="2026-10-29T10:00:00Z", user_replied=True),
                 self.c(ts="2026-10-29T10:00:00Z", user_reacted=True),
                 self.c(ts="2026-10-29T10:00:00Z", channel_kind="dm"),
                 self.c(ts="2026-10-29T10:00:00Z", sensitive=True)]
        s = open_loops.summarise(cands, self.end)
        self.assertEqual((s["tagged_total"], s["considered"], s["left_out_private_or_sensitive"]), (7, 5, 2))
        self.assertEqual((s["no_visible_reply"], s["direct_questions_among_them"], s["reacted_but_not_replied"]), (3, 1, 1))
        self.assertEqual(s["age_bands"], {"under_2_days": 1, "2_to_4_days": 1, "5_days_or_more": 1})
        self.assertTrue(s["caveats"])

    def test_rejects_names_and_text(self):
        with self.assertRaises(ValueError):
            open_loops.summarise([self.c(ts="2026-10-30T10:00:00Z", requester="Priya Shah")], self.end)
        with self.assertRaises(ValueError):
            open_loops.summarise([self.c(ts="2026-10-30T10:00:00Z", text="Can you review this?")], self.end)

    def test_graph_rejects_named_open_loops(self):
        gr = g()
        gr["open_loops"] = open_loops.summarise([self.c(ts="2026-10-30T10:00:00Z")], self.end)
        errs, _ = validate_graph.check(gr)
        self.assertFalse(any("open_loops" in e for e in errs))
        gr["open_loops"]["caveats"].append("Asked by Priya Shah")
        errs, _ = validate_graph.check(gr)
        self.assertTrue(any("names-free" in e for e in errs))

    def test_no_network_code(self):
        src = (SKILL / "scripts" / "open_loops.py").read_text()
        for bad in ("import requests", "urllib.request", "http.client", "socket"):
            self.assertNotIn(bad, src)


class Render(unittest.TestCase):
    def setUp(self):
        self.page = render_report.render(g(), r())

    def test_structure(self):
        for needle in ('id="open-share"', 'id="open-cov"', "How Chef knows", 'class="how"', "Sources and coverage",
                       "Your week, served with a side of sarcasm.", 'id="rr-data"'):
            self.assertIn(needle, self.page)
        self.assertNotIn("Not on the menu", self.page)
        self.assertEqual(self.page.count("<details"), sum(1 for s in r()["sections"] if s.get("disclosure")))

    def test_link_only_items_marked(self):
        self.assertIn("link only, not opened", self.page)

    def test_coverage_modes_labelled(self):
        for label in ("Read directly", "Found through links only", "Not selected"):
            self.assertIn(label, self.page)

    def test_script_syntax(self):
        scripts = re.findall(r"<script>(.*?)</script>", self.page, flags=re.S)
        self.assertTrue(scripts)
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
            f.write(scripts[-1])
        res = subprocess.run(["node", "--check", f.name], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, res.stderr)

    def test_data_json_parses_and_hides_nothing_extra(self):
        raw = re.search(r'id="rr-data">(.*?)</script>', self.page, flags=re.S).group(1).replace("<\\/", "</")
        data = json.loads(raw)
        self.assertEqual(set(data), {"tagline", "week_label", "share", "redactions"})
        # evidence urls are not in the share data
        self.assertNotIn("example.com/s/1", json.dumps(data["share"]))

    def test_redaction_js_matches_python(self):
        js = (SKILL / "scripts" / "share_ui.js").read_text()
        text = "Priya Shah told Tom about Acme Ledger and Project Heron."
        py = build_share.apply_redactions(text, GRAPH["redactions"], True, True)
        code = (f"const m={{exports:{{}}}};(function(module){{{js}}})(m);"
                f"console.log(m.exports.applyRedactions({json.dumps(text)},{json.dumps(GRAPH['redactions'])},true,true));")
        res = subprocess.run(["node", "-e", code], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertEqual(res.stdout.strip(), py)
        self.assertNotIn("Priya", py)

    def test_dom_behaviour(self):
        """Share flow, panels and disclosures in a DOM (skipped if jsdom is not installed)."""
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
            f.write(self.page)
        res = subprocess.run(["node", str(HERE / "dom_test.js"), f.name], capture_output=True, text=True)
        if res.returncode == 77:
            self.skipTest("jsdom not installed")
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)

    def test_unknown_chef_state_falls_back(self):
        rep = r()
        rep["chef"]["state"] = "chef-nonexistent"
        self.assertIn("<svg", render_report.render(g(), rep))


class Skill(unittest.TestCase):
    def test_five_stages_documented(self):
        for f in ("A-discovery", "B-reconstruction", "C-interpretation", "D-editorial", "E-presentation"):
            self.assertTrue((SKILL / "stages" / f"{f}.md").exists(), f)
        s = (SKILL / "SKILL.md").read_text()
        for name in ("Discovery", "Reconstruction", "Interpretation", "Editorial", "Presentation", "Chef", "sundayroast.me"):
            self.assertIn(name, s)
        self.assertNotIn("—", s)

    def test_voice_rules_in_chef_guide(self):
        c = (SKILL / "templates" / "chef.md").read_text()
        for needle in ("Em dashes", "third person", "wide-eyed chicken"):
            self.assertIn(needle, c)


if __name__ == "__main__":
    unittest.main(verbosity=1)
