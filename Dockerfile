FROM docker.io/library/python:3.10-slim

# Set folder kerja di dalam kontainer
WORKDIR /app

# Copy file requirements dari laptop/pi ke dalam kontainer
COPY requirements.txt .

# Install semua library yang ada di list kamu
RUN pip install --no-cache-dir -r requirements.txt

# (Opsional) Copy sisa kodingan kamu
COPY . .