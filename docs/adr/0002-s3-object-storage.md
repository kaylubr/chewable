# ADR 0002: S3-compatible object storage for saved photos

- **Status:** Accepted
- **Date:** 2026-09-05

## Context

A saved photo is the final composed photobooth image (WebP, up to ~10 MB). The database stores only metadata (`Photo`: id, user_id, frame, storage_key, created_at). The image bytes need an object store.

Development needs a local object store that behaves like the production target so the storage module is written once against a stable interface.

## Decision

Target **S3-compatible object storage**:

- The storage module speaks the S3 API (via a client library) and is configured entirely from `.env` (`S3_ENDPOINT_URL`, `S3_ACCESS_KEY`, `S3_SECRET_KEY`, `S3_BUCKET`, `S3_REGION` — already documented in `.env.example`).
- In development, a local S3-compatible server (MinIO) runs alongside Postgres in Docker Compose. Production points the same client at a real S3-compatible provider (R2, AWS S3, etc.) with no code change.
- The backend generates storage keys — e.g. `users/{user_id}/photos/{photo_id}.webp`. The client never chooses the path.
- Saved images are served back to the gallery by **proxying the bytes through the backend** (`GET /photos/{photo_id}/file`) after an ownership check, rather than handing out public bucket URLs or pre-signed URLs. This keeps the bucket private and avoids signed-URL expiry handling.
- In the initial version photos are not client-side encrypted; the long-term goal of server-blind client-side encryption is a separate later stage (see ADR 0006).

## Consequences

- One storage interface for dev and prod.
- The object store holds only the image bytes; Postgres holds only metadata + `storage_key`.
- Serving through the backend adds a small proxy cost, acceptable for a personal-scale gallery.

## Open questions

- Which S3 client library and whether to abstract it behind a thin storage service seam (one adapter today, possibly two later) — settle when the storage stage lands.
