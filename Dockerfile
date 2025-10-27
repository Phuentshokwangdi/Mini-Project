# Use an official Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Expose port 8000 for Django app
EXPOSE 8000

# Run Django using Gunicorn (recommended for production)
CMD ["gunicorn", "MINI_PROJECT_WEATHER.wsgi:application", "--bind", "0.0.0.0:8000"]
