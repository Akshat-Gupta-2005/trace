"""Grade trace eval runs.

Checks the mechanically verifiable assertions and writes grading.json per run.
Assertions that need human or LLM judgement are emitted with passed=None and
evidence explaining what to look at.

Usage:  python scripts/grade.py iteration-1
"""

import difflib
import io
import json
import re
import sys
from pathlib import Path

WS = Path(__file__).resolve().parent.parent
FIXTURES = WS / "fixtures"

TOKENS = [
    "PROJECT_NAME", "PROJECT_GOAL", "AUDIENCE", "STACK", "DOC_LOCATION",
    "STAR_LABEL", "RUNTIME_SHAPE", "CONTRACT_KIND", "DOC_SET",
]

MANUAL = object()


def read(p):
    try:
        return io.open(p, encoding="utf-8").read()
    except (OSError, UnicodeDecodeError):
        return ""


def find_repo(run_dir):
    """The agent worked in outputs/ledgerkit."""
    cand = run_dir / "outputs" / "ledgerkit"
    return cand if cand.exists() else run_dir / "outputs"


def md_files(repo):
    return [p for p in repo.rglob("*.md") if ".git" not in p.parts]


def named(repo, needle):
    """Content of the first .md whose name contains needle."""
    for p in sorted(md_files(repo)):
        if needle in p.name:
            return read(p), p
    return "", None


def section(text, start_pat, stop_pat=r"\n#{1,3} "):
    m = re.search(start_pat, text, re.I)
    if not m:
        return ""
    rest = text[m.end():]
    stop = re.search(stop_pat, rest)
    return rest[: stop.start()] if stop else rest


def p_block(text, n):
    m = re.search(rf"^#{{1,4}}\s*P{n}\b.*$", text, re.M)
    if not m:
        return ""
    rest = text[m.end():]
    stop = re.search(r"^#{1,4}\s", rest, re.M)
    body = rest[: stop.start()] if stop else rest
    # Keep the heading line: the date and category tag live on it.
    return m.group(0) + "\n" + body


def tree_matches_fixture(repo, fixture_name, subdirs=("src", "tests")):
    base = FIXTURES / fixture_name
    diffs = []
    for sub in subdirs:
        for src in (base / sub).rglob("*"):
            if not src.is_file():
                continue
            rel = src.relative_to(base)
            dst = repo / rel
            if not dst.exists():
                diffs.append(f"{rel} missing")
            elif read(src) != read(dst):
                diffs.append(f"{rel} modified")
    return (not diffs), "; ".join(diffs) or "src/ and tests/ byte-identical to fixture"


# ---------------------------------------------------------------- eval 0

def grade_cold_setup(repo):
    out = {}
    cfg_text, cfg_path = "", None
    for c in ["docs/0_config.md", "0_config.md", "docs/00_config.md"]:
        if (repo / c).exists():
            cfg_text, cfg_path = read(repo / c), c
            break
    claude_md = read(repo / "CLAUDE.md")
    if not cfg_text and re.search(r"project docs config", claude_md, re.I):
        cfg_text, cfg_path = claude_md, "CLAUDE.md"

    out["config-file-exists"] = (bool(cfg_text), f"found at {cfg_path}" if cfg_text
                                else "no 0_config.md and no config block in CLAUDE.md")

    missing = [t for t in TOKENS if t not in cfg_text]
    out["config-has-nine-tokens"] = (not missing,
                                     "all nine present" if not missing else f"missing: {missing}")

    ds = section(cfg_text, r"DOC_SET\s*=", r"\n\S")
    heavy = [x for x in ["7_uml", "8_architecture"] if x in ds]
    out["doc-set-is-scaled-down"] = (bool(ds) and not heavy,
                                     f"DOC_SET = {ds.strip()[:120]!r}" if ds else "no DOC_SET line")

    feats, fp = named(repo, "features")
    decs, dp = named(repo, "decisions")
    ok = bool(feats) and bool(decs) and (fp.name.startswith("3_") if fp else False) \
        and (dp.name.startswith("4_") if dp else False)
    out["numbered-files-created"] = (ok, f"features={fp}, decisions={dp}")

    srcs = ["cli.py", "parse.py", "match.py", "report.py"]
    absent = [s for s in srcs if s not in feats]
    out["code-map-covers-real-files"] = (not absent,
                                         "all four named" if not absent else f"not named: {absent}")

    allmd = " ".join(read(p) for p in md_files(repo))
    marks = [m for m in ["Decimal", "WINDOW", "UnknownFormat", "utf-8-sig",
                         "3-day", "3 day", "dateutil", "SKIP", "click"] if m in allmd]
    out["content-drawn-from-real-code"] = (len(marks) >= 3, f"real identifiers found: {marks}")

    leftover = sorted({t for p in md_files(repo) for t in re.findall(r"\{\{[A-Z_]+\}\}", read(p))})
    out["no-unsubstituted-tokens"] = (not leftover, f"leftover: {leftover}" if leftover else "none")

    wired = bool(re.search(r"session protocol|trace skill", claude_md, re.I))
    out["session-trigger-wired"] = (wired, "CLAUDE.md points at the session protocol" if wired
                                    else f"CLAUDE.md {'absent' if not claude_md else 'has no pointer'}")

    out["source-untouched"] = tree_matches_fixture(repo, "ledgerkit")
    out["assumptions-stated"] = (MANUAL, "read the run's final message")
    return out


