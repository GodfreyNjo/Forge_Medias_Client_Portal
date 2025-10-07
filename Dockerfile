FROM python:3.11-slim

WORKDIR /app

# Copy backend requirements and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Copy frontend directory
COPY frontend/ ./frontend/

EXPOSE 8000
CMD ["python", "main.py"]
