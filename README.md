# Trello Clone

This is a Trello clone project with a FastAPI backend and a frontend.
## Setup Instructions

### Backend Setup

1. Create a virtual environment:
   ```
   python -m venv backend/venv
   ```

2. Activate the virtual environment:
   ```
   backend/venv/Scripts/activate
   ```

3. Install dependencies:

   ```
   pip install fastapi uvicorn[standard] sqlalchemy alembic psycopg2-binary python-dotenv pydantic-settings
   ```
   pip install -r backend/requirements.txt
   ```
   pip freeze > backend/requirements.txt

### Frontend Setup

The frontend is currently empty. Add your frontend code here.

### Running the Project

To run the backend:
```
uvicorn main:app --reload
```
(Note: Adjust the main file name as needed)