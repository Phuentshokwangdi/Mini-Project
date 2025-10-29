# Use an official lightweight Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Copy dependency list first (for build cache optimization)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Expose port 8000 for the Django app
EXPOSE 8000

# Collect static files (optional — recommended for production)
RUN python manage.py collectstatic --noinput || true

# Use Gunicorn as the WSGI server
# Replace `jwt_auth_project` with your actual project name if different
CMD ["gunicorn", "MINI_PROJECT_WEATHER.wsgi:application", "--bind", "0.0.0.0:8000"]
