# 📄 Propuesta Formal de Proyecto (Módulo 2 - 35%)
## Sistema Modular de Detección Asistida de Neumonía en Rayos X con Explicabilidad Grad-CAM

> **Institución:** Universidad Autónoma de Occidente (UAO) — Facultad de Ingeniería  
> **Programa:** Maestría en Inteligencia Artificial y Ciencia de Datos  
> **Asignatura:** Gestión de Proyectos en IA y Ciencia de Datos  
> **Docente:** Jan Polanco Velasco  
> **Caso Asignado:** Caso 1 — Detección de Neumonía (Rayos X de Tórax)  
> **Repositorio Oficial:** [github.com/o31942/proyecto-neumonia](https://github.com/o31942/proyecto-neumonia)  
> **Tablero Kanban:** [github.com/o31942/proyecto-neumonia/projects](https://github.com/o31942/proyecto-neumonia/projects)  
> **Archivo Word Editable:** [propuesta_formal_m2_neumonia.docx](file:///C:/Users/odsanchez/.gemini/antigravity/scratch/proyecto-neumonia/docs/propuesta_formal_m2_neumonia.docx)  

---

## 📑 Tabla de Contenido Obligatoria (6 Capítulos)

1. [Capítulo 1 · Contexto y Justificación del Problema](#capítulo-1--contexto-y-justificación-del-problema)
   - 1.1. Justificación Clínica y Necesidad Operativa
   - 1.2. Restricciones Técnicas y Entorno Operacional
   - 1.3. Arquitectura MaaS de Referencia
   - 1.4. Ficha Técnica Formal del Modelo (*Model Card*)
2. [Capítulo 2 · Objetivos y Matriz de Alcance](#capítulo-2--objetivos-y-matriz-de-alcance)
   - 2.1. Objetivo General
   - 2.2. Objetivos Específicos Medibles
   - 2.3. Matriz de Alcance (*In-Scope*, *Nice-to-Have*, *Out-of-Scope*)
3. [Capítulo 3 · Cronograma, Hitos y Análisis de Ruta Crítica (CPM)](#capítulo-3--cronograma-hitos-y-análisis-de-ruta-crítica-cpm)
   - 3.1. Estructura de Desglose del Trabajo a 15 Días Hábiles
   - 3.2. Tabla de Precedencias y Duraciones de Actividades
   - 3.3. Análisis de Ruta Crítica (CPM) y Holguras
   - 3.4. Hitos de Control y Entregas Parciales
4. [Capítulo 4 · Marco de Investigación y Mapeo CRISP-DM](#capítulo-4--marco-de-investigación-y-mapeo-crisp-dm)
   - 4.1. Fundamentación Radiológica y Formato DICOM vs JPEG
   - 4.2. Técnicas de Preprocesamiento Adaptativo (CLAHE)
   - 4.3. Arquitectura Convolucional WilhemNet86 e Inferencia CPU
   - 4.4. Fundamento Matemático de Grad-CAM (XAI)
   - 4.5. Mapeo Sistemático a las 6 Fases de CRISP-DM
5. [Capítulo 5 · Historias de Usuario, Criterios de Aceptación y Estimación Ágil](#capítulo-5--historias-de-usuario-criterios-de-aceptación-y-estimación-ágil)
   - 5.1. Regla de Estimación Fibonacci 1:1
   - 5.2. Definición Formal de Historias de Usuario (HU-01 a HU-08)
   - 5.3. Criterios de Aceptación (Formato *Given-When-Then*)
   - 5.4. Sincronización con el Tablero Kanban de GitHub Projects
6. [Capítulo 6 · Gobernanza, Regulación y Gestión de Riesgos](#capítulo-6--gobernanza-regulación-y-gestión-de-riesgos)
   - 6.1. Clasificación bajo el EU AI Act (Sistema de Alto Riesgo)
   - 6.2. Estrategia de Supervisión Humana (*Human-in-the-Loop*)
   - 6.3. Transparencia, Trazabilidad y Calidad de Datos (ISO/IEC 42001)
   - 6.4. Matriz Integral de Riesgos y Planes de Contingencia
7. [Referencias Bibliográficas](#referencias-bibliográficas)

---

## Capítulo 1 · Contexto y Justificación del Problema

### 1.1. Justificación Clínica y Necesidad Operativa
La neumonía es una de las afecciones respiratorias agudas con mayor tasa de morbimortalidad a nivel global, afectando anualmente a millones de personas, especialmente en poblaciones vulnerables como niños menores de 5 años y adultos mayores. En la práctica clínica moderna, la radiografía de tórax (Chest X-Ray, CXR) constituye la prueba diagnóstica de primera línea debido a su amplia disponibilidad, bajo costo relativo y mínima dosis de radiación ionizante en comparación con la tomografía computarizada (TC).

No obstante, la interpretación de radiografías de tórax está sujeta a una elevada tasa de variabilidad inter e intraobservador entre médicos radiólogos y médicos generales de urgencias. Los estadios tempranos de la infección bacteriana o viral frecuentemente se manifiestan como opacidades alveolares tenues, infiltrados intersticiales difusos o consolidaciones basales subpleurales que pueden pasar desapercibidas en servicios de salud congestionados con fatiga médica.

La integración de un sistema de visión artificial basado en aprendizaje profundo para la clasificación binaria asistida (Normal vs. Neumonía) y la localización espacial mediante mapas de activación Grad-CAM no busca sustituir el criterio médico, sino actuar como un "segundo lector" de alta sensibilidad que mitiga errores de omisión y acelera el triaje clínico en departamentos de urgencias hospitalarias.

### 1.2. Restricciones Técnicas y Entorno Operacional
A diferencia de prototipos de laboratorio ejecutados en servidores de cómputo GPU de alto costo, el despliegue hospitalario real en economías emergentes impone restricciones de ingeniería innegociables:
1. **Restricción de Hardware (Inferencia CPU):** El sistema debe operar en estaciones de trabajo radiológicas estándar equipadas exclusivamente con procesadores centrales (CPU x86_64), sin exigir aceleradores NVIDIA ni dependencias propietarias de controladores CUDA.
2. **Heterogeneidad de Formatos Radiológicos:** Debe aceptar tanto el estándar internacional de imagen médica DICOM (PS3.3) con resoluciones dinámicas de 12 a 16 bits y metadatos de interpretación fotométrica (`MONOCHROME1` vs `MONOCHROME2`), como imágenes exportadas en formatos comunes (`JPEG`/`PNG`).
3. **Determinismo y Reproducibilidad:** Está estrictamente prohibido el uso de gestores de dependencias no controlados (`pip install` indiscriminado) o scripts dispersos en cuadernos Jupyter (`.ipynb`). Toda la pila tecnológica debe garantizar aislamiento determinista con el gestor `uv` y contratos matemáticos verificables.

### 1.3. Arquitectura MaaS de Referencia
El proyecto se articula conceptualmente bajo el modelo **MaaS (Model-as-a-Service)**, desacoplando el núcleo de inferencia matemática de la capa de interacción clínica. El pipeline orquestador encapsula la carga, validación de contrato, inferencia convolucional y cálculo de mapas térmicos en un servicio modular exportable, accesible tanto por interfaces web en Streamlit como por utilitarios de consola (CLI) o futuros microservicios REST.

### 1.4. Ficha Técnica Formal del Modelo (*Model Card*)

| Sección Model Card | Detalle y Especificación Técnica |
| :--- | :--- |
| **Nombre del Modelo** | WilhemNet86 — Detección Convolucional de Neumonía en CXR |
| **Versión y Fecha** | Versión 0.1.0-Release · Noviembre de 2026 |
| **Tipo de Modelo** | Red Neuronal Convolucional Profunda (CNN) con capa de activación Sigmoide para clasificación binaria. |
| **Entorno de Ejecución** | Inferencia sobre CPU optimizada con TensorFlow / Keras en contenedor reproducible. |
| **Uso Previsto** | Asistencia diagnóstica y priorización de triaje radiológico en radiografías de tórax anteroposteriores y posteroanteriores. |
| **Usuarios Objetivo** | Médicos radiólogos, neumólogos, médicos de urgencias y personal de salud en atención primaria. |
| **Métricas de Rendimiento** | Sensibilidad (*Recall*) $\ge 94.0\%$, Especificidad $\ge 90.0\%$, Área bajo la Curva ROC (AUC) $\ge 0.96$. |
| **Datos de Evaluación** | Cohorte radiológica balanceada con imágenes DICOM hospitalarias y series pediátricas/adultas en JPEG. |
| **Limitaciones Conocidas** | No distingue entre etiología bacteriana y viral en su salida univariada (clasifica Patología vs Normal). Su rendimiento decae ante radiografías con severa subexposición, artefactos de movimiento o presencia masiva de dispositivos externos (cables, electrodos ECG) no enmascarados. |
| **Consideraciones Éticas** | El modelo jamás debe tomar decisiones vinculantes de forma autónoma. Se exige supervisión humana obligatoria (*Human-in-the-Loop*) y revisión del mapa Grad-CAM. |

---

## Capítulo 2 · Objetivos y Matriz de Alcance

### 2.1. Objetivo General
Diseñar, implementar y evaluar un sistema de software modular de grado de ingeniería para la detección asistida de neumonía en radiografías de tórax a partir de imágenes DICOM y JPEG, integrando contratos formales de preprocesamiento adaptativo (CLAHE), inferencia convolucional en CPU, explicabilidad médica mediante Grad-CAM y despliegue interactivo en Streamlit bajo un entorno determinista gestionado con `uv`.

### 2.2. Objetivos Específicos Medibles
1. Desarrollar un subsistema controlador de ingesta y preprocesamiento de imágenes médicas capaz de estandarizar radiografías heterogéneas (DICOM de 16 bits y JPEG) a tensores float32 de dimensión $(1, 512, 512, 1)$ acotados en $[0.0, 1.0]$, aplicando CLAHE adaptativo con verificación formal de finitud matemática en un tiempo de ejecución menor a 100 milisegundos por imagen.
2. Implementar y desacoplar el motor de inferencia convolucional (WilhemNet86) y el algoritmo de explicabilidad Grad-CAM sobre la última capa convolucional (`conv_last`), garantizando la generación de mapas de calor normalizados y superposiciones térmicas Jet reproducibles en CPU con una latencia de inferencia inferior a 50 milisegundos.
3. Construir una suite exhaustiva de pruebas unitarias automatizadas con `pytest` siguiendo el patrón AAA (*Arrange, Act, Assert*) con una cobertura superior al 85% del código fuente, asegurando cero fallos y cumplimiento riguroso de convenciones de código con el linter Ruff.
4. Empaquetar y desplegar la solución en una aplicación web interactiva en Streamlit y un contenedor Docker para CPU con usuario no privilegiado, gobernado bajo los lineamientos de Sistemas de IA de Alto Riesgo del EU AI Act.

### 2.3. Matriz de Alcance (*In-Scope*, *Nice-to-Have*, *Out-of-Scope*)

| Compromiso In-Scope (Obligatorio) | Nice-to-Have (Holgura) | Out-of-Scope (Excluido) |
| :--- | :--- | :--- |
| • Lectura de DICOM (`.dcm`) con manejo de MONOCHROME1/2 y JPEG/PNG. | • Generación de reportes clínicos exportables en PDF. | • Reentrenamiento distribuido de redes neuronales desde cero en GPU. |
| • Preprocesamiento CLAHE (`clipLimit=2.0`) y resize a $512\times512$. | • Carga concurrente de lotes masivos de imágenes (Batch processing). | • Integración con sistemas PACS hospitalarios propietarios vía HL7. |
| • Verificación formal de contratos (shape, dtype, finitud, límites). | • Selector interactivo de paletas de color para Grad-CAM. | • Diagnóstico diferencial multiclase (COVID-19, tuberculosis, derrames). |
| • Inferencia en CPU WilhemNet86 y explicabilidad Grad-CAM. | • Autenticación médica por roles (RBAC). | • Aplicaciones móviles nativas iOS / Android. |
| • Suite de pruebas unitarias AAA con `pytest` (mínimo 20 tests). | • Telemetría de uso con Prometheus/Grafana. | • Despliegue en clusters de Kubernetes en producción médica. |
| • Contenedor Docker CPU reproducible y app web en Streamlit. | • Pruebas de estrés y benchmarking de concurrencia. | • Prescripción farmacológica automatizada. |

---

## Capítulo 3 · Cronograma, Hitos y Análisis de Ruta Crítica (CPM)

### 3.1. Estructura de Desglose del Trabajo a 15 Días Hábiles
El proyecto se estructura en un ciclo de desarrollo ágil de 15 días hábiles, organizado en 3 iteraciones semanales (Sprints de 5 días). La estimación temporal se rige por el principio de Fibonacci 1:1 adoptado en la UAO (1 Story Point = 1 Día hombre).

### 3.2. Tabla de Precedencias y Duraciones de Actividades

| ID | Descripción de la Actividad | Precedente | Duración (Días) | Holgura Total | ¿Ruta Crítica? |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **A1** | Configuración de entorno `uv`, `pyproject.toml` y repo Gitflow | - | 1 | 0 | **SÍ** |
| **A2** | Extracción y curaduría de muestras radiológicas (DICOM/JPG) | A1 | 1 | 2 | NO |
| **A3** | Implementación del lector DICOM y JPEG (`read_img.py`) | A1 | 2 | 0 | **SÍ** |
| **A4** | Implementación de CLAHE y asertos (`preprocess_img.py`) | A3 | 2 | 0 | **SÍ** |
| **A5** | Implementación del cargador de modelo (`load_model.py`) | A1 | 2 | 1 | NO |
| **A6** | Desarrollo del algoritmo Grad-CAM (`grad_cam.py`) | A4, A5 | 2 | 0 | **SÍ** |
| **A7** | Orquestación del pipeline end-to-end (`integrator.py`) | A6 | 1 | 0 | **SÍ** |
| **A8** | Construcción de la interfaz web en Streamlit (`app.py`) | A7 | 2 | 0 | **SÍ** |
| **A9** | Diseño de fixtures sintéticos y `conftest.py` | A4 | 1 | 1 | NO |
| **A10** | Implementación de pruebas unitarias AAA con `pytest` | A8, A9 | 2 | 0 | **SÍ** |
| **A11** | Auditoría de calidad y formateo con Ruff | A10 | 1 | 0 | **SÍ** |
| **A12** | Creación del Dockerfile CPU y verificación de imagen | A7 | 1 | 2 | NO |
| **A13** | Sincronización de CI en GitHub Actions y PR template | A11 | 1 | 0 | **SÍ** |

### 3.3. Análisis de Ruta Crítica (CPM) y Holguras
El cálculo de tiempos tempranos y tardíos revela que la Ruta Crítica (secuencia de actividades con Holgura Total = 0) está constituida por la cadena:

$$\text{Ruta Crítica (CPM)}: A_1 \rightarrow A_3 \rightarrow A_4 \rightarrow A_6 \rightarrow A_7 \rightarrow A_8 \rightarrow A_{10} \rightarrow A_{11} \rightarrow A_{13} = 1 + 2 + 2 + 2 + 1 + 2 + 2 + 1 + 1 = 14 \text{ Días Hábiles.}$$

Cualquier retraso en el preprocesamiento de imágenes ($A_4$) o en el cálculo de Grad-CAM ($A_6$) impacta directamente la fecha final de entrega. Por el contrario, la preparación de Dockerfile ($A_{12}$) y el cargador de modelo ($A_5$) poseen holguras de 2 y 1 días respectivamente, lo que permite absorber variaciones menores sin comprometer el cronograma.

### 3.4. Hitos de Control y Entregas Parciales
- **Hito 1 (Día 5):** Pipeline de datos validado (Lectura DICOM/JPEG + CLAHE + Asertos de contrato aprobados al 100%).
- **Hito 2 (Día 9):** Motor de inferencia integrado con explicabilidad Grad-CAM funcional sobre `conv_last`.
- **Hito 3 (Día 12):** Aplicación interactiva Streamlit operativa con visualización tripartita.
- **Hito 4 (Día 15):** Suite de pruebas AAA aprobada, Dockerfile testeado y repositorio sincronizado con GitHub Actions.

---

## Capítulo 4 · Marco de Investigación y Mapeo CRISP-DM

### 4.1. Fundamentación Radiológica y Formato DICOM vs JPEG
El estándar DICOM (Digital Imaging and Communications in Medicine) es la columna vertebral de la informática médica hospitalaria. A diferencia de imágenes JPEG de 8 bits (256 niveles de gris), los archivos DICOM de rayos X almacenan datos en escalas de 12 o 16 bits (hasta 65,536 niveles de radiancia), preservando detalles sutiles de atenuación tisular. Asimismo, integran metadatos cruciales como `PhotometricInterpretation`:
- `MONOCHROME1`: El valor de píxel cero representa blanco (densidad radiopaca). Típico en sistemas radiológicos heredados.
- `MONOCHROME2`: El valor de píxel cero representa negro (aire/gas radiolúcido). Estándar radiológico convencional.

El controlador implementado detecta activamente este atributo. Si se detecta `MONOCHROME1`, se aplica inversión espectral: $I_{\text{norm}} = \max(I) - I$, homogeneizando la representación física antes de la ecualización.

### 4.2. Técnicas de Preprocesamiento Adaptativo (CLAHE)
La ecualización de histograma tradicional aplica una función de transformación acumulativa global sobre toda la imagen, lo que en radiografías de tórax satura las áreas hiperlúcidas de los campos pulmonares y oscurece las estructuras óseas mediastínicas. Para resolver esta distorsión, se implementa CLAHE (*Contrast Limited Adaptive Histogram Equalization*):
1. **Descomposición Espacial:** La imagen se divide en una cuadrícula de bloques contextuales contiguos (*tiles*) de tamaño $(8, 8)$.
2. **Limitación de Contraste (`clipLimit=2.0`):** En cada bloque, el histograma local se trunca a un umbral máximo; el exceso de conteo de píxeles se redistribuye uniformemente entre todos los niveles de gris, suprimiendo la amplificación espuria de ruido de alta frecuencia.
3. **Interpolación Bilineal:** Los límites entre bloques se suavizan mediante interpolación bilineal para eliminar artefactos de frontera en tablero de ajedrez.

### 4.3. Arquitectura Convolucional WilhemNet86 e Inferencia CPU
El modelo WilhemNet86 emplea una arquitectura convolucional profunda compuesta por 4 bloques secuenciales con convoluciones 2D (filtros 3x3), capas de normalización por lotes (*Batch Normalization*) para estabilizar gradientes y activaciones ReLU. La última capa convolucional de características profundas, denominada `conv_last`, preserva resolución espacial bidimensional con 256 filtros. La cabeza de clasificación utiliza Global Average Pooling (GAP) para reducir parámetros, Dropout al 30% contra sobreajuste y una neurona densa con activación Sigmoide continua.

### 4.4. Fundamento Matemático de Grad-CAM (XAI)
Grad-CAM (*Gradient-weighted Class Activation Mapping*; Selvaraju et al., 2017) proporciona explicabilidad visual calculando la importancia de cada neurona en la última capa convolucional `conv_last` respecto al score de clase $y^c$ (probabilidad de neumonía):

1. **Cálculo de Gradientes:** Mediante `tf.GradientTape` se extrae la derivada parcial del score $y^c$ respecto a los mapas de activación $A^k$:
   $$\text{grad}_k = \frac{\partial y^c}{\partial A^k}$$

2. **Global Average Pooling de Gradientes:** Se obtiene el coeficiente de ponderación $\alpha_k$ integrando sobre las dimensiones espaciales $i, j$:
   $$\alpha_k^c = \frac{1}{Z} \sum_i \sum_j \frac{\partial y^c}{\partial A_{i,j}^k}$$

3. **Combinación Lineal y Rectificación ReLU:** Se sintetiza el mapa de calor crudo aplicando ReLU para conservar exclusivamente las características que incrementan la probabilidad de neumonía:
   $$L_{\text{Grad-CAM}}^c = \text{ReLU}\left( \sum_k \alpha_k^c \cdot A^k \right)$$

4. **Superposición Alfa-Blending:** El mapa se normaliza a $[0.0, 1.0]$, se redimensiona a $(H, W)$ original y se fusiona sobre la radiografía base: $I_{\text{final}} = 0.4 \cdot \text{JetMap} + 0.6 \cdot I_{\text{base}}$.

### 4.5. Mapeo Sistemático a las 6 Fases de CRISP-DM
- **Fase 1: Comprensión del Negocio (*Business Understanding*):** Reducción de variabilidad diagnóstica y priorización de radiografías urgentes.
- **Fase 2: Comprensión de los Datos (*Data Understanding*):** Inspección de matrices DICOM/JPEG, rango dinámico y resolución anatómica.
- **Fase 3: Preparación de Datos (*Data Preparation*):** Inversión fotométrica, CLAHE, resize a $512\times512$ y asertos formales de finitud.
- **Fase 4: Modelado (*Modeling*):** Inferencia convolucional WilhemNet86 y generación de mapas térmicos Grad-CAM.
- **Fase 5: Evaluación (*Evaluation*):** Análisis de métricas clínicas (Sensibilidad/Especificidad), verificación de invariantes y auditoría visual de activaciones.
- **Fase 6: Despliegue (*Deployment*):** Empaquetado en contenedor Docker CPU, interfaz en Streamlit e integración continua con GitHub Actions.

---

## Capítulo 5 · Historias de Usuario, Criterios de Aceptación y Estimación Ágil

### 5.1. Regla de Estimación Fibonacci 1:1
En cumplimiento de las directrices metodológicas de la asignatura, la estimación de esfuerzo ágil utiliza la escala de Fibonacci estricta con equivalencia 1:1, donde 1 Story Point (SP) equivale exactamente a 1 Día-hombre de trabajo de ingeniería enfocado.

### 5.2. Definición Formal de Historias de Usuario (HU-01 a HU-08)

#### HU-01: Ingesta Dual de Imágenes Radiológicas (DICOM y JPEG) — [3 SP]
* **Como** médico radiólogo,
* **quiero** cargar archivos radiológicos en formato DICOM (`.dcm`) o imágenes convencionales (`.jpeg`, `.png`),
* **para** procesar estudios sin necesidad de conversiones previas externas.
* **Criterio de Aceptación (Gherkin):**
  - **Given** un archivo DICOM válido con interpretación `MONOCHROME1` o `MONOCHROME2`,
  - **When** se invoca `read_dicom_or_image()`,
  - **Then** el sistema retorna un array 2D monocromático de tipo `np.uint8` en el rango $[0, 255]$ con las dimensiones espaciales nativas de la radiografía.

#### HU-02: Preprocesamiento CLAHE con Verificación de Contrato — [2 SP]
* **Como** ingeniero de datos de IA,
* **quiero** aplicar ecualización adaptativa CLAHE y redimensionamiento estandarizado,
* **para** garantizar que la red reciba tensores homogéneos e inmunes a valores corruptos.
* **Criterio de Aceptación (Gherkin):**
  - **Given** una matriz 2D uint8 de entrada,
  - **When** se ejecuta `preprocess_image(target_size=512, clip_limit=2.0)`,
  - **Then** la salida es un tensor float32 con dimensiones $(1, 512, 512, 1)$, valores acotados en $[0.0, 1.0]$ y verificación estricta de `np.isfinite()` sin valores NaN ni infinitos.

#### HU-03: Motor de Inferencia Convolucional WilhemNet86 en CPU — [3 SP]
* **Como** especialista de urgencias,
* **quiero** ejecutar la clasificación diagnóstica de la radiografía,
* **para** obtener una probabilidad continua y una etiqueta diagnóstica (`NORMAL` / `NEUMONÍA`) en menos de 50 ms.
* **Criterio de Aceptación (Gherkin):**
  - **Given** un tensor preprocesado $(1, 512, 512, 1)$,
  - **When** se invoca `PneumoniaModelLoader.predict()`,
  - **Then** el sistema entrega la probabilidad continua $p \in [0.0, 1.0]$ y la clasificación clínica según el umbral configurado.

#### HU-04: Explicabilidad Visual Médica con Grad-CAM — [3 SP]
* **Como** profesional clínico,
* **quiero** visualizar un mapa térmico superpuesto sobre la radiografía,
* **para** auditar qué regiones del parénquima pulmonar fundamentaron la predicción de la IA.
* **Criterio de Aceptación (Gherkin):**
  - **Given** el modelo convolucional y el tensor preprocesado,
  - **When** se ejecuta `generate_gradcam()` y `overlay_heatmap()`,
  - **Then** se genera un mapa de calor 2D redimensionado al tamaño original de la radiografía y una imagen RGB fusionada mediante alfa-blending al 40%.

#### HU-05: Orquestador Desacoplado del Pipeline de Diagnóstico — [2 SP]
* **Como** integrador de software,
* **quiero** un controlador desacoplado que coordine lectura, preprocesamiento, inferencia y explicabilidad,
* **para** invocar el pipeline mediante API o consola CLI.
* **Criterio de Aceptación (Gherkin):**
  - **Given** una ruta de archivo o buffer de bytes,
  - **When** se ejecuta `PneumoniaPipeline.run()`,
  - **Then** se retorna una estructura tipada `PneumoniaDiagnosisResult` con todas las métricas, latencia en ms e imágenes resultantes.

#### HU-06: Interfaz Web Interactiva en Streamlit — [3 SP]
* **Como** usuario médico,
* **quiero** interactuar con una aplicación web moderna,
* **para** cargar estudios, seleccionar muestras y ajustar umbrales clínicos en tiempo real.
* **Criterio de Aceptación (Gherkin):**
  - **Given** la aplicación web iniciada en el puerto 8501,
  - **When** el usuario carga una radiografía o selecciona una muestra de prueba,
  - **Then** la pantalla presenta en 3 columnas comparativas la imagen original, preprocesada y Grad-CAM con sus tarjetas métricas.

#### HU-07: Suite de Pruebas Unitarias Automatizadas (Patrón AAA) — [2 SP]
* **Como** asegurador de calidad (QA),
* **quiero** una suite de pruebas con `pytest` que evalúe todas las capas,
* **para** garantizar inmunidad contra regresiones antes de cada pase a producción.
* **Criterio de Aceptación (Gherkin):**
  - **Given** la ejecución de `uv run pytest -v`,
  - **When** se ejecutan las 30 pruebas unitarias con patrón AAA,
  - **Then** el 100% de los tests aprueba exitosamente en menos de 40 segundos evaluando casos límite y excepciones.

#### HU-08: Empaquetamiento en Contenedor Docker CPU Reproducible — [2 SP]
* **Como** DevOps de IA,
* **quiero** un contenedor Docker multicapa para CPU,
* **para** desplegar la solución en cualquier infraestructura hospitalaria sin requerir tarjetas NVIDIA dedicadas.
* **Criterio de Aceptación (Gherkin):**
  - **Given** la construcción de la imagen con Dockerfile,
  - **When** se lanza el contenedor en el puerto 8501,
  - **Then** el servicio responde al Healthcheck HTTP y permite la interacción web con usuario no root `appuser`.

### 5.4. Sincronización con el Tablero Kanban de GitHub Projects
Todas las historias de usuario anteriores se encuentran sincronizadas en el tablero Kanban público de GitHub Projects del repositorio:  
👉 [github.com/o31942/proyecto-neumonia/projects](https://github.com/o31942/proyecto-neumonia/projects), distribuidas en el flujo de trabajo: `Backlog` $\rightarrow$ `To Do` $\rightarrow$ `In Progress` $\rightarrow$ `In Review / Testing` $\rightarrow$ `Done`.

---

## Capítulo 6 · Gobernanza, Regulación y Gestión de Riesgos

### 6.1. Clasificación bajo el EU AI Act (Sistema de Alto Riesgo)
De conformidad con el Reglamento Europeo de Inteligencia Artificial (EU AI Act - Regulation 2024/1689), los sistemas de IA destinados a ser utilizados como componentes de seguridad en productos sanitarios o que constituyen dispositivos médicos de diagnóstico in vitro se clasifican estrictamente en la categoría de **Sistemas de IA de Alto Riesgo (High-Risk AI Systems, Anexo III, Numeral 5)**.

Esta categorización exige el cumplimiento mandatario de requisitos técnicos rigurosos: gobernanza de datos de entrenamiento, documentación técnica exhaustiva, registro continuo de eventos de inferencia, transparencia clínica, supervisión humana activa y robustez contra fallos de software.

### 6.2. Estrategia de Supervisión Humana (*Human-in-the-Loop*)
Para dar cumplimiento al Artículo 14 del EU AI Act, el sistema implementa una arquitectura estricta de *Human-in-the-Loop* (HITL):
1. La herramienta está tipificada exclusivamente como software de soporte a la decisión clínica (*Clinical Decision Support Software* - CDSS). En ningún escenario operativo emite dictámenes médicos vinculantes ni prescribe tratamientos de forma autónoma.
2. La interfaz de usuario presenta de forma prominente un aviso de advertencia clínica ineludible (*Clinical Disclaimer*), recordando al operador que el juicio final recae exclusivamente en el facultativo médico matriculado.
3. La visualización simultánea del mapa Grad-CAM previene el sesgo de automatización (*automation bias*), forzando al radiólogo a correlacionar la predicción probabilística con la semiología anatómica del paciente.

### 6.3. Transparencia, Trazabilidad y Calidad de Datos (ISO/IEC 42001)
En concordancia con el estándar internacional ISO/IEC 42001 (Sistema de Gestión de Inteligencia Artificial), el proyecto asegura:
- **Trazabilidad de Versiones:** Fijación determinista de versiones de software con `pyproject.toml` y `uv.lock`, garantizando que el entorno de ejecución pueda reproducirse idénticamente en auditorías técnicas.
- **Verificación de Invariantes Numéricos:** Los asertos de finitud (`np.isfinite`) en la capa de preprocesamiento evitan el procesamiento de datos corruptos que degraden el rendimiento del modelo.
- **Auditoría de Inferencia:** La estructura de resultados expone la latencia de inferencia en milisegundos y las dimensiones del tensor para auditoría hospitalaria.

### 6.4. Matriz Integral de Riesgos y Planes de Contingencia

| ID | Riesgo Identificado | Impacto | Estrategia de Mitigación | Plan de Contingencia |
| :---: | :--- | :---: | :--- | :--- |
| **R1** | Falso Negativo (Neumonía bacteriana no detectada en estadio temprano) | **CRÍTICO** | Configurar umbral clínico de alta sensibilidad (Recall $\ge 94\%$) y advertencia médica explícita en casos dudosos. | Protocolo hospitalario de confirmación diagnóstica con prueba PCR o TAC de tórax. |
| **R2** | Sesgo por Artefactos Externos (Marcapasos/electrodos activando Grad-CAM) | **ALTO** | Supervisión visual con mapa térmico Grad-CAM; el radiólogo descarta inmediatamente activaciones fuera de los pulmones. | Rechazo del estudio por el operador y solicitud de nueva toma radiológica limpia. |
| **R3** | Incompatibilidad de Formatos DICOM (Tags corruptos o no estándar) | **MEDIO** | Decodificación tolerante a fallos con `pydicom` (`force=True`) y fallback a decodificación OpenCV. | Aviso de error en pantalla solicitando exportación estándar en formato PNG. |
| **R4** | Degradación Silenciosa por Tensores NaN/Inf en Preprocesamiento | **ALTO** | Asertos estrictos en `preprocess_img.py` (`validate_preprocessed_contract`). | Interrupción inmediata de la ejecución antes de consumir ciclos de CPU. |
| **R5** | Vulnerabilidad en Contenedor por Ejecución con Privilegios Root | **ALTO** | Creación de usuario dedicado sin privilegios (`appuser` UID 1000) en el Dockerfile. | Aislamiento de red a nivel de host y escaneo estático de vulnerabilidades con Trivy. |

---

## Referencias Bibliográficas

1. Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., ... & Gebru, T. (2019). Model cards for model reporting. *In Proceedings of the conference on fairness, accountability, and transparency* (pp. 220-229).
2. Selvaraju, R. R., Cogswell, M., Das, A., Vedaldi, A., Parikh, D., & Batra, D. (2017). Grad-CAM: Visual explanations from deep networks via gradient-based localization. *In Proceedings of the IEEE international conference on computer vision* (pp. 618-626).
3. European Parliament and Council of the European Union. (2024). Regulation (EU) 2024/1689 laying down harmonised rules on artificial intelligence (Artificial Intelligence Act). *Official Journal of the European Union*.
4. International Organization for Standardization. (2023). Information technology — Artificial intelligence — Management system (ISO/IEC Standard No. 42001:2023).
5. Pianykh, O. S. (2008). *Digital imaging and communications in medicine (DICOM): A practical introduction and survival guide*. Springer Science & Business Media.
6. Zuiderveld, K. (1994). Contrast limited adaptive histogram equalization. *Graphics gems IV*, 474-485.
7. Chapman, P., Clinton, J., Kerber, R., Khabaza, T., Reinartz, T., Shearer, C., & Wirth, R. (2000). *CRISP-DM 1.0: Step-by-step data mining guide*. CRISP-DM Consortium.
8. Sculley, D., Holt, G., Golovin, D., Davydov, E., Phillips, T., Ebner, D., ... & Dennison, M. (2015). Hidden technical debt in machine learning systems. *Advances in neural information processing systems*, 28.
