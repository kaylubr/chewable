# Memory

## Project Overview

A privacy-conscious photobooth web app. Guests use the full experience (frame selection, webcam capture, Canvas composition, download) with no account; authentication is only required to permanently save a finished photo. See [README.md](README.md) for the stack, repo layout, setup, and current status.

## Code Style Guidelines

- One purpose per file, no giant `utils.py` or catch-all modules.
- `main.py` is wiring only (app creation, routers, middleware, CORS, exception handlers) — never endpoint logic.
- Routes stay thin: validate input → authenticate/authorize → call service → return response. No DB or storage internals in route functions.
- Business logic lives in `services/`, not in routers or models.
- Centralize env config in `src/core/config.py`, never scatter `os.getenv()` calls.
- Frontend frame logic lives in one centralized `FrameDefinition` config — capture logic only needs `photoCount`; composition reads the full definition.
- Never trust a client-supplied user ID — the server always derives the current user from the auth mechanism.
- Git commits are atomic: one logical change per commit. No "update backend" / "fix stuff".

## Architecture Notes

- **Frames are not a DB table.** Fixed enum/identifier set (VINTAGE, POLAROID, FILM, CLASSIC), owned by the frontend.
- **Data model stays small:** `User` (id, email, password_hash, created_at) and `Photo` (id, user_id, frame, storage_key, created_at). One-to-many User→Photo.
- **No persistent Session model** unless a real need shows up. Guest photobooth state lives entirely in frontend state.
- **Guest privacy:** captured images and the composed result stay client-side. Never create a DB record just because someone opened the photobooth. Never upload guest photos unless the user actively chooses to save.
- **Storage:** object storage holds images; Postgres holds only metadata + `storage_key`. Backend generates storage keys (e.g. `users/{user_id}/photos/{photo_id}.webp`) — never let the client choose the path.
- **Encryption:** normal secure transport/auth/storage for now. Client-side encryption (server never holds the key) is Stage 19, after the core app is stable — don't build or claim it early.

## Common Workflows

- Start local Postgres: `docker compose up -d`
- Backend reads `DATABASE_URL` from `.env`, never hardcode credentials; keep `.env.example` in sync.
- Minimum test coverage: auth behavior, password hashing, frame validation, photo ownership, photo create/delete, invalid uploads.
- After finishing a stage: run relevant tests, verify nothing existing broke, then commit.
- See the `photobooth-plan` skill for the full staged build order and commit sequence.
