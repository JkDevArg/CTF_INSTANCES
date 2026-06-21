FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc libc6-dev socat python3 python3-pip && \
    pip3 install --no-cache-dir flask && \
    useradd -m ctf && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY challenge.c .
RUN gcc -O0 -no-pie -fno-stack-protector \
        -o logger challenge.c && \
    chmod 555 logger

COPY server.py entrypoint.sh ./
RUN chmod +x entrypoint.sh

EXPOSE 9999 80

ENTRYPOINT ["/app/entrypoint.sh"]
