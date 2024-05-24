# Use an official Python runtime as a parent image
FROM python:3.10-slim

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

# Expose port 8080 to the outside world
EXPOSE 8080

# Migrate
CMD ["flask", "db", "upgrade"]

# Run the application
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8080", "wsgi:app"]
