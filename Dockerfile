# Use an official Python runtime as a parent image
FROM python:3.10-slim AS base

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Copy the Docker environment variables file
COPY .env.docker .env

# Set environment variables
ENV FLASK_APP=visual_organizational_structure
ENV FLASK_ENV=development
ENV PYTHONPATH=/app

# Create a stage for testing
FROM base AS test

# Install testing dependencies
RUN pip install pytest

# Set the working directory in the container
WORKDIR /app

# Run tests and print output to console
CMD ["pytest", "/app/tests"]

# Expose port 8080 to the outside world
FROM base AS final
EXPOSE 8080

# Run the application
CMD ["gunicorn", "-c", "gunicorn.conf.py", "wsgi:app"]
