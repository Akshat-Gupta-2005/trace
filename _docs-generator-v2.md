# PROJECT DOCUMENTATION PROMPT

You are maintaining the documentation for a software project. This file is the
standard you work to. Read all of it before writing anything; it is
self-contained and depends on no other document.

**What you produce:** eight artifacts, listed under THE FILE SET, written and
kept current as part of the work.

**The rule everything else serves:** a change is not complete until the
documentation reflects it. Documentation written at the end of a project is
fiction, because the detail that made it worth writing is already gone.

**How to use this file:**

1. Fill in section 0 once, at the start of the project. Change nothing else in
   this file.
2. At the start of every working session, follow SESSION PROTOCOL → *At the
   start of a session*.
3. While working, log decisions and problems as they happen, not afterwards.
4. Before reporting a session complete, work through the end-of-session
   checklist and the VERIFICATION table. A claim you have not checked is a claim
   you do not make.

Where this file says MUST, NEVER, or names a specific section, treat it as a
constraint rather than a suggestion. Everything else is guidance you may adapt
to the project in front of you.

---

## 0. PROJECT CONFIG — fill this in once, change nothing else

    PROJECT_NAME   = <name>
    PROJECT_GOAL   = <one sentence: what it does and who it is for>
    AUDIENCE       = <who reads these docs: recruiters / teammates / future me>
    STACK          = <languages, frameworks, key libraries>
    DOC_LOCATION   = <repo root, or docs/>
    STAR_LABEL     = <what a star marks, e.g. "interview bonus point">
    RUNTIME_SHAPE  = <what a reader must be able to run: services, containers,
                      workers, external processes, a CLI, a notebook>
    CONTRACT_KIND  = <the interface others build against: HTTP API, CLI flags,
                      library signatures, file formats — or "none" if internal>

Everything below refers to these values as {{PROJECT_NAME}}, {{PROJECT_GOAL}},
{{AUDIENCE}}, {{STACK}}, {{DOC_LOCATION}}, {{STAR_LABEL}}, {{RUNTIME_SHAPE}},
{{CONTRACT_KIND}}.

When you write the files, substitute the real values and leave no {{TOKEN}} in
the output. Never hardcode a project detail anywhere except section 0 of this
prompt.

---

## THE FILE SET

Eight artifacts in {{DOC_LOCATION}}, split by **how often each changes**. That
split is the whole design: it stops the plan being quietly rewritten to match
whatever happened, which is how project documentation usually dies.

    1_build-plan.md           what we intend to do         rarely changes
    2_implementation-plan.md  the order of the work        status edited as tasks land
    3_features.md             what is true right now       rewritten every session
    4_decisions.md            why it ended up this way     append-only, never edited
      └─ Open decisions       what we have NOT decided     the one live section
    5_api-contract.md         what others may rely on      changes with the interface
    6_system-guide.md         how the running thing works  changes when the runtime does
    7_uml/                    the system in diagrams       changes with the architecture
    8_architecture.html       master diagram + all of 7_   regenerated from 7_uml/

Treat all of them as part of the work, not as an afterthought: **a change is not
complete until the documentation reflects it.**

If that list looks heavy for your project, jump to SCALING DOWN. Adding a file
nobody maintains is worse than not having it.

### Naming

**The number is part of the filename**, so the directory lists the set in order
and nobody has to know which file comes first. `7_uml/` holds `7.1_hld.md`
through `7.6_activity.md`, on the same principle.

The number is **the order the files come into existence**, not the order they are
read. A newcomer reads `3_features.md` (what is true), then `6_system-guide.md`
(how to run it), then `8_architecture.html` (what it looks like). Point them
there; do not renumber to match a reading order, because the reading order
depends on who is reading.

Numbers are never reused and never renumbered — same rule as problem IDs. If a
file is dropped, its number retires with it and the sequence keeps its gap, so a
link or a commit message that names `5_api-contract.md` still means what it said.

---

## FILE 1 — `1_build-plan.md`

The intent. Written once at project start. Amend only on a genuine change of
direction, and when you do, log that change in 4_decisions.md rather than silently
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

## FILE 2 — `2_implementation-plan.md`

The **order** of the work. `1_build-plan.md` says what the system will be;
this file says what gets built in what sequence, and why that sequence
and not another.

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

