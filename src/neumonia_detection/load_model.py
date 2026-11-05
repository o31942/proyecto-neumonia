"""Módulo de carga y ejecución de inferencia del modelo de red neuronal.

Capa: Modelo (Inference Engine)
Responsabilidad única: Cargar el artefacto WilhemNet86.h5 (o construir arquitectura
compatible para entornos de test/CPU), gestionar la sesión de inferencia en CPU y
proporcionar predicciones con introspección para explicabilidad Grad-CAM.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import numpy as np

# Configurar logging
logger = logging.getLogger(__name__)

DEFAULT_MODEL_PATH: str = "models/WilhemNet86.h5"
DEFAULT_THRESHOLD: float = 0.5


def build_wilhemnet_architecture(input_shape: tuple[int, int, int] = (512, 512, 1)) -> Any:
    """Construye la arquitectura convolucional WilhemNet86 para CPU e inferencia reproducible.

    Esta arquitectura actúa como arquitectura de referencia y mock completamente
    funcional cuando el archivo de pesos binarios pesados (.h5) no se encuentra
    en el entorno (ej. clonación fresca del repositorio sin pesos descargados).

    Args:
        input_shape: Dimensiones de entrada (H, W, C), típicamente (512, 512, 1).

    Returns:
        tf.keras.Model: Modelo de Keras compilado para inferencia binaria.
    """
    from tensorflow.keras import layers, models

    inputs = layers.Input(shape=input_shape, name="input_xray")

    # Bloque Convolucional 1
    x = layers.Conv2D(32, (3, 3), padding="same", name="conv1_1")(inputs)
    x = layers.BatchNormalization(name="bn1_1")(x)
    x = layers.ReLU(name="relu1_1")(x)
    x = layers.MaxPooling2D((2, 2), name="pool1")(x)

    # Bloque Convolucional 2
    x = layers.Conv2D(64, (3, 3), padding="same", name="conv2_1")(x)
    x = layers.BatchNormalization(name="bn2_1")(x)
    x = layers.ReLU(name="relu2_1")(x)
    x = layers.MaxPooling2D((2, 2), name="pool2")(x)

    # Bloque Convolucional 3
    x = layers.Conv2D(128, (3, 3), padding="same", name="conv3_1")(x)
    x = layers.BatchNormalization(name="bn3_1")(x)
    x = layers.ReLU(name="relu3_1")(x)
    x = layers.MaxPooling2D((2, 2), name="pool3")(x)

    # Bloque Convolucional Profundo (Capa de explicabilidad para Grad-CAM)
    x = layers.Conv2D(256, (3, 3), padding="same", name="conv_last")(x)
    x = layers.BatchNormalization(name="bn_last")(x)
    x = layers.ReLU(name="relu_last")(x)

    # Cabeza de Clasificación
    x = layers.GlobalAveragePooling2D(name="gap")(x)
    x = layers.Dense(128, activation="relu", name="dense_1")(x)
    x = layers.Dropout(0.3, name="dropout_1")(x)
    outputs = layers.Dense(1, activation="sigmoid", name="output_sigmoid")(x)

    model = models.Model(inputs=inputs, outputs=outputs, name="WilhemNet86")
    return model


class PneumoniaModelLoader:
    """Cargador y controlador del modelo de detección de neumonía."""

    def __init__(
        self,
        model_path: str | Path = DEFAULT_MODEL_PATH,
        threshold: float = DEFAULT_THRESHOLD,
    ) -> None:
        """Inicializa el cargador de modelo.

        Args:
            model_path: Ruta al archivo WilhemNet86.h5.
            threshold: Umbral de decisión para clasificar como NEUMONÍA (por defecto 0.5).
        """
        self.model_path = Path(model_path)
        self.threshold = threshold
        self._model: Any = None
        self._last_conv_layer_name: str | None = None

    def load(self) -> Any:
        """Carga el modelo desde disco o inicializa la arquitectura de referencia.

        Returns:
            tf.keras.Model: Modelo listo para predicción e introspección.
        """
        import tensorflow as tf

        if self.model_path.exists() and self.model_path.is_file():
            logger.info("Cargando artefacto de modelo desde %s", self.model_path)
            self._model = tf.keras.models.load_model(str(self.model_path), compile=False)
        else:
            logger.warning(
                "Artefacto %s no encontrado en disco. Inicializando arquitectura WilhemNet86 funcional.",
                self.model_path,
            )
            self._model = build_wilhemnet_architecture()

        self._last_conv_layer_name = self._find_last_conv_layer()
        return self._model

    @property
    def model(self) -> Any:
        """Retorna el modelo subyacente, cargándolo perezosamente si no ha sido instanciado."""
        if self._model is None:
            self.load()
        return self._model

    def _find_last_conv_layer(self) -> str:
        """Encuentra dinámicamente el nombre de la última capa convolucional 4D."""
        import tensorflow as tf

        for layer in reversed(self.model.layers):
            if isinstance(layer, (tf.keras.layers.Conv2D, tf.keras.layers.SeparableConv2D)):
                return str(layer.name)
        # Si no se encuentra Conv2D explícita, buscar cualquier capa con salida 4D
        for layer in reversed(self.model.layers):
            try:
                shape = layer.output.shape
                if len(shape) == 4 and shape[-1] not in (1, None):
                    return str(layer.name)
            except Exception:
                continue
        return "conv_last"

    def get_last_conv_layer_name(self) -> str:
        """Retorna el identificador de la última capa convolucional para Grad-CAM."""
        if self._last_conv_layer_name is None:
            self._last_conv_layer_name = self._find_last_conv_layer()
        return self._last_conv_layer_name

    def predict(self, preprocessed_tensor: np.ndarray) -> tuple[float, str]:
        """Ejecuta inferencia sobre un tensor normalizado (1, 512, 512, 1).

        Args:
            preprocessed_tensor: Tensor preprocesado float32 con dimensiones (1, 512, 512, 1).

        Returns:
            tuple[float, str]: (probabilidad de neumonía [0.0, 1.0], etiqueta diagnóstica).

        Raises:
            ValueError: Si las dimensiones del tensor no son compatibles.
        """
        if preprocessed_tensor.ndim != 4 or preprocessed_tensor.shape[0] != 1:
            raise ValueError(
                f"El tensor debe tener shape (1, H, W, 1), recibido: {preprocessed_tensor.shape}"
            )

        raw_output = self.model(preprocessed_tensor, training=False)
        prob = float(np.squeeze(raw_output.numpy()))
        label = "NEUMONÍA" if prob >= self.threshold else "NORMAL"
        return prob, label
