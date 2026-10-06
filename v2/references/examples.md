# Worked examples

Three entries written out in full, at the level of detail that makes them worth
keeping. Each is followed by the thin version of the same entry — what it looks like
when written from memory at the end of a session — so the difference is visible.

All three come from one imaginary project, so they cross-reference each other the way
real entries should: **Sift**, a document-ingestion service where an API accepts
uploads, a Postgres table holds a job queue, and a pool of workers extracts text.

## Contents

- [A problem entry (`P<n>`, file 4 §4.3)](#a-problem-entry)
- [An open decision (`OD<n>`, file 4 §4.4)](#an-open-decision)
- [A talking point (file 3 §3.6)](#a-talking-point)

---

## A problem entry

<a id="p7"></a>
### P7 — Two workers processed the same upload *(2026-08-14, conceptual)*

**Symptom:** 3 of 400 documents in the nightly batch had two `extraction` rows with
different `worker_id`s and identical `content_hash`. No error was logged anywhere —
the run reported `400 ok, 0 failed`. Found only because a downstream count was 403.

**Root cause:** the claim was two statements — `SELECT id FROM jobs WHERE status =
'pending' LIMIT 1`, then `UPDATE jobs SET status = 'running' WHERE id = $1`. Between
them, a second worker ran the same SELECT and saw the same row. My first theory was
connection-pool reuse handing two workers the same transaction; that was wrong, and
I spent an afternoon on it. The give-away was that the duplicates clustered at the
start of each batch — the moment when all eight workers poll simultaneously — which
points at a race between workers, not at state inside one.

**Fix:** collapsed the two statements into one, with
`SELECT ... FOR UPDATE SKIP LOCKED` in a CTE that does the UPDATE and returns the row
([src/queue/claim.py](../src/queue/claim.py)). `SKIP LOCKED` rather than a plain `FOR UPDATE` because the
plain form makes the other seven workers block on the same row and serialises the
pool.

**Verified:** [`tests/test_claim.py`](../tests/test_claim.py)`::test_no_double_claim` runs 8 workers against 200
jobs and asserts each `job_id` appears exactly once. With `SKIP LOCKED` removed it
still passes (it just runs slower); with the CTE split back into two statements it
fails on 4–11 rows per run. The test was watched failing both ways before the fix
was called done.

**Generalises to:** read-then-write against shared rows is a claim only if the
database is told it is one. Two statements that look atomic in the application are
two statements to the database.

### The thin version

> ### P7 — Race condition in job queue *(August, bug)*
> **Symptom:** duplicate extractions.
> **Root cause:** race between workers.
> **Fix:** added `SKIP LOCKED`.
> **Verified:** tests pass.
> **Generalises to:** watch out for race conditions.

Everything in the thin version is true and none of it is useful. It does not say how
the duplicates were noticed (silently, by a count mismatch — the transferable part),
it does not record the wrong theory that cost an afternoon, "tests pass" is not
evidence because it does not say the test was seen failing, and the lesson is a
slogan. Six months later the thin version cannot even be used to check whether the
same bug has come back.

---

## An open decision

No `<a id="od3">` anchor here, deliberately — this entry is deleted the day the question
is answered, so anything linking to it would break. Other files name `OD3` as plain text.

### OD3 — Where does extracted text live: Postgres, or object storage?

**Blocks:** nothing today — documents average 40 KB and Postgres is comfortable.
It blocks the OCR work in W4, because scanned PDFs run 2–8 MB of text per document
and that is the point where the current answer stops being obviously fine. It is
also the last moment the choice is cheap: once the search index is built on top of
whatever this is, moving it means a reindex.

**Options:**

| Option | Costs | Buys you |
|---|---|---|
| `TEXT` column in `extractions` | Table grows ~6 GB/month once OCR lands; backup and restore time grows with it; every `SELECT *` gets expensive | One store, transactional with the job row, no second failure mode |
| S3/MinIO, key in the row | A second thing that can be down, and a cleanup path for orphaned objects when a transaction rolls back | Postgres stays small; text is streamable; storage cost drops roughly 10× |
| Postgres now, S3 above a size threshold | Two read paths in the code forever, and a threshold nobody will revisit | Defers the migration without blocking OCR |

**Leaning:** the third, with the threshold at 256 KB — but weakly, and mostly because
it is reversible. The honest objection is that "two read paths forever" is how the
last project got hard to change, and a threshold set once and never revisited is a
constant pretending to be a decision.

**What would settle it:** the OCR spike in W4 produces a real size distribution over
~500 scanned documents. If the 95th percentile is under 256 KB the split option is
mostly theatre and option 1 wins on simplicity. Deadline: this has to be settled
before W5 (search index), because the index is built over whichever store this is.

**Raised:** 2026-09-02.

### The thin version

> ### OD3 — Storage for extracted text?
> **Blocks:** OCR.
> **Options:** Postgres or S3.
> **Leaning:** probably S3.
> **What would settle it:** think about it more.

This is a reminder, not a record. "Postgres or S3" with no costs beside them means
the comparison gets re-done from scratch next time, which is exactly what the section
exists to prevent. "Probably S3" without a reason cannot be argued with, so it will
either be followed blindly or ignored. And "think about it more" is the tell that
this entry will still be here in six months: there is no event that ends it.

---

## A talking point

Written for `{{AUDIENCE}}` = *interviewers and teammates*, with `{{STAR_LABEL}}` =
*interview bonus point*. Note that it is about a trap avoided, cross-references the
problem ID, and can be said out loud in under a minute.

### ★★ The queue claim is one statement, not two

Explains [the single-statement claim](#f-single-statement-claim) in §3.4.

Sift's workers pull jobs from a Postgres table rather than a message broker. The
claim — the moment a job stops being available and becomes *mine* — is a single
statement: a CTE that selects one pending row `FOR UPDATE SKIP LOCKED` and updates it
to `running` in the same breath.

The naive version is the one I shipped first: select a pending row, then update it.
It reads as atomic and it is not. Two workers polling at the same instant see the
same row, and both claim it. What makes this worth talking about is the failure
*mode*, not the race: nothing errors. Both workers succeed, both write a result, and
the run reports zero failures. We found it because a downstream count was 403 instead
of 400 (see [P7](4_decisions.md#p7)). A bug that reports success is a different class of problem from one
that crashes, and it is the reason the fix has a test that was watched failing rather
than a test that merely passes.

The question this answers is "why not just use a real queue?" — and the answer is
that for eight workers and a few hundred thousand jobs a day, `SKIP LOCKED` gives you
at-least-once delivery, visibility into the queue with plain SQL, and one fewer
service to run. The moment that stops being true is when the polling cost shows up in
the database's CPU profile, and the threshold for revisiting it is written down in
`1_build-plan.md` §4.

### The thin version

> ### ★★ Job queue
> Built a job queue in Postgres using `SKIP LOCKED` for concurrency. This is a
> robust and performant approach that avoids the need for additional
> infrastructure like RabbitMQ, and demonstrates strong knowledge of database
> internals.

This describes a feature rather than teaching anything. It has no naive version, so
there is nothing for the reader to learn; it claims "robust" and "performant" without
a number; it says what was avoided but not when avoiding it stops being right; and it
cannot survive "why?" twice — the second "why?" is "what actually goes wrong without
it?", and the entry does not know.
