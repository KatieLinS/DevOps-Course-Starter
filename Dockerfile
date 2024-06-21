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
RUN poetry install
# Copy across application code as the last step to optimise building process
COPY . /


# Configure for local development
FROM base AS development
ENV FLASK_DEBUG=true
ENTRYPOINT poetry run flask run --host 0.0.0.0


# Configure for production
FROM base AS production
ENV FLASK_DEBUG=false 
# ^^ overriden by the settings in .env file
ENTRYPOINT poetry run flask run --host 0.0.0.0


# Configure for testing
# FROM base AS testing
# ENTRYPOINT poetry run flask run --host 0.0.0.0