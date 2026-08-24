FROM python:3.11-slim

WORKDIR /app

# Install system dependencies required for packet capture
RUN apt-get update && apt-get install -y \
    tcpdump \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python setup.py install

EXPOSE 8000

CMD ["uvicorn", "src.dashboard:app", "--host", "0.0.0.0", "--port", "8000"]
