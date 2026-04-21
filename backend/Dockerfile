# Use a lightweight Python image
FROM python:3.11-slim

WORKDIR /app

# OpenCV requires specific system libraries to process video frames in Linux
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install gdown and fetch the YOLOv8 model from your Google Drive
# (Replace the ID with your actual GDrive YOLOv8.pt link)
RUN pip install gdown==4.7.3 && \
    gdown "https://drive.google.com/file/d/1LnpDiyhXziFG2Y5yNHsYJQB2PG5bwavU/view?usp=sharing" -O model.pt

# Copy the rest of the backend application
COPY . .

# Expose the Render port
EXPOSE 10000

# Boot the FastAPI server
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "10000"]