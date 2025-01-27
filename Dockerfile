
ARG PYTHON_VERSION=3.9.2
FROM python:${PYTHON_VERSION}-slim-buster as base

ARG REDIS_HOST
ARG REDIS_KEY

ENV REDIS_HOST=${REDIS_HOST}
ENV REDIS_KEY=${REDIS_KEY}


# Expose the port that the application listens on.
EXPOSE 8000

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE = 1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED = 1

WORKDIR /app

# Copy the source code into the container.
COPY . /app

COPY docker_requirements.txt .
RUN pip install --no-cache-dir -r docker_requirements.txt 

# Run the application.
CMD uvicorn prod.api:app --host=0.0.0.0 --port=8000
