# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

ARG PYTHON_VERSION=3.9.2
FROM python:${PYTHON_VERSION}-slim as base

# Expose the port that the application listens on.
EXPOSE 8000


WORKDIR /app

# Copy the source code into the container.
COPY . /app

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Run the application.
CMD uvicorn 'service.api:app' --host=0.0.0.0 --port=8000
