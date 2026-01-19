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

### Docker (Recommended)

```bash
# 1. Copy environment file
cp .env.example .env

# 2. Start services (PostgreSQL + API)
docker-compose up --build

# 3. Run migrations
docker-compose exec api python manage.py migrate

# 4. Load sample data
docker-compose exec api python manage.py loaddata initial_data

# 5. Create superuser
docker-compose exec api python manage.py createsuperuser
```

API available at: http://localhost:8000

### Local Development

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your database credentials

# 4. Run migrations and load data
python manage.py migrate
python manage.py loaddata initial_data

# 5. Run server
python manage.py runserver
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
  -d '{"username": "admin", "password": "admin"}'

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
- **Nested Data**: Client detail includes credits with bank info

## Sample Data

Load fixtures with sample data:

```bash
python manage.py loaddata initial_data
```

Includes: 5 banks, 10 clients, 23 credits

## Postman Collection

Import `postman_collection.json` into Postman for ready-to-use API requests.

## Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=apps --cov-report=html
```

## Project Structure

```
your_credit/
├── apps/
│   ├── banks/          # Bank management
│   ├── clients/        # Client management
│   ├── credits/        # Credit management
│   └── core/           # Base models & fixtures
├── your_credit/        # Project settings
├── docker-compose.yml
├── Dockerfile
├── postman_collection.json
└── requirements.txt
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Debug mode | `False` |
| `SECRET_KEY` | Django secret key | - |
| `ALLOWED_HOSTS` | Allowed hosts | `localhost,127.0.0.1` |
| `POSTGRES_DB` | Database name | `your_credit` |
| `POSTGRES_USER` | Database user | `postgres` |
| `POSTGRES_PASSWORD` | Database password | `postgres` |
| `POSTGRES_HOST` | Database host | `db` |
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
