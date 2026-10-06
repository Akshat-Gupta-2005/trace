---
name: trace
description: "Maintains a numbered set of living project docs — features, decisions log, build and implementation plans, API contract, system guide, UML diagrams — that are updated as part of the work instead of written at the end. Use this whenever starting or finishing a working session on a project that has these docs, when a non-obvious choice needs recording, when a bug or wrong assumption needs writing up, when a question needs parking as an open decision, when a feature's status or the code map changes, or when someone asks what the state of a project is. Also use when setting up documentation for a new project, or when asked for a decision log, an ADR, a system guide or runbook, a features list, or architecture diagrams. Prefer this over ad-hoc doc writing even when the user does not name the files."
---

# Documenting projects

A numbered set of artifacts, kept current as part of the work rather than written at
the end. The rule everything else serves: **a change is not complete until the
documentation reflects it.** Documentation written at the end of a project is
fiction, because the detail that made it worth writing is already gone.

Where this skill says MUST or NEVER, or names a specific file or section, treat it as
a constraint. Everything else is guidance to adapt to the project in front of you.

## Step 1 — resolve the project config

This skill hardcodes no project detail. Each project keeps its own config, and every
template refers to its values as `{{PROJECT_NAME}}`, `{{PROJECT_GOAL}}`, and so on.

Look for it, in this order:

1. `docs/0_config.md`
2. `0_config.md` at the repo root
3. a `## Project docs config` block in the project's `CLAUDE.md`

Read it before doing anything else, and substitute the real values when you write —
leave no `{{TOKEN}}` in any output file.

### If no config exists

