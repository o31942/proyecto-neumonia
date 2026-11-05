"""Módulo integrador del pipeline de detección de neumonía.

Capa: Controlador (Pipeline Orchestrator)
Responsabilidad única: Orquestar el flujo end-to-end conectando lectura,
preprocesamiento, inferencia del modelo y explicabilidad Grad-CAM.
"""

from __future__ import annotations

import argparse
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Union

import numpy as np

from neumonia_detection.grad_cam import generate_gradcam, overlay_heatmap
from neumonia_detection.load_model import PneumoniaModelLoader
from neumonia_detection.preprocess_img import preprocess_image
from neumonia_detection.read_img import read_dicom_or_image


@dataclass
class PneumoniaDiagnosisResult:
    """Estructura de datos que encapsula el resultado integral del diagnóstico."""

    source_identifier: str
    probability: float
    prediction_label: str
    is_pneumonia: bool
    raw_image: np.ndarray
    preprocessed_tensor: np.ndarray
    gradcam_heatmap: np.ndarray
    gradcam_overlay: np.ndarray
    inference_time_ms: float

    @property
    def confidence_percentage(self) -> float:
        """Retorna la confianza expresada en porcentaje [0.0%, 100.0%]."""
        return self.probability * 100.0 if self.is_pneumonia else (1.0 - self.probability) * 100.0


class PneumoniaPipeline:
    """Orquestador desacoplado para el análisis de Rayos X de tórax."""

    def __init__(
        self,
        model_loader: PneumoniaModelLoader | None = None,
        target_size: int = 512,
        clip_limit: float = 2.0,
        gradcam_alpha: float = 0.4,
    ) -> None:
        """Inicializa el pipeline inyectando dependencias configurables.

        Args:
            model_loader: Instancia del cargador de modelo. Si es None, se crea uno por defecto.
            target_size: Dimensión de resolución cuadrada para la red (512 por defecto).
            clip_limit: Límite de corte para CLAHE (2.0 por defecto).
            gradcam_alpha: Opacidad para la superposición de Grad-CAM (0.4 por defecto).
        """
        self.model_loader = model_loader or PneumoniaModelLoader()
        self.target_size = target_size
        self.clip_limit = clip_limit
        self.gradcam_alpha = gradcam_alpha

    def run(
        self,
        source: Union[str, Path, BinaryIO, bytes],
        source_name: str = "image",
    ) -> PneumoniaDiagnosisResult:
        """Ejecuta el pipeline de diagnóstico completo sobre una fuente de imagen.

        Args:
            source: Ruta del archivo (.dcm, .jpg, etc.), objeto binario o bytes.
            source_name: Nombre o identificador para propósitos de reporte.

        Returns:
            PneumoniaDiagnosisResult: Resultado completo estructurado.
        """
        start_time = time.perf_counter()

        # 1. Capa Controlador - Lectura
        raw_image = read_dicom_or_image(source)

        # 2. Capa Controlador - Preprocesamiento CLAHE + Resize + Contrato formal
        preprocessed_tensor = preprocess_image(
            raw_image,
            target_size=self.target_size,
            clip_limit=self.clip_limit,
        )

        # 3. Capa Modelo - Inferencia
        probability, label = self.model_loader.predict(preprocessed_tensor)
        is_pneumonia = label == "NEUMONÍA"

        # 4. Capa Modelo - Explicabilidad Grad-CAM
        last_conv = self.model_loader.get_last_conv_layer_name()
        heatmap = generate_gradcam(
            model=self.model_loader.model,
            preprocessed_tensor=preprocessed_tensor,
            last_conv_layer_name=last_conv,
        )

        # 5. Capa Modelo - Superposición
        resized_heatmap, overlay = overlay_heatmap(
            heatmap=heatmap,
            original_image=raw_image,
            alpha=self.gradcam_alpha,
        )

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return PneumoniaDiagnosisResult(
            source_identifier=source_name,
            probability=probability,
            prediction_label=label,
            is_pneumonia=is_pneumonia,
            raw_image=raw_image,
            preprocessed_tensor=preprocessed_tensor,
            gradcam_heatmap=resized_heatmap,
            gradcam_overlay=overlay,
            inference_time_ms=elapsed_ms,
        )


def main() -> None:
    """Punto de entrada de línea de comandos para el integrador."""
    parser = argparse.ArgumentParser(
        description="Pipeline CLI de Diagnóstico de Neumonía en Rayos X (UAO)"
    )
    parser.add_argument("image_path", type=str, help="Ruta a la imagen (.dcm, .jpg, .png)")
    parser.add_argument("--model-path", type=str, default="models/WilhemNet86.h5", help="Ruta al modelo .h5")
    parser.add_argument("--threshold", type=float, default=0.5, help="Umbral de clasificación")

    args = parser.parse_args()

    loader = PneumoniaModelLoader(model_path=args.model_path, threshold=args.threshold)
    pipeline = PneumoniaPipeline(model_loader=loader)

    print(f"\nProcesando imagen: {args.image_path}...")
    try:
        result = pipeline.run(args.image_path, source_name=Path(args.image_path).name)
        print("\n" + "=" * 50)
        print("          RESULTADO DEL DIAGNÓSTICO")
        print("=" * 50)
        print(f"Archivo:          {result.source_identifier}")
        print(f"Predicción:       {result.prediction_label}")
        print(f"Probabilidad:     {result.probability:.4f} ({result.confidence_percentage:.2f}%)")
        print(f"Dimensión Original: {result.raw_image.shape}")
        print(f"Tensor Preproc.:  {result.preprocessed_tensor.shape}")
        print(f"Tiempo Inferencia: {result.inference_time_ms:.2f} ms")
        print("=" * 50 + "\n")
    except Exception as exc:
        print(f"Error procesando la imagen: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
