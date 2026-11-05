"""Paquete de detección de neumonía en Rayos X con explicabilidad Grad-CAM.

Proyecto Módulo 1 - Maestría en IA y Ciencia de Datos (UAO)
Gestión de Proyectos en IA y CD
"""

from neumonia_detection.grad_cam import generate_gradcam, overlay_heatmap
from neumonia_detection.integrator import PneumoniaDiagnosisResult, PneumoniaPipeline
from neumonia_detection.load_model import PneumoniaModelLoader
from neumonia_detection.preprocess_img import preprocess_image
from neumonia_detection.read_img import read_dicom_or_image

__version__ = "0.1.0"

__all__ = [
    "read_dicom_or_image",
    "preprocess_image",
    "PneumoniaModelLoader",
    "generate_gradcam",
    "overlay_heatmap",
    "PneumoniaPipeline",
    "PneumoniaDiagnosisResult",
]
