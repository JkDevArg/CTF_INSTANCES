FROM python:3.11-slim
RUN apt-get update && apt-get install -y gcc binutils libc-dev --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*
RUN pip install flask --no-cache-dir
WORKDIR /app
COPY app/ .
RUN chmod +x entrypoint.sh
EXPOSE 80
ENTRYPOINT ["./entrypoint.sh"]
