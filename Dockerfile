# Use an official Python runtime as a parent image
FROM python:3.12.4-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt /app/

# Install the dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the Django project code to the container
COPY . /app/

# Expose port 8000 to allow connections
EXPOSE 80

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
