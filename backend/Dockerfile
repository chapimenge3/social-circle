FROM python:3.11-slim-buster

# Create user and group
RUN groupadd -r django && useradd --no-log-init -r -g django django

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set work directory called `app`
RUN mkdir -p /code
WORKDIR /code

# psycopg2 binary dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt /tmp/requirements.txt

RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

# Copy local project
COPY . /code/


# this is to make the user owner same as the host user 
# so that you can have the access to file.
USER 1000:1000

# Expose port 8000
EXPOSE 8000
