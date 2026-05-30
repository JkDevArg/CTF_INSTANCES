FROM ubuntu:22.04
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc gcc-multilib socat netcat-openbsd gdb python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /pwn
COPY vuln.c flag.txt ./
# Compilar con protecciones deshabilitadas — propósito educativo
RUN gcc -o vuln vuln.c \
      -fno-stack-protector \
      -no-pie \
      -z execstack \
      -m64
RUN chmod 755 vuln
EXPOSE 4444
CMD ["socat", "TCP-LISTEN:4444,reuseaddr,fork", "EXEC:./vuln,pty,stderr,setsid,sigint,sane"]
