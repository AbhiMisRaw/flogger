FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy dependency files first to leverage Docker's layer caching
COPY pyproject.toml poetry.lock ./

# Install Poetry and dependencies
RUN pip3 install poetry gunicorn && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

COPY . .
# Everything here is initialized by poetry run
RUN chmod +x /app/entrypoint.sh

# Use the script as the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# This is your default production command
CMD ["gunicorn", "flogger.wsgi:application", "--bind", "0.0.0.0:8000"]