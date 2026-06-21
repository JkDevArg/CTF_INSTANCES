FROM python:3.11-alpine
RUN pip install flask --no-cache-dir
WORKDIR /app
COPY app/ .
COPY traffic.pcap .
COPY keylog.txt .
EXPOSE 80
CMD ["python", "server.py"]
