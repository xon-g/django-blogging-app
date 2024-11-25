# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Install npm
RUN apt-get update && apt-get install -y npm postgresql-client

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=app.settings

# Run npm install and build
RUN npm install --prefix /app/theme/static_src
RUN npm run build --prefix /app/theme/static_src

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
