# Menggunakan image python yang ringan dan stabil untuk runtime production
FROM python:3.11-slim

# Set folder kerja di dalam container
WORKDIR /app

# Install dependency Python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua skrip yang dibutuhkan ke dalam container
COPY *.py ./
COPY entrypoint.sh ./

RUN chmod +x /app/entrypoint.sh

# Jalankan skrip sesuai mode saat container dimulai
CMD ["/app/entrypoint.sh"]