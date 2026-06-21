FROM python:3.11-slim
RUN pip install --no-cache-dir flask
WORKDIR /app
COPY app/ .
RUN chmod +x entrypoint.sh
EXPOSE 80
ENTRYPOINT ["/app/entrypoint.sh"]
