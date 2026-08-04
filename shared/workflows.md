# shared/workflows.md — Stage Flow

Defines how work moves through the control room.

## Stage flow
1. **Intake** — orchestrator receives a plain-language request.
2. **Brief** — product strategist converts it into an automation brief.
3. **Design** — architect designs the approach.
4. **Build** — builder implements the automation.
5. **Validate** — quality guardian checks the result.
6. **Deliver** — orchestrator returns a useful outcome to the user.
7. **Improve** — self improver periodically reviews and proposes improvements.

## How agents hand off work
- Each specialist receives a compact input from the previous stage.
- Each specialist returns a compact output to the next stage.
- The orchestrator coordinates every handoff.

## When to stop and wait
- Stop and ask the user when a required value is truly missing.
- Stop and wait when a safety gate requires approval.
- Stop and hold when validation fails and fixes are needed.

## How work moves between profiles
- Work moves strictly forward through the runtime order.
- A profile does not perform another profile's job.
- The orchestrator may re-route work only when a stage fails or a value is missing.
