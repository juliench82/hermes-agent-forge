# shared/context-policy.md — Context Policy

Keeps context compact across profiles and prevents bloat.

## Minimal context handoffs
- Each handoff carries only what the next stage needs.
- Drop unrelated history when moving between profiles.

## Compact summaries
- Summarize stage outputs in a few lines.
- Do not forward full transcripts between specialists.

## Stage tracking
- Track the current stage and the next stage explicitly.
- Carry a short stage marker with each handoff.

## Avoiding bloat across profiles
- Do not re-read files already processed in the same run.
- Do not accumulate raw logs in working context.
- Keep each profile's working context focused on its single job.
