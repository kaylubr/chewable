# Chewables

A privacy-conscious photobooth web app. Guests can use the full experience — frame selection, webcam capture, Canvas composition, download — with no account. Authentication is only required to permanently save a finished photo.

> **Status:** The full guest flow works end to end: frame selection → webcam capture (5s countdown between shots) → in-browser Canvas composition → download. Signed-in users can save finished photos to a private gallery and delete them. Agent-facing conventions and the stage plan live in [AGENTS.md](AGENTS.md).

## Stack

| Layer    | Technology                                                        |
| -------- | ----------------------------------------------------------------- |
| Backend  | Python 3.14, FastAPI, SQLAlchemy 2 (async) + asyncpg, Pydantic v2 |
| Frontend | SvelteKit (Svelte 5, runes), TypeScript, Vite                     |
| Testing  | Backend: pytest + httpx. Frontend: Vitest + jsdom                 |
| Database | PostgreSQL 17 (Docker Compose for local dev), Alembic migrations  |
| Storage  | S3-compatible object storage — MinIO in local dev                 |
| Auth     | Argon2 password hashing, signed JWT access tokens (stateless)     |

## Repository layout

```
src/core/   FastAPI backend package (installed as the "chewable" project)
  main.py         App wiring only: app creation, CORS, routers, lifespan
  config.py       Centralized env config (pydantic-settings)
  api/            Routers: health, auth (register/login/me), photos
  models/         User + Photo ORM models (no Frame table)
  schemas/        Auth + photo request/response models
  services/       Auth, photo, and object-storage business logic
  security.py     Argon2 hashing + JWT sign/verify
  frames.py       Supported frame identifier vocabulary (backend validation)
  db/             SQLAlchemy async engine, session factory, declarative Base
src/ui/     SvelteKit frontend
  src/lib/frames/         Frame types + centralized frame registry
  src/lib/photobooth/     Booth session state machine, capture controller, composition
  src/lib/auth/           Client auth store (localStorage token)
  src/lib/api/            Typed backend API client
  src/routes/             Landing, /photobooth/{frame,camera,result}, /login, /register, /photos
  static/frames/          Frame overlay PNGs (test.png is a dev placeholder)
tests/      Backend pytest suite (auth, photos, services, storage failures)
alembic/    Database migrations
compose.yml PostgreSQL 17 + MinIO services
```

## Prerequisites

- [uv](https://docs.astral.sh/uv/) (Python tooling)
- [Node.js](https://nodejs.org/) + npm (frontend)
- [Docker](https://www.docker.com/) (local Postgres + MinIO)

## Local development

### 1. Start the services

```sh
docker compose up -d
```

Runs `postgres:17-alpine` on host port **5434** and MinIO on **9000/9001** (ports chosen to avoid conflicts with other local Postgres instances).

### 2. Configure

Copy `.env.example` to `.env` (backend) and `src/ui/.env.example` to `src/ui/.env` (frontend `PUBLIC_API_BASE`). The backend reads `DATABASE_URL`, `S3_*`, and `AUTH_SECRET` from `.env` — credentials are never hardcoded.

### 3. Run migrations

```sh
uv run alembic upgrade head
```

### 4. Run the backend

```sh
uv run fastapi dev src/core/main.py
```

The API is served at <http://localhost:8000>, with interactive docs at <http://localhost:8000/docs>.

### 5. Run the frontend

```sh
cd src/ui
npm install
npm run dev
```

The app is served at <http://localhost:5173>, and the backend CORS config already allows this origin.

## Useful commands

| Command                              | What it does                              |
| ------------------------------------ | ----------------------------------------- |
| `docker compose up -d`               | Start local Postgres + MinIO              |
| `uv run alembic upgrade head`        | Apply database migrations                 |
| `uv run fastapi dev src/core/main.py`| Run the FastAPI backend                   |
| `uv run pytest`                      | Run the backend test suite                |
| `npm run dev` (in `src/ui`)          | Run the SvelteKit dev server              |
| `npm run check` (in `src/ui`)        | Type-check the frontend                   |
| `npm test` (in `src/ui`)             | Run the frontend Vitest suite             |

## Frames

Frames are **not** a database table or a backend concern — they are a fixed, frontend-owned set. Each frame is a static PNG overlay plus a `FrameDefinition` entry:

- Type definitions live in `src/ui/src/lib/frames/types.ts`. `FrameId` is the stable vocabulary (`VINTAGE`, `POLAROID`, `FILM`, `CLASSIC`).
- The registry `src/ui/src/lib/frames/frames.ts` maps each id to its overlay image, photo count, canvas size, and photo-slot rectangles.
- Adding a frame = drop the PNG in `static/frames/` and add one entry to the registry. No per-frame component, no backend/DB change, no migration.
- Capture logic reads only `photoCount`; composition reads the full definition.

**Currently registered:** `FILM` (35mm film strip, 4 photos, 1620×2880 canvas). Only `test.png` exists as a dev placeholder — real artwork comes from the designers.

## Architecture notes

- **Privacy first:** captured webcam frames and the composed result stay client-side. No DB record exists just for opening the photobooth, and guest photos are never uploaded unless the user actively chooses to save. Saved photos travel over TLS in production and live in the user's private object-storage prefix.
- **Client-side booth state:** the frame → capture → result flow lives in module-scoped runes (`store.svelte.ts`) and resets on reload. A guarded state machine (`session.ts`) makes illegal transitions (e.g. duplicate captures) impossible.
- **Auth is only for persistence:** Argon2-hashed passwords, stateless signed JWTs, no server-side session table. Logout is the client discarding its token.
- **Data model stays small:** `User` (id, email, password_hash, created_at) and `Photo` (id, user_id, frame, storage_key, created_at). No persistent session model, no Frame table.
- **Storage:** object storage holds images; Postgres holds only metadata + server-generated `storage_key` (e.g. `users/{user_id}/photos/{photo_id}.webp`). The client never chooses the path, and every photo read/delete verifies ownership first.
- **Server derives identity:** the backend never trusts a client-supplied user ID; the current user always comes from the Bearer token.
- **Encryption status:** transport security, auth, authorization, and storage security are in place. Photos are **not** client-side encrypted — the server (and an operator with the storage keys) can read saved images. True end-to-end privacy via client-side encryption is a deliberate later stage, not yet implemented.
