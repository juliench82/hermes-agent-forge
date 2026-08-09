# Intent-Fidelity Loop

> **Status:** additive policy. Extends — does not modify — `shared/context-policy.md`,
> `shared/workflows.md`, and `profiles/quality-guardian/skill.md`.
> **Purpose:** keep the raw user prompt as the immutable source of truth and
> re-verify every artifact against it, closing the Comprehension Debt gap.

## 1. The gap this closes

The default chain `Intake → Product Strategist → Architect → Builder → Quality Guardian`
treats Intake as a one-time parse. Downstream stages verify output only against
*derived* specs (the brief, the architecture doc), which can themselves drift from
the original ask. Nothing re-checks the final artifact against the raw user prompt.

## 2. New immutable state: `original_request`

- Captured once by the **Orchestrator (Intake)** at task acceptance, **verbatim**.
- Added to the context-policy handoff payload as `original_request`.
- **Immutable**: no downstream stage may rewrite, summarize, or replace it.
- Travels unchanged through every handoff.
- The Product Strategist's derived `brief` is a *separate* field; both travel together.

Handoff payload (additive fields):
```
original_request : <verbatim user prompt — never mutated>
brief            : <Product Strategist's derived spec — may be re-derived>
attempts         : <int, intent-verifier retry count, starts at 0>
intent_score     : <int 1–10, from latest Quality Guardian intent check>
```

## 3. Intent-verifier — 4th Quality Guardian check

Quality Guardian now runs **four** checks. The first three are unchanged
(secrets / tests / safety). The fourth is new:

- **Intent fidelity** — score 1–10 how well the final artifact satisfies
  `original_request` *specifically* (not the derived brief). Output: `intent_score`
  plus a one-paragraph justification citing the concrete gap.

Rubric:
- **9–10** — fully satisfies `original_request`; no meaningful gap.
- **7–8** — minor gap; acceptable to finalize.
- **4–6** — partial; route back for re-derivation.
- **1–3** — substantial drift; route back.

## 4. Stop condition (explicit gate)

The pipeline gains its first explicit finalize/loop gate:

- `intent_score ≥ 8` **and** secrets/tests/safety PASS → **FINALIZE**.
- `intent_score < 8` → route back to **Product Strategist** (not Builder).
  Drift usually starts at brief-writing, so re-derive the brief against
  `original_request` before rebuilding.
- Hard cap: `attempts` must not exceed **2** retries (3 total passes).
  Still `< 8` after the cap → finalize the best artifact and tag the task
  `intent-unresolved` for human review. This bounds the infinite-loop risk.

| intent_score | other checks | attempts | action |
|---|---|---|---|
| ≥ 8 | PASS | any | finalize |
| < 8 | any | < 2 | → Product Strategist (re-derive brief) |
| < 8 | any | = 2 | finalize + tag `intent-unresolved` |

## 5. Bilevel outer loop (Self-Improver)

Self-Improver already runs async. Extend its watch to repeated intent-verifier
failures across tasks:

- If `intent-unresolved` tags (or `intent_score < 8` requiring retry) recur for
  the same profile across **N** tasks, Self-Improver flags that profile's
  `skill.md` for revision. The inner loop fixes the artifact; the outer loop
  fixes the agent that produces the artifact.

## 6. Scope — what does NOT change

- Profile boundaries and the one-job-only rule are preserved.
- Existing Quality Guardian checks (secrets/tests/safety) are untouched.
- No pipeline restructuring — only one new state field (`original_request`),
  one new verification axis, and one explicit gate.
