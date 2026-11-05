"""Script generador de la presentación en PowerPoint (.pptx) para la sustentación UAO."""

from __future__ import annotations

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

# Paleta de colores institucional / médica
COLOR_PRIMARY = RGBColor(16, 44, 87)       # Navy Profundo
COLOR_SECONDARY = RGBColor(53, 162, 159)   # Teal / Médico
COLOR_ACCENT = RGBColor(218, 73, 73)       # Coral / Alerta
COLOR_BG_DARK = RGBColor(10, 25, 47)       # Dark Navy
COLOR_TEXT_DARK = RGBColor(30, 41, 59)     # Slate 800
COLOR_TEXT_LIGHT = RGBColor(241, 245, 249) # Slate 100
COLOR_CARD_BG = RGBColor(248, 250, 252)    # Gris suave


def create_presentation() -> str:
    prs = Presentation()
    prs.slide_width = Inches(13.333)  # 16:9 Widescreen
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text: str, category_text: str = "MAESTRÍA EN IA Y CIENCIA DE DATOS — UAO"):
        # Header banner
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_SECONDARY

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_PRIMARY

    def add_card(slide, left, top, width, height, title, items, border_color=COLOR_SECONDARY):
        # Card background
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = COLOR_CARD_BG
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)

        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.25)
        tf.margin_bottom = Inches(0.2)

        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(16)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_PRIMARY

        for it in items:
            p = tf.add_paragraph()
            p.text = f"•  {it}"
            p.font.size = Pt(12)
            p.font.color.rgb = COLOR_TEXT_DARK
            p.space_before = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 1: PORTADA
    # -------------------------------------------------------------
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_BG_DARK
    bg1.line.fill.background()

    tb1 = slide1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.333), Inches(4.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "UNIVERSIDAD AUTÓNOMA DE OCCIDENTE — MAESTRÍA EN IA Y CD"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_SECONDARY

    p = tf1.add_paragraph()
    p.text = "Detección Asistida de Neumonía en Rayos X"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_LIGHT
    p.space_before = Pt(10)

    p = tf1.add_paragraph()
    p.text = "Arquitectura Modular MVC, Explicabilidad Grad-CAM, Testing AAA y Reproducibilidad"
    p.font.size = Pt(18)
    p.font.color.rgb = RGBColor(148, 163, 184)
    p.space_before = Pt(8)

    p = tf1.add_paragraph()
    p.text = "Gestión de Proyectos en IA y CD  |  Prof. Jan Polanco Velasco  |  Caso 1: Neumonía (Rayos X)"
    p.font.size = Pt(14)
    p.font.color.rgb = COLOR_SECONDARY
    p.space_before = Pt(30)

    # -------------------------------------------------------------
    # SLIDE 2: CONTEXTO CLÍNICO Y PROBLEMA
    # -------------------------------------------------------------
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "1. El Problema Clínico y los Requisitos de Ingeniería")
    add_card(
        slide2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8),
        "🩺 Desafío Médico Radiológico",
        [
            "La neumonía presenta alta variabilidad interobservador en radiografías de tórax incipientes.",
            "Heterogeneidad de formatos de entrada: imágenes DICOM (.dcm) hospitalarias de 16-bits vs exportaciones estándar (JPEG/PNG).",
            "Manejo de interpretación fotométrica: MONOCHROME1 (huesos oscuros) vs MONOCHROME2 (huesos blancos).",
            "La 'Caja Negra' está prohibida: se exige explicabilidad espacial (XAI) para sustentar la decisión clínica."
        ]
    )
    add_card(
        slide2, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8),
        "⚙️ Reglas de Juego de Ingeniería",
        [
            "Prohibición estricta de 'pip install' y 'requirements.txt': determinismo 100% con 'uv' y 'pyproject.toml'.",
            "Prohibición de Jupyter Notebooks (.ipynb) en producción: código modular en layout 'src/'.",
            "Arquitectura desacoplada en 3 capas (Modelo - Vista - Controlador).",
            "Contratos matemáticos formales entre capas con asertos de finitud e invariantes numéricos.",
            "Inferencia CPU reproducible sin dependencias obligatorias de hardware NVIDIA/GPU."
        ],
        border_color=COLOR_PRIMARY
    )

    # -------------------------------------------------------------
    # SLIDE 3: ARQUITECTURA MODULAR MVC
    # -------------------------------------------------------------
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "2. Arquitectura de Software Modular (Patrón MVC)")
    add_card(
        slide3, Inches(0.8), Inches(1.8), Inches(3.6), Inches(4.8),
        "🕹️ Controlador (Controller)",
        [
            "read_img.py: Lee DICOM y JPEG/PNG, normaliza densidades a uint8 (H, W).",
            "preprocess_img.py: Aplica CLAHE adaptativo, resize (512,512) y asertos.",
            "integrator.py: Orquestador end-to-end con inyección de dependencias y CLI."
        ]
    )
    add_card(
        slide3, Inches(4.8), Inches(1.8), Inches(3.6), Inches(4.8),
        "🧠 Modelo (Model & XAI)",
        [
            "load_model.py: Carga artefacto WilhemNet86.h5 o inicializa arquitectura funcional en CPU.",
            "Inferencia probabilística con umbral clínico parametrizable.",
            "grad_cam.py: Cálculo de gradientes en tf.GradientTape sobre conv_last y mapa Jet."
        ],
        border_color=COLOR_PRIMARY
    )
    add_card(
        slide3, Inches(8.8), Inches(1.8), Inches(3.6), Inches(4.8),
        "🖥️ Vista (View)",
        [
            "app.py: Interfaz web profesional desarrollada en Streamlit.",
            "Comparativa tripartita: Radiografía original vs CLAHE 512x512 vs Grad-CAM.",
            "Ajuste interactivo de umbral, clipLimit CLAHE y opacidad en vivo.",
            "Métricas diagnósticas y alerta clínica de patología."
        ]
    )

    # -------------------------------------------------------------
    # SLIDE 4: PIPELINE DE PREPROCESAMIENTO Y CONTRATOS
    # -------------------------------------------------------------
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "3. Preprocesamiento CLAHE y Contratos Matemáticos")
    add_card(
        slide4, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8),
        "🔬 Pipeline de Transformación",
        [
            "Entrada: Matriz 2D uint8 (H, W) en escala de grises.",
            "CLAHE (Contrast Limited Adaptive Histogram Equalization): clipLimit=2.0, tileGridSize=(8, 8).",
            "Resalta consolidaciones e infiltrados alveolares sutiles sin sobre-amplificar ruido de fondo.",
            "Interpolación bilineal para estandarizar a resolución fija de (512, 512) px.",
            "Normalización de precisión simple float32 en rango continuo [0.0, 1.0].",
            "Expansión dimensional: tensor tetradimensional final (1, 512, 512, 1)."
        ]
    )
    add_card(
        slide4, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8),
        "🛡️ Validación Formal de Contratos",
        [
            "Shape exacto: assert tensor.shape == (1, 512, 512, 1)",
            "Tipo exacto: assert tensor.dtype == np.float32",
            "Finitud matemática estricta: assert np.isfinite(tensor).all() -> ¡Cero NaN y cero Infinitos!",
            "Rango acotado: assert 0.0 <= min y max <= 1.0",
            "Beneficio: Inmunidad total ante degradaciones silenciosas o fallos en capas de Batch Normalization."
        ],
        border_color=COLOR_ACCENT
    )

    # -------------------------------------------------------------
    # SLIDE 5: INFERENCIA Y GRAD-CAM
    # -------------------------------------------------------------
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "4. Inferencia Convolucional y Explicabilidad Grad-CAM")
    add_card(
        slide5, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8),
        "⚡ Arquitectura WilhemNet86 (CPU)",
        [
            "Bloques Convolucionales con BatchNormalization, ReLU y MaxPooling.",
            "Capa convolucional profunda objetivo: conv_last (256 filtros).",
            "GlobalAveragePooling2D + Dense con Dropout (0.3).",
            "Activación Sigmoide final: probabilidad continua p ∈ [0.0, 1.0].",
            "Inferencia en CPU optimizada con latencia inferior a 50 ms."
        ]
    )
    add_card(
        slide5, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8),
        "🔥 Algoritmo Grad-CAM Paso a Paso",
        [
            "1. Se extraen mapas de activación A_k de la capa conv_last.",
            "2. tf.GradientTape calcula los gradientes dy/dA_k de la neurona de salida.",
            "3. Global Average Pooling sobre gradientes -> pesos de importancia alfa_k.",
            "4. Combinación lineal ponderada + activación ReLU (solo aportes positivos).",
            "5. Normalización [0.0, 1.0] e interpolación bilineal al tamaño original (H, W).",
            "6. Fusión alfa-blending (40% Jet Colormap + 60% Radiografía base)."
        ],
        border_color=COLOR_PRIMARY
    )

    # -------------------------------------------------------------
    # SLIDE 6: TESTING AAA Y CALIDAD DE SOFTWARE
    # -------------------------------------------------------------
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "5. Suite de Testing AAA y Calidad de Código")
    add_card(
        slide6, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8),
        "🧪 Estructura de Pruebas (Patrón AAA)",
        [
            "30 pruebas unitarias automatizadas con pytest.",
            "Arrange: Configuración de fixtures sintéticas (DICOM y JPEG) en conftest.py.",
            "Act: Ejecución del método o función bajo prueba.",
            "Assert: Verificación de tipos, dimensiones, excepciones y contratos.",
            "Cobertura total de capas: test_read_img, test_preprocess, test_load_model, test_grad_cam, test_integrator.",
            "Resultado: 30 passed in 30.85s (100% de éxito)."
        ]
    )
    add_card(
        slide6, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8),
        "🚀 Tooling Industrial y CI/CD",
        [
            "uv: Creación determinista del entorno y bloqueo con uv.lock.",
            "ruff: Linter y formateador ultrarrápido (cero violaciones PEP 8).",
            "Gitflow: Ramas 'main' (producción) y 'develop' (desarrollo activo).",
            "Conventional Commits: Historial atómico con feat:, test:, chore:, docs:.",
            "GitHub Actions: Pipeline en .github/workflows/ci.yml que corre ruff y pytest en cada push.",
            "Plantilla UAO: .github/PULL_REQUEST_TEMPLATE.md oficial integrada."
        ],
        border_color=COLOR_SECONDARY
    )

    # -------------------------------------------------------------
    # SLIDE 7: DOCKER Y GOBERNANZA DE IA
    # -------------------------------------------------------------
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "6. Contenedor Reproducible y Gobernanza (EU AI Act)")
    add_card(
        slide7, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8),
        "🐳 Dockerfile CPU Reproducible",
        [
            "Imagen base python:3.12-slim liviana y segura.",
            "Instalación determinista de paquetes desde uv oficial.",
            "Inferencia 100% en CPU (no requiere drivers CUDA ni GPUs dedicadas).",
            "Seguridad reforzada: ejecución bajo usuario no root 'appuser' (UID 1000).",
            "Healthcheck automático en el puerto 8501.",
            "Ejecución en 1 comando: docker run -p 8501:8501 neumonia-app"
        ]
    )
    add_card(
        slide7, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8),
        "⚖️ Gobernanza de IA (EU AI Act / ISO 42001)",
        [
            "Clasificación: Sistema de IA de Alto Riesgo (Anexo III - Dispositivos Médicos).",
            "Supervisión Humana (Human-in-the-loop): El sistema es asistente, no juez clínico autónomo.",
            "Transparencia: Disclaimer médico explícito en UI y explicabilidad con Grad-CAM.",
            "Trazabilidad: Registro y exposición en UI de dimensiones, contratos y latencia.",
            "Gestión de riesgos: Asertos que detienen inferencia ante entradas corruptas."
        ],
        border_color=COLOR_PRIMARY
    )

    # -------------------------------------------------------------
    # SLIDE 8: DEMO Y CONCLUSIONES
    # -------------------------------------------------------------
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "7. Demostración en Vivo y Conclusiones de Ingeniería")
    add_card(
        slide8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8),
        "🖥️ Demostración en Streamlit",
        [
            "Acceso en vivo: http://localhost:8501 (o mediante iniciar_app.bat).",
            "Caso 1: Carga de sample_bacteria.jpeg -> Alerta patológica de Neumonía y Grad-CAM focalizado.",
            "Caso 2: Carga de sample_viral.dcm -> Detección de patrones intersticiales difusos.",
            "Caso 3: Carga de sample_normal.dcm -> Predicción Normal y baja activación de calor.",
            "Interactividad: Modificación dinámica de umbrales clínicos en tiempo real."
        ]
    )
    add_card(
        slide8, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8),
        "🏆 Conclusiones Principales",
        [
            "La ingeniería de software rigurosa convierte un modelo experimental en un producto industrial confiable.",
            "El patrón MVC desacopla el modelo de IA: cambiar de WilhemNet a ResNet/EfficientNet no afecta la vista ni los lectores.",
            "El gestor 'uv' garantiza reproducibilidad matemática exacta en cualquier entorno o CI.",
            "Explicabilidad (Grad-CAM) y asertos formales son indispensables para IA en salud."
        ],
        border_color=COLOR_SECONDARY
    )

    output_path = "C:/Users/odsanchez/.gemini/antigravity/scratch/proyecto-neumonia/sustentacion_neumonia_uao.pptx"
    prs.save(output_path)
    return output_path


if __name__ == "__main__":
    path = create_presentation()
    print(f"Presentación generada con éxito en: {path}")
