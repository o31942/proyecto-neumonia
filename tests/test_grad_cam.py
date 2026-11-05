"""Pruebas unitarias para el módulo grad_cam.py siguiendo el patrón AAA."""

from __future__ import annotations

import numpy as np

from neumonia_detection.grad_cam import generate_gradcam, overlay_heatmap
from neumonia_detection.load_model import PneumoniaModelLoader


class TestGradCam:
    """Suite de validación de explicabilidad mediante Grad-CAM."""

    def test_generate_gradcam_heatmap_contract(
        self, sample_preprocessed_tensor: np.ndarray, loaded_model_instance: PneumoniaModelLoader
    ) -> None:
        # Arrange
        model = loaded_model_instance.model
        tensor = sample_preprocessed_tensor
        last_conv = loaded_model_instance.get_last_conv_layer_name()

        # Act
        heatmap = generate_gradcam(
            model=model,
            preprocessed_tensor=tensor,
            last_conv_layer_name=last_conv,
        )

        # Assert
        assert isinstance(heatmap, np.ndarray)
        assert heatmap.ndim == 2
        assert heatmap.dtype == np.float32
        assert float(heatmap.min()) >= 0.0
        assert float(heatmap.max()) <= 1.0

    def test_overlay_heatmap_dimensions_and_channels(
        self, sample_grayscale_image: np.ndarray
    ) -> None:
        # Arrange
        original = sample_grayscale_image
        orig_h, orig_w = original.shape
        synthetic_heatmap = np.random.uniform(0.0, 1.0, size=(64, 64)).astype(np.float32)

        # Act
        resized_map, overlay_rgb = overlay_heatmap(
            heatmap=synthetic_heatmap,
            original_image=original,
            alpha=0.4,
        )

        # Assert
        assert resized_map.shape == (orig_h, orig_w)
        assert resized_map.dtype == np.float32
        assert overlay_rgb.shape == (orig_h, orig_w, 3)
        assert overlay_rgb.dtype == np.uint8

    def test_overlay_heatmap_alpha_blending(self, sample_grayscale_image: np.ndarray) -> None:
        # Arrange
        original = sample_grayscale_image
        heatmap = np.ones((32, 32), dtype=np.float32)

        # Act
        _, overlay_low_alpha = overlay_heatmap(heatmap, original, alpha=0.1)
        _, overlay_high_alpha = overlay_heatmap(heatmap, original, alpha=0.9)

        # Assert
        assert not np.array_equal(overlay_low_alpha, overlay_high_alpha)
