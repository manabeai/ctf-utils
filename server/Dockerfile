FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy requirements first for better caching
COPY pyproject.toml uv.lock* ./

# Install Python dependencies with uv
RUN uv pip install --system --no-cache flask>=3.0.0

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p static js templates

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]