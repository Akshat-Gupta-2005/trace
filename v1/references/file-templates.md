# File templates — files 1 to 6

Section-by-section structure and rules for the prose files. Files 7 and 8 (diagrams)
are in `diagrams.md`.

Read the section for the file you are about to create or restructure. A routine
append to an existing file does not need this.

All `{{TOKEN}}` values come from the project config — see SKILL.md, *Step 1*. Leave
no token unsubstituted in the output.

## Contents

- [File 1 — `1_build-plan.md`](#file-1--1_build-planmd) — the intent, written once
- [File 2 — `2_implementation-plan.md`](#file-2--2_implementation-planmd) — the order of the work
- [File 3 — `3_features.md`](#file-3--3_featuresmd) — what is true right now
- [File 4 — `4_decisions.md`](#file-4--4_decisionsmd) — why it ended up this way
- [File 5 — `5_api-contract.md`](#file-5--5_api-contractmd) — what others may rely on
- [File 6 — `6_system-guide.md`](#file-6--6_system-guidemd) — how the running thing works

---

## File 1 — `1_build-plan.md`

The intent. Written once at project start. Amend only on a genuine change of
direction, and when you do, log that change in `4_decisions.md` rather than silently
editing the plan.

    # {{PROJECT_NAME}} — Build Plan
    One paragraph: {{PROJECT_GOAL}}, and why it exists.

    ## 1. Tech Stack
    Table: | Layer | Tool | Why this one |
    Cover everything in {{STACK}}. The "Why" column is mandatory — "it is
    popular" is not a reason. Note anything deliberately NOT used, and why.

    ## 2. Architecture
    A diagram plus a short paragraph per component. State which components
    depend on which, and which are independent — independence is what allows
    parallelism and isolated testing.

    ## 3. Data / Domain Model
    Core entities, their shape, and the rules that must always hold.

    ## 4. Core Logic
    The central formulas, algorithms, or business rules. For each: what it
    computes, what it assumes, and where those assumptions break.
    Documenting the limits of an approach is worth more than describing it.

    ## 5. Phase Plan
    Phases with deliverables. Each phase names a concrete artifact that can be
    demonstrated, not an activity. "Five callable functions" not "work on the
    engine".

    ## 6. Repo Structure
    Directory tree, one line of purpose per file or folder.

    ## 7. Definition of Done
    The specific, checkable conditions under which {{PROJECT_NAME}} is
    finished. Include the non-code ones: documentation, reproducibility, tests
    passing.

---

## File 2 — `2_implementation-plan.md`

The **order** of the work. `1_build-plan.md` says what the system will be; this file
says what gets built in what sequence, and why that sequence and not another.

Unlike the other files, this one has **editable status** — a task row moves from
`Planned` to `Done` in place. It is a plan being executed, not a record.

    # {{PROJECT_NAME}} — Implementation Plan

    ## 1. Dependency graph
    Which work units depend on which. A diagram or a table. The point is to
    make visible what can be done in parallel and what is a hard sequence —
    and to expose any unit that blocks everything else, which is the one to
    de-risk first.

    ## 2..N. One section per work unit (W0, W1, …)
    Each unit has:
      - a one-line goal, in terms of a demonstrable artifact
      - a numbered task table: | # | Status | Task, with its acceptance test |
      - what it deliberately does NOT include, so scope creep is visible
      - the checkpoint, if any: the measurement that decides whether the next
        unit is worth starting

    ## Go/no-go checkpoints
    Any point where evidence could change the plan. State the number that
    decides it and what happens in each direction, BEFORE measuring. A
    checkpoint written after the result is not a checkpoint.

    ## Documentation checkpoints
    The moments where something is learned that cannot be recovered later —
    a calibration result, a first real timing, a spike outcome. Name which
    file records it.

    ## Start here
    The one section a returning reader needs: what is done, what is in
    progress, what is next, and any carve-out waiting on a human.

Rules:

- **A task's acceptance test is part of the task.** "Build the worker" is not a task;
  "the worker claims a job, and two workers never claim the same one" is.
- Keep completed units in place with their status, rather than deleting them. The
  order the work actually happened in is evidence about the plan's quality.
- When reality diverges from the plan — and it will — update the status, and log
  **why** it diverged in `4_decisions.md`. The divergence is the interesting part.
- "Start here" is the section that goes stale first and is read first. Rewrite it
  every session, like `3_features.md`'s "Last updated".

---

## File 3 — `3_features.md`

What is true right now. Rewritten as the project changes. Anyone should be able to
open this and learn what exists, what works, and what is left.

### 3.1 Header

    # FEATURES — {{PROJECT_NAME}}

    Living document. Updated at the end of every working session, as part of
    the work. Reasoning and history live in 4_decisions.md.

    **Last updated:** <date> — <one line: what phase just completed, headline
    numbers, what is next>

The "Last updated" line is the most-read line in the file. It must let a reader
reconstruct project state in five seconds. Rewrite it every session; never let it go
stale. Keep the previous session's line, demoted to "**Earlier —**", so the file
carries its own recent history.

### 3.2 Status legend

    | Status     | Meaning                                  |
    | `Planned`  | Agreed, not started                      |
    | `Building` | In progress right now                    |
    | `Done`     | Implemented AND verified                 |
    | `Cut`      | Deliberately dropped — see 4_decisions.md |

`Done` requires evidence — a passing test, a measured number, a working command — not
"the code is written". Status inflation is the fastest way to make this file
worthless.

Mark standout items with one to three stars, where a star means `{{STAR_LABEL}}`.
Only mark what is genuinely non-obvious; if everything is starred, nothing is.

### 3.3 Code map

An ASCII tree of every file with a one-line purpose, plus a short "Not yet built" list
naming what is still missing. A reader should be able to find the right file from this
section alone, without opening the repo.

**Audit the "Not yet built" list every session.** It rots faster than any other
section, because items leave it silently when they get built. A list that still claims
a shipped feature is missing destroys trust in the whole file.

If `{{PROJECT_NAME}}` has one central pipeline — a request path, a data flow, a model
lifecycle — add a numbered table tracing it end to end:

    | Step | File | State | What happens |

### 3.4 Feature sections

Group features by layer or subsystem, in dependency order (foundations first). One
table per group:

    | Feature | Status | What it does | Lives in | Star |

Rules:

- One row per feature, one line of description. If it needs a paragraph, it is two
  features.
- "What it does" must contain something concrete — a number, a filename, a measured
  result. "Handles errors" is worthless; "falls back to the second provider on
  unparseable output, not only on a dead server" is useful.
- "Lives in" is a real path, kept correct when files move.
- Add rows for features that emerged mid-build, not only planned ones.

End with a group for deferred and rejected work:

    | Feature | Status | Note (why deferred or cut, what would change it) |

### 3.5 Current state / measured results

The real numbers as of the last update: benchmarks, metrics, test counts, timings,
sample output. Include the exact command that reproduces them.

Every number must be one actually observed, with the conditions it was measured under.
Refresh whenever the underlying thing changes — a stale number here is worse than
none, because it will be quoted.

### 3.6 Talking points

One entry per starred feature, written for `{{AUDIENCE}}`. Two or three paragraphs
each:

    ### <stars> <short title>
    What it is, in one or two sentences.
    Why it is non-obvious — the naive approach and why it fails.
    The question it answers, and the answer, in a form that can be said out
    loud in under a minute.

Rules:

- Write these AS YOU GO. Reconstructing the reasoning weeks later loses the details
  that made it interesting.
- The best entries describe a trap avoided or a wrong path corrected, not a feature
  delivered.
- Cross-reference the source: the problem ID in `4_decisions.md`, or the file path that
  shows it.
- Every claim must be defensible under follow-up questioning. If a point cannot survive
  "why?" twice, cut it.
- Order by strength, not by chronology.

A worked example is in `examples.md`.

### 3.7 Open items

Checkbox list of everything outstanding, including work blocked on a human
(credentials, downloads, decisions). Remove items when done — this list must never
contain a completed item.

An open item is a **task**. An unanswered question is not a task; it belongs in
`4_decisions.md` §4.4 (Open decisions). Keeping them apart stops "decide X" sitting in
a to-do list for a month with no options written down.

---

## File 4 — `4_decisions.md`

Why `{{PROJECT_NAME}}` ended up this way. **Append-only.** Never edit or delete an
entry. If a decision is reversed, add a new entry saying so and referencing the old
one — the history of changed minds is the point.

This is the file that cannot be reconstructed from the code later, which makes it the
most valuable of the set.

### 4.1 Header

    # DECISIONS — {{PROJECT_NAME}}

    Append-only record of choices made and problems solved.
    Current state lives in 3_features.md.

### 4.2 Decisions log

    | Date | Decision | Why |

Log a decision whenever:

- a technology, library, or approach is chosen over an alternative
- a default, threshold, or parameter is set to a non-obvious value
- something is deliberately NOT done
- a previous decision is reversed
- a value changes based on evidence — state what the evidence was

The "Why" column carries the weight. It must answer the question a sceptical reader
would ask, and it must name the alternative that was rejected. If the why is "it was
the obvious choice", the row probably should not exist.

### 4.3 Problems faced and fixed

The highest-value section in any of these files, and the one most often skipped. One
numbered entry per real problem:

    ### P<n> — <one-line title> *(when, category)*
    **Symptom:** what was actually observed — error text, wrong number, failing
    test. Quote it verbatim where possible.
    **Root cause:** the real reason, not the surface reason.
    **Fix:** what changed.
    **Verified:** how you know the fix works — ideally the mechanism seen
    failing with the fix removed.
    **Generalises to:** the transferable lesson, in one sentence.

Add an entry for:

- every bug found, including ones caught by tests rather than by failure
- every wrong assumption discovered
- every design approach that had to be redone
- problems designed out before they shipped, where the reasoning is useful

Do not sanitise these. An entry saying "my threshold was conceptually wrong" is worth
ten saying "fixed a typo".

Category tags worth using: `conceptual`, `latent`, `design trap`, `assumption`,
`tooling`, `caught by tests`, `found by a user`.

Number problems sequentially and never renumber them — talking points and commit
messages will reference these IDs.

A worked example is in `examples.md`.

### 4.4 Open decisions

**The one section of this file that is not append-only.** Everything above records
what was decided; this records what has not been, so the same question is not
re-argued from scratch three sessions later.

    ## Open decisions

    ### OD<n> — <the question, as a question>
    **Blocks:** what cannot proceed, or what is provisional until this is
    settled. If nothing is blocked, say so — some questions can wait, and
    knowing that is useful.
    **Options:**
    | Option | Costs | Buys you |
    **Leaning:** which one, and why — or "genuinely undecided".
    **What would settle it:** the measurement, the prototype, the user answer,
    or the deadline that forces it. A question with no route to an answer is a
    question that will still be open in six months.
    **Raised:** <date>.

Rules:

- **Options must be real.** Two options where one is a straw man is a decision already
  made and pretending otherwise.
- **State what it costs to stay undecided.** Sometimes that is nothing, and the honest
  answer is "defer". Sometimes it is a rewrite, and that changes priority.
- **When it is answered:** write a dated row in §4.2 (or a `Cut` in `3_features.md`),
  referencing `OD<n>`, and **delete the OD entry**. It has graduated; leaving it
  duplicates the record in two places that will drift.
- Number them separately from problems (OD1, OD2…) so an ID never means two things.
- Review this section at the start of every session. An entry unchanged for several
  sessions is either blocked on something you should name, or is not actually open.

A worked example is in `examples.md`.

---

## File 5 — `5_api-contract.md`

What other code may rely on: `{{CONTRACT_KIND}}`. Skip this file only if nothing
consumes `{{PROJECT_NAME}}` but `{{PROJECT_NAME}}`.

This file is a **promise**, so it changes only when the interface changes — and every
change is dated in place, because a consumer needs to know what changed and when, not
just what is true now.

    # {{PROJECT_NAME}} — Interface Contract

    ## 0. What this file is
    One paragraph: this is what a client may depend on. Anything not written
    here is an implementation detail and may change without notice.

    ## 1. Obligations on the client
    The rules a consumer MUST follow, each with what breaks if they do not.
    Put this FIRST. Rules buried at the end are rules nobody reads, and the
    ones that corrupt data silently are exactly the ones that must be read.

    ## 2..N. One section per endpoint / command / function
    For each:
      - the shape of the request and the response, as a real example, not a
        schema sketch
      - every field, with meaning — especially fields that look optional and
        are not
      - the states the response can be in, and which of them a client must
        NOT conflate (this is where most client bugs come from)
      - errors: codes, and what a client should do about each

    ## Errors
    One table of every error shape, with the code a client branches on. State
    plainly that clients branch on the code, never on the message text.

    ## Versioning
    What a breaking change is here, and how one would be shipped.

Rules:

- **Write examples from real captured output**, not from memory of the schema. A
  contract that does not match the wire is worse than none.
- Mark every later change inline with a date — *(Clarified 2026-09-17.)* — so a reader
  can see what moved without diffing the file.
- If a field exists because of a bug, say so and link the problem ID. That is the field
  nobody will understand in six months.
- The contract and the code drift silently. Whenever a response shape changes, the
  change is not done until this file changes in the same commit.

---

## File 6 — `6_system-guide.md`

How the running thing actually runs: `{{RUNTIME_SHAPE}}`. This is the file that
answers "I cloned it, now what?" and "it is broken, where do I look?" — questions the
other files deliberately do not answer.

Written for someone capable who has never run this system, including yourself after
three weeks away.

    # SYSTEM GUIDE — the running system, explained

    ## 1. The shape of it
    What the system is, in terms of its moving parts and their speeds.
    If two parts have different failure profiles or different latencies, say
    so here — that difference usually explains the whole architecture.

    ## 2. The parts
    One subsection per process, container, or service:
      - what it is, and why THIS tool or image (pinned version, if pinned)
      - what it owns that nothing else owns
      - what it looks like when it is down — the symptom, not the theory

    ## 3. How they find each other
    Names, addresses, ports, and the difference between how things address
    each other internally and how you address them from outside. Include the
    configuration trap that bit someone: every project has one.

    ## 4. How state is handled
    Where the durable state lives, what is derived and rebuildable, how the
    schema is created and migrated, how test instances are built, and what is
    NOT handled — backups, restore, retention. An honest gap list here is
    worth more than a confident description of what exists.

    ## 5. One request, traced through the parts
    The end-to-end path, naming which component does which step. The single
    most useful section for a newcomer.

    ## 6. Everyday commands
    Copy-pasteable. Start, check health, read logs, talk to the database,
    rebuild one part, stop, and the destructive one — clearly marked as the
    command that destroys data.

    ## 7. When it breaks, this is what it looks like
    | Symptom | Usually |
    Built from failures actually hit, not imagined ones. This table is the
    highest-value section in the file and can only be written by having
    suffered.

    ## 8. Habits this codebase runs on
    The two or three rules that explain the most decisions, each with the
    incident that produced it.

    ## 9. Glossary
    Every term a newcomer would have to look up, defined AS USED HERE — not
    the textbook definition.

Rules:

- **Verify while writing.** Run each command; check each port, name and path against
  the live system. This file's value is that it is executable.
- Name what is NOT set up. "No backups, one instance in a Docker volume" is the
  sentence that gets backups scheduled.
- Where a design choice looks odd, give the one-line reason inline. The guide is where
  people encounter the oddity, so it is where the reason belongs.
