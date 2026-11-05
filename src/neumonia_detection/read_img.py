"""Módulo de lectura de imágenes de Rayos X (DICOM y formatos estándar).

Capa: Controlador (Data Reader)
Responsabilidad única: Cargar archivos DICOM (.dcm) y formatos estándar (.jpg, .jpeg, .png)
desde disco o flujos de bytes en memoria, retornando un array 2D monocromático uint8 (H, W).
"""

from __future__ import annotations

import io
from pathlib import Path
from typing import BinaryIO

import cv2
import numpy as np
import pydicom
from pydicom.dataset import FileDataset


def _normalize_to_uint8(image_array: np.ndarray) -> np.ndarray:
    """Escala un array numérico 2D al rango uint8 [0, 255] de forma segura.

    Args:
        image_array: Array bidimensional con los valores de píxeles en cualquier rango.

    Returns:
        np.ndarray: Array bidimensional de tipo np.uint8 en el rango [0, 255].
    """
    min_val = float(np.min(image_array))
    max_val = float(np.max(image_array))

    if max_val == min_val:
        return np.zeros_like(image_array, dtype=np.uint8)

    scaled = (image_array - min_val) / (max_val - min_val) * 255.0
    return np.clip(scaled, 0, 255).astype(np.uint8)


def read_dicom(source: str | Path | BinaryIO | bytes) -> np.ndarray:
    """Lee una imagen médica en formato DICOM (.dcm) y extrae su matriz de píxeles.

    Gestiona la interpretación fotométrica (MONOCHROME1 vs MONOCHROME2) para
    asegurar que las zonas densas (huesos/consolidaciones) se visualicen adecuadamente.

    Args:
        source: Ruta del archivo (.dcm), objeto binario tipo archivo o buffer de bytes.

    Returns:
        np.ndarray: Matriz 2D de píxeles en escala de grises con dtype np.uint8.

    Raises:
        FileNotFoundError: Si la ruta especificada no existe en disco.
        ValueError: Si el archivo DICOM no contiene una matriz de píxeles válida.
    """
    if isinstance(source, (str, Path)):
        file_path = Path(source)
        if not file_path.exists():
            raise FileNotFoundError(f"No se encontró el archivo DICOM: {file_path}")
        dataset: FileDataset = pydicom.dcmread(str(file_path), force=True)
    elif isinstance(source, bytes):
        dataset = pydicom.dcmread(io.BytesIO(source), force=True)
    elif hasattr(source, "read"):
        dataset = pydicom.dcmread(source, force=True)
    else:
        raise TypeError(f"Tipo de fuente no soportado para DICOM: {type(source)}")

    if not hasattr(dataset, "pixel_array"):
        raise ValueError("El archivo DICOM no contiene el atributo requerido 'pixel_array'.")

    pixel_array = dataset.pixel_array.astype(np.float32)

    # Invertir si la interpretación fotométrica es MONOCHROME1 (0 representa blanco)
    photometric = getattr(dataset, "PhotometricInterpretation", "MONOCHROME2")
    if str(photometric).strip() == "MONOCHROME1":
        pixel_array = np.max(pixel_array) - pixel_array

    # Si la imagen tiene canales adicionales (ej. color o multiframe), reducir a 2D
    if pixel_array.ndim == 3:
        if pixel_array.shape[0] == 1:
            pixel_array = pixel_array[0]
        elif pixel_array.shape[-1] == 3:
            pixel_array = cv2.cvtColor(pixel_array.astype(np.uint8), cv2.COLOR_RGB2GRAY).astype(
                np.float32
            )
        else:
            pixel_array = pixel_array[0]

    return _normalize_to_uint8(pixel_array)


def read_standard_image(source: str | Path | BinaryIO | bytes) -> np.ndarray:
    """Lee una imagen en formato estándar (.jpeg, .jpg, .png) en escala de grises.

    Args:
        source: Ruta del archivo, objeto binario o buffer de bytes.

    Returns:
        np.ndarray: Matriz 2D de píxeles en escala de grises con dtype np.uint8.

    Raises:
        FileNotFoundError: Si la ruta del archivo no existe.
        ValueError: Si los datos no pueden decodificarse como una imagen válida.
    """
    if isinstance(source, (str, Path)):
        file_path = Path(source)
        if not file_path.exists():
            raise FileNotFoundError(f"No se encontró el archivo de imagen: {file_path}")
        img = cv2.imread(str(file_path), cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError(f"No fue posible decodificar la imagen: {file_path}")
        return img

    if isinstance(source, bytes):
        buffer = source
    elif hasattr(source, "read"):
        source.seek(0)
        buffer = source.read()
    else:
        raise TypeError(f"Tipo de fuente no soportado para imagen estándar: {type(source)}")

    np_arr = np.frombuffer(buffer, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(
            "Los bytes suministrados no corresponden a una imagen válida decodificable."
        )
    return img


def read_dicom_or_image(
    source: str | Path | BinaryIO | bytes,
    file_extension_hint: str | None = None,
) -> np.ndarray:
    """Punto de entrada unificado para leer cualquier imagen de Rayos X (DICOM o estándar).

    Intenta primero determinar el tipo a partir de la extensión o indicación,
    con degradación elegante a decodificación estándar o DICOM si falla.

    Args:
        source: Ruta del archivo, objeto tipo archivo binario o buffer de bytes.
        file_extension_hint: Extensión opcional (ej. '.dcm', '.jpg', '.jpeg', '.png')
            para optimizar la selección del lector.

    Returns:
        np.ndarray: Matriz 2D (H, W) con valores en np.uint8 [0, 255].

    Raises:
        ValueError: Si el formato no es reconocido o no puede ser leído.
    """
    hint = ""
    if file_extension_hint:
        hint = file_extension_hint.lower()
    elif isinstance(source, (str, Path)):
        hint = Path(source).suffix.lower()

    if hint == ".dcm" or hint.endswith("dicom"):
        return read_dicom(source)

    if hint in [".jpg", ".jpeg", ".png"]:
        return read_standard_image(source)

    # Si no hay pista o no coincide, intentar primero DICOM y luego estándar
    try:
        return read_dicom(source)
    except Exception:
        try:
            return read_standard_image(source)
        except Exception as exc:
            raise ValueError(
                "No fue posible interpretar el archivo ni como DICOM ni como imagen estándar."
            ) from exc