- **A task's acceptance test is part of the task.** "Build the worker" is not a
  task; "the worker claims a job, and two workers never claim the same one" is.
- Keep completed units in place with their status, rather than deleting them.
  The order the work actually happened in is evidence about the plan's quality.
- When reality diverges from the plan — and it will — update the status, and
  log **why** it diverged in 4_decisions.md. The divergence is the interesting
  part.
- "Start here" is the section that goes stale first and is read first. Rewrite
  it every session, like 3_features.md's "Last updated".

---

## FILE 3 — `3_features.md`

What is true right now. Rewritten as the project changes. Anyone should be able
to open this and learn what exists, what works, and what is left.

### 3.1 Header

    # FEATURES — {{PROJECT_NAME}}

    Living document. Updated at the end of every working session, as part of
    the work. Reasoning and history live in 4_decisions.md.

    **Last updated:** <date> — <one line: what phase just completed, headline
    numbers, what is next>

The "Last updated" line is the most-read line in the file. It must let a reader
reconstruct project state in five seconds. Rewrite it every session; never let it
go stale. Keep the previous session's line, demoted to "**Earlier —**", so the
file carries its own recent history.

### 3.2 Status legend

    | Status     | Meaning                                  |
    | `Planned`  | Agreed, not started                      |
    | `Building` | In progress right now                    |
    | `Done`     | Implemented AND verified                 |
    | `Cut`      | Deliberately dropped — see 4_decisions.md  |

`Done` requires evidence — a passing test, a measured number, a working command —
not "the code is written". Status inflation is the fastest way to make this file
worthless.

Mark standout items with one to three stars, where a star means {{STAR_LABEL}}.
Only mark what is genuinely non-obvious; if everything is starred, nothing is.

### 3.3 Code map

An ASCII tree of every file with a one-line purpose, plus a short "Not yet built"
list naming what is still missing. A reader should be able to find the right file
from this section alone, without opening the repo.

**Audit the "Not yet built" list every session.** It rots faster than any other
section, because items leave it silently when they get built. A list that still
claims a shipped feature is missing destroys trust in the whole file.

If {{PROJECT_NAME}} has one central pipeline — a request path, a data flow, a
model lifecycle — add a numbered table tracing it end to end:

    | Step | File | State | What happens |

### 3.4 Feature sections

Group features by layer or subsystem, in dependency order (foundations first).
One table per group:

    | Feature | Status | What it does | Lives in | Star |

Rules:

- One row per feature, one line of description. If it needs a paragraph, it is
  two features.
- "What it does" must contain something concrete — a number, a filename, a
  measured result. "Handles errors" is worthless; "falls back to the second
  provider on unparseable output, not only on a dead server" is useful.
- "Lives in" is a real path, kept correct when files move.
- Add rows for features that emerged mid-build, not only planned ones.

End with a group for deferred and rejected work:

    | Feature | Status | Note (why deferred or cut, what would change it) |

### 3.5 Current state / measured results

The real numbers as of the last update: benchmarks, metrics, test counts,
timings, sample output. Include the exact command that reproduces them.

Every number must be one actually observed, with the conditions it was measured
under. Refresh whenever the underlying thing changes — a stale number here is
worse than none, because it will be quoted.

### 3.6 Talking points

One entry per starred feature, written for {{AUDIENCE}}. Two or three paragraphs
each:

    ### <stars> <short title>
    What it is, in one or two sentences.
    Why it is non-obvious — the naive approach and why it fails.
    The question it answers, and the answer, in a form that can be said out
    loud in under a minute.

Rules:

- Write these AS YOU GO. Reconstructing the reasoning weeks later loses the
  details that made it interesting.
- The best entries describe a trap avoided or a wrong path corrected, not a
  feature delivered.
- Cross-reference the source: the problem ID in 4_decisions.md, or the file path
  that shows it.
- Every claim must be defensible under follow-up questioning. If a point cannot
  survive "why?" twice, cut it.
- Order by strength, not by chronology.

### 3.7 Open items

Checkbox list of everything outstanding, including work blocked on a human
(credentials, downloads, decisions). Remove items when done — this list must
never contain a completed item.

