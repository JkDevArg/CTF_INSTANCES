FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        golang-go \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir flask && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY app/ .
RUN chmod +x entrypoint.sh

EXPOSE 80
ENTRYPOINT ["/app/entrypoint.sh"]
