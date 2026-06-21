FROM python:3.11-slim
RUN pip install --no-cache-dir flask
WORKDIR /app
COPY app.py .
RUN mkdir -p /app/static
COPY fugitivo.png /app/static/fugitivo.png
EXPOSE 80
CMD ["python3", "app.py"]
