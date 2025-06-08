#!/bin/bash

# Run Flask app locally with uv

echo "Installing dependencies with uv..."
uv pip install --system flask>=3.0.0

echo "Creating necessary directories..."
mkdir -p static js templates

echo "Starting Flask server..."
python app.py