Do not guess and do not invent one silently. Ask these nine questions, in one pass,
and say why you are asking (you are about to set up the project's documentation):

| Token | The question |
|---|---|
| `PROJECT_NAME` | What is it called? |
| `PROJECT_GOAL` | One sentence: what does it do, and who is it for? |
| `AUDIENCE` | Who reads these docs — recruiters, teammates, future you? |
| `STACK` | Languages, frameworks, key libraries. |
| `DOC_LOCATION` | Repo root, or `docs/`? |
| `STAR_LABEL` | What does a star mark — e.g. "interview bonus point", "worth a blog post"? |
| `RUNTIME_SHAPE` | What must a reader be able to run: services, containers, workers, a CLI, a notebook? |
| `CONTRACT_KIND` | The interface others build against: HTTP API, CLI flags, library signatures, file formats — or "none" if nothing external consumes this. |
| `DOC_SET` | Which files this project keeps. Work **Scaling down** below from the top and stop at the last row the project actually meets — do not propose the full set because it looks thorough. Then let them cut it further. |

Several answers are usually already visible in the repo — the stack from the manifest
files, the runtime shape from a compose file or `Procfile`. Propose those and ask for
confirmation instead of making the person type them out. `AUDIENCE` and `STAR_LABEL`
are the two you genuinely cannot infer.

Then write the config file and stop to let them correct it:

    # Project docs config

        PROJECT_NAME   = ...
        PROJECT_GOAL   = ...
        AUDIENCE       = ...
        STACK          = ...
        DOC_LOCATION   = ...
        STAR_LABEL     = ...
        RUNTIME_SHAPE  = ...
        CONTRACT_KIND  = ...
        DOC_SET        = 3_features.md, 4_decisions.md, ...

`DOC_SET` is the list of files you create — create what it names and nothing else — and
it is what stops the end-of-session checklist nagging about files this project
deliberately does not keep. Update it when a file is added or retired.

### Then wire the session trigger

A skill loads when a request matches its description; nothing makes it load at the
start of a session just because it would be useful. So the project has to say so.
Add this line to the project's `CLAUDE.md` (create the file if there is none):

    Before starting work, follow the trace skill's session protocol.

Without that line the start-of-session read never reliably happens, and the docs
drift from the first session onward.

## The file set

Artifacts in `{{DOC_LOCATION}}`, split by **how often each changes**. That split is
the whole design: it stops the plan being quietly rewritten to match whatever
happened, which is how project documentation usually dies.

    1_build-plan.md           what we intend to do         rarely changes
    2_implementation-plan.md  the order of the work        status edited as tasks land
    3_features.md             what is true right now       rewritten every session
    4_decisions.md            why it ended up this way     append-only, never edited
      └─ Open decisions       what we have NOT decided     the one live section
    5_api-contract.md         what others may rely on      changes with the interface
    6_system-guide.md         how the running thing works  changes when the runtime does
    7_uml/                    the system in diagrams       changes with the architecture
    8_architecture.html       master diagram + all of 7_   regenerated from 7_uml/

Full section-by-section templates for files 1–6 are in
`references/file-templates.md`; files 7 and 8 are in `references/diagrams.md`.
Read the relevant one before writing or restructuring a file — not before a routine
append to an existing one.

If that list looks heavy for the project, see **Scaling down**. Adding a file nobody
maintains is worse than not having it.

### Naming

**The number is part of the filename**, so the directory lists the set in order and
nobody has to know which file comes first. `7_uml/` holds `7.1_hld.md` through
`7.6_activity.md`, on the same principle.

The number is **the order the files come into existence**, not the order they are
read. A newcomer reads `3_features.md` (what is true), then `6_system-guide.md` (how
to run it), then `8_architecture.html` (what it looks like). Point them there; do not
renumber to match a reading order, because the reading order depends on who is
reading.

Numbers are never reused and never renumbered — same rule as problem IDs. If a file
is dropped, its number retires with it and the sequence keeps its gap, so a link or a
commit message naming `5_api-contract.md` still means what it said.

## Session protocol

These files stay current by making the update a **step in the session**, not a thing
to remember afterwards. A session that ends without this is not finished.

### At the start of a session

1. Read `3_features.md`'s **Last updated** line and §3.7 Open items.
2. Read `4_decisions.md` §4.4 **Open decisions** — you may be about to re-decide
   something, or to answer something that is waiting.
3. Read `2_implementation-plan.md`'s **Start here**.
4. If any of the three disagree with the repo, fix the doc **first**, before new work.
   Starting from a wrong description is how the second wrong thing gets built.

### During the session

Log as you go, not at the end:

- a non-obvious choice → a dated row in `4_decisions.md` §4.2, **now**
- a bug found → a `P<n>` entry, **now**, while the symptom is still quoted exactly and
  the wrong theory you held first is still fresh
- a question you cannot answer → an `OD<n>` entry with its options
- a question you just answered → the OD entry graduates to a decision row and is
  deleted

The cost of writing these later is not the writing. It is that the detail that made
the entry worth having is gone.

`references/examples.md` has a worked `P<n>`, a worked `OD<n>` and a worked talking
point. Read it the first few times you write one — the failure mode is entries too
vague to be worth the space, and the examples show the level of detail that earns its
keep.

### At the end of the session — the checklist

Run through this, skipping any file not in `DOC_SET`:

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

A claim you have not checked is a claim you do not make. Work the **Verification**
table below before reporting a session complete.

## The trigger matrix

Which change forces which file. Read it the other way too: if you edited one file in
the right column, check whether the row's other files need the same change.

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

## Verification

Documentation is code with no compiler, so check it the way you would check code.

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

- **A number without its conditions is not a measurement.** Say what was measured, on
  what, when.
- **"It works" needs to have been seen failing.** For anything that guards something —
  a test, a check, a gate — the useful evidence is that it fails when the mechanism is
  removed. State that evidence in the doc, or do not claim the guarantee.

## Writing style

- Concrete over abstract. Numbers, filenames, commands, quoted errors.
- Record the WHY, always. The what is recoverable from the code; the why is not.
- Keep rejected approaches and failed attempts. They are evidence of judgement, and
  they stop the same ground being re-covered.
- State limitations plainly. "This assumes X, which breaks when Y" is a strength, not
  an admission.
- No marketing language: no "robust", "seamless", "powerful", "state-of-the-art".
- Assume the reader is capable but has no context — including yourself in three weeks.
- Tables for scanning, prose for reasoning. Do not write a paragraph where a table row
  will do, and do not compress an explanation into a table cell.
- Write for the reader of each file. The guide is read by someone whose system is on
  fire; the contract by someone writing a client; the decisions log by someone asking
  "why on earth is it like this?".

### Never

- delete history to make the project look cleaner
- mark something `Done` without verification
- leave a "Last updated" or "Start here" line stale
- copy in a number without having observed it
- write "improved performance" or "various fixes" — say what, and by how much
- edit a `4_decisions.md` entry after it is written (§4.4 excepted, by design)
- let `8_architecture.html` and `7_uml/` disagree

## Cross-linking

- `3_features.md` links to `4_decisions.md` problem IDs and decision dates.
- `4_decisions.md` does not link forward to `3_features.md`; it is history and must
  stay valid even as the current state changes underneath it.
- `2_implementation-plan.md` links to the `4_decisions.md` rows that changed the plan.
- `6_system-guide.md` and `7_uml/` link to each other — prose and picture of the same
  thing — and both link to problem IDs where a shape exists because of one.
- `5_api-contract.md` links to nothing internal. A consumer should not need the rest
  of the docs to use the interface.
- All of them link to real repo paths, kept correct when files move.
- **Exactly one "Last updated" line exists, in `3_features.md`.** One place to look for
  project state. Every other file's currency is implied by the trigger matrix.

## Scaling down

The set is not all-or-nothing. Add a file when the question it answers is being asked,
and not before. Use this to propose `DOC_SET` during setup.

| Project size | Keep |
|---|---|
| under a week, solo | `3_features.md` + `4_decisions.md` (including Open decisions) |
| a month, solo | add `1_build-plan.md` and `2_implementation-plan.md` |
| anything with a consumer | add `5_api-contract.md` the day the second piece of code calls the first |
| anything with more than one process | add `6_system-guide.md` before the second time you rediscover how to start it |
| architecture you cannot hold in your head | add `7_uml/`, then `8_architecture.html` |

Read that last row strictly. "Someone will read this" is not the trigger — everything
gets explained to someone, so that test licenses the whole set for a four-module CLI
and you end up maintaining diagrams of something a person can read in ten minutes.
The trigger is that you cannot keep the component graph in your head: several
services, a schema with real cardinality, or a flow whose order matters and is not
obvious from the call stack. A single-process tool almost never qualifies, however
many people read it.

**Start from the bottom row you actually meet and stop.** Each file above
`3_features.md` and `4_decisions.md` needs a reason you can say out loud. If the
honest reason is "it seemed thorough", that file will not be maintained, and an
unmaintained file is worse than a missing one.

Starting at `3_features.md` with no 1 or 2 is correct, not untidy: the gap says those
files were never written, and if they arrive later they take their own numbers without
disturbing anything already linked.

The problems section and the open decisions section earn their keep at every size. The
plan does not.

## Reference files

| File | What is in it | When to read it |
|---|---|---|
| `references/file-templates.md` | Section-by-section templates and rules for files 1–6 | Before creating one of those files, or restructuring it |
| `references/diagrams.md` | `7_uml/` (7.1–7.6) and `8_architecture.html` | Before touching diagrams or regenerating the HTML page |
| `references/examples.md` | A worked problem entry, open decision and talking point | The first few times you write one, or when an entry feels thin |
