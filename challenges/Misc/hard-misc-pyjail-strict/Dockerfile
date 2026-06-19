FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends socat && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir flask
RUN useradd -m ctf
WORKDIR /app
COPY app/ .
RUN chmod +x entrypoint.sh
EXPOSE 9999 80
ENTRYPOINT ["/app/entrypoint.sh"]
