"""Pruebas unitarias para el módulo load_model.py siguiendo el patrón AAA."""

from __future__ import annotations

import numpy as np
import pytest

from neumonia_detection.load_model import PneumoniaModelLoader, build_wilhemnet_architecture


class TestLoadModel:
    """Suite de pruebas para el cargador de modelo e inferencia en CPU."""

    def test_build_wilhemnet_architecture(self) -> None:
        # Arrange
        input_shape = (512, 512, 1)

        # Act
        model = build_wilhemnet_architecture(input_shape=input_shape)

        # Assert
        assert model is not None
        assert model.input_shape == (None, 512, 512, 1)
        assert model.output_shape == (None, 1)
        layer_names = [layer.name for layer in model.layers]
        assert "conv_last" in layer_names
        assert "output_sigmoid" in layer_names

    def test_loader_instantiation_and_lazy_load(self) -> None:
        # Arrange
        loader = PneumoniaModelLoader(threshold=0.6)

        # Act
        model = loader.model

        # Assert
        assert model is not None
        assert loader.threshold == 0.6
        assert loader.get_last_conv_layer_name() == "conv_last"

    def test_predict_returns_valid_probability_and_label(
        self, sample_preprocessed_tensor: np.ndarray, loaded_model_instance: PneumoniaModelLoader
    ) -> None:
        # Arrange
        loader = loaded_model_instance
        tensor = sample_preprocessed_tensor

        # Act
        prob, label = loader.predict(tensor)

        # Assert
        assert isinstance(prob, float)
        assert 0.0 <= prob <= 1.0
        assert label in ["NORMAL", "NEUMONÍA"]

    def test_predict_threshold_logic(
        self, sample_preprocessed_tensor: np.ndarray, loaded_model_instance: PneumoniaModelLoader
    ) -> None:
        # Arrange
        loader = loaded_model_instance
        tensor = sample_preprocessed_tensor

        # Act con umbral 0.0 (cualquier prob >= 0.0 es NEUMONÍA)
        loader.threshold = 0.0
        _, label_high = loader.predict(tensor)

        # Act con umbral 1.1 (ninguna prob <= 1.0 puede superar 1.1)
        loader.threshold = 1.1
        _, label_low = loader.predict(tensor)

        # Assert
        assert label_high == "NEUMONÍA"
        assert label_low == "NORMAL"

    def test_predict_invalid_tensor_shape(
        self, loaded_model_instance: PneumoniaModelLoader
    ) -> None:
        # Arrange
        invalid_tensor = np.zeros((512, 512), dtype=np.float32)

        # Act & Assert
        with pytest.raises(ValueError, match="El tensor debe tener shape"):
            loaded_model_instance.predict(invalid_tensor)
