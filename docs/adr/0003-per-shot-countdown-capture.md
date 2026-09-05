# ADR 0003: Per-shot countdown capture flow

- **Status:** Accepted
- **Date:** 2026-09-05

## Context

A frame requires N photos. The capture UX needs a countdown so the subject can pose between shots. The existing client-side state machine (`session.ts`) already models `countdown -> capturing` transitions and forbids a second capture while one is in flight.

The question was whether one countdown precedes an automatic N-photo burst, or each individual shot gets its own countdown.

## Decision

Use a **per-shot countdown**:

- The camera shows a live preview. The user taps a capture control.
- A 5-second countdown runs, then exactly **one** still is captured.
- The next capture is armed only after the previous one completes, so total wall time for N photos is roughly N × 5 seconds.
- The state machine enforces that only one capture runs at a time; duplicate/simultaneous captures are structurally impossible (not merely prevented by disabling the button).
- After the Nth capture the flow transitions to composition (`composing -> result`).

## Consequences

- Predictable, deliberate pacing — the subject gets a fresh 5-second warning before every shot.
- Matches the existing `countdown -> capturing -> countdown -> ...` state transitions without new states.
- Slower than an auto-burst, but the product goal is a deliberate photobooth feel, not speed.

## Open questions

- Whether the countdown is shown as an overlay on the live preview and whether the user can cancel mid-countdown (state machine already allows `countdown -> camera-ready` for cancel) — decide when the camera stage lands.
