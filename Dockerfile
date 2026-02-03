# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the package
COPY ga_cli/ ./ga_cli/
COPY setup.py .
COPY README.md .

# Install the package
RUN pip install --no-cache-dir .

# Create directory for credentials
RUN mkdir -p /root/.ga-cli

# Set entrypoint
ENTRYPOINT ["ga-cli"]

# Default command shows help
CMD ["--help"]
