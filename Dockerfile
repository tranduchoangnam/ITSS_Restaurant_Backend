
FROM python:3.11-slim AS python-base

ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.4.1 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    # paths
    # this is where our requirements + virtual environment will stored
    PYSETUP_PATH="/workspace" \
    VENV_PATH="/workspace/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM python-base AS poetry-base
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    # deps for installing poetry
    curl

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python

# `builder-base` stage is used to build deps + create our virtual environment
FROM poetry-base AS builder-base
RUN apt-get update && \
    apt-get install --no-install-recommends -y  \
    # deps for building python deps
    build-essential \
    libpq-dev

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml README.md ./

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --only main


# Development Stage
FROM python-base AS development

# Copy môi trường ảo và Poetry
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base /workspace/.venv /workspace/.venv

# Cài đặt thư viện cần thiết
RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# Mount mã nguồn và cache thư viện (sẽ dùng volumes từ docker-compose)
COPY . .

# Mở cổng cho FastAPI
EXPOSE 8000

# Run FastAPI
CMD ["poetry", "run", "uvicorn", "backend.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
