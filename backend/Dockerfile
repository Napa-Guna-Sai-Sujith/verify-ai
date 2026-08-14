FROM python:3.11-slim

# Install system dependencies including Tesseract OCR and language packs
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-kan \
    tesseract-ocr-tel \
    tesseract-ocr-tam \
    tesseract-ocr-hin \
    tesseract-ocr-eng \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port and run uvicorn
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
