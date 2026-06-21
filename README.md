# pyapi

A FastAPI-based application with modular architecture, featuring AI-powered chatbots and GitHub OAuth2 authentication.

## Core Features
- **Modular Architecture:** Organized into `auth`, `users`, `chatbots`, and `roles` modules for maintainability.
- **AI Chatbot Integration:** Interface with AI models (via OpenRouter) to support conversation history and system prompts.
- **GitHub OAuth2 Authentication:** Secure login using GitHub.
- **Database Management:** Uses SQLAlchemy with Alembic for schema migrations.
- **Docker-ready:** Includes `docker-compose.test.yml` for isolated testing environments with MySQL.

## Installation

### Prerequisites
- Python 3.10+
- Docker & Docker Compose (for testing environment)

### Setup
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables (create a `.env` file).
4. Run database migrations:
   ```bash
   alembic upgrade head
   ```

## API Usage

### GitHub Authentication
1. **Initiate Login:** Navigate to `http://127.0.0.1:8000/auth/github`. This redirects to GitHub.
2. **Callback:** Upon success, GitHub redirects to the callback URL (configured in your app settings) which validates the session.

### AI Chatbot
- **Create Chat:** `POST /chat/new`
- **Send Message:** `POST /chat/send/{conversation_id}` (History is automatically managed)
- **View History:** `GET /chat/view/{conversation_id}`

### Swagger Documentation
Once running, access interactive documentation at `http://127.0.0.1:8000/docs`.

## Testing
Run the automated test suite using the provided script:
```bash
bash scripts/test.sh
```
Ensure your test Docker container is running as defined in `docker-compose.test.yml`.
