#!/usr/bin/env python3
"""Summarise opt-in "open loops": times someone tagged or asked the user for something and no
reply from the user is visible. Names-free and text-free by design.

Input (JSON list) is gathered by Claude from Slack mention searches and thread reads. One object per tag:
  {"ts": "2026-10-28T14:02:00Z", "channel_kind": "public|private|dm|group",
   "thread": true, "direct_question": true, "user_replied": false, "user_reacted": true, "sensitive": false}
Nothing else is accepted: no ids, no names, no message text.

Usage: python3 open_loops.py --input candidates.json --end 2026-10-31
Output: a summary for the evidence graph's `open_loops` field.

What it deliberately does not do: see unread counts or bookmarks (no tool exposes them), judge anyone,
or count private, group or sensitive conversations. Those are only counted as "left out".
"""
import argparse
import datetime as dt
import json
import sys

ALLOWED = {"ts", "channel_kind", "thread", "direct_question", "user_replied", "user_reacted", "sensitive"}
BANDS = (("under_2_days", 0, 2), ("2_to_4_days", 2, 5), ("5_days_or_more", 5, 10_000))


def parse_ts(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00")).date()


def summarise(cands, end):
    for c in cands:
        extra = set(c) - ALLOWED
        if extra:
            raise ValueError(f"unexpected fields {sorted(extra)}: only the allowed fields may be passed, never names or text")
    considered = [c for c in cands if c.get("channel_kind") == "public" and not c.get("sensitive")]
    left_out = len(cands) - len(considered)
    no_reply = [c for c in considered if not c.get("user_replied") and not c.get("user_reacted")]
    reacted_only = [c for c in considered if not c.get("user_replied") and c.get("user_reacted")]
    questions = [c for c in no_reply if c.get("direct_question")]
    bands = {name: 0 for name, _, _ in BANDS}
    for c in no_reply:
        age = (end - parse_ts(c["ts"])).days
        for name, lo, hi in BANDS:
            if lo <= age < hi:
                bands[name] += 1
                break
    return {
        "enabled": True,
        "tagged_total": len(cands),
        "considered": len(considered),
        "left_out_private_or_sensitive": left_out,
        "no_visible_reply": len(no_reply),
        "direct_questions_among_them": len(questions),
        "reacted_but_not_replied": len(reacted_only),
        "age_bands": bands,
        "caveats": [
            "Counts only tags where no reply from you is visible in the thread. A reply elsewhere, a call or a chat will not show.",
            "Private, group and sensitive conversations are left out, not counted.",
            "Unread counts and bookmarks are not visible to the tools.",
        ],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--end", required=True)
    a = ap.parse_args()
    cands = json.load(open(a.input))
    print(json.dumps(summarise(cands, dt.date.fromisoformat(a.end)), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
