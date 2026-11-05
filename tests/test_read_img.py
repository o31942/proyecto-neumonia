"""Pruebas unitarias para el módulo read_img.py siguiendo el patrón AAA."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from neumonia_detection.read_img import (
    _normalize_to_uint8,
    read_dicom,
    read_dicom_or_image,
    read_standard_image,
)


class TestReadStandardImage:
    """Pruebas para lectura de imágenes estándar (JPEG, PNG)."""

    def test_read_standard_image_from_path(self, sample_jpeg_file: Path) -> None:
        # Arrange
        file_path = sample_jpeg_file

        # Act
        image = read_standard_image(file_path)

        # Assert
        assert isinstance(image, np.ndarray)
        assert image.ndim == 2
        assert image.dtype == np.uint8
        assert image.shape == (256, 256)

    def test_read_standard_image_from_bytes(self, sample_jpeg_file: Path) -> None:
        # Arrange
        with open(sample_jpeg_file, "rb") as f:
            raw_bytes = f.read()

        # Act
        image = read_standard_image(raw_bytes)

        # Assert
        assert isinstance(image, np.ndarray)
        assert image.ndim == 2
        assert image.dtype == np.uint8

    def test_read_standard_image_file_not_found(self, tmp_path: Path) -> None:
        # Arrange
        non_existent = tmp_path / "inexistente.jpeg"

        # Act & Assert
        with pytest.raises(FileNotFoundError):
            read_standard_image(non_existent)

    def test_read_standard_image_corrupt_bytes(self) -> None:
        # Arrange
        corrupt_bytes = b"datos_binarios_no_imagen_12345"

        # Act & Assert
        with pytest.raises(ValueError, match="no corresponden a una imagen válida"):
            read_standard_image(corrupt_bytes)


class TestReadDicom:
    """Pruebas para lectura de archivos médicos DICOM."""

    def test_read_dicom_from_path(self, sample_dicom_file: Path) -> None:
        # Arrange
        file_path = sample_dicom_file

        # Act
        image = read_dicom(file_path)

        # Assert
        assert isinstance(image, np.ndarray)
        assert image.ndim == 2
        assert image.dtype == np.uint8
        assert image.shape == (256, 256)

    def test_read_dicom_from_bytes(self, sample_dicom_file: Path) -> None:
        # Arrange
        with open(sample_dicom_file, "rb") as f:
            raw_bytes = f.read()

        # Act
        image = read_dicom(raw_bytes)

        # Assert
        assert isinstance(image, np.ndarray)
        assert image.ndim == 2
        assert image.dtype == np.uint8

    def test_read_dicom_file_not_found(self, tmp_path: Path) -> None:
        # Arrange
        non_existent = tmp_path / "no_existe.dcm"

        # Act & Assert
        with pytest.raises(FileNotFoundError):
            read_dicom(non_existent)


class TestReadDicomOrImageUnified:
    """Pruebas para la función unificada read_dicom_or_image."""

    def test_unified_reader_with_jpeg(self, sample_jpeg_file: Path) -> None:
        # Arrange
        file_path = sample_jpeg_file

        # Act
        image = read_dicom_or_image(file_path)

        # Assert
        assert isinstance(image, np.ndarray)
        assert image.ndim == 2
        assert image.dtype == np.uint8

    def test_unified_reader_with_dicom(self, sample_dicom_file: Path) -> None:
        # Arrange
        file_path = sample_dicom_file

        # Act
        image = read_dicom_or_image(file_path)

        # Assert
        assert isinstance(image, np.ndarray)
        assert image.ndim == 2
        assert image.dtype == np.uint8

    def test_normalize_to_uint8_constant_array(self) -> None:
        # Arrange
        constant_arr = np.ones((50, 50), dtype=np.float32) * 42.0

        # Act
        result = _normalize_to_uint8(constant_arr)

        # Assert
        assert result.shape == (50, 50)
        assert result.dtype == np.uint8
        assert np.all(result == 0)
