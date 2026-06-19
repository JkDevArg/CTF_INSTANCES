FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    socat \
    gcc \
    python3 \
    python3-pip \
    && pip3 install flask --no-cache-dir \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m ctf

WORKDIR /home/ctf

COPY --chown=ctf:ctf challenge.c flag.txt entrypoint.sh server.py .

# Compile: NX (kernel default), PIE, canary, partial RELRO
RUN gcc -o nexus challenge.c \
        -O0 -pie -fpie -fstack-protector-strong \
        -Wl,-z,relro \
    && chown ctf:ctf nexus \
    && chmod +x nexus entrypoint.sh

# Copy the exact libc that will be used at runtime (players need it for offsets)
RUN cp /lib/x86_64-linux-gnu/libc.so.6 /home/ctf/libc.so.6 \
    && chown ctf:ctf /home/ctf/libc.so.6

# Remove gcc
RUN apt-get remove -y gcc && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

USER ctf

EXPOSE 9999 80

ENTRYPOINT ["./entrypoint.sh"]
