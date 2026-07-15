# BoilerPlate for FastAPI

A FastAPI boilerplate for ecommerce applications with SQLAlchemy ORM, PostgreSQL, JWT authentication, and Alembic migrations.

## Tech Stack

- **Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Database:** PostgreSQL
- **Auth:** JWT (python-jose) + bcrypt (passlib)
- **Migrations:** Alembic
- **Validation:** Pydantic

## Project Structure

```
app/
├── api/            # Route handlers
│   └── auth.py     # Signup & login endpoints
├── core/           # Business logic
│   ├── config.py   # App settings (DB, JWT, CORS)
│   ├── exceptions.py   # Custom exception classes
│   ├── security.py     # Password hashing & JWT utils
│   └── validators.py   # Input validation functions
├── database/
│   ├── base.py     # SQLAlchemy declarative base
│   └── session.py  # DB engine & session factory
├── model/
│   └── user_model.py   # User ORM model
└── schema/
    └── user_schema.py  # Pydantic request/response schemas
```

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

Copy `.env` and update values:

| Variable | Description |
|----------|-------------|
| `POSTGRES_USER` | Database user |
| `POSTGRES_PASSWORD` | Database password |
| `POSTGRES_HOST` | Database host |
| `POSTGRES_PORT` | Database port |
| `POSTGRES_DB` | Database name |
| `SECRET_KEY` | JWT signing secret |
| `DEBUG` | Enable debug mode |

### 3. Create the database

```bash
createdb -U postgres ecompukar
```

### 4. Run migrations

```bash
alembic upgrade head
```

### 5. Start the server

```bash
uvicorn main:app --reload
```

Server runs at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

## API Endpoints

### Auth

| Method | Path | Description |
|--------|------|-------------|
| POST | `/auth/signup` | Register a new user |
| POST | `/auth/login` | Login, returns JWT |

### Signup

```
POST /auth/signup
Content-Type: application/json

{
    "name": "John Doe",
    "email": "john@example.com",
    "phone_number": "9841234567",
    "password": "StrongPass1!"
}
```

Validation rules:
- **name:** 2–100 characters
- **email:** Valid email format
- **phone_number:** 7–15 digits
- **password:** Min 8 chars, uppercase, lowercase, digit, special character

### Login

```
POST /auth/login
Content-Type: application/json

{
    "email": "john@example.com",
    "password": "StrongPass1!"
}
```

Response:
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer",
    "user": {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com"
    }
}
```

## Migrations

Generate a new migration after model changes:

```bash
alembic revision --autogenerate -m "description"
```

Apply pending migrations:

```bash
alembic upgrade head
```

Rollback one step:

```bash
alembic downgrade -1
```
