# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This repo produces a **Claude Code skill**, not an application. The deliverable is
Markdown that another Claude instance reads at runtime. `workspace/` exists only
to test that Markdown; nothing in it ships to users.

Two halves, with different rules:

- `v2/` — the current skill. This is the product. Prose changes here change behaviour.
  `v1/` is the previous version, kept for rollback and comparison; leave it alone unless
  deliberately back-porting.
- `workspace/` — the test harness. Fixtures, a grader, and run outputs.

`_docs-generator-v2.md` is the 750-line monolithic prompt the skill was converted
from. It is kept as provenance and is **not** loaded by anything. Do not edit it to
reflect changes made to the skill; it is a historical record.

## Commands

```bash
# Grade the eval runs (works from any cwd - paths resolve from __file__)
python workspace/scripts/grade.py iteration-1

# Sanity-check the grader against untouched fixtures.
# Expect roughly 2/9, 1/7, 2/12 - see "Control runs" below.
python workspace/scripts/grade.py iteration-0-control

# Run the fixture app's own tests (needs click, python-dateutil, pytest)
cd workspace/fixtures/ledgerkit && PYTHONPATH=src pytest -q   # -> 5 passed
```

There is no build, lint or install step. Python 3.11 is what the fixtures and grader
are developed against.

## The skill's architecture

`v2/SKILL.md` loads **in full** every time the skill triggers; the files under
`references/` load only when `SKILL.md` tells the reader to open them. That split is
the entire design, and it imposes a hard constraint:

**Keep `SKILL.md` under ~500 lines.** `v2` is currently 344. When adding material, ask
whether it is needed on every invocation. Templates, worked examples and
diagram-specific guidance belong in `references/`; the session protocol, trigger
matrix and verification rules belong in `SKILL.md` because they apply every time.

| File | Lines | Loads |
|---|---|---|
| `v2/SKILL.md` | 344 | every trigger |
| `v2/references/file-templates.md` | 487 | before creating/restructuring files 1-6 |
| `v2/references/diagrams.md` | 154 | before touching `7_uml/` or the HTML page |
| `v2/references/examples.md` | 162 | when writing a `P<n>`, `OD<n>` or talking point |

### Which version to edit

**Changes go in `v2/`.** `v1/` is frozen at the original conversion and exists so the
anchor convention can be declined or compared against; editing it defeats the point of
keeping it. If a change belongs in both, say so explicitly rather than assuming.

`v2` adds explicit `<a id="...">` anchors (`p<n>`, `w<n>`, `s<n>-<n>`, `f-<slug>`) so
cross-document ID references are clickable. `OD<n>` entries deliberately get no anchor —
they are deleted on graduation, so any link to one is a broken link with a scheduled
date. The eval numbers below are from `v1`; `v2` has not been re-measured.

### Invariants that break things silently

- **The skill's `name:` frontmatter, its directory name, and the pointer line it
  writes into user projects must all agree.** They are currently all `trace`. A rename
  touches: the frontmatter, both directory names, the `Before starting work, follow the
  trace skill's session protocol` line inside `SKILL.md`, `evals/evals.json`'s
  `skill_name`, the grader's docstring and its `session-trigger-wired` regex, and the
  README's install commands. Missing one leaves a skill that installs but does not fire.
- **The grader's `session-trigger-wired` check matches `session protocol|trace skill`,
  not the bare word `trace`.** `trace` is too common a word to match a user's
  `CLAUDE.md` reliably. If the skill is renamed to something distinctive, this can be
  simplified; if renamed to something generic, keep the two-word form.
- **No `{{TOKEN}}` may survive into generated output.** The skill's templates use
  `{{PROJECT_NAME}}`-style placeholders resolved from the *user's* project config, not
  from anything in this repo. `no-unsubstituted-tokens` asserts this.

## The eval harness

Three scenarios, each run twice — once by an agent given the skill (`with_skill/`) and
once by an agent given nothing (`without_skill/`). Both arms work on their own copy of
a fixture repo so they cannot collide.

