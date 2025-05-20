# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the app code
COPY . .

EXPOSE 8080

# Run the app with Gunicorn for production
CMD ["python", "app.py"]
