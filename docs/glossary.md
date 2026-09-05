# Chewables Glossary

Shared vocabulary for the Chewables photobooth. Terms here mean exactly what this file says; prefer them over loose synonyms in code, docs, and review.

## Booth / capture

- **Booth session** — The ephemeral, client-side state of one photobooth run: current state, selected frame, captured stills, countdown. Lives in module-scoped runes and resets on reload (ADR 0004). Not a database record.
- **Frame** — A static visual overlay plus a `FrameDefinition` describing how captured photos sit under it. Not a database entity and not rendered by the backend. A frame is artwork + one registry entry in `src/lib/frames/frames.ts`.
- **FrameDefinition** — The configuration object for one frame: `id`, `name`, `image`, `photoCount`, `width`, `height`, `photoSlots`. Capture logic reads only `photoCount`; composition reads the full definition.
- **PhotoSlot** — One rectangle on the frame canvas where a captured photo is drawn: `x`, `y`, `width`, `height`, `rotation`. Explicit configuration data measured against the frame's canvas; never inferred from the image.
- **PhotoCapture** — One webcam still taken during a booth session, held in browser memory as a data URL with its capture index.
- **Composition** — The client-side Canvas step that draws captured photos into the frame's photo slots and paints the frame overlay on top, producing the final WebP image.
- **Countdown** — A 5-second pre-shot delay before each individual capture (ADR 0003). One countdown per shot, not one per burst.
- **Guest** — A user running the booth with no account. Guests can capture, compose, and download; their photos never leave the browser.

## Identity / auth

- **User** — The database account: id, email, unique username, password hash, optional OAuth columns, created_at.
- **Stateless signed token** — The auth credential issued at login (ADR 0001): self-validating, carries the user id and expiry, no session table, short-lived, no refresh token in the initial version.
- **Save** — The authenticated action that uploads a finished composition to the backend and records a `Photo` row. A guest who presses Save is routed through login first.

## Persistence / storage

- **Photo** — A saved-photo metadata row: id, user_id (FK), frame id string, storage_key, created_at. One-to-many User → Photo.
- **Storage key** — The backend-generated object-store path, e.g. `users/{user_id}/photos/{photo_id}.webp`. The client never chooses it.
- **Object storage** — S3-compatible storage holding the image bytes (ADR 0002); MinIO in dev, a real S3-compatible provider in prod.
