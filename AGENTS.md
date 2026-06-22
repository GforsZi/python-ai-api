# Agent Instructions for pyapi Repository

This document provides guidance for agents working within this repository.

## Core Development Commands

- **Running the application:**
  ```bash
  uvicorn app.main:app --reload
  ```

- **Database Migrations (Alembic):**
  - Create a new migration: `alembic revision -m "description"`
  - Apply latest migrations: `alembic upgrade head`

- **Testing:**
  - Standard test execution: `bash scripts/test.sh`
  - Prerequisites: Ensure the Docker MySQL container defined in `docker-compose.test.yml` is running.

## Key Directories

- **`app/`**: Application source code.
  - **`app/core/`**: Central infrastructure (config, database, seeder).
  - **`app/modules/`**: Feature-specific domain logic (auth, users, chatbots, roles).
    - Each module typically contains: `router.py`, `service.py`, `models.py`, `schemas.py`.
  - **`app/shared/`**: Utilities and dependency injection (e.g., `get_current_user`).
  - **`app/cli/`**: Executable CLI scripts (e.g., `seeds.py`).
- **`tests/`**: Test suite mirroring the `app/` structure.
  - `tests/shared/`: Tests for `app/shared/` utilities.
  - `tests/core/`: Tests for `app/core/` infrastructure.
  - `tests/cli/`: Tests for CLI utilities.
  - Use `conftest.py` for shared fixtures.
- **`scripts/`**: Automation scripts.
  - `test.sh`: Standardized test runner.

## Development Conventions

- **Authentication:** GitHub OAuth2 is implemented in `app/modules/auth/router.py`.
- **API Framework:** FastAPI, using Pydantic for validation and SQLAlchemy for ORM.
- **AI Integration:** Chatbot logic resides in `app/modules/chatbots/router.py` utilizing the `OpenAI` client.
- **Environment:** Secrets are loaded via `dotenv`. Ensure `.env` is populated.

## Verification

- **Lint/Type-Check:** Follow PEP 8 and Python type hinting standards.
- **Testing:** Always ensure new features are covered by tests in `tests/`.
