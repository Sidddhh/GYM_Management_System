# Use official Python image
FROM python:3.10-slim

# Set working directory in the container
WORKDIR /app

# Copy everything from your project to the container
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port (Flask runs on 5000)
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
