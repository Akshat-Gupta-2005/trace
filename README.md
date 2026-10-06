# trace

A [Claude Code](https://claude.com/claude-code) skill that keeps a project's
documentation current **as the work happens**, instead of producing it at the end.

The rule it exists to enforce: *a change is not complete until the documentation
reflects it.* Documentation written at the end of a project is fiction, because the
detail that made it worth writing is already gone.

## The idea

Most project docs die the same way: the plan gets quietly rewritten to match whatever
actually happened, so it stops being evidence of anything. This skill splits the
documentation by **how often each file changes**, and treats the fast-moving and
slow-moving parts as different artifacts:

| File | Holds | Changes |
|---|---|---|
| `1_build-plan.md` | what we intend to do | rarely |
| `2_implementation-plan.md` | the order of the work | status edited as tasks land |
| `3_features.md` | what is true right now | rewritten every session |
| `4_decisions.md` | why it ended up this way | **append-only, never edited** |
| └─ Open decisions | what we have *not* decided | the one live section |
| `5_api-contract.md` | what others may rely on | with the interface |
| `6_system-guide.md` | how the running thing works | with the runtime |
| `7_uml/` | the system in diagrams | with the architecture |
| `8_architecture.html` | master diagram + all of `7_uml/` | regenerated from `7_uml/` |

You do **not** adopt all eight. The skill scales the set to the project — a three-week
solo CLI gets `3_features.md` and `4_decisions.md` and nothing else. Adding a file
nobody maintains is worse than not having it.

The two that earn their keep at every size are the **problems log** (`P<n>` entries:
symptom, root cause, fix, how it was verified, what it generalises to) and **open
decisions** (`OD<n>`: the question, real costed options, what would settle it). Those
are the parts that cannot be reconstructed from the code six months later.

## Versions

Two versions live side by side so a change can be rolled back or compared:

| | `SKILL.md` | What it is |
|---|---|---|
| [`v1/`](v1/) | 298 lines | the original conversion — plain-text ID references |
| [`v2/`](v2/) | 344 lines | adds cross-document anchors, so IDs and paths are clickable |

**`v2` is the current version.** `v1` is kept because the anchor convention adds a line
of HTML above every problem entry, and that is a taste call somebody may want to decline.

## Install

Copy the version you want to a directory named `trace` — the directory name must match
the `name:` field in the skill's frontmatter, or it will not load.

**For all your projects:**

```bash
git clone https://github.com/<your-username>/trace.git /tmp/t \
  && cp -r /tmp/t/v2 ~/.claude/skills/trace \
  && rm -rf /tmp/t
```

**For one project** (committed with the code, so teammates get it too):

```bash
cd /path/to/your/project
mkdir -p .claude/skills
git clone https://github.com/<your-username>/trace.git /tmp/t \
  && cp -r /tmp/t/v2 .claude/skills/trace \
  && rm -rf /tmp/t
```

Restart Claude Code and run `/skills` to confirm `trace` is listed.

## Using it

### First run on a project

Say *"set up project documentation for this repo."* The skill will:

1. Look for `docs/0_config.md`, not find it, and ask you nine questions — inferring
   the stack and runtime from the repo, and genuinely asking only about the two it
   cannot guess: who reads these docs, and what a star should mark.
2. Write `docs/0_config.md`. Every template refers to those values, so no project
   detail is ever hardcoded in the skill.
3. Propose a `DOC_SET` scaled to your project. **Push back here if it proposes too
   much** — this is the decision that determines whether the docs survive.
4. Create only those files, populated from your actual code.
5. Add a pointer line to your `CLAUDE.md`.

### That `CLAUDE.md` line matters

```
Before starting work, follow the trace skill's session protocol.
```

A skill loads when a request matches its description — nothing makes it fire at the
start of a session just because that would be useful. That one line is what makes the
start-of-session check happen. Delete it and the docs drift silently.

### Day to day

| You say | What happens |
|---|---|
| *starting work* | Reads the Last-updated line, Open items and Open decisions; if any disagree with the repo, fixes the docs **first** |
| *"log this decision"* | A dated row in `4_decisions.md`, naming the rejected alternative |
| *"write up this bug"* | A numbered `P<n>`: symptom, root cause, fix, verification, lesson |
| *"I can't decide X"* | An `OD<n>` with real costed options and what would settle it |
| *"wrap up the session"* | The full checklist — Last updated, code map audit, status check, open-decision graduation, verification |

## Cross-links (v2)

The docs reference each other constantly — a talking point cites a problem ID, a feature
row names the file it lives in. In `v2` those references are clickable, via explicit
anchors rather than the IDs a renderer derives from heading text. A derived anchor breaks
the moment someone rewords a title, and these headings are exactly where the format puts
titles, dates and categories.

```markdown
<a id="p7"></a>
### P7 — Two workers processed the same upload *(2026-08-14, conceptual)*
```

Four anchor families:

| Anchor | On | Linked as |
|---|---|---|
| `p<n>` | each problem entry | `[P7](4_decisions.md#p7)` |
| `w<n>` | each work unit | `[W3](2_implementation-plan.md#w3)` |
| `s<n>-<n>` | each numbered section | `[§3.5](3_features.md#s3-5)` |
| `f-<slug>` | each feature row | `[JSON renderer](3_features.md#f-json-renderer)` |

Features use a slug rather than a number because `3_features.md` is rewritten every
session and rows come and go — a numeric sequence there would be mostly gaps within a
month, and the name is what identifies a feature anyway.

**`OD<n>` entries are deliberately never anchored or linked.** An open decision is
deleted when it graduates, so every link to one is a broken link with a scheduled date.
Problem IDs are safe precisely because they are append-only and never renumbered.

Two of these links do more than save a click, because a broken link is *visible* where a
wrong sentence is not:

- **"Lives in" is a link, not a path.** A file that moved shows up as a dead link
  instead of a plausible-looking wrong path.
- **`Verified:` links the test that proves it.** The claim and its evidence end up one
  click apart — the difference between a doc asserting something and a doc showing it.

## Repository layout

```
v1/
  SKILL.md                     298 lines - loads on every trigger
  references/                  templates, diagrams, worked examples
v2/                            current
  SKILL.md                     344 lines
  references/
    file-templates.md          files 1-6, section by section
    diagrams.md                7_uml/ and 8_architecture.html
    examples.md                a worked P<n>, OD<n> and talking point,
                               each shown beside its thin version
evals/evals.json               3 test cases, 32 assertions (shared by both versions)
workspace/
  fixtures/                    a fake CSV-reconciliation CLI used for testing,
                               in bare and stale-docs variants
  scripts/grade.py             the grader
_docs-generator-v2.md          the original monolithic prompt this came from
CLAUDE.md                      guidance for working on this repo
```

`SKILL.md` is deliberately kept under the ~500-line budget, because it loads in full
every time the skill fires. The reference files load only when the skill says to read
them.

## Does it actually work?

Tested with three cases, each run twice — once with the skill, once without — against
a fixture repo with six specific staleness bugs planted in its docs.

| | with skill | baseline |
|---|---|---|
| cold setup (no docs) | **8/9** | 3/9 |
| log a bug mid-session | **7/7** | 6/7 |
| end-of-session update | **12/12** | 10/12 |

**Read that honestly.** Two of the three cases hand the baseline a decisions file
*already written in the skill's format*, so it copies the shape and the format
assertions measure nothing. Only the cold-setup case is a clean comparison, and that
is where the gap is real.

The differences that are not format-copying:

- With the skill, the mid-session run did the start-of-session check first, found the
  docs disagreed with the repo, and fixed that drift **before** writing up the bug it
  was asked about. The baseline wrote an excellent entry and left the staleness.
- The baseline filed an answered open decision into a "Resolved" section instead of
  deleting it — producing exactly the two-copies-that-drift problem the rule prevents.

Cost: roughly **33% more tokens and 24% more wall-clock time** per session. The skill
asks Claude to verify claims — run the command, run the suite, render the diagram —
and that is where the time goes. It is the point, but you should expect it.

These numbers are from `v1`. Reproduce with
`python workspace/scripts/grade.py iteration-1` after re-running the test
cases.

## Known limitations

Stated plainly, in the spirit of the skill itself:

- **The multi-session claim is untested.** The evals measure whether Claude can follow
  the protocol in one session. Every documentation system works in week one; they die
  in week four. There is no evidence here about that.
- **`v2` has not been re-evaluated.** The anchor conventions are untested against the
  eval harness; only `v1` has measured results.
- **The session trigger is one line of text** in a file anyone can edit, and its
  absence fails silently.
- **`8_architecture.html` is the weakest file in the set** — a hand-maintained HTML
  page duplicating diagrams that GitHub renders natively from Mermaid. Consider
  skipping it.
- **`3_features.md` §3.6 (Talking points) is interview prep** in general-purpose
  clothing. Useful if that is what you want; skippable otherwise.
- **The description has not been tuned for triggering accuracy**, so it may fire on
  requests that only wanted a README.

## Credit

Built with [skill-creator](https://claude.com/claude-code). The substance comes from
[`_docs-generator-v2.md`](_docs-generator-v2.md), included here as provenance.
