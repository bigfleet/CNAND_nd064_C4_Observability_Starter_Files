# Use the official Python image.
# https://hub.docker.com/_/python
FROM mcr.microsoft.com/devcontainers/python:3.11-bullseye

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME

ARG PROJECT_ID
ENV PROJECT_ID ${PROJECT_ID}

# Cache requirements building layer, grpcio takes forever these days
COPY requirements.txt ./requirements.txt

# Install production dependencies.
RUN apt-get update && apt-get install -y python-dev build-essential gcc && \
    pip install --upgrade pip && \
    python3 -m pip install --upgrade setuptools && \
    pip install -r requirements.txt

COPY . ./

CMD ["gunicorn", "--access-logfile", "-", "--error-logfile", "-", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
