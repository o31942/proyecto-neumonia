"""Fixtures compartidas de pytest para la suite de pruebas unitarias (AAA Pattern)."""

from __future__ import annotations

import io
from pathlib import Path

import cv2
import numpy as np
import pydicom
from pydicom.dataset import Dataset, FileDataset, FileMetaDataset
import pytest

from neumonia_detection.load_model import PneumoniaModelLoader, build_wilhemnet_architecture


@pytest.fixture
def sample_grayscale_image() -> np.ndarray:
    """Fixture que retorna una imagen sintética 2D uint8 (256, 256) con patrones de prueba."""
    # Arrange
    img = np.zeros((256, 256), dtype=np.uint8)
    # Dibujar círculos y rectángulos para simular estructuras torácicas
    cv2.circle(img, (128, 128), 60, 180, -1)
    cv2.rectangle(img, (40, 40), (90, 200), 120, -1)
    cv2.rectangle(img, (166, 40), (216, 200), 120, -1)
    return img


@pytest.fixture
def sample_jpeg_file(tmp_path: Path, sample_grayscale_image: np.ndarray) -> Path:
    """Fixture que guarda una imagen JPEG temporal en disco y retorna su ruta."""
    # Arrange
    file_path = tmp_path / "test_xray.jpeg"
    cv2.imwrite(str(file_path), sample_grayscale_image)
    return file_path


@pytest.fixture
def sample_dicom_file(tmp_path: Path, sample_grayscale_image: np.ndarray) -> Path:
    """Fixture que genera un archivo DICOM temporal válido con metadatos mínimos."""
    # Arrange
    file_path = tmp_path / "test_xray.dcm"

    file_meta = FileMetaDataset()
    file_meta.MediaStorageSOPClassUID = "1.2.840.10008.5.1.4.1.1.7"  # Secondary Capture Image
    file_meta.MediaStorageSOPInstanceUID = "1.2.3.4.5"
    file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian

    ds = FileDataset(str(file_path), {}, file_meta=file_meta, preamble=b"\0" * 128)
    ds.Modality = "CR"
    ds.PatientName = "Test^Patient"
    ds.PatientID = "12345"
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.SamplesPerPixel = 1
    ds.PixelRepresentation = 0
    ds.HighBit = 7
    ds.BitsStored = 8
    ds.BitsAllocated = 8
    ds.Rows, ds.Columns = sample_grayscale_image.shape
    ds.PixelData = sample_grayscale_image.tobytes()

    ds.save_as(str(file_path), write_like_original=False)
    return file_path


@pytest.fixture
def sample_preprocessed_tensor() -> np.ndarray:
    """Fixture que retorna un tensor float32 con forma (1, 512, 512, 1) y valores en [0, 1]."""
    # Arrange
    np.random.seed(42)
    return np.random.uniform(0.0, 1.0, size=(1, 512, 512, 1)).astype(np.float32)


@pytest.fixture(scope="session")
def loaded_model_instance():
    """Fixture de sesión que crea una instancia de modelo compilada para pruebas rápidas."""
    # Arrange
    loader = PneumoniaModelLoader()
    loader.load()
    return loader