```
workspace/
  fixtures/
    ledgerkit/            bare repo, no docs      -> eval-0
    ledgerkit-with-docs/  docs with planted rot   -> eval-1, eval-2
  scripts/grade.py        32 assertions
  iteration-1/            run outputs (gitignored)
    eval-<n>-<name>/
      eval_metadata.json  prompt + assertion texts
      with_skill/outputs/ledgerkit/
      without_skill/outputs/ledgerkit/
      {with,without}_skill/grading.json, timing.json
```

`grade.py` dispatches on directory name via the `GRADERS` dict, so **the three eval
directory names are load-bearing**: `eval-0-cold-setup`, `eval-1-log-a-bug`,
`eval-2-end-of-session`. Renaming a directory silently skips its grading.

Assertions that need human judgement return the `MANUAL` sentinel and are written to
`grading.json` with `passed: null`. They are excluded from the pass-rate denominator —
do not "fix" them into automated checks unless the check is genuinely objective.

### The fixture rot is deliberate

`workspace/fixtures/ledgerkit-with-docs/docs/` contains statements that are **false against its
own code, on purpose**. `3_features.md` claims JSON output and report rendering are
"Not yet built" while `report.py` implements both; it says 3 tests where there are 5;
`Two CSV layouts` sits at `Building` though it is complete; and `OD1` asks a question
the code already answers.

Those six defects are what the evals measure. **Do not correct them.** If you find
yourself tidying the fixture docs, you are deleting the test.

### Control runs

Before trusting any result, `iteration-0-control` grades *untouched* fixture copies.
It should score near-zero (2/9, 1/7, 2/12), and the only assertions that pass should be
the "do no harm" ones — `source-untouched`, `append-only-respected`,
`true-not-built-item-retained`, `no-unsubstituted-tokens`. If the control score rises
after you edit an assertion, that assertion has become vacuous.

Rebuild the control with:

```bash
cd workspace && rm -rf iteration-0-control
for spec in "eval-0-cold-setup:ledgerkit" "eval-1-log-a-bug:ledgerkit-with-docs" \
            "eval-2-end-of-session:ledgerkit-with-docs"; do
  name="${spec%%:*}"; fix="${spec##*:}"
  mkdir -p "iteration-0-control/$name/with_skill/outputs"
  cp -r "fixtures/$fix" "iteration-0-control/$name/with_skill/outputs/ledgerkit"
  cp "iteration-1/$name/eval_metadata.json" "iteration-0-control/$name/"
done
```

### Known weaknesses in the current evals

Recorded so they are not rediscovered:

- **Evals 1 and 2 are contaminated.** They hand the baseline a `4_decisions.md` already
  written in the skill's format, so it copies the shape. Format assertions
  (`has-five-fields`, `numbered-p2`, `dated-and-categorised`) therefore measure nothing
  in those two cases. Only eval-0 is a clean comparison. A future iteration should give
  the fixture docs a *different* house style.
- **`building-status-corrected` is unreliable.** Two with-skill runs disagreed on
  whether `Done` is legitimate without a `parse.py` test, and both readings are
  defensible under the skill's own definition of `Done`.
- **`eval-0` with-skill has no `timing.json`** — that run was killed after a 37-minute
  diagram loop, so it is excluded from cost means.

## Re-running the evals

Spawn all six agents **in the same turn** so they finish together. Each needs its own
fixture copy at `iteration-<n>/<eval>/<arm>/outputs/ledgerkit`. With-skill agents get
the path to `v2/SKILL.md` and are told to treat it as authoritative; baseline agents
get the prompt alone. Prompts live in `evals/evals.json`.

Agents cannot ask questions, so their prompts must say the user is unavailable and
assumptions should be stated in the final message.

Capture `total_tokens` and `duration_ms` from each completion notification into
`timing.json` immediately — that data arrives only once and is not persisted anywhere
else.

## Editing the skill's prose

The skill is instructions for a model, so the usual failure is a rule that sounds
reasonable and is unbounded. One shipped example: *"add diagrams for anything you will
explain to someone else"* licensed the full eight-file set plus UML for a four-module
CLI, because everything gets explained to someone. The fix was a stricter trigger plus
an explicit stopping condition on the render step.

When adding a rule, state the condition under which it **stops** applying, and prefer
explaining why it matters over an all-caps imperative.
