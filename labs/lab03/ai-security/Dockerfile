FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir flask requests
COPY app.py system_prompt.txt ./
EXPOSE 8080
CMD ["python", "app.py"]
