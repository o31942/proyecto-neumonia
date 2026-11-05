# 🫁 Detección de Neumonía en Rayos X con Explicabilidad Grad-CAM

[![Python 3.12](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![Package Manager: uv](https://img.shields.io/badge/packaging-uv-purple.svg)](https://docs.astral.sh/uv/)
[![Linter: Ruff](https://img.shields.io/badge/linter-ruff-orange.svg)](https://docs.astral.sh/ruff/)
[![Tests: Pytest](https://img.shields.io/badge/tests-pytest-green.svg)](https://docs.pytest.org/)
[![Architecture: MVC](https://img.shields.io/badge/architecture-MVC-informational.svg)]()
[![Docker: CPU Ready](https://img.shields.io/badge/docker-CPU%20Ready-2496ED.svg)](https://www.docker.com/)

Proyecto del **Módulo 1: Arquitectura Modular, Calidad de Software y Reproducibilidad en IA**  
**Maestría en Inteligencia Artificial y Ciencia de Datos**  
**Universidad Autónoma de Occidente (UAO)**  
*Docente:* Jan Polanco Velasco  

---

## 📋 1. Descripción del Proyecto

Este repositorio implementa una solución de software de grado de ingeniería para la detección asistida de **Neumonía** en radiografías de tórax a partir de imágenes médicas en formato **DICOM (`.dcm`)** y formatos fotográficos estándar (**JPEG / PNG**).

El sistema incorpora:
1. **Pipeline de Preprocesamiento Adaptativo:** Ecualización CLAHE (`clipLimit=2.0`), redimensionamiento cuadrático a $512 \times 512$ píxeles y normalización con verificación formal de invariantes matemáticos.
2. **Inferencia en CPU Optimizada:** Red neuronal convolucional (`WilhemNet86`) con evaluación probabilística.
3. **Explicabilidad Algorítmica (XAI - Grad-CAM):** Mapas de calor superpuestos que señalan las consolidaciones parenquimatosas e infiltrados pulmonares determinantes en la clasificación.
4. **Capa de Presentación Web (Streamlit):** Interfaz interactiva para el personal de salud con carga de imágenes, ajuste de umbrales en tiempo real y visualización comparativa tripartita.

---

## 🏛️ 2. Arquitectura de Software (Patrón MVC)

El proyecto sigue una estricta separación de responsabilidades (*Clean Architecture / High Cohesion & Low Coupling*):

```
proyecto-neumonia/
├── .github/
│   ├── PULL_REQUEST_TEMPLATE.md       # Plantilla oficial de Pull Request UAO
│   └── workflows/
│       └── ci.yml                     # Integración continua con uv, ruff y pytest
├── src/
│   └── neumonia_detection/            # Paquete principal instalable
│       ├── __init__.py                # Exportaciones públicas del paquete
│       ├── read_img.py                # [Controlador] Lectura DICOM y JPEG/PNG
│       ├── preprocess_img.py          # [Controlador] CLAHE, resize 512x512 y contrato
│       ├── load_model.py              # [Modelo] Carga de WilhemNet86 e inferencia CPU
│       ├── grad_cam.py                # [Modelo] Explicabilidad visual y mapas térmicos
│       ├── integrator.py              # [Controlador] Orquestador del flujo end-to-end y CLI
│       └── app.py                     # [Vista] Aplicación web en Streamlit
├── tests/                             # Suite de pruebas unitarias (Patrón AAA)
│   ├── conftest.py                    # Fixtures reutilizables
│   ├── test_read_img.py               # Pruebas de lectura y manejo de errores
│   ├── test_preprocess.py             # Pruebas de CLAHE y contratos matemáticos
│   ├── test_load_model.py             # Pruebas de inferencia y umbrales
│   ├── test_grad_cam.py               # Pruebas de activación y superposición
│   └── test_integrator.py             # Pruebas de integración completa
├── data/
│   └── sample/                        # Muestras radiológicas de prueba (DICOM y JPEG)
├── models/
│   └── .gitkeep                       # Directorio para pesos (.h5 ignorados por git)
├── .dockerignore
├── .gitignore                         # Ignora *.h5, *.ipynb, .venv, etc.
├── Dockerfile                         # Contenedor reproducible CPU-only
├── pyproject.toml                     # Metadatos del proyecto y configuración uv/ruff/pytest
└── README.md
```

### 🧩 Contratos de Entrada y Salida entre Capas

| Módulo | Capa MVC | Entrada | Salida | Responsabilidad Única |
| :--- | :--- | :--- | :--- | :--- |
| `read_img.py` | Controlador | Archivo / Bytes (`.dcm`, `.jpeg`) | `uint8 (H, W)` | Cargar píxeles y manejar MONOCHROME1/2 |
| `preprocess_img.py` | Controlador | `uint8 (H, W)` | `float32 (1, 512, 512, 1)` | CLAHE `clipLimit=2.0`, resize y asserts [0, 1] |
| `load_model.py` | Modelo | `float32 (1, 512, 512, 1)` | `(float prob, str label)` | Inferencia binaria (`NORMAL` vs `NEUMONÍA`) |
| `grad_cam.py` | Modelo | Tensor + Modelo | `(H, W) float32`, `(H, W, 3) uint8` | Calcular gradientes y mapa superpuesto |
| `integrator.py` | Controlador | Fuente de imagen | `PneumoniaDiagnosisResult` | Orquestar pipeline y reportar resultados |
| `app.py` | Vista | Archivo cargado por usuario | Interfaz gráfica Streamlit | Renderizar diagnóstico, alertas y mapas |

---

## 🚀 3. Instalación y Ejecución con `uv`

> ⚠️ **Regla de Oro del Curso:** Está prohibido el uso de `pip install` o `requirements.txt`. Toda la gestión de dependencias y entornos virtuales se realiza con [`uv`](https://docs.astral.sh/uv/).

### Paso 1: Clonar o posicionarse en el proyecto
```bash
cd proyecto-neumonia
```

### Paso 2: Crear el entorno virtual y sincronizar dependencias
```bash
uv sync --extra dev
```

### Paso 3: Ejecutar la aplicación interactiva Streamlit
```bash
uv run streamlit run src/neumonia_detection/app.py
```
La aplicación abrirá automáticamente en tu navegador en `http://localhost:8501`.

### Paso 4: Ejecución alternativa por consola (CLI)
```bash
uv run python -m neumonia_detection.integrator data/sample/sample_normal.dcm
uv run python -m neumonia_detection.integrator data/sample/sample_bacteria.jpeg
```

---

## 🧪 4. Pruebas Unitarias y Calidad de Código

### Ejecución de Pruebas con `pytest` (Patrón AAA)
Cada prueba está rigurosamente estructurada en tres fases explícitas:
- **Arrange (Preparar):** Instanciación de datos sintéticos o fixtures.
- **Act (Actuar):** Ejecución del método bajo prueba.
- **Assert (Afirmar):** Verificación de tipos, dimensiones, invariantes o excepciones.

```bash
# Ejecutar toda la suite de pruebas unitarias
uv run pytest -v

# Ejecutar con reporte de cobertura de código
uv run pytest --cov=src/neumonia_detection tests/
```

### Análisis Estático de Código y Formato con `ruff`
```bash
# Validar reglas de estilo y errores con linter
uv run ruff check src/ tests/

# Formatear el código de acuerdo al estándar PEP 8
uv run ruff format src/ tests/
```

---

## 🐳 5. Despliegue en Contenedor Docker (CPU Only)

El contenedor está optimizado exclusivamente para inferencia en CPU (sin requerir GPUs NVIDIA ni drivers CUDA):

```bash
# Construir la imagen Docker
docker build -t neumonia-detector:latest .

# Ejecutar el contenedor
docker run -d -p 8501:8501 --name neumonia-app neumonia-detector:latest
```
Acceder al servicio web en `http://localhost:8501`.

---

## 🌿 6. Flujo Git, Ramas y Pull Requests

El repositorio implementa **Gitflow** y **Conventional Commits**:
- `main`: Rama de código en producción estable.
- `develop`: Rama de integración activa.
- `feature/<nombre>`: Ramas de funcionalidades específicas.

### Formato de Commits:
```bash
feat(preprocess): implementar CLAHE con clipLimit=2.0 y validacion de contrato
test(read_img): agregar 7 pruebas unitarias AAA para lectura DICOM y JPEG
refactor(integrator): desacoplar inyeccion de dependencias del modelo
chore(docker): optimizar imagen multicapa para inferencia CPU
```

### Plantilla de Pull Request:
Cualquier contribución debe utilizar la plantilla oficial ubicada en `.github/PULL_REQUEST_TEMPLATE.md` detallando las capas MVC afectadas, evidencia de paso de `pytest` y `ruff`, y justificaciones de diseño.
