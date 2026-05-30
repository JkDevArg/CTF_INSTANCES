FROM python:3.11-alpine
WORKDIR /app
COPY app/ .
RUN pip install flask --no-cache-dir
EXPOSE 80
CMD ["python", "app.py"]
