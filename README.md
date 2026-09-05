# Chewables

A privacy-conscious photobooth web app. Guests can use the full experience — frame selection, webcam capture, Canvas composition, download — with no account. Authentication is only required to permanently save a finished photo.

> **Status:** Early scaffolding. The backend (FastAPI) and frontend (SvelteKit) run independently, and the photobooth flow itself is not built out yet.

## Stack

| Layer    | Technology                                                        |
| -------- | ----------------------------------------------------------------- |
| Backend  | Python 3.14, FastAPI, SQLAlchemy 2 (async) + asyncpg, Pydantic v2 |
| Frontend | SvelteKit (Svelte 5, runes), TypeScript, Vite                     |
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
  src/routes/     +page.svelte (landing), photobooth/+page.svelte (placeholder)
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

| Command                        | What it does                              |
| ------------------------------ | ----------------------------------------- |
| `docker compose up -d`         | Start local Postgres                      |
| `uv run chewable`              | Run the FastAPI backend                   |
| `npm run dev` (in `src/ui`)    | Run the SvelteKit dev server              |
| `npm run check` (in `src/ui`)  | Type-check the frontend                   |
| `uv run pytest`                | Run backend tests (when tests exist)      |

## Architecture notes

- **Privacy first:** captured webcam images and the composed result stay client-side. No database record is created just because someone opened the photobooth, and guest photos are never uploaded unless the user actively chooses to save.
- **Frames are not a database table.** They're a fixed frontend-owned set (VINTAGE, POLAROID, FILM, CLASSIC).
- **Data model stays small:** `User` (id, email, password_hash, created_at) and `Photo` (id, user_id, frame, storage_key, created_at). No persistent session model.
- **Storage:** object storage holds images; Postgres holds only metadata plus a server-generated `storage_key` (e.g. `users/{user_id}/photos/{photo_id}.webp`). The client never chooses the path.
- **Server derives identity:** the backend never trusts a client-supplied user ID; the current user always comes from the auth mechanism.
