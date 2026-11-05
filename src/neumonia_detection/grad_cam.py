"""Módulo de explicabilidad algorítmica mediante Grad-CAM.

Capa: Modelo (Explicabilidad / XAI)
Responsabilidad única: Generar mapas de activación de clases ponderados por gradiente
(Grad-CAM) para explicar visualmente qué regiones anatómicas del tórax influyeron
en la predicción del modelo convolucional.
"""

from __future__ import annotations

from typing import Any

import cv2
import numpy as np


def generate_gradcam(
    model: Any,
    preprocessed_tensor: np.ndarray,
    last_conv_layer_name: str | None = None,
    pred_index: int | None = None,
) -> np.ndarray:
    """Genera la matriz de calor Grad-CAM bidimensional en rango [0.0, 1.0].

    Calcula los gradientes de la predicción con respecto a los mapas de características
    de la última capa convolucional usando tf.GradientTape, pondera espacialmente
    los canales y aplica ReLU.

    Args:
        model: Instancia de tf.keras.Model.
        preprocessed_tensor: Tensor de entrada (1, H, W, 1) float32.
        last_conv_layer_name: Nombre de la capa convolucional objetivo. Si es None,
            se deduce automáticamente.
        pred_index: Índice de la clase objetivo (para clasificación binaria típicamente None).

    Returns:
        np.ndarray: Mapa de calor 2D (H_feat, W_feat) normalizado en [0.0, 1.0].
    """
    import tensorflow as tf

    if last_conv_layer_name is None:
        # Buscar la última capa convolucional
        for layer in reversed(model.layers):
            if isinstance(layer, (tf.keras.layers.Conv2D, tf.keras.layers.SeparableConv2D)):
                last_conv_layer_name = layer.name
                break
        if last_conv_layer_name is None:
            last_conv_layer_name = "conv_last"

    # Construir un modelo intermedio que retorne los mapas de la capa convolucional y la predicción final
    grad_model = tf.keras.models.Model(
        inputs=model.inputs,
        outputs=[model.get_layer(last_conv_layer_name).output, model.output],
    )

    tensor_tf = tf.cast(preprocessed_tensor, tf.float32)

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(tensor_tf)
        if pred_index is None:
            class_channel = predictions[:, 0]
        else:
            class_channel = predictions[:, pred_index]

    # Gradiente de la neurona de salida con respecto a los mapas convolucionales
    grads = tape.gradient(class_channel, conv_outputs)
    if grads is None:
        # Fallback de seguridad en caso de arquitectura sin gradiente detectable
        return np.zeros((conv_outputs.shape[1], conv_outputs.shape[2]), dtype=np.float32)

    # Global Average Pooling sobre los gradientes para obtener la importancia de cada canal
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    # Ponderar los mapas de características por la importancia de sus canales
    conv_outputs_val = conv_outputs[0]
    heatmap = conv_outputs_val @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    # Aplicar ReLU: solo nos interesan las características que contribuyen positivamente
    heatmap = tf.maximum(heatmap, 0.0)

    # Normalización min-max a [0.0, 1.0]
    max_val = tf.math.reduce_max(heatmap)
    if max_val > 0:
        heatmap = heatmap / max_val

    return heatmap.numpy().astype(np.float32)


def overlay_heatmap(
    heatmap: np.ndarray,
    original_image: np.ndarray,
    alpha: float = 0.4,
    colormap: int = cv2.COLORMAP_JET,
) -> tuple[np.ndarray, np.ndarray]:
    """Superpone el mapa de calor Grad-CAM sobre la imagen original de Rayos X.

    Redimensiona el mapa de calor a las dimensiones exactas de la imagen original (H, W),
    aplica una paleta de color RGB (por defecto JET) y realiza mezcla alfa ponderada.

    Args:
        heatmap: Mapa de calor 2D float32 [0.0, 1.0].
        original_image: Imagen original 2D uint8 (H, W) en escala de grises.
        alpha: Factor de opacidad del mapa de calor (0.0 = solo imagen, 1.0 = solo mapa).
        colormap: Código de mapa de color de OpenCV (cv2.COLORMAP_JET por defecto).

    Returns:
        tuple[np.ndarray, np.ndarray]:
            - resized_heatmap: Mapa de calor float32 redimensionado a (H, W).
            - overlay: Imagen RGB resultante uint8 de dimensiones (H, W, 3).
    """
    orig_h, orig_w = original_image.shape[:2]

    # Redimensionar el mapa de calor a las dimensiones originales del tórax
    resized_heatmap = cv2.resize(heatmap, (orig_w, orig_h), interpolation=cv2.INTER_LINEAR)
    resized_heatmap = np.clip(resized_heatmap, 0.0, 1.0).astype(np.float32)

    # Convertir mapa de calor normalizado [0, 1] a uint8 [0, 255]
    heatmap_uint8 = np.uint8(255.0 * resized_heatmap)

    # Aplicar mapa de color
    colored_heatmap = cv2.applyColorMap(heatmap_uint8, colormap)

    # Asegurar que la imagen base sea RGB uint8 (H, W, 3)
    if original_image.ndim == 2:
        base_rgb = cv2.cvtColor(original_image, cv2.COLOR_GRAY2BGR)
    elif original_image.ndim == 3 and original_image.shape[-1] == 1:
        base_rgb = cv2.cvtColor(original_image.squeeze(-1), cv2.COLOR_GRAY2BGR)
    else:
        base_rgb = original_image.copy()

    # Mezcla ponderada: alpha * heatmap + (1 - alpha) * base
    beta = 1.0 - alpha
    superimposed = cv2.addWeighted(colored_heatmap, alpha, base_rgb, beta, 0.0)

    # Convertir de BGR a RGB para interoperabilidad con matplotlib/streamlit
    superimposed_rgb = cv2.cvtColor(superimposed, cv2.COLOR_BGR2RGB)

    return resized_heatmap, superimposed_rgb
