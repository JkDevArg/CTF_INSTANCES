FROM arm32v7/ubuntu:22.04
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc socat netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /pwn
COPY vuln_arm.c flag.txt ./
RUN gcc -o vuln_arm vuln_arm.c -fno-stack-protector -no-pie
EXPOSE 4445
CMD ["socat", "TCP-LISTEN:4445,reuseaddr,fork", "EXEC:./vuln_arm,pty,stderr,setsid,sigint,sane"]
