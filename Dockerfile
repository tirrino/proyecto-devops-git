FROM python:3.12-slim
WORKDIR /app
COPY app.py .

# Crear usuario no privilegiado y directorios seguros
RUN useradd -r -u 10001 appuser && \
    mkdir -p /data && \
    chown -R appuser:appuser /app /data

USER appuser
EXPOSE 8080

# Validación de salud del contenedor
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health')"

CMD ["python", "app.py"]  