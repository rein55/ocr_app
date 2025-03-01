# Dockerfile
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies sistem (misal: build-essential)
RUN apt-get update && apt-get install -y build-essential

# Copy requirements.txt dan install dependencies Python
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy seluruh project
COPY . .

# Expose port untuk FastAPI (misalnya 8000)
EXPOSE 8000

# Perintah default untuk menjalankan FastAPI
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]

# Jika ingin menjalankan aplikasi Streamlit via Docker, ganti CMD-nya menjadi:
# CMD ["streamlit", "run", "streamlit_app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
