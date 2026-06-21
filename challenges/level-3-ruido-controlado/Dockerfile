FROM python:3.11-slim
RUN pip install flask Pillow --no-cache-dir
WORKDIR /app
COPY app/ .
RUN chmod +x entrypoint.sh
EXPOSE 80
ENTRYPOINT ["./entrypoint.sh"]
