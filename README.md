## Flogg.

📝 Flog (Blog-Flog) Application is a high-performance, containerized blogging platform built with

- **Python 3.12**
- Django
- PostgreSQL 

## Feature

- Markdown Enabled Story teller
- AI Conversion feature to study and understand the blog in any context user wants.
- **Git** like **CLI tools** to manage notes/blogs/story in a central repository.

## AI-Feature demo

![Demo Video](./contents/Screen%20Recording%202026-04-15%20at%209.12.11 PM.mov)




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