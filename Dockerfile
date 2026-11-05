# ==============================================================================
# Dockerfile - Inferencia CPU Reproducible con uv y Streamlit
# Caso 1: Detección de Neumonía en Rayos X (UAO)
# ==============================================================================

FROM python:3.12-slim

# Evitar generación de archivos .pyc y buffer de salida
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1 \
    PORT=8501

WORKDIR /app

# Instalar dependencias del sistema mínimas requeridas por OpenCV y libgl
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Instalar uv desde la imagen oficial de Astral
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copiar archivos de definición de dependencias
COPY pyproject.toml ./

# Sincronizar dependencias usando uv directamente en el entorno de Python del sistema
RUN uv pip install --system -r <(uv pip compile pyproject.toml)

# Copiar código fuente y muestras
COPY src/ /app/src/
COPY data/ /app/data/
COPY models/ /app/models/
COPY README.md /app/

# Crear usuario no root por seguridad
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "src/neumonia_detection/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