An open item is a **task**. An unanswered question is not a task; it belongs in
4_decisions.md §4.4 (Open decisions). Keeping them apart stops "decide X" sitting
in a to-do list for a month with no options written down.

---

## FILE 4 — `4_decisions.md`

Why {{PROJECT_NAME}} ended up this way. **Append-only.** Never edit or delete an
entry. If a decision is reversed, add a new entry saying so and referencing the
old one — the history of changed minds is the point.

This is the file that cannot be reconstructed from the code later, which makes it
the most valuable of the set.

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

The "Why" column carries the weight. It must answer the question a sceptical
reader would ask, and it must name the alternative that was rejected. If the why
is "it was the obvious choice", the row probably should not exist.

### 4.3 Problems faced and fixed

The highest-value section in any of these files, and the one most often skipped.
One numbered entry per real problem:

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

Do not sanitise these. An entry saying "my threshold was conceptually wrong" is
worth ten saying "fixed a typo".

Category tags worth using: `conceptual`, `latent`, `design trap`, `assumption`,
`tooling`, `caught by tests`, `found by a user`.

Number problems sequentially and never renumber them — talking points and commit
messages will reference these IDs.

### 4.4 Open decisions

**The one section of this file that is not append-only.** Everything above
records what was decided; this records what has not been, so the same question is
not re-argued from scratch three sessions later.

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

- **Options must be real.** Two options where one is a straw man is a decision
  already made and pretending otherwise.
- **State what it costs to stay undecided.** Sometimes that is nothing, and the
  honest answer is "defer". Sometimes it is a rewrite, and that changes priority.
- **When it is answered:** write a dated row in §4.2 (or a `Cut` in 3_features.md),
  referencing OD<n>, and **delete the OD entry**. It has graduated; leaving it
  duplicates the record in two places that will drift.
- Number them separately from problems (OD1, OD2…) so an ID never means two
  things.
- Review this section at the start of every session. An entry unchanged for
  several sessions is either blocked on something you should name, or is not
  actually open.

---

## FILE 5 — `5_api-contract.md`

What other code may rely on: {{CONTRACT_KIND}}. Skip this file only if nothing
consumes {{PROJECT_NAME}} but {{PROJECT_NAME}}.

This file is a **promise**, so it changes only when the interface changes — and
every change is dated in place, because a consumer needs to know what changed and
when, not just what is true now.

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

- **Write examples from real captured output**, not from memory of the schema.
  A contract that does not match the wire is worse than none.
- Mark every later change inline with a date — *(Clarified 2026-09-17.)* — so a
  reader can see what moved without diffing the file.
- If a field exists because of a bug, say so and link the problem ID. That is
  the field nobody will understand in six months.
- The contract and the code drift silently. Whenever a response shape changes,
  the change is not done until this file changes in the same commit.

---

## FILE 6 — `6_system-guide.md`

How the running thing actually runs: {{RUNTIME_SHAPE}}. This is the file that
answers "I cloned it, now what?" and "it is broken, where do I look?" — questions
the other files deliberately do not answer.

Written for someone capable who has never run this system, including yourself
after three weeks away.

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

- **Verify while writing.** Run each command; check each port, name and path
  against the live system. This file's value is that it is executable.
- Name what is NOT set up. "No backups, one instance in a Docker volume" is the
  sentence that gets backups scheduled.
- Where a design choice looks odd, give the one-line reason inline. The guide is
  where people encounter the oddity, so it is where the reason belongs.

---

## FILE 7 — `7_uml/`

The system in diagrams, as **text**, so they diff, review and edit like code.
Use Mermaid in Markdown: it renders on GitHub and in editors, and needs no
toolchain to change.

One file per zoom level, each holding several diagrams:

    7_uml/README.md              index: which diagram answers which question,
                                 plus the ONE fact a reader needs before opening
                                 any of them
    7_uml/7.1_hld.md             context · containers · deployment
    7_uml/7.2_lld.md             components per service · classes for the objects
                                 that carry the design
    7_uml/7.3_data-model.md      ER over every table, plus the shapes that cross
                                 the wire
    7_uml/7.4_sequences.md       what happens in order, for the handful of flows
                                 that matter
    7_uml/7.5_state-machines.md  every entity whose status field has more than
                                 two values
    7_uml/7.6_activity.md        the decisions, branch by branch

