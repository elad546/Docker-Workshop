FROM python:3.12-alpine
WORKDIR /app
RUN pip install --no-cache-dir redis
COPY server.py .
EXPOSE 5000
CMD ["python", "server.py"]
