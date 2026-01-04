# AnythingAI Tasks Backend API

A scalable REST API for task management with authentication and role-based access control built with FastAPI, SQLAlchemy, and JWT.

## Features

- **User Authentication**: Secure JWT-based authentication with password hashing
- **Task Management**: Full CRUD operations for task management
- **Role-Based Access Control**: Admin and regular user roles
- **Database**: SQLAlchemy ORM with SQLite
- **CORS Support**: Configured for local frontend development
- **API Documentation**: Auto-generated Swagger UI and ReDoc
- **Frontend Dashboard**: Simple HTML/JavaScript dashboard for task management

## Project Structure

See main repository for complete structure.

## Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate: `source venv/bin/activate` (Windows: `venv\Scripts\activate`)
4. Install: `pip install -r requirements.txt`
5. Run: `uvicorn app.main:app --reload`

## API Endpoints

### Authentication
- POST /api/v1/auth/register - Register new user
- POST /api/v1/auth/login - Login and get JWT token

### Tasks
- POST /api/v1/tasks/ - Create task
- GET /api/v1/tasks/ - List all tasks
- GET /api/v1/tasks/my-tasks - Get user's tasks
- GET /api/v1/tasks/{id} - Get task by ID
- PUT /api/v1/tasks/{id} - Update task
- DELETE /api/v1/tasks/{id} - Delete task

## Documentation


**Note:** These URLs are for local development. After starting the server with `uvicorn app.main:app --reload`, access the documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Database

Uses SQLite by default. Includes User and Task models with relationships.

## Security

- Passwords hashed with bcrypt
- JWT token authentication
- Input validation with Pydantic
- SQL Injection protected by ORM

## License

MIT License
