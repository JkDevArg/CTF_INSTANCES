FROM python:3.11-slim
RUN pip install flask pyjwt cryptography --no-cache-dir
WORKDIR /app
COPY app/ .
EXPOSE 80
CMD ["python", "app.py"]
