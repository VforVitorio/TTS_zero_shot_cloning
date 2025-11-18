FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies for audio and compilation
RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    libsndfile1 \
    espeak-ng \
    git \
    && rm -rf /var/lib/apt/lists/*

# espeak-ng is required for VITS model phonemization

COPY requirements.txt /opt/requirements.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /opt/requirements.txt

WORKDIR /opt