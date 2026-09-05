# Chewables

A privacy-conscious photobooth web app. Guests can use the full experience — frame selection, webcam capture, Canvas composition, download — with no account. Authentication is only required to permanently save a finished photo.

> **Status:** Frame selection works end-to-end (frame config → session state → picker page → camera placeholder). Webcam capture, composition, download, auth, and saving are not built yet. Agent-facing conventions and stage plan live in [AGENTS.md](AGENTS.md).

## Stack

| Layer    | Technology                                                        |
| -------- | ----------------------------------------------------------------- |
| Backend  | Python 3.14, FastAPI, SQLAlchemy 2 (async) + asyncpg, Pydantic v2 |
| Frontend | SvelteKit (Svelte 5, runes), TypeScript, Vite                     |
| Testing | Backend: pytest. Frontend: Vitest + jsdom + Testing Library        |
| Database | PostgreSQL 17 (Docker Compose for local dev)                      |
| Storage  | Object storage for saved images (planned, not yet wired)          |

## Repository layout

```
src/core/   FastAPI backend package (installed as the "chewable" project)
  main.py         App wiring only: app creation, CORS, routers
  config.py       Centralized env config (pydantic-settings)
  api/router.py   API routes (currently just GET /api/health)
  db/             SQLAlchemy async engine, session factory, declarative Base
src/ui/     SvelteKit frontend
  src/lib/frames/         Frame types + centralized frame registry
  src/lib/photobooth/     Client booth session state machine + shared store
  src/routes/             Landing page, /photobooth/frame, /photobooth/camera
  static/frames/          Frame overlay PNGs (test.png is a dev placeholder)
compose.yml Local PostgreSQL 17 service
```

## Prerequisites

- [uv](https://docs.astral.sh/uv/) (Python tooling)
- [Node.js](https://nodejs.org/) + npm (frontend)
- [Docker](https://www.docker.com/) (local Postgres)

## Local development

### 1. Start Postgres

```sh
docker compose up -d
```

Runs a `postgres:17-alpine` container on host port **5434** (chosen to avoid conflicts with other local Postgres instances).

### 2. Configure the backend

Copy `.env.example` to `.env` (it points `DATABASE_URL` at the Docker Postgres). The backend reads `DATABASE_URL` from `.env` — credentials are never hardcoded.

### 3. Run the backend

```sh
uv run fastapi dev src/core/main.py
```

The API is served at <http://localhost:8000>, with interactive docs at <http://localhost:8000/docs>.

### 4. Run the frontend

```sh
cd src/ui
npm install
npm run dev
```

The app is served at <http://localhost:5173>, and the backend CORS config already allows this origin.

## Useful commands

| Command                              | What it does                            |
| ------------------------------------ | --------------------------------------- |
| `docker compose up -d`               | Start local Postgres                    |
| `uv run fastapi dev src/core/main.py`| Run the FastAPI backend                 |
| `npm run dev` (in `src/ui`)          | Run the SvelteKit dev server            |
| `npm run check` (in `src/ui`)        | Type-check the frontend                 |
| `npm test` (in `src/ui`)             | Run the frontend Vitest suite           |
| `uv run pytest`                      | Run backend tests (when tests exist)    |

## Frames

Frames are **not** a database table or a backend concern — they are a fixed, frontend-owned set. Each frame is a static PNG overlay plus a `FrameDefinition` entry:

- Type definitions live in `src/ui/src/lib/frames/types.ts`. `FrameId` is the stable vocabulary (`VINTAGE`, `POLAROID`, `FILM`, `CLASSIC`).
- The registry `src/ui/src/lib/frames/frames.ts` maps each id to its overlay image, photo count, canvas size, and photo-slot rectangles.
- Adding a frame = drop the PNG in `static/frames/` and add one entry to the registry. No per-frame component, no backend/DB change.
- Capture logic reads only `photoCount`; composition reads the full definition.

**Currently registered:** `FILM` (35mm film strip, 4 photos, 1620×2880 canvas). Only `test.png` exists as a dev placeholder — real artwork comes from the designers.

## Architecture notes

- **Privacy first:** captured images and the composed result stay client-side. No DB record exists just for opening the photobooth; guest photos are never uploaded unless the user chooses to save.
- **Client-side booth state:** the frame → capture → result flow lives in module-scoped runes (`store.svelte.ts`) and resets on reload. A guarded state machine (`session.ts`) makes illegal transitions (e.g. duplicate captures) impossible.
- **Data model stays small:** `User` (id, email, password_hash, created_at) and `Photo` (id, user_id, frame, storage_key, created_at). No persistent session model.
- **Storage:** object storage holds images; Postgres holds only metadata + server-generated `storage_key` (e.g. `users/{user_id}/photos/{photo_id}.webp`). The client never chooses the path.
- **Server derives identity:** the backend never trusts a client-supplied user ID; the current user always comes from the auth mechanism.
