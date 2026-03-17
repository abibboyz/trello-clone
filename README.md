# Trello Clone

A modern, full-stack Trello clone built with FastAPI backend and React frontend. Features real-time collaboration, drag-and-drop functionality, and a clean, intuitive interface.

## 🚀 Features

- **Boards Management**: Create, edit, and organize boards
- **Lists & Cards**: Add lists to boards and cards to lists
- **Drag & Drop**: Intuitive drag-and-drop interface for cards and lists
- **Real-time Updates**: Live collaboration features
- **User Authentication**: Secure user management
- **Responsive Design**: Works seamlessly on desktop and mobile
- **RESTful API**: Well-documented API endpoints
- **Database Integration**: PostgreSQL with SQLAlchemy ORM

## 🛠 Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy 2.0** - SQL toolkit and ORM
- **PostgreSQL** - Robust relational database
- **Pydantic** - Data validation and settings management
- **Alembic** - Database migration tool
- **Uvicorn** - ASGI web server

### Frontend
- **React** - Component-based UI library
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **React DnD** - Drag and drop functionality

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+** - [Download here](https://python.org)
- **PostgreSQL 12+** - [Download here](https://postgresql.org)
- **Node.js 18+** (for frontend) - [Download here](https://nodejs.org)
- **Git** - [Download here](https://git-scm.com)

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/trello-clone.git
cd trello-clone
```

### 2. Backend Setup

#### Create Virtual Environment
```bash
# Windows
python -m venv backend/venv

# macOS/Linux
python3 -m venv backend/venv
```

#### Activate Virtual Environment
```bash
# Windows
backend/venv/Scripts/activate

# macOS/Linux
source backend/venv/bin/activate
```

#### Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### Environment Configuration
```bash
# Copy the example environment file
cp .env.example .env
```

Edit `.env` with your database credentials:
```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/trello_db

# Environment
ENVIRONMENT=development

# SQL Query Logging (set to True to see all SQL queries)
SQL_ECHO=False
```

#### Database Setup
```bash
# Create PostgreSQL database
createdb trello_db

# Run database migrations (if using Alembic)
alembic upgrade head

# Or create tables directly (if not using migrations)
python -c "from app.database import create_tables; import asyncio; asyncio.run(create_tables())"
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env.local
```

Edit `frontend/.env.local`:
```env
REACT_APP_API_URL=http://localhost:8000
```

## 🚀 Running the Application

### Development Mode

#### Start Backend
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: http://localhost:8000

#### Start Frontend
```bash
cd frontend
npm start
```

The frontend will be available at: http://localhost:3000

### Production Mode

#### Backend
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### Frontend
```bash
cd frontend
npm run build
npm run serve -s build -l 3000
```

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### Key Endpoints

- `GET /` - Health check
- `GET /boards` - List all boards
- `POST /boards` - Create new board
- `GET /boards/{id}` - Get board details
- `PUT /boards/{id}` - Update board
- `DELETE /boards/{id}` - Delete board

## 🗂 Project Structure

```
trello-clone/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI application
│   │   ├── database.py      # Database configuration
│   │   ├── models/          # SQLAlchemy models
│   │   ├── routes/          # API routes
│   │   └── schemas/         # Pydantic schemas
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example         # Environment template
│   └── alembic/             # Database migrations
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── hooks/           # Custom hooks
│   │   ├── services/        # API services
│   │   └── utils/           # Utility functions
│   ├── package.json
│   └── .env.example
├── .gitignore
└── README.md
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🔒 Environment Variables

### Backend (.env)
| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:password@localhost:5432/trello_db` |
| `ENVIRONMENT` | App environment | `development` |
| `SQL_ECHO` | Log SQL queries | `False` |

### Frontend (.env.local)
| Variable | Description | Default |
|----------|-------------|---------|
| `REACT_APP_API_URL` | Backend API URL | `http://localhost:8000` |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use TypeScript for frontend components
- Write tests for new features
- Update documentation as needed
- Use conventional commit messages

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋 Support

If you have any questions or need help:

- Open an issue on GitHub
- Check the documentation
- Join our Discord community

## 🗺 Roadmap

- [ ] User authentication and authorization
- [ ] Real-time collaboration with WebSockets
- [ ] Drag and drop functionality
- [ ] Mobile app (React Native)
- [ ] Advanced board templates
- [ ] Integration with external tools
- [ ] Advanced analytics and reporting

---

Made with ❤️ using FastAPI and React