# ---------------------------------------------------------------- eval 1

def grade_log_a_bug(repo):
    out = {}
    decs, dp = named(repo, "decisions")
    base = read(FIXTURES / "ledgerkit-with-docs" / "docs" / "4_decisions.md")

    b2 = p_block(decs, 2)
    out["entry-appended-to-decisions"] = (bool(b2), f"P2 block {'found' if b2 else 'absent'} in {dp}")
    p1_count = len(re.findall(r"^#{1,4}\s*P1\b", decs, re.M))
    out["numbered-p2"] = (bool(b2) and p1_count == 1,
                          f"P2 present={bool(b2)}, P1 headings={p1_count}")

    fields = ["Symptom", "Root cause", "Fix", "Verified", "Generalises"]
    miss = [f for f in fields if f.lower() not in b2.lower()]
    out["has-five-fields"] = (not miss, "all five" if not miss else f"missing: {miss}")

    cats = ["latent", "design trap", "conceptual", "assumption", "caught by tests", "tooling"]
    has_cat = any(c in b2.lower() for c in cats)
    out["dated-and-categorised"] = ("2026-09-19" in b2 and has_cat,
                                    f"date={'2026-09-19' in b2}, category={has_cat}")

    silent = [w for w in ["silent", "no error", "no warning", "did not exist",
                          "didn't exist", "quietly"] if w in b2.lower()]
    out["captures-silent-failure"] = (bool(silent), f"silence cues: {silent}")

    fixsec = section(b2, r"\*\*Fix:?\*\*", r"\*\*")
    real = [w for w in ["match.py", "min(", "nearest", "candidates", "date distance"]
            if w in fixsec]
    out["fix-names-real-code"] = (bool(real), f"cues in Fix: {real}")

    p1_old, p1_new = p_block(base, 1), p_block(decs, 1)
    rows_old = re.findall(r"^\| 2026-07.*$", base, re.M)
    rows_new = re.findall(r"^\| 2026-07.*$", decs, re.M)
    same = p1_old.strip() == p1_new.strip() and rows_old == rows_new
    out["append-only-respected"] = (same, "P1 and the 2026-07 rows unchanged" if same
                                    else "existing entries were edited")

    tests_ok, tests_ev = tree_matches_fixture(repo, "ledgerkit-with-docs", subdirs=("tests",))
    added_test = not tests_ok
    ver = section(b2, r"\*\*Verified:?\*\*", r"\*\*")
    hedged = any(w in ver.lower() for w in ["not yet", "no test", "not verified",
                                            "unverified", "pending", "should be",
                                            "todo", "no regression test"])
    out["verified-is-honest"] = (MANUAL,
                                 f"regression test added={added_test} ({tests_ev}); "
                                 f"Verified text hedges={hedged}; text={ver.strip()[:200]!r}")
    out["generalises-is-transferable"] = (MANUAL, section(b2, r"\*\*Generalises[^*]*\*\*", r"\n\n").strip()[:200])
    return out


# ---------------------------------------------------------------- eval 2

