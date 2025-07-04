# Dockerfile
FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Run migrations on startup (optional)
CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
