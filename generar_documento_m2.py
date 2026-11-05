"""Script generador del Documento Formal de Propuesta de Proyecto M2 (15 páginas).

Cumple los lineamientos editoriales de la UAO:
- Márgenes de 2.5 cm en los 4 bordes.
- Interlineado de 1.5 líneas.
- Cuerpo de texto en 12 pt.
- Portada institucional UAO completa.
- Los 6 Capítulos obligatorios del M2.
"""

from __future__ import annotations

import os
from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Inches, Pt, RGBColor


def set_cell_background(cell, color_hex: str) -> None:
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150) -> None:
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def create_proposal_document(output_path: str) -> str:
    doc = Document()

    # Configuración de márgenes: 2.5 cm (aproximadamente 0.984 pulgadas)
    for section in doc.sections:
        section.top_margin = Inches(0.984)
        section.bottom_margin = Inches(0.984)
        section.left_margin = Inches(0.984)
        section.right_margin = Inches(0.984)

    # Estilos base
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)
    normal_style.paragraph_format.line_spacing = 1.5
    normal_style.paragraph_format.space_after = Pt(6)

    def add_p(text: str, bold=False, italic=False, space_after=6, align=WD_ALIGN_PARAGRAPH.JUSTIFY) -> None:
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(space_after)
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.name = 'Calibri'
        run.font.size = Pt(12)
        return p

    def add_h1(text: str) -> None:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(8)
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(18)
        run.font.color.rgb = RGBColor(16, 44, 87)

    def add_h2(text: str) -> None:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(53, 162, 159)

    def add_h3(text: str) -> None:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(16, 44, 87)

    # =========================================================================
    # PORTADA FORMAL INSTITUCIONAL
    # =========================================================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(36)
    p_inst.paragraph_format.space_after = Pt(8)
    r = p_inst.add_run("UNIVERSIDAD AUTÓNOMA DE OCCIDENTE\nFACULTAD DE INGENIERÍA\nMAESTRÍA EN INTELIGENCIA ARTIFICIAL Y CIENCIA DE DATOS")
    r.bold = True
    r.font.size = Pt(14)
    r.font.color.rgb = RGBColor(16, 44, 87)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(72)
    p_title.paragraph_format.space_after = Pt(12)
    r_t = p_title.add_run("PROPUESTA FORMAL DE PROYECTO (M2):\nSISTEMA MODULAR DE DETECCIÓN ASISTIDA DE NEUMONÍA EN RAYOS X CON EXPLICABILIDAD GRAD-CAM")
    r_t.bold = True
    r_t.font.size = Pt(18)
    r_t.font.color.rgb = RGBColor(16, 44, 87)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(90)
    r_s = p_sub.add_run("Formulación, Gestión Ágil, Gobernanza de IA y Planificación Industrial\nCaso 1: Neumonía (Rayos X de Tórax)")
    r_s.italic = True
    r_s.font.size = Pt(13)
    r_s.font.color.rgb = RGBColor(53, 162, 159)

    p_auth = doc.add_paragraph()
    p_auth.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_auth.paragraph_format.space_after = Pt(40)
    r_a = p_auth.add_run("AUTORES:\nEquipo de Desarrollo — Maestría en IA y CD\n\nDOCENTE:\nJan Polanco Velasco\nAsignatura: Gestión de Proyectos en IA y Ciencia de Datos")
    r_a.font.size = Pt(12)

    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_date.paragraph_format.space_before = Pt(60)
    r_d = p_date.add_run("Santiago de Cali, Colombia\n2026")
    r_d.bold = True
    r_d.font.size = Pt(12)

    doc.add_page_break()

    # =========================================================================
    # TABLA DE CONTENIDO FORMAL
    # =========================================================================
    add_h1("TABLA DE CONTENIDO OBLIGATORIA (6 CAPÍTULOS)")
    toc_items = [
        ("Capítulo 1 · Contexto y Justificación del Problema", "3"),
        ("    1.1. Justificación Clínica y Necesidad Operativa", "3"),
        ("    1.2. Restricciones Técnicas y Entorno Operacional", "4"),
        ("    1.3. Arquitectura MaaS de Referencia", "4"),
        ("    1.4. Ficha Técnica Formal del Modelo (Model Card)", "5"),
        ("Capítulo 2 · Objetivos y Matriz de Alcance", "7"),
        ("    2.1. Objetivo General", "7"),
        ("    2.2. Objetivos Específicos Medibles", "7"),
        ("    2.3. Matriz de Alcance (In-Scope, Nice-to-Have, Out-of-Scope)", "8"),
        ("Capítulo 3 · Cronograma, Hitos y Análisis de Ruta Crítica (CPM)", "9"),
        ("    3.1. Estructura de Desglose del Trabajo a 15 Días Hábiles", "9"),
        ("    3.2. Tabla de Precedencias y Duraciones de Actividades", "10"),
        ("    3.3. Análisis de Ruta Crítica (CPM) y Holguras", "10"),
        ("    3.4. Hitos de Control y Entregas Parciales", "11"),
        ("Capítulo 4 · Marco de Investigación y Mapeo CRISP-DM", "12"),
        ("    4.1. Fundamentación Radiológica y Formato DICOM vs JPEG", "12"),
        ("    4.2. Técnicas de Preprocesamiento Adaptativo (CLAHE)", "12"),
        ("    4.3. Arquitectura Convolucional WilhemNet86 e Inferencia CPU", "13"),
        ("    4.4. Fundamento Matemático de Grad-CAM (XAI)", "13"),
        ("    4.5. Mapeo Sistemático a las 6 Fases de CRISP-DM", "14"),
        ("Capítulo 5 · Historias de Usuario, Criterios de Aceptación y Estimación Ágil", "15"),
        ("    5.1. Regla de Estimación Fibonacci 1:1", "15"),
        ("    5.2. Definición Formal de Historias de Usuario (HU-01 a HU-08)", "15"),
        ("    5.3. Criterios de Aceptación (Formato Given-When-Then)", "16"),
        ("    5.4. Sincronización con el Tablero Kanban de GitHub Projects", "18"),
        ("Capítulo 6 · Gobernanza, Regulación y Gestión de Riesgos", "19"),
        ("    6.1. Clasificación bajo el EU AI Act (Sistema de Alto Riesgo)", "19"),
        ("    6.2. Estrategia de Supervisión Humana (Human-in-the-Loop)", "19"),
        ("    6.3. Transparencia, Trazabilidad y Calidad de Datos (ISO/IEC 42001)", "20"),
        ("    6.4. Matriz Integral de Riesgos y Planes de Contingencia", "21"),
        ("Referencias Bibliográficas", "23"),
    ]
    for item, page in toc_items:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.line_spacing = 1.15
        p_t.paragraph_format.space_after = Pt(2)
        r1 = p_t.add_run(item)
        r1.font.size = Pt(11)
        r2 = p_t.add_run(f" {'·' * (65 - len(item))} {page}")
        r2.font.size = Pt(11)
        r2.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_page_break()

    # =========================================================================
    # CAPÍTULO 1
    # =========================================================================
    add_h1("CAPÍTULO 1 · CONTEXTO Y JUSTIFICACIÓN DEL PROBLEMA")
    
    add_h2("1.1. Justificación Clínica y Necesidad Operativa")
    add_p(
        "La neumonía es una de las afecciones respiratorias agudas con mayor tasa de morbimortalidad a nivel global, afectando anualmente a millones de personas, especialmente en poblaciones vulnerables como niños menores de 5 años y adultos mayores. En la práctica clínica moderna, la radiografía de tórax (Chest X-Ray, CXR) constituye la prueba diagnóstica de primera línea debido a su amplia disponibilidad, bajo costo relativo y mínima dosis de radiación ionizante en comparación con la tomografía computarizada (TC)."
    )
    add_p(
        "No obstante, la interpretación de radiografías de tórax está sujeta a una elevada tasa de variabilidad inter e intraobservador entre médicos radiólogos y médicos generales de urgencias. Los estadios tempranos de la infección bacteriana o viral frecuentemente se manifiestan como opacidades alveolares tenues, infiltrados intersticiales difusos o consolidaciones basales subpleurales que pueden pasar desapercibidas en servicios de salud congestionados con fatiga médica."
    )
    add_p(
        "La integración de un sistema de visión artificial basado en aprendizaje profundo para la clasificación binaria asistida (Normal vs. Neumonía) y la localización espacial mediante mapas de activación Grad-CAM no busca sustituir el criterio médico, sino actuar como un 'segundo lector' de alta sensibilidad que mitiga errores de omisión y acelera el triaje clínico en departamentos de urgencias hospitalarias."
    )

    add_h2("1.2. Restricciones Técnicas y Entorno Operacional")
    add_p(
        "A diferencia de prototipos de laboratorio ejecutados en servidores de cómputo GPU de alto costo, el despliegue hospitalario real en economías emergentes impone restricciones de ingeniería innegociables:"
    )
    add_p(
        "1. Restricción de Hardware (Inferencia CPU): El sistema debe operar en estaciones de trabajo radiológicas estándar equipadas exclusivamente con procesadores centrales (CPU x86_64), sin exigir aceleradores NVIDIA ni dependencias propietarias de controladores CUDA."
    )
    add_p(
        "2. Heterogeneidad de Formatos Radiológicos: Debe aceptar tanto el estándar internacional de imagen médica DICOM (Digital Imaging and Communication in Medicine, PS3.3) con resoluciones dinámicas de 12 a 16 bits y metadatos de interpretación fotométrica (MONOCHROME1 vs MONOCHROME2), como imágenes exportadas en formatos comunes (JPEG/PNG)."
    )
    add_p(
        "3. Determinismo y Reproducibilidad: Está estrictamente prohibido el uso de gestores de dependencias no controlados (pip install indiscriminado) o scripts dispersos en cuadernos Jupyter (.ipynb). Toda la pila tecnológica debe garantizar aislamiento determinista con el gestor uv y contratos matemáticos verificables."
    )

    add_h2("1.3. Arquitectura MaaS de Referencia")
    add_p(
        "El proyecto se articula conceptualmente bajo el modelo MaaS (Model-as-a-Service), desacoplando el núcleo de inferencia matemática de la capa de interacción clínica. El pipeline orquestador encapsula la carga, validación de contrato, inferencia convolucional y cálculo de mapas térmicos en un servicio modular exportable, accesible tanto por interfaces web en Streamlit como por utilitarios de consola (CLI) o futuros microservicios REST."
    )

    add_h2("1.4. Ficha Técnica Formal del Modelo (Model Card)")
    add_p(
        "Siguiendo el estándar de Mitchell et al. (2019) y las directrices de gobernanza de la UAO, se documenta la Model Card del sistema:"
    )

    # Tabla Model Card
    mc_table = doc.add_table(rows=1, cols=2)
    mc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = mc_table.rows[0].cells
    hdr[0].text = "Sección Model Card"
    hdr[1].text = "Detalle y Especificación Técnica"
    set_cell_background(hdr[0], "102C57")
    set_cell_background(hdr[1], "102C57")
    hdr[0].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
    hdr[0].paragraphs[0].runs[0].bold = True
    hdr[1].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
    hdr[1].paragraphs[0].runs[0].bold = True

    mc_data = [
        ("Nombre del Modelo", "WilhemNet86 — Detección Convolucional de Neumonía en CXR"),
        ("Versión y Fecha", "Versión 0.1.0-Release · Noviembre de 2026"),
        ("Tipo de Modelo", "Red Neuronal Convolucional Profunda (CNN) con capa de activación Sigmoide para clasificación binaria."),
        ("Entorno de Ejecución", "Inferencia sobre CPU optimizada con TensorFlow / Keras en contenedor reproducible."),
        ("Uso Previsto", "Asistencia diagnóstica y priorización de triaje radiológico en radiografías de tórax anteroposteriores y posteroanteriores."),
        ("Usuarios Objetivo", "Médicos radiólogos, neumólogos, médicos de urgencias y personal de salud en atención primaria."),
        ("Métricas de Rendimiento", "Sensibilidad (Recall) ≥ 94.0%, Especificidad ≥ 90.0%, Área bajo la Curva ROC (AUC) ≥ 0.96."),
        ("Datos de Evaluación", "Cohorte radiológica balanceada con imágenes DICOM hospitalarias y series pediátricas/adultas en JPEG."),
        ("Limitaciones Conocidas", "No distingue entre etiología bacteriana y viral en su salida univariada (clasifica Patología vs Normal). Su rendimiento decae ante radiografías con severa subexposición, artefactos de movimiento o presencia masiva de dispositivos externos (cables, electrodos ECG) no enmascarados."),
        ("Consideraciones Éticas", "El modelo jamás debe tomar decisiones vinculantes de forma autónoma. Se exige supervisión humana obligatoria (Human-in-the-Loop) y revisión del mapa Grad-CAM."),
    ]
    for sec, det in mc_data:
        row = mc_table.add_row().cells
        row[0].text = sec
        row[1].text = det
        row[0].paragraphs[0].runs[0].bold = True
        set_cell_background(row[0], "F1F5F9")
        set_cell_margins(row[0], 80, 80, 100, 100)
        set_cell_margins(row[1], 80, 80, 100, 100)

    doc.add_page_break()

    # =========================================================================
    # CAPÍTULO 2
    # =========================================================================
    add_h1("CAPÍTULO 2 · OBJETIVOS Y MATRIZ DE ALCANCE")

    add_h2("2.1. Objetivo General")
    add_p(
        "Diseñar, implementar y evaluar un sistema de software modular de grado de ingeniería para la detección asistida de neumonía en radiografías de tórax a partir de imágenes DICOM y JPEG, integrando contratos formales de preprocesamiento adaptativo (CLAHE), inferencia convolucional en CPU, explicabilidad médica mediante Grad-CAM y despliegue interactivo en Streamlit bajo un entorno determinista gestionado con uv."
    )

    add_h2("2.2. Objetivos Específicos Medibles")
    add_p(
        "1. Desarrollar un subsistema controlador de ingesta y preprocesamiento de imágenes médicas capaz de estandarizar radiografías heterogéneas (DICOM de 16 bits y JPEG) a tensores float32 de dimensión (1, 512, 512, 1) acotados en [0.0, 1.0], aplicando CLAHE adaptativo con verificación formal de finitud matemática en un tiempo de ejecución menor a 100 milisegundos por imagen."
    )
    add_p(
        "2. Implementar y desacoplar el motor de inferencia convolucional (WilhemNet86) y el algoritmo de explicabilidad Grad-CAM sobre la última capa convolucional (conv_last), garantizando la generación de mapas de calor normalizados y superposiciones térmicas Jet reproducibles en CPU con una latencia de inferencia inferior a 50 milisegundos."
    )
    add_p(
        "3. Construir una suite exhaustiva de pruebas unitarias automatizadas con pytest siguiendo el patrón AAA (Arrange, Act, Assert) con una cobertura superior al 85% del código fuente, asegurando cero fallos y cumplimiento riguroso de convenciones de código con el linter Ruff."
    )
    add_p(
        "4. Empaquetar y desplegar la solución en una aplicación web interactiva en Streamlit y un contenedor Docker para CPU con usuario no privilegiado, gobernado bajo los lineamientos de Sistemas de IA de Alto Riesgo del EU AI Act."
    )

    add_h2("2.3. Matriz de Alcance (In-Scope, Nice-to-Have, Out-of-Scope)")
    add_p(
        "Para blindar el proyecto contra desviaciones de alcance (Scope Creep) durante los Sprints de desarrollo, se define la siguiente matriz de compromisos:"
    )

    scope_table = doc.add_table(rows=1, cols=3)
    scope_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    s_hdr = scope_table.rows[0].cells
    s_hdr[0].text = "Compromiso In-Scope (Obligatorio)"
    s_hdr[1].text = "Nice-to-Have (Holgura)"
    s_hdr[2].text = "Out-of-Scope (Excluido)"
    set_cell_background(s_hdr[0], "102C57")
    set_cell_background(s_hdr[1], "35A29F")
    set_cell_background(s_hdr[2], "DA4949")
    for cell in s_hdr:
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        cell.paragraphs[0].runs[0].bold = True

    scope_data = [
        ("• Lectura de DICOM (.dcm) con manejo de MONOCHROME1/2 y JPEG/PNG.", "• Generación de reportes clínicos exportables en PDF.", "• Reentrenamiento distribuido de redes neuronales desde cero en GPU."),
        ("• Preprocesamiento CLAHE (clipLimit=2.0) y resize a (512,512).", "• Carga concurrente de lotes masivos de imágenes (Batch processing).", "• Integración con sistemas PACS hospitalarios propietarios vía HL7."),
        ("• Verificación formal de contratos (shape, dtype, finitud, límites).", "• Selector interactivo de paletas de color para Grad-CAM.", "• Diagnóstico diferencial multiclase (COVID-19, tuberculosis, derrames)."),
        ("• Inferencia en CPU WilhemNet86 y explicabilidad Grad-CAM.", "• Autenticación médica por roles (RBAC).", "• Aplicaciones móviles nativas iOS / Android."),
        ("• Suite de pruebas unitarias AAA con pytest (mínimo 20 tests).", "• Telemetría de uso con Prometheus/Grafana.", "• Despliegue en clusters de Kubernetes en producción médica."),
        ("• Contenedor Docker CPU reproducible y app web en Streamlit.", "• Pruebas de estrés y benchmarking de concurrencia.", "• Prescripción farmacológica automatizada."),
    ]
    for in_s, nice_s, out_s in scope_data:
        row = scope_table.add_row().cells
        row[0].text = in_s
        row[1].text = nice_s
        row[2].text = out_s
        set_cell_margins(row[0], 60, 60, 80, 80)
        set_cell_margins(row[1], 60, 60, 80, 80)
        set_cell_margins(row[2], 60, 60, 80, 80)

    doc.add_page_break()

    # =========================================================================
    # CAPÍTULO 3
    # =========================================================================
    add_h1("CAPÍTULO 3 · CRONOGRAMA, HITOS Y ANÁLISIS DE RUTA CRÍTICA (CPM)")

    add_h2("3.1. Estructura de Desglose del Trabajo a 15 Días Hábiles")
    add_p(
        "El proyecto se estructura en un ciclo de desarrollo ágil de 15 días hábiles, organizado en 3 iteraciones semanales (Sprints de 5 días). La estimación temporal se rige por el principio de Fibonacci 1:1 adoptado en la UAO (1 Story Point = 1 Día hombre)."
    )

    add_h2("3.2. Tabla de Precedencias y Duraciones de Actividades")
    add_p(
        "A continuación se presenta la matriz de actividades del proyecto, detallando dependencias lógicas, duraciones estimadas y holguras calculadas:"
    )

    act_table = doc.add_table(rows=1, cols=6)
    act_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    a_hdr = act_table.rows[0].cells
    for i, col_name in enumerate(["ID", "Descripción de la Actividad", "Precedente", "Duración (Días)", "Holgura Total", "¿Ruta Crítica?"]):
        a_hdr[i].text = col_name
        set_cell_background(a_hdr[i], "102C57")
        a_hdr[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        a_hdr[i].paragraphs[0].runs[0].bold = True

    activities = [
        ("A1", "Configuración de entorno uv, pyproject.toml y repo Gitflow", "-", "1", "0", "SÍ"),
        ("A2", "Extracción y curaduría de muestras radiológicas (DICOM/JPG)", "A1", "1", "2", "NO"),
        ("A3", "Implementación del lector DICOM y JPEG (read_img.py)", "A1", "2", "0", "SÍ"),
        ("A4", "Implementación de CLAHE y asertos (preprocess_img.py)", "A3", "2", "0", "SÍ"),
        ("A5", "Implementación del cargador de modelo (load_model.py)", "A1", "2", "1", "NO"),
        ("A6", "Desarrollo del algoritmo Grad-CAM (grad_cam.py)", "A4, A5", "2", "0", "SÍ"),
        ("A7", "Orquestación del pipeline end-to-end (integrator.py)", "A6", "1", "0", "SÍ"),
        ("A8", "Construcción de la interfaz web en Streamlit (app.py)", "A7", "2", "0", "SÍ"),
        ("A9", "Diseño de fixtures sintéticos y conftest.py", "A4", "1", "1", "NO"),
        ("A10", "Implementación de pruebas unitarias AAA con pytest", "A8, A9", "2", "0", "SÍ"),
        ("A11", "Auditoría de calidad y formateo con Ruff", "A10", "1", "0", "SÍ"),
        ("A12", "Creación del Dockerfile CPU y verificación de imagen", "A7", "1", "2", "NO"),
        ("A13", "Sincronización de CI en GitHub Actions y PR template", "A11", "1", "0", "SÍ"),
    ]
    for row_data in activities:
        cells = act_table.add_row().cells
        for idx, val in enumerate(row_data):
            cells[idx].text = val
            if idx == 5 and val == "SÍ":
                set_cell_background(cells[idx], "FEE2E2")
                cells[idx].paragraphs[0].runs[0].bold = True
                cells[idx].paragraphs[0].runs[0].font.color.rgb = RGBColor(218, 73, 73)
            set_cell_margins(cells[idx], 50, 50, 60, 60)

    add_h2("3.3. Análisis de Ruta Crítica (CPM) y Holguras")
    add_p(
        "El cálculo de tiempos tempranos (Early Start - ES, Early Finish - EF) y tiempos tardíos (Late Start - LS, Late Finish - LF) revela que la Ruta Crítica (secuencia de actividades con Holgura Total = 0) está constituida por la cadena:"
    )
    add_p(
        "Ruta Crítica (CPM): A1 ➔ A3 ➔ A4 ➔ A6 ➔ A7 ➔ A8 ➔ A10 ➔ A11 ➔ A13 = 1 + 2 + 2 + 2 + 1 + 2 + 2 + 1 + 1 = 14 Días Hábiles.",
        bold=True
    )
    add_p(
        "Cualquier retraso en el preprocesamiento de imágenes (A4) o en el cálculo de Grad-CAM (A6) impacta directamente la fecha final de entrega. Por el contrario, la preparación de Dockerfile (A12) y el cargador de modelo (A5) poseen holguras de 2 y 1 días respectivamente, lo que permite absorber variaciones menores sin comprometer el cronograma."
    )

    add_h2("3.4. Hitos de Control y Entregas Parciales")
    add_p("• Hito 1 (Día 5): Pipeline de datos validado (Lectura DICOM/JPEG + CLAHE + Asertos de contrato aprobados al 100%).")
    add_p("• Hito 2 (Día 9): Motor de inferencia integrado con explicabilidad Grad-CAM funcional sobre conv_last.")
    add_p("• Hito 3 (Día 12): Aplicación interactiva Streamlit operativa con visualización tripartita.")
    add_p("• Hito 4 (Día 15): Suite de pruebas AAA aprobada, Dockerfile testeado y repositorio sincronizado con GitHub Actions.")

    doc.add_page_break()

    # =========================================================================
    # CAPÍTULO 4
    # =========================================================================
    add_h1("CAPÍTULO 4 · MARCO DE INVESTIGACIÓN Y MAPEO CRISP-DM")

    add_h2("4.1. Fundamentación Radiológica y Formato DICOM vs JPEG")
    add_p(
        "El estándar DICOM (Digital Imaging and Communications in Medicine) es la columna vertebral de la informática médica hospitalaria. A diferencia de imágenes JPEG de 8 bits (256 niveles de gris), los archivos DICOM de rayos X almacenan datos en escalas de 12 o 16 bits (hasta 65,536 niveles de radiancia), preservando detalles sutiles de atenuación tisular. Asimismo, integran metadatos cruciales como PhotometricInterpretation:"
    )
    add_p(
        "• MONOCHROME1: El valor de píxel cero representa blanco (densidad radiopaca). Típico en sistemas radiológicos heredados."
    )
    add_p(
        "• MONOCHROME2: El valor de píxel cero representa negro (aire/gas radiolúcido). Estándar radiológico convencional."
    )
    add_p(
        "El controlador implementado detecta activamente este atributo. Si se detecta MONOCHROME1, se aplica inversión espectral: I_norm = max(I) - I, homogeneizando la representación física antes de la ecualización."
    )

    add_h2("4.2. Técnicas de Preprocesamiento Adaptativo (CLAHE)")
    add_p(
        "La ecualización de histograma tradicional aplica una función de transformación acumulativa global sobre toda la imagen, lo que en radiografías de tórax satura las áreas hiperlúcidas de los campos pulmonares y oscurece las estructuras óseas mediastínicas. Para resolver esta distorsión, se implementa CLAHE (Contrast Limited Adaptive Histogram Equalization):"
    )
    add_p(
        "1. Descomposición Espacial: La imagen se divide en una cuadrícula de bloques contextuales contiguos (tiles) de tamaño (8, 8)."
    )
    add_p(
        "2. Limitación de Contraste (clipLimit=2.0): En cada bloque, el histograma local se trunca a un umbral máximo; el exceso de conteo de píxeles se redistribuye uniformemente entre todos los niveles de gris, suprimiendo la amplificación espuria de ruido de alta frecuencia."
    )
    add_p(
        "3. Interpolación Bilineal: Los límites entre bloques se suavizan mediante interpolación bilineal para eliminar artefactos de frontera en tablero de ajedrez."
    )

    add_h2("4.3. Arquitectura Convolucional WilhemNet86 e Inferencia CPU")
    add_p(
        "El modelo WilhemNet86 emplea una arquitectura convolucional profunda compuesta por 4 bloques secuenciales con convoluciones 2D (filtros 3x3), capas de normalización por lotes (Batch Normalization) para estabilizar gradientes y activaciones ReLU. La última capa convolucional de características profundas, denominada 'conv_last', preserva resolución espacial bidimensional con 256 filtros. La cabeza de clasificación utiliza Global Average Pooling (GAP) para reducir parámetros, Dropout al 30% contra sobreajuste y una neurona densa con activación Sigmoide continua."
    )

    add_h2("4.4. Fundamento Matemático de Grad-CAM (XAI)")
    add_p(
        "Grad-CAM (Gradient-weighted Class Activation Mapping; Selvaraju et al., 2017) proporciona explicabilidad visual calculando la importancia de cada neurona en la última capa convolucional conv_last respecto al score de clase y^c (probabilidad de neumonía):"
    )
    add_p(
        "1. Cálculo de Gradientes: Mediante tf.GradientTape se extrae la derivada parcial del score y^c respecto a los mapas de activación A^k:"
    )
    add_p(
        "   grad_k = ∂y^c / ∂A^k",
        bold=True, align=WD_ALIGN_PARAGRAPH.CENTER
    )
    add_p(
        "2. Global Average Pooling de Gradientes: Se obtiene el coeficiente de ponderación alfa_k integrando sobre las dimensiones espaciales i, j (altura y ancho del mapa):"
    )
    add_p(
        "   α_k^c = (1 / Z) ∑_i ∑_j (∂y^c / ∂A_{i,j}^k)",
        bold=True, align=WD_ALIGN_PARAGRAPH.CENTER
    )
    add_p(
        "3. Combinación Lineal y Rectificación ReLU: Se sintetiza el mapa de calor crudo aplicando ReLU para conservar exclusivamente las características que incrementan la probabilidad de neumonía:"
    )
    add_p(
        "   L_Grad-CAM^c = ReLU( ∑_k α_k^c · A^k )",
        bold=True, align=WD_ALIGN_PARAGRAPH.CENTER
    )
    add_p(
        "4. Superposición Alfa-Blending: El mapa se normaliza a [0.0, 1.0], se redimensiona a (H, W) original y se fusiona sobre la radiografía base en escala de grises: I_final = 0.4 · JetMap + 0.6 · I_base."
    )

    add_h2("4.5. Mapeo Sistemático a las 6 Fases de CRISP-DM")
    add_p("• Fase 1: Comprensión del Negocio (Business Understanding): Reducción de variabilidad diagnóstica y priorización de radiografías urgentes.")
    add_p("• Fase 2: Comprensión de los Datos (Data Understanding): Inspección de matrices DICOM/JPEG, rango dinámico y resolución anatómica.")
    add_p("• Fase 3: Preparación de Datos (Data Preparation): Inversión fotométrica, CLAHE, resize a 512x512 y asertos formales de finitud.")
    add_p("• Fase 4: Modelado (Modeling): Inferencia convolucional WilhemNet86 y generación de mapas térmicos Grad-CAM.")
    add_p("• Fase 5: Evaluación (Evaluation): Análisis de métricas clínicas (Sensibilidad/Especificidad), verificación de invariantes y auditoría visual de activaciones.")
    add_p("• Fase 6: Despliegue (Deployment): Empaquetado en contenedor Docker CPU, interfaz en Streamlit e integración continua con GitHub Actions.")

    doc.add_page_break()

    # =========================================================================
    # CAPÍTULO 5
    # =========================================================================
    add_h1("CAPÍTULO 5 · HISTORIAS DE USUARIO, CRITERIOS DE ACEPTACIÓN Y KANBAN")

    add_h2("5.1. Regla de Estimación Fibonacci 1:1")
    add_p(
        "En cumplimiento de las directrices metodológicas de la asignatura, la estimación de esfuerzo ágil utiliza la escala de Fibonacci estricta con equivalencia 1:1, donde 1 Story Point (SP) equivale exactamente a 1 Día-hombre de trabajo de ingeniería enfocado. Se utilizan valores de 1, 2, 3, 5 y 8 SP."
    )

    add_h2("5.2. Definición Formal de Historias de Usuario (HU)")
    add_p(
        "A continuación se detallan las 8 Historias de Usuario nucleares del proyecto, redactadas en formato estándar con sus respectivos Criterios de Aceptación (AC) bajo sintaxis Gherkin (Given-When-Then):"
    )

    # HU-01 a HU-08
    hus = [
        ("HU-01: Ingesta Dual de Imágenes Radiológicas (DICOM y JPEG)", "3 SP",
         "Como médico radiólogo, quiero cargar archivos radiológicos en formato DICOM (.dcm) o imágenes convencionales (.jpeg, .png), para procesar estudios sin necesidad de conversiones previas externas.",
         "Given un archivo DICOM válido con interpretación MONOCHROME1 o MONOCHROME2, When se invoca read_dicom_or_image(), Then el sistema retorna un array 2D monocromático de tipo np.uint8 en el rango [0, 255] con las dimensiones espaciales nativas de la radiografía."),
        
        ("HU-02: Preprocesamiento CLAHE con Verificación de Contrato", "2 SP",
         "Como ingeniero de datos de IA, quiero aplicar ecualización adaptativa CLAHE y redimensionamiento estandarizado, para garantizar que la red reciba tensores homogéneos e inmunes a valores corruptos.",
         "Given una matriz 2D uint8 de entrada, When se ejecuta preprocess_image(target_size=512, clip_limit=2.0), Then la salida es un tensor float32 con dimensiones (1, 512, 512, 1), valores acotados en [0.0, 1.0] y verificación estricta de np.isfinite() sin valores NaN ni infinitos."),

        ("HU-03: Motor de Inferencia Convolucional WilhemNet86 en CPU", "3 SP",
         "Como especialista de urgencias, quiero ejecutar la clasificación diagnóstica de la radiografía, para obtener una probabilidad continua y una etiqueta diagnóstica (NORMAL / NEUMONÍA) en menos de 50 ms.",
         "Given un tensor preprocesado (1, 512, 512, 1), When se invoca PneumoniaModelLoader.predict(), Then el sistema entrega la probabilidad continua p ∈ [0.0, 1.0] y la clasificación clínica según el umbral configurado."),

        ("HU-04: Explicabilidad Visual Médica con Grad-CAM", "3 SP",
         "Como profesional clínico, quiero visualizar un mapa térmico superpuesto sobre la radiografía, para auditar qué regiones del parénquima pulmonar fundamentaron la predicción de la IA.",
         "Given el modelo convolucional y el tensor preprocesado, When se ejecuta generate_gradcam() y overlay_heatmap(), Then se genera un mapa de calor 2D redimensionado al tamaño original de la radiografía y una imagen RGB fusionada mediante alfa-blending al 40%."),

        ("HU-05: Orquestador Desacoplado del Pipeline de Diagnóstico", "2 SP",
         "Como integrador de software, quiero un controlador desacoplado que coordine lectura, preprocesamiento, inferencia y explicabilidad, para invocar el pipeline mediante API o consola CLI.",
         "Given una ruta de archivo o buffer de bytes, When se ejecuta PneumoniaPipeline.run(), Then se retorna una estructura tipada PneumoniaDiagnosisResult con todas las métricas, latencia en ms e imágenes resultantes."),

        ("HU-06: Interfaz Web Interactiva en Streamlit", "3 SP",
         "Como usuario médico, quiero interactuar con una aplicación web moderna, para cargar estudios, seleccionar muestras y ajustar umbrales clínicos en tiempo real.",
         "Given la aplicación web iniciada en el puerto 8501, When el usuario carga una radiografía o selecciona una muestra de prueba, Then la pantalla presenta en 3 columnas comparativas la imagen original, preprocesada y Grad-CAM con sus tarjetas métricas."),

        ("HU-07: Suite de Pruebas Unitarias Automatizadas (Patrón AAA)", "2 SP",
         "Como asegurador de calidad (QA), quiero una suite de pruebas con pytest que evalúe todas las capas, para garantizar inmunidad contra regresiones antes de cada pase a producción.",
         "Given la ejecución de 'uv run pytest -v', When se ejecutan las 30 pruebas unitarias con patrón AAA, Then el 100% de los tests aprueba exitosamente en menos de 40 segundos evaluando casos límite y excepciones."),

        ("HU-08: Empaquetamiento en Contenedor Docker CPU Reproducible", "2 SP",
         "Como DevOps de IA, quiero un contenedor Docker multicapa para CPU, para desplegar la solución en cualquier infraestructura hospitalaria sin requerir tarjetas NVIDIA dedicadas.",
         "Given la construcción de la imagen con Dockerfile, When se lanza el contenedor en el puerto 8501, Then el servicio responde al Healthcheck HTTP y permite la interacción web con usuario no root appuser."),
    ]

    for title, sp, desc, ac in hus:
        add_h3(f"{title} — [{sp}]")
        add_p(desc, italic=True)
        add_p(f"Criterio de Aceptación (Gherkin): {ac}", bold=False)

    add_h2("5.4. Sincronización con el Tablero Kanban de GitHub Projects")
    add_p(
        "Todas las historias de usuario anteriores se encuentran reflejadas en el tablero Kanban público de GitHub Projects del repositorio (https://github.com/o31942/proyecto-neumonia/projects), distribuidas en el flujo de trabajo: Backlog ➔ To Do ➔ In Progress ➔ In Review ➔ Done."
    )

    doc.add_page_break()

    # =========================================================================
    # CAPÍTULO 6
    # =========================================================================
    add_h1("CAPÍTULO 6 · GOBERNANZA, REGULACIÓN Y GESTIÓN DE RIESGOS")

    add_h2("6.1. Clasificación bajo el EU AI Act (Sistema de Alto Riesgo)")
    add_p(
        "De conformidad con el Reglamento Europeo de Inteligencia Artificial (EU AI Act - Regulation 2024/1689), los sistemas de IA destinados a ser utilizados como componentes de seguridad en productos sanitarios o que constituyen dispositivos médicos de diagnóstico in vitro se clasifican estrictamente en la categoría de Sistemas de IA de Alto Riesgo (High-Risk AI Systems, Anexo III, Numeral 5)."
    )
    add_p(
        "Esta categorización exige el cumplimiento mandatario de requisitos técnicos rigurosos: gobernanza de datos de entrenamiento, documentación técnica exhaustiva, registro continuo de eventos de inferencia, transparencia clínica, supervisión humana activa y robustez contra fallos de software."
    )

    add_h2("6.2. Estrategia de Supervisión Humana (Human-in-the-Loop)")
    add_p(
        "Para dar cumplimiento al Artículo 14 del EU AI Act, el sistema implementa una arquitectura estricta de 'Human-in-the-Loop' (HITL):"
    )
    add_p(
        "1. La herramienta está tipificada exclusivamente como software de soporte a la decisión clínica (Clinical Decision Support Software - CDSS). En ningún escenario operativo emite dictámenes médicos vinculantes ni prescribe tratamientos de forma autónoma."
    )
    add_p(
        "2. La interfaz de usuario presenta de forma prominente un aviso de advertencia clínica ineludible ('Clinical Disclaimer'), recordando al operador que el juicio final recae exclusivamente en el facultativo médico matriculado."
    )
    add_p(
        "3. La visualización simultánea del mapa Grad-CAM previene el sesgo de automatización (automation bias), forzando al radiólogo a correlacionar la predicción probabilística con la semiología anatómica del paciente."
    )

    add_h2("6.3. Transparencia, Trazabilidad y Calidad de Datos (ISO/IEC 42001)")
    add_p(
        "En concordancia con el estándar internacional ISO/IEC 42001 (Sistema de Gestión de Inteligencia Artificial), el proyecto asegura:"
    )
    add_p(
        "• Trazabilidad de Versiones: Fijación determinista de versiones de software con pyproject.toml y uv.lock, garantizando que el entorno de ejecución pueda reproducirse idénticamente en auditorías técnicas."
    )
    add_p(
        "• Verificación de Invariantes Numéricos: Los asertos de finitud (np.isfinite) en la capa de preprocesamiento evitan el procesamiento de datos corruptos que degraden el rendimiento del modelo."
    )
    add_p(
        "• Auditoría de Inferencia: La estructura de resultados expone la latencia de inferencia en milisegundos y las dimensiones del tensor para auditoría hospitalaria."
    )

    add_h2("6.4. Matriz Integral de Riesgos y Planes de Contingencia")
    add_p("A continuación se evalúan los riesgos tecnológicos, éticos y operativos del sistema:")

    risk_table = doc.add_table(rows=1, cols=5)
    risk_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    r_hdr = risk_table.rows[0].cells
    for i, col_name in enumerate(["ID", "Riesgo Identificado", "Impacto", "Estrategia de Mitigación", "Plan de Contingencia"]):
        r_hdr[i].text = col_name
        set_cell_background(r_hdr[i], "102C57")
        r_hdr[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        r_hdr[i].paragraphs[0].runs[0].bold = True

    risks = [
        ("R1", "Falso Negativo (Neumonía bacteriana no detectada en estadio temprano)", "CRÍTICO", "Configurar umbral clínico de alta sensibilidad (Recall ≥ 94%) y advertencia médica explícita en casos dudosos.", "Protocolo hospitalario de confirmación diagnóstica con prueba PCR o TAC de tórax."),
        ("R2", "Sesgo por Artefactos Externos (Marcapasos/electrodos activando Grad-CAM)", "ALTO", "Supervisión visual con mapa térmico Grad-CAM; el radiólogo descarta inmediatamente activaciones fuera de los pulmones.", "Rechazo del estudio por el operador y solicitud de nueva toma radiológica limpia."),
        ("R3", "Incompatibilidad de Formatos DICOM (Tags corruptos o no estándar)", "MEDIO", "Decodificación tolerante a fallos con pydicom (force=True) y fallback a decodificación OpenCV.", "Aviso de error en pantalla solicitando exportación estándar en formato PNG."),
        ("R4", "Degradación Silenciosa por Tensores NaN/Inf en Preprocesamiento", "ALTO", "Asertos estrictos en preprocess_img.py (validate_preprocessed_contract).", "Interrupción inmediata de la ejecución antes de consumir ciclos de CPU."),
        ("R5", "Vulnerabilidad en Contenedor por Ejecución con Privilegios Root", "ALTO", "Creación de usuario dedicado sin privilegios (appuser UID 1000) en el Dockerfile.", "Aislamiento de red a nivel de host y escaneo estático de vulnerabilidades con Trivy."),
    ]
    for row_data in risks:
        cells = risk_table.add_row().cells
        for idx, val in enumerate(row_data):
            cells[idx].text = val
            if idx == 2 and val in ["CRÍTICO", "ALTO"]:
                set_cell_background(cells[idx], "FEE2E2")
                cells[idx].paragraphs[0].runs[0].bold = True
                cells[idx].paragraphs[0].runs[0].font.color.rgb = RGBColor(218, 73, 73)
            set_cell_margins(cells[idx], 50, 50, 60, 60)

    doc.add_page_break()

    # =========================================================================
    # REFERENCIAS BIBLIOGRÁFICAS
    # =========================================================================
    add_h1("REFERENCIAS BIBLIOGRÁFICAS")
    refs = [
        "1. Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., ... & Gebru, T. (2019). Model cards for model reporting. In Proceedings of the conference on fairness, accountability, and transparency (pp. 220-229).",
        "2. Selvaraju, R. R., Cogswell, M., Das, A., Vedaldi, A., Parikh, D., & Batra, D. (2017). Grad-CAM: Visual explanations from deep networks via gradient-based localization. In Proceedings of the IEEE international conference on computer vision (pp. 618-626).",
        "3. European Parliament and Council of the European Union. (2024). Regulation (EU) 2024/1689 laying down harmonised rules on artificial intelligence (Artificial Intelligence Act). Official Journal of the European Union.",
        "4. International Organization for Standardization. (2023). Information technology — Artificial intelligence — Management system (ISO/IEC Standard No. 42001:2023).",
        "5. Pianykh, O. S. (2008). Digital imaging and communications in medicine (DICOM): A practical introduction and survival guide. Springer Science & Business Media.",
        "6. Zuiderveld, K. (1994). Contrast limited adaptive histogram equalization. Graphics gems IV, 474-485.",
        "7. Chapman, P., Clinton, J., Kerber, R., Khabaza, T., Reinartz, T., Shearer, C., & Wirth, R. (2000). CRISP-DM 1.0: Step-by-step data mining guide. CRISP-DM Consortium.",
        "8. Sculley, D., Holt, G., Golovin, D., Davydov, E., Phillips, T., Ebner, D., ... & Dennison, M. (2015). Hidden technical debt in machine learning systems. Advances in neural information processing systems, 28.",
    ]
    for ref in refs:
        add_p(ref, space_after=8, align=WD_ALIGN_PARAGRAPH.LEFT)

    doc.save(output_path)
    return output_path


if __name__ == "__main__":
    out_dir = "C:/Users/odsanchez/.gemini/antigravity/scratch/proyecto-neumonia/docs"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "propuesta_formal_m2_neumonia.docx")
    path = create_proposal_document(target)
    print(f"Documento Word M2 generado exitosamente en: {path}")
