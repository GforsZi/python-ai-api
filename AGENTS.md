\
# Agent Instructions for pyapi Repository

This document provides guidance for agents working within this repository to ensure efficient and accurate task completion.

## Core Development Commands

- **Running the application:** The primary way to run the application is likely through `uvicorn`. A common command might be:
  ```bash
  uvicorn app.main:app --reload
  ```
  *Note:* The exact entry point (`app.main:app`) may vary; inspect `app/main.py` for confirmation.

- **Database Migrations (Alembic):**
  - Initialize Alembic: `alembic init alembic` (if not already initialized)
  - Create migration script: `alembic revision -m "migration description"`
  - Apply migrations: `alembic upgrade head`
  - View migration history: `alembic history`

## Testing

- **No explicit test runner configuration found.** Standard Python testing practices are assumed. If tests are present, they can likely be run using:
  ```bash
  pytest
  ```
  *Note:* If `pytest` is not installed, run `pip install pytest` first. It's recommended to inspect the `tests` directory for specific test commands or setup requirements.

## Key Directories and Files

- **`app/`**: Contains the main application logic, structured into modules (e.g., `users`, `chatbots`, `auth`, `roles`).
  - `app/main.py`: Likely the main entry point for the FastAPI application.
  - `app/core/`: Contains core functionalities like database connection (`database.py`) and configuration (`config.py`).
- **`alembic/`**: Manages database migrations.
  - `alembic/versions/`: Contains individual migration scripts.

## Environment and Dependencies

- **`requirements.txt`**: Lists all project dependencies. Use `pip install -r requirements.txt` to install them.
- **Environment Variables:** Configuration is likely managed via environment variables, potentially loaded by `python-dotenv` (indicated by `python-dotenv` in `requirements.txt`). Inspect `app/core/config.py` for details.

## Important Conventions and Quirks

- **API Framework:** The project uses FastAPI, indicating a RESTful API design.
- **Database:** SQLAlchemy is used for ORM, suggesting a relational database backend.
- **AI Integration:** The presence of `openai` and related libraries suggests potential AI-powered features.

## Verification

- After making changes, ensure the application runs without errors and that any modified endpoints function as expected.
- For migrations, verify that `alembic history` shows the new migration and `alembic upgrade head` completes successfully.

# System Instructions
- Always respond, explain, and write code comments in English.
- The user will provide inputs/instructions in Indonesian. Understand it perfectly and execute the coding tasks based on that.
