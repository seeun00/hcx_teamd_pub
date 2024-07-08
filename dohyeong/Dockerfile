# Base image
FROM python:3.9-slim

# Install tini
RUN apt-get update && apt-get install -y tini

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Create working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app/

# Expose ports
EXPOSE 8000
EXPOSE 8501

# Use tini as the entry point to manage processes
ENTRYPOINT ["/usr/bin/tini", "--"]

# Start FastAPI and Streamlit
CMD ["sh", "-c", "uvicorn fastapi_app:app --host 0.0.0.0 --port 8000 & streamlit run streamlit_app.py --server.port 8501 --server.enableCORS false"]
