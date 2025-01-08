# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
  pkg-config \
  libmariadb-dev \
  gcc \
  && rm -rf /var/lib/apt/lists/*

# Set up the directory structure
RUN mkdir -p /my_backend_app/config /my_backend_app/app

# Set the working directory for the config
WORKDIR /my_backend_app/config


# Install packages
RUN pip install --no-cache-dir Flask
RUN pip install --no-cache-dir debugpy
RUN pip install --no-cache-dir flask_sqlalchemy
RUN pip install --no-cache-dir sqlalchemy_utils
RUN pip install --no-cache-dir mysqlclient
RUN pip install --no-cache-dir scikit-learn
RUN pip install --no-cache-dir pytest

# Set the working directory for the app
WORKDIR /my_backend_app/app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Command to run Flask server
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
