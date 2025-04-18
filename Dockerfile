# Use official Python slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Avoid buffering logs (good for Docker logs)
ENV PYTHONUNBUFFERED=1

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the entire app code into the container
COPY . .

# Expose Flask’s default port
EXPOSE 5000

# Default command to run the Flask app
CMD ["python", "app.py"]
