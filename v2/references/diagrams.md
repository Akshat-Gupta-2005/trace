# Diagrams — file 7 (`7_uml/`) and file 8 (`8_architecture.html`)

Read this before creating a diagram, changing the architecture a diagram shows, or
regenerating the HTML page. The two files are a pair: `7_uml/` is the source under
review, `8_architecture.html` is the artifact you hand to someone who will not clone
the repo.

## Contents

- [File 7 — `7_uml/`](#file-7--7_uml) — one file per zoom level
- [File 8 — `8_architecture.html`](#file-8--8_architecturehtml) — the single-page version
- [Keeping the two in step](#keeping-the-two-in-step)

---

## File 7 — `7_uml/`

The system in diagrams, as **text**, so they diff, review and edit like code. Use
Mermaid in Markdown: it renders on GitHub and in editors, and needs no toolchain to
change.

One file per zoom level, each holding several diagrams:

    7_uml/README.md              index: which diagram answers which question,
                                 plus the ONE fact a reader needs before opening
                                 any of them — every entry a link, since an index
                                 nobody can click is a table of contents by hand
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

- **Branch labels are the real return values in the code**, not paraphrases. A diagram
  that renames things is a second vocabulary to maintain.
- **Every diagram carries its "why".** A box with no reason beside it is decoration.
  Where a shape exists because an alternative failed, name the problem ID: that is how
  a diagram teaches instead of describing.
- **Draw what is NOT built**, marked as such (dashed, or labelled PLANNED). Diagrams
  that show only what exists get read as showing everything.
- **Render before committing.** A diagram that does not parse is invisible on GitHub,
  and one that parses can still overlap into illegibility — so look at it, do not just
  lint it. Check two things and stop: does it parse, and can every label be read.
  Crossing edges, imperfect spacing and unlovely box placement are not defects — they
  are what a layout engine produces, and chasing them is an unbounded loop against a
  renderer you do not control. If a diagram is still unreadable after one fix, it is
  too big: split it, rather than tuning it again.
- Prefer several small diagrams to one that needs zooming. The container diagram and
  the class diagram answer different questions; a combined one answers neither.

### Linking the prose and the picture

`6_system-guide.md` and these files describe the same system in two forms, so each
should be one click from the other. Make it mutual:

- A guide section that describes structure links to the diagram of it —
  `see [the container diagram](7_uml/7.1_hld.md)` from §1 or §2.
- Each diagram file links back to the section that explains it in prose —
  `explained in [6_system-guide.md §5](../6_system-guide.md#s6-5)`.
- Where a shape exists because of a problem, both ends link the ID:
  `[P7](../4_decisions.md#p7)`.

One-directional linking is the failure mode here: whoever is reading the diagram is the
person who most needs the prose, and they are the one who did not come via the guide.

### Which diagram answers which question

Use this to decide whether a new diagram is needed at all, and where it goes. If the
question is already answered by an existing diagram, extend that one.

| The question a reader is asking | The diagram | Lives in |
|---|---|---|
| What is this system, and what does it talk to? | context | `7.1_hld.md` |
| What processes are there, and what runs where? | container, deployment | `7.1_hld.md` |
| What is inside this one service? | component | `7.2_lld.md` |
| What do the objects carrying the design look like? | class | `7.2_lld.md` |
| What is stored, and how does it relate? | ER | `7.3_data-model.md` |
| What crosses the wire? | schema / payload shapes | `7.3_data-model.md` |
| What happens, in what order, when X? | sequence | `7.4_sequences.md` |
| What states can this entity be in, and what moves it? | state machine | `7.5_state-machines.md` |
| Where does the logic branch, and on what? | activity | `7.6_activity.md` |

A state machine earns its place as soon as a status field has more than two values —
that is where the illegal transitions hide, and a table of states does not show them.

---

## File 8 — `8_architecture.html`

One self-contained page: a **master diagram** plus every diagram from `7_uml/`, in
sections, openable by double-click with nothing installed. This is what you send
someone who will not clone the repo, and what you put on a screen in a review.

    ## Structure
    §0  Master diagram — the whole system on one canvas, hand-laid so it
        renders with NO network and no JavaScript.
    §1..N  Every 7_uml/ diagram, grouped by zoom level, each with the prose
        that explains it, and each headed by a link to the 7_uml/ file it was
        generated from — so the question "which of these is canonical?" is
        answered on the page instead of guessed.
    §last  What changed since the previous version of this page.

Rules:

- **Do not edit the previous version in place.** Add the new one beside it and end with
  a v-old-vs-built table. The old page records what was believed at the time, which is
  evidence; overwriting it destroys that.
- **The master diagram must not depend on a CDN.** Plain HTML and inline SVG. The rest
  may render client-side, but every block falls back to showing its own source text
  when the library cannot load.
- **The page is generated FROM `7_uml/`, never instead of it.** A fix belongs in both,
  in the same commit. If they drift, `7_uml/` is right — it is the one under review.
- **Open it in a browser before committing, and look at it.** Count the rendered
  diagrams; check for arrows pointing at nothing, labels clipped behind boxes, and text
  running off the canvas. None of that is catchable by reading source.

### The fallback pattern

Every client-rendered block shows its own source when the renderer does not load, so
the page is never blank on a locked-down machine or an aeroplane:

    <div class="diagram">
      <pre class="mermaid">
    graph LR
      A[api] --> B[(queue)]
      B --> C[worker]
      </pre>
      <noscript><p>Diagram source shown above — JavaScript is off.</p></noscript>
    </div>

Keeping the source inside the element that renders it means there is exactly one copy
of the diagram text on the page, so a fallback can never disagree with the rendering.

---

## Keeping the two in step

The two files drift in one direction: someone fixes the HTML because that is what they
were looking at, and `7_uml/` keeps the old shape. Two habits prevent it:

1. **Change `7_uml/` first, regenerate second.** If you find yourself editing
   `8_architecture.html` by hand to fix a diagram, stop and fix the Mermaid source.
2. **Same commit, both files.** A commit that touches one and not the other is the
   moment the drift starts, and it is invisible afterwards.

When they already disagree, `7_uml/` wins — it is the version that gets reviewed in
diffs, so it is the version someone has actually read.
