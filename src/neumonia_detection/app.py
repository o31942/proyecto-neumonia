"""Interfaz Web Interactiva en Streamlit para Detección de Neumonía.

Capa: Vista (User Interface)
Responsabilidad única: Permitir la carga de imágenes médicas (DICOM y JPEG/PNG),
ejecutar el análisis en tiempo real y presentar métricas clínicas junto con la
explicabilidad visual Grad-CAM.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import streamlit as st
from PIL import Image

from neumonia_detection.integrator import PneumoniaPipeline
from neumonia_detection.load_model import PneumoniaModelLoader

# Configuración de página de Streamlit
st.set_page_config(
    page_title="Detección de Neumonía - Rayos X | UAO",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource
def get_cached_pipeline(threshold: float, clip_limit: float, alpha: float) -> PneumoniaPipeline:
    """Instancia y almacena en caché el pipeline del modelo para optimizar el rendimiento."""
    loader = PneumoniaModelLoader(threshold=threshold)
    loader.load()
    return PneumoniaPipeline(
        model_loader=loader,
        clip_limit=clip_limit,
        gradcam_alpha=alpha,
    )


def render_header() -> None:
    """Renderiza el encabezado institucional y aviso médico."""
    st.title("🫁 Detección Asistida de Neumonía en Rayos X de Tórax")
    st.markdown(
        "**Maestría en Inteligencia Artificial y Ciencia de Datos — UAO**  \n"
        "*Módulo 1: Arquitectura Modular, Calidad de Software y Reproducibilidad en IA*"
    )
    st.info(
        "⚕️ **Aviso Clínico de Asistencia Diagnóstica:** Esta herramienta es un prototipo "
        "académico diseñado para la asistencia en la interpretación radiológica. No reemplaza "
        "el juicio clínico de un especialista médico radiólogo.",
        icon="ℹ️",
    )


def main() -> None:
    """Punto de entrada principal de la aplicación Streamlit."""
    render_header()

    # Barra lateral: Parámetros y ejemplos
    st.sidebar.header("⚙️ Configuración del Pipeline")
    threshold = st.sidebar.slider(
        "Umbral de Decisión Diagnóstica",
        min_value=0.1,
        max_value=0.9,
        value=0.5,
        step=0.05,
        help="Probabilidad a partir de la cual el caso se clasifica como NEUMONÍA.",
    )
    clip_limit = st.sidebar.slider(
        "Límite de Contraste CLAHE",
        min_value=1.0,
        max_value=5.0,
        value=2.0,
        step=0.5,
        help="Controla la amplificación de contraste adaptativo local.",
    )
    alpha = st.sidebar.slider(
        "Opacidad de Grad-CAM",
        min_value=0.1,
        max_value=0.9,
        value=0.4,
        step=0.05,
        help="Transparencia del mapa térmico superpuesto sobre la radiografía.",
    )

    st.sidebar.markdown("---")
    st.sidebar.header("📁 Casos de Prueba Disponibles")
    sample_dir = Path("data/sample")
    sample_files: list[Path] = []
    if sample_dir.exists():
        sample_files = sorted(
            [f for f in sample_dir.iterdir() if f.suffix.lower() in [".dcm", ".jpeg", ".jpg", ".png"]]
        )

    selected_sample = None
    if sample_files:
        sample_names = ["-- Ninguno (Cargar archivo propio) --"] + [f.name for f in sample_files]
        choice = st.sidebar.selectbox("Seleccionar muestra precargada:", sample_names)
        if choice != "-- Ninguno (Cargar archivo propio) --":
            selected_sample = sample_dir / choice

    # Obtener el pipeline configurado
    pipeline = get_cached_pipeline(threshold=threshold, clip_limit=clip_limit, alpha=alpha)

    # Área de Carga de Archivo
    st.markdown("### 📤 Cargar Radiografía de Tórax")
    uploaded_file = st.file_uploader(
        "Seleccione un archivo DICOM (.dcm) o Imagen (.jpeg, .jpg, .png):",
        type=["dcm", "jpeg", "jpg", "png"],
        help="Puede cargar archivos radiológicos estándar o imágenes exportadas.",
    )

    source_to_process = None
    source_name = ""

    if uploaded_file is not None:
        source_to_process = uploaded_file
        source_name = uploaded_file.name
    elif selected_sample is not None:
        source_to_process = selected_sample
        source_name = selected_sample.name
        st.caption(f"Mostrando caso de prueba de muestra: `{source_name}`")

    if source_to_process is None:
        st.write("👆 *Por favor cargue una radiografía o seleccione una muestra de la barra lateral para iniciar el análisis.*")
        return

    # Ejecutar análisis
    with st.spinner("Procesando imagen, aplicando CLAHE y calculando Grad-CAM..."):
        try:
            result = pipeline.run(source_to_process, source_name=source_name)
        except Exception as e:
            st.error(f"Error procesando la imagen: {e}")
            return

    # Visualización de Resultados
    st.markdown("---")
    st.subheader("📊 Resultado del Diagnóstico")

    col_metric1, col_metric2, col_metric3 = st.columns(3)
    with col_metric1:
        if result.is_pneumonia:
            st.metric(label="Diagnóstico Predictivo", value="NEUMONÍA", delta="Patológico", delta_color="inverse")
        else:
            st.metric(label="Diagnóstico Predictivo", value="NORMAL", delta="Sin Hallazgos", delta_color="normal")

    with col_metric2:
        st.metric(
            label="Probabilidad de Neumonía",
            value=f"{result.probability * 100.0:.2f}%",
        )

    with col_metric3:
        st.metric(
            label="Tiempo de Inferencia",
            value=f"{result.inference_time_ms:.1f} ms",
        )

    # Panel de Alerta Visual
    if result.is_pneumonia:
        st.error(
            f"⚠️ **Alerta Diagnóstica:** Se detectaron patrones de consolidación compatibles con "
            f"**Neumonía** con una confianza estimada del {result.probability * 100.0:.1f}%. "
            f"Consulte el mapa térmico Grad-CAM a la derecha para ver las áreas pulmonares con mayor activación.",
            icon="🚨",
        )
    else:
        st.success(
            f"✅ **Sin evidencia de neumonía:** La radiografía fue clasificada como **Normal** "
            f"(Confianza: {(1.0 - result.probability) * 100.0:.1f}%).",
            icon="✅",
        )

    # Panel de Visualización Comparativo de Imágenes
    st.markdown("### 🔍 Análisis Visual y Explicabilidad (XAI)")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**1. Radiografía Original (H, W)**")
        st.image(
            result.raw_image,
            caption=f"Original: {result.raw_image.shape[1]}x{result.raw_image.shape[0]} px",
            use_container_width=True,
            clamp=True,
        )

    with col2:
        st.markdown("**2. Preprocesado CLAHE (512x512)**")
        # Mostrar el canal de entrada a la red
        prep_view = (result.preprocessed_tensor[0, :, :, 0] * 255.0).astype(np.uint8)
        st.image(
            prep_view,
            caption="Contrato Red: 512x512 px (float32 [0.0, 1.0])",
            use_container_width=True,
            clamp=True,
        )

    with col3:
        st.markdown("**3. Explicabilidad Grad-CAM**")
        st.image(
            result.gradcam_overlay,
            caption="Activación de Clase sobrepuesta (Jet Colormap)",
            use_container_width=True,
        )

    # Detalles Técnicos del Contrato
    with st.expander("🛠️ Verificación Técnica de Contratos y Tensores"):
        st.json({
            "archivo": result.source_identifier,
            "dimension_original": list(result.raw_image.shape),
            "tensor_preprocesado_shape": list(result.preprocessed_tensor.shape),
            "tensor_dtype": str(result.preprocessed_tensor.dtype),
            "tensor_min": float(result.preprocessed_tensor.min()),
            "tensor_max": float(result.preprocessed_tensor.max()),
            "valores_finitos": bool(np.isfinite(result.preprocessed_tensor).all()),
            "gradcam_heatmap_shape": list(result.gradcam_heatmap.shape),
            "latencia_ms": round(result.inference_time_ms, 2),
        })


if __name__ == "__main__":
    main()
