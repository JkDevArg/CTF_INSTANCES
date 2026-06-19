FROM python:3.11-slim
RUN pip install --no-cache-dir flask
WORKDIR /app
COPY app/ .
EXPOSE 80
CMD ["python3", "app.py"]
