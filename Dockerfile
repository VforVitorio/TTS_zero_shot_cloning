FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies for audio
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /opt/requirements.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /opt/requirements.txt

WORKDIR /opt