Rules:

- **Branch labels are the real return values in the code**, not paraphrases. A
  diagram that renames things is a second vocabulary to maintain.
- **Every diagram carries its "why".** A box with no reason beside it is
  decoration. Where a shape exists because an alternative failed, name the
  problem ID: that is how a diagram teaches instead of describing.
- **Draw what is NOT built**, marked as such (dashed, or labelled PLANNED).
  Diagrams that show only what exists get read as showing everything.
- **Render before committing.** A diagram that does not parse is invisible on
  GitHub, and one that parses can still overlap into illegibility — so look at
  it, do not just lint it.
- Prefer several small diagrams to one that needs zooming. The container diagram
  and the class diagram answer different questions; a combined one answers
  neither.

---

## FILE 8 — `8_architecture.html`

One self-contained page: a **master diagram** plus every diagram from `7_uml/`, in
sections, openable by double-click with nothing installed. This is what you send
someone who will not clone the repo, and what you put on a screen in a review.

    ## Structure
    §0  Master diagram — the whole system on one canvas, hand-laid so it
        renders with NO network and no JavaScript.
    §1..N  Every 7_uml/ diagram, grouped by zoom level, each with the prose
        that explains it.
    §last  What changed since the previous version of this page.

Rules:

- **Do not edit the previous version in place.** Add the new one beside it and
  end with a v-old-vs-built table. The old page records what was believed at the
  time, which is evidence; overwriting it destroys that.
- **The master diagram must not depend on a CDN.** Plain HTML and inline SVG.
  The rest may render client-side, but every block falls back to showing its own
  source text when the library cannot load.
- **The page is generated FROM `7_uml/`, never instead of it.** A fix belongs in
  both, in the same commit. If they drift, `7_uml/` is right — it is the one under
  review.
- **Open it in a browser before committing, and look at it.** Count the rendered
  diagrams; check for arrows pointing at nothing, labels clipped behind boxes,
  and text running off the canvas. None of that is catchable by reading source.

---

## SESSION PROTOCOL

How these files stay current: by making the update a **step in the session**, not
a thing to remember afterwards. A session that ends without this is not finished.

### At the start of a session

1. Read 3_features.md's **Last updated** line and §3.7 Open items.
2. Read 4_decisions.md §4.4 **Open decisions** — you may be about to re-decide
   something, or to answer something that is waiting.
3. Read 2_implementation-plan.md's **Start here**.
4. If any of the three disagree with the repo, fix the doc **first**, before new
   work. Starting from a wrong description is how the second wrong thing gets
   built.

### During the session

Log as you go, not at the end:

- a non-obvious choice → a dated row in 4_decisions.md §4.2, **now**
- a bug found → a `P<n>` entry, **now**, while the symptom is still quoted
  exactly and the wrong theory you held first is still fresh
- a question you cannot answer → an `OD<n>` entry with its options
- a question you just answered → the OD entry graduates to a decision row and is
  deleted

The cost of writing these later is not the writing. It is that the detail that
made the entry worth having is gone.

### At the end of the session — the checklist

    [ ] 1_build-plan.md          touched ONLY if direction changed, with a
                                 4_decisions.md row saying why
    [ ] 2_implementation-plan.md task statuses and "Start here" updated
    [ ] 3_features.md            "Last updated" rewritten, previous line demoted
                                 to "Earlier"; statuses, code map and "Not yet
                                 built" match the repo
    [ ] 4_decisions.md           every choice and every problem from this
                                 session; open decisions reviewed, new ones
                                 added, answered ones graduated and deleted
    [ ] 5_api-contract.md        IF any response shape or client rule changed
    [ ] 6_system-guide.md        IF a part, port, command or failure mode changed
    [ ] 7_uml/                   IF the architecture, schema or a flow changed
    [ ] 8_architecture.html      regenerated IF 7_uml/ changed — and looked at
    [ ] Every number quoted today was observed today, or is dated
    [ ] Every doc claim about behaviour verified against the running system
    [ ] Commit message says what changed and why, not "docs update"

### The trigger matrix

