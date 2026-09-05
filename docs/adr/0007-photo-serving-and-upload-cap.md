# ADR 0007: Backend-proxied saved-photo serving and 10 MB upload cap

- **Status:** Accepted
- **Date:** 2026-09-05

## Context

The saved-photo gallery (`/photos`) must show a user only their own photos. The images live in a private S3-compatible bucket (ADR 0002). Two serving options were considered: backend-proxied bytes after an ownership check, or pre-signed object-store URLs. Upload size also needs a bound.

## Decision

- **Serve saved images by proxying through the backend.** `GET /photos/{photo_id}/file` verifies ownership, then streams the object bytes from storage to the client. No public bucket, no pre-signed URL expiry handling.
- `GET /photos` returns metadata (id, frame, created_at) plus the authenticated file URL; it never exposes another user's photos.
- **Enforce a 10 MB upload cap** on `POST /photos`. A 1620×2880 WebP composition is typically well under this; the cap mainly blocks abuse. Oversized uploads are rejected with a safe error.

## Consequences

- One consistent authenticated serving path for the frontend, working against any S3-compatible provider.
- The backend carries the image bytes on reads (a proxy cost), acceptable at personal-gallery scale.
- 10 MB bounds request size without risking legitimate large compositions.

## Open questions

- Content-Type / cache headers on the file endpoint; settle when the gallery stage lands.
