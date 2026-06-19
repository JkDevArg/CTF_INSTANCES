FROM ubuntu:22.04
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc socat file binutils \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /rev
COPY crackme.c ./
RUN gcc -O2 -o crackme crackme.c -lm
EXPOSE 4446
CMD ["socat", "TCP-LISTEN:4446,reuseaddr,fork", "EXEC:./crackme,pty,stderr,setsid,sigint,sane"]
