"""Módulo de preprocesamiento de imágenes de Rayos X.

Capa: Controlador (Preprocesamiento)
Responsabilidad única: Transformar una imagen 2D uint8 (H, W) en un tensor normalizado
con CLAHE y redimensionamiento a (512, 512), satisfaciendo el contrato estricto
requerido por el modelo de aprendizaje profundo: (1, 512, 512, 1), float32, rango [0.0, 1.0].
"""

from __future__ import annotations

import cv2
import numpy as np

# Constantes del contrato arquitectónico
DEFAULT_TARGET_SIZE: int = 512
DEFAULT_CLIP_LIMIT: float = 2.0
DEFAULT_TILE_GRID_SIZE: tuple[int, int] = (8, 8)


def apply_clahe(
    image: np.ndarray,
    clip_limit: float = DEFAULT_CLIP_LIMIT,
    tile_grid_size: tuple[int, int] = DEFAULT_TILE_GRID_SIZE,
) -> np.ndarray:
    """Aplica ecualización adaptativa de histograma con limitación de contraste (CLAHE).

    Mejora el contraste local de estructuras pulmonares sutiles (infiltrados,
    consolidaciones y broncogramas aéreos) sin amplificar ruido en exceso.

    Args:
        image: Array 2D uint8 en escala de grises.
        clip_limit: Límite de corte de contraste para el algoritmo CLAHE.
        tile_grid_size: Tamaño de las celdas de la cuadrícula contextual (filas, columnas).

    Returns:
        np.ndarray: Array 2D uint8 con contraste adaptativo optimizado.

    Raises:
        ValueError: Si la imagen no es un array 2D o su tipo no es np.uint8.
    """
    if not isinstance(image, np.ndarray):
        raise TypeError(f"La entrada debe ser np.ndarray, recibido: {type(image)}")
    if image.ndim != 2:
        raise ValueError(f"CLAHE requiere un array bidimensional (H, W), recibido: ndim={image.ndim}")
    if image.dtype != np.uint8:
        raise ValueError(f"CLAHE requiere dtype np.uint8, recibido: {image.dtype}")

    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    return clahe.apply(image)


def resize_image(
    image: np.ndarray,
    target_size: int = DEFAULT_TARGET_SIZE,
) -> np.ndarray:
    """Redimensiona una imagen 2D a una dimensión cuadrada fija (target_size, target_size).

    Utiliza interpolación bilineal adaptativa de OpenCV.

    Args:
        image: Array 2D (H, W).
        target_size: Dimensión de alto y ancho objetivo en píxeles.

    Returns:
        np.ndarray: Array 2D de dimensiones (target_size, target_size).
    """
    if target_size <= 0:
        raise ValueError(f"target_size debe ser un entero positivo, recibido: {target_size}")

    return cv2.resize(image, (target_size, target_size), interpolation=cv2.INTER_LINEAR)


def normalize_tensor(image: np.ndarray) -> np.ndarray:
    """Normaliza los valores de píxel al rango cerrado [0.0, 1.0] con precisión float32.

    Args:
        image: Array de píxeles con valores en rango [0, 255].

    Returns:
        np.ndarray: Array con dtype np.float32 en el rango [0.0, 1.0].
    """
    norm = image.astype(np.float32) / 255.0
    return np.clip(norm, 0.0, 1.0)


def validate_preprocessed_contract(tensor: np.ndarray, target_size: int = DEFAULT_TARGET_SIZE) -> None:
    """Valida los invariantes del contrato de salida del preprocesamiento.

    Verifica:
    1. Shape exacto (1, target_size, target_size, 1).
    2. Tipo de dato exacto np.float32.
    3. Rango acotado entre 0.0 y 1.0 inclusive.
    4. Ausencia total de valores no finitos (NaN, Inf, -Inf).

    Raises:
        AssertionError: Si alguna condición del contrato se incumple.
    """
    expected_shape = (1, target_size, target_size, 1)
    if tensor.shape != expected_shape:
        raise AssertionError(f"Shape incorrecto: esperado {expected_shape}, obtenido {tensor.shape}")

    if tensor.dtype != np.float32:
        raise AssertionError(f"Dtype incorrecto: esperado float32, obtenido {tensor.dtype}")

    if not np.isfinite(tensor).all():
        raise AssertionError("El tensor preprocesado contiene valores no finitos (NaN o Inf).")

    min_val = float(tensor.min())
    max_val = float(tensor.max())
    if min_val < 0.0 or max_val > 1.0:
        raise AssertionError(
            f"Valores fuera de rango [0.0, 1.0]: min={min_val}, max={max_val}"
        )


def preprocess_image(
    image: np.ndarray,
    target_size: int = DEFAULT_TARGET_SIZE,
    clip_limit: float = DEFAULT_CLIP_LIMIT,
    tile_grid_size: tuple[int, int] = DEFAULT_TILE_GRID_SIZE,
) -> np.ndarray:
    """Pipeline completo de preprocesamiento para detección de neumonía.

    Aplica en secuencia:
    1. Validación de entrada (H, W) uint8.
    2. Ecualización CLAHE con clipLimit=2.0 y tileGridSize=(8, 8).
    3. Redimensionamiento a (target_size, target_size).
    4. Normalización a float32 en [0.0, 1.0].
    5. Expansión de dimensiones a (1, target_size, target_size, 1).
    6. Verificación formal de contrato de salida.

    Args:
        image: Array 2D uint8 en escala de grises.
        target_size: Tamaño espacial cuadrático (por defecto 512).
        clip_limit: Límite de contraste para CLAHE (por defecto 2.0).
        tile_grid_size: Tamaño de rejilla para CLAHE (por defecto (8, 8)).

    Returns:
        np.ndarray: Tensor cuatridimensional (1, target_size, target_size, 1) float32.
    """
    clahe_img = apply_clahe(image, clip_limit=clip_limit, tile_grid_size=tile_grid_size)
    resized_img = resize_image(clahe_img, target_size=target_size)
    normalized = normalize_tensor(resized_img)

    # Expandir dimensiones para cumplir (Batch, Height, Width, Channels)
    tensor = np.expand_dims(normalized, axis=(0, -1))

    # Asegurar contrato
    validate_preprocessed_contract(tensor, target_size=target_size)

    return tensor
