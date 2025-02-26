# Perform common operations, dependency installation etc...
FROM python:3.12.1 AS base
# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
# Add Environment variable
ENV PATH=$PATH:/root/.local/bin/
# Set work directory
WORKDIR /
# Copy across pyproject.toml
COPY poetry.lock pyproject.toml /
# Install poetry
RUN poetry install --no-root
# Copy across application code as the last step to optimise building process
COPY . /


# Configure for development
FROM base AS development
ENV FLASK_DEBUG=true
ENTRYPOINT poetry run flask run --host 0.0.0.0


# Configure for production
FROM base AS production
ENV FLASK_DEBUG=false 
# ^^ overriden by the settings in .env file
ENTRYPOINT poetry run flask run --host 0.0.0.0


# Configure for test
FROM base AS test
WORKDIR /todo_app
ENTRYPOINT poetry run pytest


# Configure for dependency check
FROM base AS dependency-check
WORKDIR /todo_app
ENTRYPOINT poetry run safety check