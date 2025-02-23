# Use a lightweight Python image
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Ensure instance directory exists for SQLite persistence
RUN mkdir -p /app/instance

# Expose the Flask port
EXPOSE 5000

# Run the Flask application
CMD ["python", "run.py"]