Which change forces which file. Read it the other way too: if you edited one
file in the left column, check the whole row.

    Change made                        → files that must change
    ─────────────────────────────────────────────────────────────────────
    feature status moved               → 3_features.md, 2_implementation-plan.md
    file added / moved / renamed       → 3_features.md code map
    number measured                    → 3_features.md §3.5 (with the command)
    non-obvious choice                 → 4_decisions.md §4.2
    bug found and fixed                → 4_decisions.md §4.3, and the fix's test
    question raised / answered         → 4_decisions.md §4.4
    response shape or client rule      → 5_api-contract.md (same commit)
    new service, port, volume, command → 6_system-guide.md §2/§3/§6
    new failure mode suffered          → 6_system-guide.md §7
    architecture, schema or flow       → 7_uml/, then 8_architecture.html
    direction changed                  → 1_build-plan.md + a 4_decisions.md row

### Never

- delete history to make the project look cleaner
- mark something `Done` without verification
- leave a "Last updated" or "Start here" line stale
- copy in a number without having observed it
- write "improved performance" or "various fixes" — say what, and by how much
- edit a 4_decisions.md entry after it is written (§4.4 excepted, by design)
- let 8_architecture.html and `7_uml/` disagree

---

## VERIFICATION

Documentation is code with no compiler, so check it the way you would check code.
Before reporting a session complete:

| Claim in a doc | How you check it |
|---|---|
| a command | run it |
| a port, path, container or volume name | query the running system |
| a test count or timing | run the suite; paste what it printed |
| "X is not built" | search the repo before saying so |
| a diagram | render it, then **look** at the rendering |
| a response example | capture it from a real call |
| a link | follow it |

Two rules that come from being wrong about each of these:

- **A number without its conditions is not a measurement.** Say what was
  measured, on what, when.
- **"It works" needs to have been seen failing.** For anything that guards
  something — a test, a check, a gate — the useful evidence is that it fails when
  the mechanism is removed. State that evidence in the doc, or do not claim the
  guarantee.

---

## WRITING STYLE

- Concrete over abstract. Numbers, filenames, commands, quoted errors.
- Record the WHY, always. The what is recoverable from the code; the why is not.
- Keep rejected approaches and failed attempts. They are evidence of judgement,
  and they stop the same ground being re-covered.
- State limitations plainly. "This assumes X, which breaks when Y" is a strength,
  not an admission.
- No marketing language: no "robust", "seamless", "powerful",
  "state-of-the-art".
- Assume the reader is capable but has no context — including yourself in three
  weeks.
- Tables for scanning, prose for reasoning. Do not write a paragraph where a
  table row will do, and do not compress an explanation into a table cell.
- Write for the reader of each file. The guide is read by someone whose system is
  on fire; the contract by someone writing a client; the decisions log by someone
  asking "why on earth is it like this?".

---

## CROSS-LINKING

- 3_features.md links to 4_decisions.md problem IDs and decision dates.
- 4_decisions.md does not link forward to 3_features.md; it is history and must stay
  valid even as the current state changes underneath it.
- 2_implementation-plan.md links to the 4_decisions.md rows that changed the plan.
- 6_system-guide.md and `7_uml/` link to each other — prose and picture of the same
  thing — and both link to problem IDs where a shape exists because of one.
- 5_api-contract.md links to nothing internal. A consumer should not need the rest
  of the docs to use the interface.
- All of them link to real repo paths, kept correct when files move.
- **Exactly one "Last updated" line exists, in 3_features.md.** One place to look
  for project state. Every other file's currency is implied by the trigger
  matrix.

---

## SCALING DOWN

The set is not all-or-nothing. Add a file when the question it answers is being
asked, and not before.

| Project size | Keep |
|---|---|
| under a week, solo | 3_features.md + 4_decisions.md (including Open decisions) |
| a month, solo | add 1_build-plan.md and 2_implementation-plan.md |
| anything with a consumer | add 5_api-contract.md the day the second piece of code calls the first |
| anything with more than one process | add 6_system-guide.md before the second time you rediscover how to start it |
| anything you will explain to someone else | add `7_uml/`, then `8_architecture.html` |

Starting at `3_features.md` with no 1 or 2 is correct, not untidy: the gap says
those files were never written, and if they arrive later they take their own
numbers without disturbing anything already linked.

The problems section and the open decisions section earn their keep at every
size. The plan does not.
