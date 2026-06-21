FROM python:3.11-alpine
RUN pip install flask --no-cache-dir
WORKDIR /app
COPY app/ .
COPY OverUma.exe .
EXPOSE 80
CMD ["python", "server.py"]