def grade_end_of_session(repo):
    out = {}
    feats, fp = named(repo, "features")
    decs, dp = named(repo, "decisions")
    base_d = read(FIXTURES / "ledgerkit-with-docs" / "docs" / "4_decisions.md")

    lu = re.search(r"\*\*Last updated:?\*\*(.*)", feats)
    lu_txt = lu.group(1) if lu else ""
    out["last-updated-rewritten"] = ("2026-09-19" in lu_txt,
                                     f"Last updated line: {lu_txt.strip()[:160]!r}")
    earlier = re.search(r"\*\*Earlier", feats, re.I)
    out["previous-line-demoted"] = (bool(earlier) and "2026-07-28" in feats,
                                    f"Earlier line={bool(earlier)}, old date retained={'2026-07-28' in feats}")

    nyb = section(feats, r"\*\*Not yet built\*\*|##+ *Not yet built", r"\n#{2,3} ")
    out["code-map-gains-report"] = ("report.py" in feats, "report.py named in the file")
    out["stale-json-claim-removed"] = ("JSON output for machine consumers" not in nyb,
                                       f"'Not yet built' now: {nyb.strip()[:220]!r}")
    out["stale-rendering-claim-removed"] = ("raw tuples" not in nyb, "'raw tuples' claim gone" if
                                            "raw tuples" not in nyb else "still claims raw tuples")
    out["true-not-built-item-retained"] = ("window" in nyb.lower(),
                                           "--window still listed" if "window" in nyb.lower()
                                           else "audit deleted a still-true item")

    row = next((l for l in feats.splitlines() if "Two CSV layouts" in l), "")
    out["building-status-corrected"] = ("Building" not in row and bool(row),
                                        f"row: {row.strip()[:160]!r}")

    out["test-count-corrected"] = (bool(re.search(r"\b5\b[^\n]{0,20}(tests?|passed)", feats, re.I))
                                   and "3 tests passing" not in feats,
                                   f"'3 tests passing' present={'3 tests passing' in feats}")
    out["test-count-actually-observed"] = (MANUAL, "check the run transcript for a real pytest invocation")

    od = section(decs, r"##+ *Open decisions", r"\n## ")
    # "Deleted" means gone from the file, not relocated to a "Resolved" section -
    # the whole point of graduating is that the record lives in ONE place.
    od1_heading = re.search(r"^#{1,4}\s*OD1\b.*$", decs, re.M)
    out["od1-graduated"] = (od1_heading is None,
                            "no OD1 heading anywhere in the file"
                            if od1_heading is None
                            else f"OD1 still present as: {od1_heading.group(0)[:120]!r}")
    log = section(decs, r"##+ *Decisions log", r"\n##+ ")
    out["od1-decision-row-added"] = ("OD1" in log, "decisions log references OD1" if "OD1" in log
                                     else "no row references OD1")

    openitems = section(feats, r"##+ *Open items", r"\n## ")
    out["open-item-removed"] = ("output format story" not in openitems,
                                f"open items: {openitems.strip()[:200]!r}")

    p1_same = p_block(base_d, 1).strip() == p_block(decs, 1).strip()
    rows_old = re.findall(r"^\| 2026-07.*$", base_d, re.M)
    rows_new = re.findall(r"^\| 2026-07.*$", decs, re.M)
    out["append-only-respected"] = (p1_same and rows_old == rows_new,
                                    "P1 and original rows unchanged" if p1_same and rows_old == rows_new
                                    else "existing entries were edited")
    return out


GRADERS = {
    "eval-0-cold-setup": grade_cold_setup,
    "eval-1-log-a-bug": grade_log_a_bug,
    "eval-2-end-of-session": grade_end_of_session,
}


def main(iteration):
    it = WS / iteration
    summary = {}
    for eval_dir in sorted(it.iterdir()):
        if not eval_dir.is_dir() or eval_dir.name not in GRADERS:
            continue
        meta = json.loads(read(eval_dir / "eval_metadata.json"))
        texts = {a["id"]: a["text"] for a in meta["assertions"]}
        for arm in ("with_skill", "without_skill"):
            run = eval_dir / arm
            if not run.exists():
                continue
            repo = find_repo(run)
            results = GRADERS[eval_dir.name](repo)
            exps = []
            for aid, text in texts.items():
                passed, ev = results.get(aid, (MANUAL, "not checked"))
                exps.append({
                    "id": aid,
                    "text": text,
                    "passed": None if passed is MANUAL else bool(passed),
                    "evidence": ev,
                })
            auto = [e for e in exps if e["passed"] is not None]
            got = sum(1 for e in auto if e["passed"])
            payload = {
                "eval_name": eval_dir.name,
                "configuration": arm,
                "expectations": exps,
                "auto_checked": len(auto),
                "auto_passed": got,
                "pass_rate": round(got / len(auto), 3) if auto else None,
            }
            io.open(run / "grading.json", "w", encoding="utf-8").write(
                json.dumps(payload, indent=2))
            summary.setdefault(eval_dir.name, {})[arm] = f"{got}/{len(auto)}"
            print(f"{eval_dir.name:24} {arm:15} {got}/{len(auto)} auto-checked assertions")
    print()
    for name, arms in summary.items():
        print(name, arms)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "iteration-1")
