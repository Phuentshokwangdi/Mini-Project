# Use an official lightweight Python image
FROM python:3.12-slim

# --- Build Arguments (passed from GitHub Actions) ---
ARG SECRET_KEY
ARG DEBUG
ARG OPENWEATHER_API_KEY
ARG JWT_SECRET_KEY

# --- Environment Variables ---
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SECRET_KEY=${SECRET_KEY} \
    DEBUG=${DEBUG} \
    OPENWEATHER_API_KEY=${OPENWEATHER_API_KEY} \
    JWT_SECRET_KEY=${JWT_SECRET_KEY}

# Set work directory
WORKDIR /app

# Copy dependency list first (for cache optimization)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Expose port 8000
EXPOSE 8000

# Collect static files (optional — recommended for production)
RUN python manage.py collectstatic --noinput || true

# Use Gunicorn as the WSGI server
# Replace `MINI_PROJECT_WEATHER` with your actual project folder if different
CMD ["gunicorn", "MINI_PROJECT_WEATHER.wsgi:application", "--bind", "0.0.0.0:8000"]
