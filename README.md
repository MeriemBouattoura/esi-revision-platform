# ESI Revision Platform

A student-focused revision platform for École supérieure d'informatique (ESI), Algiers. Phase one includes curriculum navigation APIs, PDF document management, moderated question suggestions, server-graded quizzes, preparation statistics, personal to-do lists, authentication, and a responsive frontend shell. Social features are intentionally reserved for phase two.

## Architecture

- **Backend:** Python 3.12, FastAPI, SQLAlchemy 2 typed ORM, Alembic, Pydantic v2, PostgreSQL 16, JWT access tokens, bcrypt.
- **Frontend:** React 18, Vite, React Router 6, Tailwind CSS, Axios, TanStack Query.
- **Services:** Docker Compose runs PostgreSQL, the auto-reloading API, and the auto-reloading web client.
- **API:** `/api/v1`; interactive OpenAPI UI at [http://localhost:8000/docs](http://localhost:8000/docs).

## Run with Docker Compose

1. Copy `.env.example` to `.env`. Change `POSTGRES_PASSWORD` and `JWT_SECRET` before deploying or sharing a development environment.
2. Start the services from the project root:

   ```sh
   docker compose up --build
   ```

   The backend container applies Alembic migrations on startup. The frontend is at [http://localhost:5173](http://localhost:5173), and the API is at [http://localhost:8000](http://localhost:8000).
3. In another terminal, seed the curriculum and demo accounts:

   ```sh
   docker compose exec backend python seed.py
   ```

   Demo sign-in: `admin@esi.dz` / `ESIrevision2026!` and `student@esi.dz` / `ESIrevision2026!`. Change these credentials for any non-disposable environment.

The backend and frontend source directories are mounted into their containers for hot reload. Uploaded PDFs are kept in the named `uploads` volume; PostgreSQL data is kept in `postgres_data`.

## Migrations

The initial schema migration is `backend/alembic/versions/0001_initial.py`.

```sh
docker compose exec backend alembic upgrade head
docker compose exec backend alembic current
```

## Tests

Backend tests use an isolated in-memory SQLite database and exercise account registration/login, admin-only routes, quiz answer privacy and grading, weighted preparation statistics, and todo ownership.

```sh
docker compose run --rm backend pytest -q
```

## API outline

- Authentication: `POST /api/v1/auth/register`, `POST /api/v1/auth/login`, `GET /api/v1/auth/me`.
- Academics: `/api/v1/years`, `/api/v1/years/{id}/semesters`, `/api/v1/semesters/{id}/modules`, `/api/v1/modules/{id}`.
- Courses and questions: `/api/v1/modules/{id}/courses`, `/api/v1/courses`, `/api/v1/questions`.
- Quizzes: `/api/v1/quizzes/generate`, `/api/v1/quizzes/submit`, `/api/v1/quizzes/history`.
- Statistics and tasks: `/api/v1/modules/{id}/stats`, `/api/v1/todos`.

## Next steps

The UI currently provides the authenticated shell and placeholder destinations. The next frontend phase is to build the course/PDF revision experience, quiz setup and play flow, and module preparation statistics screens.
