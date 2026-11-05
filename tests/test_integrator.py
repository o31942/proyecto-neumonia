"""Pruebas unitarias para el módulo integrator.py siguiendo el patrón AAA."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from neumonia_detection.integrator import PneumoniaDiagnosisResult, PneumoniaPipeline
from neumonia_detection.load_model import PneumoniaModelLoader


class TestIntegratorPipeline:
    """Suite de integración end-to-end para el orquestador."""

    def test_pipeline_run_on_jpeg(
        self, sample_jpeg_file: Path, loaded_model_instance: PneumoniaModelLoader
    ) -> None:
        # Arrange
        pipeline = PneumoniaPipeline(model_loader=loaded_model_instance)
        file_path = sample_jpeg_file

        # Act
        result = pipeline.run(file_path, source_name="test_chest.jpeg")

        # Assert
        assert isinstance(result, PneumoniaDiagnosisResult)
        assert result.source_identifier == "test_chest.jpeg"
        assert 0.0 <= result.probability <= 1.0
        assert result.prediction_label in ["NORMAL", "NEUMONÍA"]
        assert isinstance(result.is_pneumonia, bool)
        assert result.raw_image.ndim == 2
        assert result.preprocessed_tensor.shape == (1, 512, 512, 1)
        assert result.gradcam_overlay.ndim == 3
        assert result.gradcam_overlay.shape[-1] == 3
        assert result.inference_time_ms > 0.0

    def test_pipeline_run_on_dicom(
        self, sample_dicom_file: Path, loaded_model_instance: PneumoniaModelLoader
    ) -> None:
        # Arrange
        pipeline = PneumoniaPipeline(model_loader=loaded_model_instance)
        file_path = sample_dicom_file

        # Act
        result = pipeline.run(file_path, source_name="test_dicom.dcm")

        # Assert
        assert isinstance(result, PneumoniaDiagnosisResult)
        assert result.source_identifier == "test_dicom.dcm"
        assert 0.0 <= result.probability <= 1.0
        assert result.preprocessed_tensor.shape == (1, 512, 512, 1)

    def test_confidence_percentage_calculation(self) -> None:
        # Arrange
        res_normal = PneumoniaDiagnosisResult(
            source_identifier="test",
            probability=0.2,
            prediction_label="NORMAL",
            is_pneumonia=False,
            raw_image=np.zeros((10, 10), dtype=np.uint8),
            preprocessed_tensor=np.zeros((1, 512, 512, 1), dtype=np.float32),
            gradcam_heatmap=np.zeros((10, 10), dtype=np.float32),
            gradcam_overlay=np.zeros((10, 10, 3), dtype=np.uint8),
            inference_time_ms=15.0,
        )
        res_pneu = PneumoniaDiagnosisResult(
            source_identifier="test2",
            probability=0.85,
            prediction_label="NEUMONÍA",
            is_pneumonia=True,
            raw_image=np.zeros((10, 10), dtype=np.uint8),
            preprocessed_tensor=np.zeros((1, 512, 512, 1), dtype=np.float32),
            gradcam_heatmap=np.zeros((10, 10), dtype=np.float32),
            gradcam_overlay=np.zeros((10, 10, 3), dtype=np.uint8),
            inference_time_ms=20.0,
        )

        # Act & Assert
        assert pytest.approx(res_normal.confidence_percentage, 0.01) == 80.0
        assert pytest.approx(res_pneu.confidence_percentage, 0.01) == 85.0
