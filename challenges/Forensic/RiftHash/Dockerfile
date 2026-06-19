FROM python:3.11-alpine
RUN pip install flask --no-cache-dir
WORKDIR /app
COPY app/ .
RUN chmod +x entrypoint.sh
EXPOSE 80
ENTRYPOINT ["./entrypoint.sh"]
