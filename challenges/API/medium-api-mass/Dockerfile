FROM python:3.11-alpine
RUN pip install flask --no-cache-dir
WORKDIR /app
COPY app/ .
EXPOSE 80
CMD ["python", "app.py"]
