# Containerized Django Blog Web App

This is a Django web application configured to run in a Dockerized environment with PostgreSQL as the database and Nginx as reverse proxy server. The setup uses Docker Compose to manage services.

## Features

1. Django development server with hot-reloading.
2. Django Rest Framework
3. PostgreSQL 14 as the database.
4. Nginx server.
5. Docker Compose for service orchestration.
6. Automatic database initialization and application startup.
7. HTMX and Jquery
8. Tailwind CSS and DaisyUI
9. User Authentication

## Usage

1. Populate the `.env` file accordingly. See the `.env-example` as reference.
2. Build and start the service by running `docker compose up`
3. Access the application in your browser at `http://localhost:8000`

## Run Migrations

```bash
docker exec -it django_app python manage.py migrate
```

## Seeders

To seed users, posts, and comments data:

```bash
docker exec -it django_app python manage.py seed_data
```

## Tests

```bash
docker exec -it django_app python manage.py test
```
