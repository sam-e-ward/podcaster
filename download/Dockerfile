FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

CMD ["./download.sh"]
