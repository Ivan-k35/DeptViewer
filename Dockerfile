
FROM python:3.12

ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/


RUN pip install --no-cache-dir -r requirements.txt


COPY . /app/

EXPOSE 8000
