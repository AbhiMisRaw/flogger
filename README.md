## Flogg.
📝 Flog (Blog-Flog) AppFlog is a high-performance, containerized blogging platform built with

- **Python 3.12**
- Django
- PostgreSQL 

It is architected for production-grade stability using **Gunicorn** as the application server and Nginx as a reverse proxy to serve static assets efficiently.

## 🚀 FeaturesModern Backend: 
Powered by Django and Poetry for dependency management.Production Ready: Multi-stage Docker setup with Nginx and Gunicorn.Automated Workflow: Custom entrypoint.sh handles database migrations and static file collection automatically on startup.Secure Networking: Isolated database and application containers; only Nginx is exposed to the public.

🛠 Prerequisites 
- Docker/Docker Compose
- Poetry (for local development) 

### Installation & Setup

1. Clone the repositoryBashgit clone https://github.com/abhidevmishra/blog-flog.git
cd blog-flog

2. Configure Environment VariablesCreate a .env file in the root directory. This file is ignored by git to keep your secrets safe.
```Plaintext
DEBUG=True
SECRET_KEY=your-super-secret-key
DB_NAME=django_db
DB_USER=django_user
DB_PASSWORD=django_pass
DB_HOST=db
DB_PORT=5432
SENTRY_DSN=your-sentry-dsn
```

3. Build and Start the ContainersUse Docker Compose to build the images and spin up the services.
```Bash
docker compose up --build -d
```
The entrypoint.sh script will automatically run 
```bash
python manage.py migrate
``` 
and 
```bash
python manage.py collectstatic
```

### 🌐 Architecture Overview

The application is split into three main services defined in `docker-compose.yml:ServiceTechnologyRoleWebDjango + GunicornHandles` business logic and API requests. `DBPostgreSQL 15` Persistent relational data storage.Nginx `NginxReverse proxy & serves files from static_volume. 

### 🔧 Useful CommandsView Logs:

```Bash
docker compose logs -f web
```

Run Migrations Manually:
```Bash
docker compose exec web python manage.py migrate
```
Create a Superuser:
```Bash
docker compose exec web python manage.py createsuperuser
```

Clean Slate (Remove Volumes):
```Bash
docker compose down -v
```