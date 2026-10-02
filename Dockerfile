FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_HOME=/app \
    GUNICORN_WORKERS=3 \
    GUNICORN_THREADS=1 \
    GUNICORN_TIMEOUT=120 \
    GUNICORN_KEEPALIVE=5 \
    GUNICORN_LOG_LEVEL=info \
    GUNICORN_ACCESSLOG=- \
    GUNICORN_ERRORLOG=-

WORKDIR ${APP_HOME}

COPY requirements.txt .

# Optional build-time proxy
ARG HTTP_PROXY=""
ARG HTTPS_PROXY=""

RUN HTTP_PROXY="${HTTP_PROXY}" HTTPS_PROXY="${HTTPS_PROXY}" \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD sh -c '\
PROJECT_MODULE=$(find . -type f -name "wsgi.py" | head -n 1 | sed "s#^\./##" | cut -d"/" -f1) && \
if [ -z "$PROJECT_MODULE" ]; then \
  echo "Error: could not detect Django project module (wsgi.py not found)"; \
  exit 1; \
fi && \
python manage.py migrate && \
python manage.py collectstatic --noinput && \
exec gunicorn "${PROJECT_MODULE}.wsgi:application" \
  --bind 0.0.0.0:8000 \
  --workers "${GUNICORN_WORKERS}" \
  --threads "${GUNICORN_THREADS}" \
  --timeout "${GUNICORN_TIMEOUT}" \
  --keep-alive "${GUNICORN_KEEPALIVE}" \
  --log-level "${GUNICORN_LOG_LEVEL}" \
  --access-logfile "${GUNICORN_ACCESSLOG}" \
  --error-logfile "${GUNICORN_ERRORLOG}"'