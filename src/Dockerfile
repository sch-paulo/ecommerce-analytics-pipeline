# ETL Dockerfile
FROM python:3.12

WORKDIR /app

COPY config /app/config
COPY data /app/data
COPY schema /app/schema
COPY src /app/src

COPY ../src/requirements.txt /app/src/requirements.txt
RUN pip install --no-cache-dir -r /app/src/requirements.txt

ENV PYTHONPATH=/app

CMD ["python", "src/load_to_db.py"]
