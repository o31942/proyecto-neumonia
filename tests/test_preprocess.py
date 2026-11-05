"""Pruebas unitarias para el módulo preprocess_img.py siguiendo el patrón AAA."""

from __future__ import annotations

import numpy as np
import pytest

from neumonia_detection.preprocess_img import (
    apply_clahe,
    normalize_tensor,
    preprocess_image,
    resize_image,
    validate_preprocessed_contract,
)


class TestPreprocessImage:
    """Suite de validación de preprocesamiento y contratos matemáticos."""

    def test_apply_clahe_enhances_contrast(self, sample_grayscale_image: np.ndarray) -> None:
        # Arrange
        original = sample_grayscale_image.copy()

        # Act
        enhanced = apply_clahe(original, clip_limit=2.0)

        # Assert
        assert enhanced.shape == original.shape
        assert enhanced.dtype == np.uint8
        # Debe haber alteración de contraste local
        assert not np.array_equal(original, enhanced)

    def test_apply_clahe_invalid_dimensions(self) -> None:
        # Arrange
        invalid_3d = np.zeros((100, 100, 3), dtype=np.uint8)

        # Act & Assert
        with pytest.raises(ValueError, match="requiere un array bidimensional"):
            apply_clahe(invalid_3d)

    def test_apply_clahe_invalid_dtype(self) -> None:
        # Arrange
        float_img = np.zeros((100, 100), dtype=np.float32)

        # Act & Assert
        with pytest.raises(ValueError, match="requiere dtype np.uint8"):
            apply_clahe(float_img)

    def test_resize_image_dimensions(self, sample_grayscale_image: np.ndarray) -> None:
        # Arrange
        target_size = 512

        # Act
        resized = resize_image(sample_grayscale_image, target_size=target_size)

        # Assert
        assert resized.shape == (target_size, target_size)

    def test_normalize_tensor_bounds(self, sample_grayscale_image: np.ndarray) -> None:
        # Arrange
        image = sample_grayscale_image

        # Act
        normalized = normalize_tensor(image)

        # Assert
        assert normalized.dtype == np.float32
        assert float(normalized.min()) >= 0.0
        assert float(normalized.max()) <= 1.0

    def test_validate_preprocessed_contract_valid_tensor(
        self, sample_preprocessed_tensor: np.ndarray
    ) -> None:
        # Arrange
        tensor = sample_preprocessed_tensor

        # Act & Assert (no debe lanzar excepción)
        validate_preprocessed_contract(tensor, target_size=512)

    def test_validate_preprocessed_contract_nan_detection(self) -> None:
        # Arrange
        corrupt_tensor = np.zeros((1, 512, 512, 1), dtype=np.float32)
        corrupt_tensor[0, 10, 10, 0] = np.nan

        # Act & Assert
        with pytest.raises(AssertionError, match="valores no finitos"):
            validate_preprocessed_contract(corrupt_tensor)

    def test_validate_preprocessed_contract_out_of_bounds(self) -> None:
        # Arrange
        out_of_bounds_tensor = np.ones((1, 512, 512, 1), dtype=np.float32) * 1.5

        # Act & Assert
        with pytest.raises(AssertionError, match="Valores fuera de rango"):
            validate_preprocessed_contract(out_of_bounds_tensor)

    def test_preprocess_image_full_pipeline_contract(
        self, sample_grayscale_image: np.ndarray
    ) -> None:
        # Arrange
        input_image = sample_grayscale_image

        # Act
        tensor = preprocess_image(input_image, target_size=512, clip_limit=2.0)

        # Assert (Contrato formal)
        assert tensor.shape == (1, 512, 512, 1)
        assert tensor.dtype == np.float32
        assert float(tensor.min()) >= 0.0
        assert float(tensor.max()) <= 1.0
        assert np.isfinite(tensor).all()
