# Trello Clone

A full-stack Trello-style project with a FastAPI backend and a React frontend.

This README has been updated to match the current backend behavior, route architecture, error handling, and test layout.

## Features

- Board, list, and card creation flow
- Relational model workflow: Board -> List -> Card
- FastAPI OpenAPI docs at /docs
- Async SQLAlchemy services
- Separate API test suite for endpoint coverage

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy 2.x (async)
- Pydantic v2
- PostgreSQL (default)
- Uvicorn
- Pytest and pytest-asyncio

### Frontend
- React
- TypeScript
- Tailwind CSS

## Prerequisites

- Python 3.9+
- PostgreSQL 12+
- Node.js 18+
- Git

## Setup

### 1. Clone

```bash
git clone https://github.com/yourusername/trello-clone.git
cd trello-clone
```

### 2. Backend

```bash
# from repo root
python -m venv backend/venv

# Windows
backend\venv\Scripts\activate

# macOS/Linux
source backend/venv/bin/activate

cd backend
pip install -r requirements.txt
```

Create .env in backend/ with values such as:

```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/trello_db
ENVIRONMENT=development
SQL_ECHO=False
```

Create tables (without Alembic migrations):

```bash
python -c "from app.core.database import create_tables; import asyncio; asyncio.run(create_tables())"
```

### 3. Frontend

```bash
cd ../frontend
npm install
```

## Run

### Backend

```bash
cd backend
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm start
```

## API Docs

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI: http://localhost:8000/openapi.json

## Current API Endpoints

- GET /
- POST /boards/
- GET /boards/
- GET /boards/{board_id}
- POST /lists/
- GET /lists/
- GET /lists/{list_id}
- POST /cards/
- GET /cards/
- GET /cards/{card_id}

Notes:
- Router duplication issue was fixed. Endpoints are now clean (no /boards/boards style duplicates).
- Create order must be: board first, then list, then card.

## Error Handling Behavior

The backend now returns controlled API errors instead of raw internal server errors for common invalid states:

- POST /boards/ -> 400 when board title already exists
- POST /lists/ -> 404 when board_id does not exist
- POST /cards/ -> 404 when list_id does not exist
- GET /boards/{board_id} -> 404 when board not found
- GET /lists/{list_id} -> 404 when list not found
- GET /cards/{card_id} -> 404 when card not found

## Backend Architecture

The backend follows a layered pattern:

1. routes layer
- Files under app/routes expose HTTP endpoints.
- They validate HTTP-level behavior and call services.

2. service layer
- Files under app/service contain business logic and DB operations.
- This is where relation checks and transaction handling live.

3. models layer
- Files under app/models define SQLAlchemy ORM entities and relations.

4. schemas layer
- Files under app/schemas define request/response contracts (Pydantic v2).

5. core layer
- app/core/database.py configures engine, session factory, and table utilities.

## How To Start Working In This Project

### Recommended workflow for new contributors

1. Read app/main.py to understand router composition.
2. Open app/routes, then trace each endpoint into app/service.
3. Check model relationships in app/models before changing service logic.
4. Update or add schemas in app/schemas when request/response changes.
5. Add tests first or alongside changes in tests/api_tests.
6. Run tests and verify API docs in /docs.

### Example feature development flow

1. Add or change schema (request/response).
2. Implement service logic with proper DB rollback/error handling.
3. Wire endpoint in route file with response_model and error responses.
4. Add tests in tests/api_tests for success and failure scenarios.
5. Run pytest and manual Swagger checks.

## Project Structure

```text
trello-clone/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── core/
│   │   │   └── database.py
│   │   ├── models/
│   │   │   ├── board.py
│   │   │   ├── list.py
│   │   │   └── card.py
│   │   ├── routes/
│   │   │   ├── boards.py
│   │   │   ├── lists.py
│   │   │   └── cards.py
│   │   ├── schemas/
│   │   │   ├── board.py
│   │   │   ├── list.py
│   │   │   └── card.py
│   │   └── service/
│   │       ├── board_service.py
│   │       ├── list_service.py
│   │       └── card_service.py
│   ├── tests/
│   │   ├── db_tests/
│   │   └── api_tests/
│   ├── requirements.txt
│   └── DATABASE_USAGE.md
├── frontend/
└── README.md
```

## Testing

### Run all backend tests

```bash
cd backend
pytest
```

### Run API tests only

```bash
cd backend
python -m pytest tests/api_tests -q
```

### API tests include

- Board create/get/list/not-found cases
- List create/get/list/not-found cases
- Card create/get/list/not-found cases
- Parent-relation validation cases (board_id/list_id existence)

## Environment Variables

### Backend (.env)

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | SQLAlchemy async connection string | postgresql+asyncpg://user:password@localhost:5432/trello_db |
| ENVIRONMENT | Runtime environment | development |
| SQL_ECHO | SQL log output | False |

## Contributing

1. Create a feature branch.
2. Keep endpoint and service changes consistent.
3. Add or update tests in tests/api_tests.
4. Update README/API notes if behavior changes.
5. Open a pull request.