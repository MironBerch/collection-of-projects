FROM python:3.13-alpine

RUN apk add --no-cache \
    ffmpeg \
    # Для pydub и компиляции:
    make \
    gcc \
    g++ \
    musl-dev \
    flac

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

COPY pyproject.toml uv.lock* ./

RUN uv sync

COPY . .
