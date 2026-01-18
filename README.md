# Your Credit API

REST API for managing credits, clients, and banks built with Django REST Framework.

## Tech Stack

- **Python 3.12** + **Django 6.0**
- **Django REST Framework** - API development
- **PostgreSQL** - Database
- **JWT Authentication** - via `djangorestframework-simplejwt`
- **drf-spectacular** - OpenAPI/Swagger documentation
- **pytest** - Testing framework
- **Docker** - Containerization

## Quick Start

### Local Development

```bash
# 1. Clone and navigate
cd your_credit

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your database credentials

# 5. Run migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Run server
python manage.py runserver
```

### Docker

```bash
# Development
docker-compose up --build

# Production
cp .env.prod.example .env.prod
# Edit .env.prod with production values
docker-compose -f docker-compose.prod.yml up -d --build
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `POST /api/login/` | Obtain JWT token |
| `POST /api/login/refresh/` | Refresh JWT token |
| `/api/clientes/` | Clients CRUD |
| `/api/creditos/` | Credits CRUD |
| `/api/bancos/` | Banks CRUD |
| `/api/docs/` | Swagger UI |
| `/api/schema/` | OpenAPI schema |

## Authentication

All endpoints require JWT authentication.

```bash
# Get token
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_user", "password": "your_pass"}'

# Use token
curl -H "Authorization: Bearer <access_token>" \
  http://localhost:8000/api/clientes/
```

## Features

- **Pagination**: 10 items per page (`?page=2`)
- **Filtering**: `?credit_type=MORTGAGE`, `?person_type=INDIVIDUAL`
- **Search**: `?search=john`
- **Ordering**: `?ordering=-created_at`
- **Soft Delete**: Records are not physically deleted

## Testing

```bash
# Install test dependencies
pip install pytest pytest-django

# Run all tests
pytest

# Verbose output
pytest -v

# Specific app
pytest apps/banks/tests.py
```

## Project Structure

```
your_credit/
├── apps/
│   ├── banks/          # Bank management
│   ├── clients/        # Client management
│   ├── credits/        # Credit management
│   └── core/           # Base models
├── your_credit/        # Project settings
├── docker-compose.yml  # Dev Docker config
├── docker-compose.prod.yml
├── Dockerfile
├── requirements.txt
└── pytest.ini
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Debug mode | `False` |
| `SECRET_KEY` | Django secret key | - |
| `ALLOWED_HOSTS` | Allowed hosts | `localhost,127.0.0.1` |
| `POSTGRES_DB` | Database name | `your_credit` |
| `POSTGRES_USER` | Database user | `postgres` |
| `POSTGRES_PASSWORD` | Database password | - |
| `POSTGRES_HOST` | Database host | `localhost` |
| `POSTGRES_PORT` | Database port | `5432` |

## Security

- JWT authentication with 1-hour access token lifetime
- Content Security Policy (CSP) headers
- Permissions Policy headers
- Soft delete for data retention

## AI Usage

This project was developed with AI assistance (Claude/Antigravity).

**AI helped with:**

- Security headers Configurations 
- Unit tests 
- Documentation

**Why AI?**

Accelerates repetitive tasks and suggests best practices, allowing focus on architecture and business decisions.

## License

MIT
