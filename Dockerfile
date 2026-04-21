# Use a lightweight Python base image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and force stdout logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies required by OpenCV and Ultralytics
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download the YOLO model directly from your Google Drive link
# This prevents GitHub from blocking your push due to large file sizes!
RUN gdown 1HJbaMj-Q9CxmaDEyWtrdgwvdapnPBTcp -O /app/yolov8s.pt

# Copy the rest of your backend code into the container
COPY ./backend /app/backend

# Expose the port FastAPI will run on
EXPOSE 8000

# Start the FastAPI server on 0.0.0.0 so Render can route traffic to it
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]