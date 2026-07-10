# ===============================
# Base Image
# ===============================
FROM python:3.12-slim

# ===============================
# Environment
# ===============================
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ===============================
# Working Directory
# ===============================
WORKDIR /app

# ===============================
# Install System Dependencies
# ===============================
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# ===============================
# Install Python Dependencies
# ===============================
COPY requirements.txt .

RUN pip install --upgrade pip

# Install CPU-only PyTorch
RUN pip install \
    torch torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/cpu

# Install the rest of the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ===============================
# Copy Project
# ===============================
COPY . .

# ===============================
# Expose FastAPI Port
# ===============================
EXPOSE 8000

# ===============================
# Start FastAPI
# ===============================
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]