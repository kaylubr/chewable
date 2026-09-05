# ADR 0004: Guest photobooth session stays in browser memory

- **Status:** Accepted
- **Date:** 2026-09-05

## Context

Guests can run the whole photobooth — frame selection, webcam capture, Canvas composition, download — without an account and without touching the backend. The product rule is that captured images and the composed result stay client-side, and no anonymous DB record is created just for opening the booth.

The photobooth state already lives in module-scoped runes (`store.svelte.ts`) shared across the `/photobooth` routes.

## Decision

Keep the guest session **in browser memory only**:

- The selected frame, the captured stills (data URLs), and the composed result are held in module-scoped runes state.
- No persistence to IndexedDB/localStorage and no upload of guest photos. Reloading mid-flow resets the booth and the user restarts.
- The composed result is cached in memory once produced, so download/save re-use it instead of recomposing on every request.

## Consequences

- Guest photos never touch disk or the network; the privacy claim on the landing page stays literally true.
- An accidental reload loses an in-progress session — accepted trade-off for simplicity and privacy.
- Holding captures as in-memory data URLs is fine for the expected photo count and canvas sizes.

## Open questions

- Memory pressure if a frame ever needs many large captures; revisit only if it becomes a real problem.
