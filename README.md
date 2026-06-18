# pyapi

A FastAPI-based application with SQLAlchemy, Alembic for migrations, and modular architecture.

## Installation

### Prerequisites
- Python 3.10+
- MySQL (required by `aiomysql`)

### Setup
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables (create a `.env` file based on your environment needs).
4. Run database migrations:
   ```bash
   alembic upgrade head
   ```
5. Seed initial data (optional):
   ```bash
   python app/seeds.py
   ```

## Running the Application
Start the development server:
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

## API Usage

### Swagger Documentation
FastAPI automatically generates interactive API documentation. Once the server is running, visit:
- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

### Example Request (via `curl`)
If you need to interact with an endpoint (e.g., fetching users):

```bash
curl -X GET "http://127.0.0.1:8000/users" \
     -H "accept: application/json"
```

*Note: Replace `/users` with the actual endpoint path defined in `app/modules/<module>/router.py`.*
