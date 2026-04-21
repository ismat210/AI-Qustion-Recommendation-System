FROM python:3.11-slim

# ======================================================
# SYSTEM DEPENDENCIES
# ======================================================
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libgl1 \
    libglib2.0-0 \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# ======================================================
# WORKDIR
# ======================================================
WORKDIR /app

# ======================================================
# COPY DEPENDENCIES FIRST (CACHE OPTIMIZATION)
# ======================================================
COPY pyproject.toml uv.lock ./

# install uv
RUN pip install --no-cache-dir uv

# ======================================================
# 🔥 IMPORTANT FIX: FORCE CPU-ONLY TORCH
# ======================================================
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu

# install project dependencies
RUN uv sync

# ======================================================
# COPY SOURCE CODE
# ======================================================
COPY . /app

# ======================================================
# ENV SETTINGS
# ======================================================
ENV PYTHONPATH=/app

# ======================================================
# PORT
# ======================================================
EXPOSE 8000

# ======================================================
# RUN SERVER
# ======================================================
CMD ["uv", "run", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]