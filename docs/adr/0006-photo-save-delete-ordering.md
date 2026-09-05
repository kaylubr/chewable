# ADR 0006: Photo save/delete ordering and failure handling

- **Status:** Accepted
- **Date:** 2026-09-05

## Context

Saving a photo spans two systems: object storage holds the image bytes, Postgres holds the metadata row. Deleting must remove both. The product rules require that a failure never leaves a misleading "saved" record, and that users can only reach their own photos.

## Decision

### Save order: object store first, then DB row

`POST /photos` runs:

1. Authenticate the user (server-derived, never client-supplied).
2. Validate the frame id against the supported set and the upload (WebP only, ≤ 10 MB).
3. Generate the storage key: `users/{user_id}/photos/{photo_id}.webp`.
4. Upload the image to object storage.
5. Only after a successful upload, create the `Photo` row.

If the upload fails, no row is created and the API returns a storage error — there is no misleading saved record. If the row insert fails after a successful upload, the uploaded object is best-effort deleted (an orphaned, invisible object is the accepted residual).

### Delete order: DB row first, then object

`DELETE /photos/{photo_id}` runs:

1. Authenticate and verify the photo belongs to the current user.
2. Delete the `Photo` row.
3. Delete the object-store file.

If the object delete fails after the row is gone, an orphaned file remains in storage but is invisible to users — the gallery never references a file that is missing.

## Consequences

- The visible state (the gallery) never shows a photo whose file is missing, and a failed save never appears saved.
- Orphaned objects are possible only on rare partial failures and are invisible to users.

## Open questions

- Whether to add periodic orphan cleanup later; not needed in the initial version.
