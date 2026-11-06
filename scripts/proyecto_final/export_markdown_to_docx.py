# -*- coding: utf-8 -*-
"""
@file export_markdown_to_docx.py
@description Compilador Maestro bajo Estándar Oficial APA 7ma Edición (American Psychological Association):
             1. Resuelve e inserta los diagramas arquitectónicos pre-renderizados en alta resolución (04_IMAGENES_DIAGRAMAS/).
             2. Aplica formato estricto APA 7 para Figuras:
                - "Figura X" en Negrita (arriba a la izquierda).
                - Título de la figura en Cursiva (Title Case).
                - Imagen centrada y nítida (escala 2x).
                - "Nota." descriptiva y detallada al pie con contexto técnico objetivo y fuentes.
             3. Aplica formato estricto APA 7 para Tablas:
                - "Tabla X" en Negrita (arriba a la izquierda).
                - Título de la tabla en Cursiva (Title Case).
                - CERO bordes verticales (regla estricta APA 7).
                - Bordes horizontales superior, divisor de cabecera e inferior (1 pt #0F172A).
                - Anchos proporcionales calculados inteligentemente (fijados con w:tblLayout="fixed" y w:tblGrid).
                - "Nota." descriptiva y detallada al pie de la tabla.
             4. Portada Académica y Profesional APA 7 en Página 1:
                - Título del trabajo en Negrita, subtítulo, lista completa de autores (Grupo 01),
                  afiliación institucional UTP, asignatura, docente asesor y fecha.
             5. Ficha Técnica de Control Documental en la cabecera de la Página 2.
             6. Jerarquía de Títulos APA 7:
                - Nivel 1: Centrado, Negrita, Mayúsculas y Minúsculas.
                - Nivel 2: Alineado a la izquierda, Negrita.
                - Nivel 3: Alineado a la izquierda, Negrita y Cursiva.
             7. Tipografía oficial: Calibri 11 pt (cuerpo) y márgenes de 1 pulgada (2.54 cm).
             8. Encabezado con Cornisa (Running Head) y numeración dinámica (Página X de Y).
@project LeoFit Pedidos Sistema - Sustentación Proyecto Final (Semana 18)
@author Grupo 01 - UTP (Lead Architect: Lady Loayza)
"""

import os
import sys
import re
import math
import hashlib
import subprocess
import tempfile
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PROYECTO_FINAL_DIR = os.path.join(BASE_DIR, "_PROYECTO_FINAL_LOCAL")

if not os.path.exists(PROYECTO_FINAL_DIR):
    raise FileNotFoundError("_PROYECTO_FINAL_LOCAL/ no encontrado. Ejecutar en el entorno del equipo.")

ENTREGABLES_DIR = os.path.join(PROYECTO_FINAL_DIR, "02_ENTREGABLES_UTP")
HTML_DIR = os.path.abspath(os.path.join(ENTREGABLES_DIR, "00_HTML"))
DOCX_DIR = os.path.abspath(os.path.join(ENTREGABLES_DIR, "01_DOCX"))
DIAG_DIR = os.path.abspath(os.path.join(ENTREGABLES_DIR, "04_IMAGENES_DIAGRAMAS"))
CSS_FILE = os.path.join(HTML_DIR, "style.css")

os.makedirs(HTML_DIR, exist_ok=True)
os.makedirs(DOCX_DIR, exist_ok=True)
os.makedirs(DIAG_DIR, exist_ok=True)

# Leer estilos CSS maestros
CSS_CONTENT = ""
if os.path.exists(CSS_FILE):
    with open(CSS_FILE, "r", encoding="utf-8") as f:
        CSS_CONTENT = f.read()

# Metadatos descriptivos de diagramas para formato APA 7
DIAGRAM_METADATA = {
    "01_ADR-001_ELECCION_RENDER_NEON_VS_AWS": [
        {
            "title": "Árbol de Decisión Tecnológica para la Infraestructura de Despliegue",
            "note": "Diagrama de flujo de decisión arquitectónica que contrasta los requerimientos de la fase MVP y sustentación frente a producción corporativa, evaluando umbrales cuantitativos de presupuesto, concurrencia (RPS/DAU) y requisitos de cumplimiento normativo (ADR-001)."
        },
        {
            "title": "Diagrama de Transición de Estados entre la Fase MVP y la Arquitectura AWS Plena",
            "note": "Modelo de máquina de estados que especifica los tres estadios de infraestructura de LeoFit: Estado 1 (PaaS Render + Neon), Estado 2 (Híbrido con base de datos en VPC AWS) y Estado 3 (Cluster ECS Fargate Multi-AZ con Aurora Serverless v2 y Redis)."
        }
    ],
    "02_ADR-002_ARQUITECTURA_OBJETIVO_AWS_Y_COMPLEMENTOS": [
        {
            "title": "Arquitectura Objetivo Empresarial en Amazon Web Services (AWS)",
            "note": "Topología de alta disponibilidad en AWS que integra CloudFront CDN, AWS WAF, Application Load Balancer Multi-AZ, clúster ECS Fargate con contenedores Docker, Amazon Aurora Serverless v2 PostgreSQL, ElastiCache Redis y buckets S3 privados."
        },
        {
            "title": "Topología de Red y Segmentación de Seguridad Multi-AZ en AWS",
            "note": "Estructura de aislamiento de red en Virtual Private Cloud (VPC) distribuida en zonas de disponibilidad us-east-1a y us-east-1b, con subredes públicas, privadas de aplicación y aisladas de datos, orquestadas mediante Security Groups y NAT Gateways."
        },
        {
            "title": "Flujo de Emisión de CPE, Almacenamiento Seguro en S3 y Custodia Legal a 5 Años",
            "note": "Diagrama de secuencia de la arquitectura objetivo que desacopla la custodia de comprobantes (XML UBL 2.1, CDR y PDF con QR) hacia Amazon S3 Standard con regla de ciclo de vida automática hacia S3 Glacier Flexible Retrieval a los 36 meses, conforme al Artículo 87 del Código Tributario (ADR-002)."
        }
    ],
    "03_CUMPLIMIENTO_SUNAT_CPE": [
        {
            "title": "Flujo Operativo de Emisión, Firma Digital y Validación de CPE ante SUNAT",
            "note": "Diagrama de secuencia del proceso de facturación electrónica conforme al estándar UBL 2.1: generación del XML, firma digital con certificado X.509, envío al Operador de Servicios Electrónicos (OSE) o SUNAT, recepción síncrona del CDR y contingencia fiscal."
        },
        {
            "title": "Diagrama de Estados del Ciclo de Vida del Comprobante de Pago Electrónico",
            "note": "Transición de estados del documento fiscal desde su generación inicial en estado Borrador, pasando por Firmado, Emitido, Aceptado por SUNAT, Rechazado o derivado a Contingencia Offline con almacenamiento en cola resiliente."
        }
    ],
    "04_INTEGRACION_PAGOS_SANDBOX_VS_PRODUCCION": [
        {
            "title": "Flujo de Tokenización de Tarjetas y Procesamiento Seguro PCI-DSS",
            "note": "Secuencia de interacción con las pasarelas de pago (IziPay / Culqi) mediante tokenización en el cliente. Garantiza cumplimiento PCI-DSS Nivel 1 al evitar que los datos sensibles del titular de tarjeta toquen los servidores backend de LeoFit."
        },
        {
            "title": "Matriz de Transición y Segregación entre Ambientes Sandbox y Producción",
            "note": "Arquitectura de alternancia de credenciales criptográficas, endpoints de pasarela, certificados SSL y webhooks mediante variables de entorno aisladas para desarrollo, homologación académica y producción comercial."
        }
    ],
    "05_ARQUITECTURA_REPOSITORIO_Y_ESTANDARES": [
        {
            "title": "Diagrama de Contenedores y Capas Limpias (Clean Architecture) del Sistema LeoFit",
            "note": "Modelo arquitectónico de arquitectura por capas que delimita el Frontend PWA (React 19 / Vite), la API Gateway / REST Backend (Node.js / Express), la capa de dominio con validación Zod, y el motor relacional PostgreSQL 16 con pool de conexiones transaccionales."
        },
        {
            "title": "Flujo de Pipeline de Integración y Despliegue Continuo (CI/CD)",
            "note": "Automatización del ciclo de vida del software con GitHub Actions: verificación de tipado TypeScript, ejecución de 190 pruebas unitarias/integración (Jest + Vitest), escaneo de seguridad OWASP y despliegue automatizado a Render y GitHub Pages."
        }
    ]
}

DOCUMENTS = [
    {
        "id": "ENT-OFIC-001",
        "title": "Hoja Oficial de Entrega Académica y Enlaces del Proyecto Final",
        "subtitle": "Sustentación Oficial y Auditoría Técnica de Arquitectura (Semana 18)",
        "src": os.path.join(PROYECTO_FINAL_DIR, "00_HOJA_DE_ENTREGA_Y_ENLACES_PROYECTO_FINAL.md"),
        "html_dest": os.path.join(HTML_DIR, "00_HOJA_DE_ENTREGA_Y_ENLACES_PROYECTO_FINAL.html"),
        "docx_dest": os.path.join(DOCX_DIR, "00_HOJA_DE_ENTREGA_Y_ENLACES_PROYECTO_FINAL.docx"),
        "category": "ENTREGABLE OFICIAL DE SUSTENTACIÓN",
        "version": "v2.4.0",
        "date": "Noviembre de 2026",
        "doc_type": "Hoja de Entrega y Enlaces Oficiales",
        "running_head": "LEOFIT SOLUTIONS: HOJA OFICIAL DE ENTREGA SEMANA 18"
    },
    {
        "id": "ADR-001",
        "title": "ADR-001: Elección de Render + Neon PostgreSQL frente a Arquitectura AWS",
        "subtitle": "Registro de Decisión Arquitectónica para Etapa de Validación MVP y Sustentación",
        "src": os.path.join(PROYECTO_FINAL_DIR, "01_ANEXOS_TECNICOS", "01_ADR-001_ELECCION_RENDER_NEON_VS_AWS.md"),
        "html_dest": os.path.join(HTML_DIR, "01_ADR-001_ELECCION_RENDER_NEON_VS_AWS.html"),
        "docx_dest": os.path.join(DOCX_DIR, "01_ADR-001_ELECCION_RENDER_NEON_VS_AWS.docx"),
        "category": "ARQUITECTURA DE SOFTWARE (ADR)",
        "version": "v2.4.0",
        "date": "Noviembre de 2026",
        "doc_type": "Architecture Decision Record (ADR)",
        "running_head": "LEOFIT SOLUTIONS: ADR-001 RENDER Y NEON VS AWS"
    },
    {
        "id": "ADR-002",
        "title": "ADR-002: Arquitectura Objetivo Nativa AWS y Complementos Empresariales",
        "subtitle": "Diseño de Alta Disponibilidad, Escalabilidad Horizontal y Contingencia Operativa",
        "src": os.path.join(PROYECTO_FINAL_DIR, "01_ANEXOS_TECNICOS", "02_ADR-002_ARQUITECTURA_OBJETIVO_AWS_Y_COMPLEMENTOS.md"),
        "html_dest": os.path.join(HTML_DIR, "02_ADR-002_ARQUITECTURA_OBJETIVO_AWS_Y_COMPLEMENTOS.html"),
        "docx_dest": os.path.join(DOCX_DIR, "02_ADR-002_ARQUITECTURA_OBJETIVO_AWS_Y_COMPLEMENTOS.docx"),
        "category": "ARQUITECTURA DE SOFTWARE (ADR)",
        "version": "v2.4.0",
        "date": "Noviembre de 2026",
        "doc_type": "Architecture Decision Record (ADR)",
        "running_head": "LEOFIT SOLUTIONS: ADR-002 ARQUITECTURA OBJETIVO AWS"
    },
    {
        "id": "DOC-SUNAT-001",
        "title": "Anexo 03: Cumplimiento Normativo SUNAT y Comprobantes de Pago Electrónicos (CPE)",
        "subtitle": "Estándar UBL 2.1, Flujo de Facturación Electrónica, PSE/OSE y Contingencia Fiscal",
        "src": os.path.join(PROYECTO_FINAL_DIR, "01_ANEXOS_TECNICOS", "03_CUMPLIMIENTO_SUNAT_CPE.md"),
        "html_dest": os.path.join(HTML_DIR, "03_CUMPLIMIENTO_SUNAT_CPE.html"),
        "docx_dest": os.path.join(DOCX_DIR, "03_CUMPLIMIENTO_SUNAT_CPE.docx"),
        "category": "CUMPLIMIENTO NORMATIVO Y TRIBUTARIO",
        "version": "v2.4.0",
        "date": "Noviembre de 2026",
        "doc_type": "Especificación Técnica Normativa",
        "running_head": "LEOFIT SOLUTIONS: CUMPLIMIENTO SUNAT CPE UBL 2.1"
    },
    {
        "id": "DOC-PAY-001",
        "title": "Anexo 04: Integración de Pasarela de Pagos y Cumplimiento PCI-DSS",
        "subtitle": "Arquitectura de Tokenización Segura, Sandbox y Transición a Producción",
        "src": os.path.join(PROYECTO_FINAL_DIR, "01_ANEXOS_TECNICOS", "04_INTEGRACION_PAGOS_SANDBOX_VS_PRODUCCION.md"),
        "html_dest": os.path.join(HTML_DIR, "04_INTEGRACION_PAGOS_SANDBOX_VS_PRODUCCION.html"),
        "docx_dest": os.path.join(DOCX_DIR, "04_INTEGRACION_PAGOS_SANDBOX_VS_PRODUCCION.docx"),
        "category": "SEGURIDAD FINANCIERA Y PAGOS",
        "version": "v2.4.0",
        "date": "Noviembre de 2026",
        "doc_type": "Especificación de Integración Financiera",
        "running_head": "LEOFIT SOLUTIONS: PASARELA DE PAGOS Y PCI-DSS"
    },
    {
        "id": "DOC-ARCH-001",
        "title": "Anexo 05: Arquitectura del Repositorio, Patrones y Estándares de Código",
        "subtitle": "Estructura Modular Clean Architecture, Convenciones TypeScript y Flujo CI/CD",
        "src": os.path.join(PROYECTO_FINAL_DIR, "01_ANEXOS_TECNICOS", "05_ARQUITECTURA_REPOSITORIO_Y_ESTANDARES.md"),
        "html_dest": os.path.join(HTML_DIR, "05_ARQUITECTURA_REPOSITORIO_Y_ESTANDARES.html"),
        "docx_dest": os.path.join(DOCX_DIR, "05_ARQUITECTURA_REPOSITORIO_Y_ESTANDARES.docx"),
        "category": "ESTÁNDARES DE INGENIERÍA",
        "version": "v2.4.0",
        "date": "Noviembre de 2026",
        "doc_type": "Guía Oficial de Arquitectura y Estándares",
        "running_head": "LEOFIT SOLUTIONS: ARQUITECTURA Y ESTÁNDARES"
    },
    {
        "id": "DOC-TRAC-001",
        "title": "Anexo 06: Matriz de Trazabilidad Académica y Rúbrica de Evaluación",
        "subtitle": "Mapeo Integral de Criterios del Jurado contra Evidencias Reales de Código",
        "src": os.path.join(PROYECTO_FINAL_DIR, "01_ANEXOS_TECNICOS", "06_MATRIZ_TRAZABILIDAD_JURADO.md"),
        "html_dest": os.path.join(HTML_DIR, "06_MATRIZ_TRAZABILIDAD_JURADO.html"),
        "docx_dest": os.path.join(DOCX_DIR, "06_MATRIZ_TRAZABILIDAD_JURADO.docx"),
        "category": "TRAZABILIDAD Y EVALUACIÓN",
        "version": "v2.4.0",
        "date": "Noviembre de 2026",
        "doc_type": "Matriz de Trazabilidad Jurado UTP",
        "running_head": "LEOFIT SOLUTIONS: MATRIZ DE TRAZABILIDAD UTP"
    },
    {
        "id": "DOC-COMP-001",
        "title": "Compendio General de Anexos Técnicos y Arquitectura Oficial",
        "subtitle": "Índice Maestro de Especificaciones de Ingeniería — Proyecto LeoFit",
        "src": os.path.join(PROYECTO_FINAL_DIR, "01_ANEXOS_TECNICOS", "README.md"),
        "html_dest": os.path.join(HTML_DIR, "COMPENDIO_ANEXOS_TECNICOS_LEOFIT.html"),
        "docx_dest": os.path.join(DOCX_DIR, "COMPENDIO_ANEXOS_TECNICOS_LEOFIT.docx"),
        "category": "COMPENDIO MAESTRO",
        "version": "v2.4.0",
        "date": "Noviembre de 2026",
        "doc_type": "Compendio Ejecutivo de Ingeniería",
        "running_head": "LEOFIT SOLUTIONS: COMPENDIO GENERAL DE ANEXOS"
    },
    {
        "id": "AUD-REAL-001",
        "title": "Inventario Real del Código Fuente y Auditoría de Arquitectura",
        "subtitle": "Auditoría Forense de Archivos, Rutas y Métricas de Calidad ISO 25010",
        "src": os.path.join(PROYECTO_FINAL_DIR, "03_AUDITORIA_READONLY", "00_INVENTARIO_REAL.md"),
        "html_dest": os.path.join(HTML_DIR, "AUDITORIA_INVENTARIO_REAL_CODIGO.html"),
        "docx_dest": os.path.join(DOCX_DIR, "AUDITORIA_INVENTARIO_REAL_CODIGO.docx"),
        "category": "AUDITORÍA FORENSE DE SOFTWARE",
        "version": "v2.4.0",
        "date": "Noviembre de 2026",
        "doc_type": "Reporte de Auditoría Forense",
        "running_head": "LEOFIT SOLUTIONS: AUDITORÍA REAL DE CÓDIGO"
    }
]

def find_diagram_png(src_path, doc_id, index, code_text):
    """
    Busca el archivo PNG pre-renderizado del diagrama probando ambas convenciones de nombres.
    """
    base_name = os.path.splitext(os.path.basename(src_path))[0]
    h = hashlib.md5(code_text.strip().encode("utf-8")).hexdigest()[:8]

    candidate1 = os.path.join(DIAG_DIR, f"{base_name}_diag_{index+1}_{h}.png")
    if os.path.exists(candidate1) and os.path.getsize(candidate1) > 1000:
        return candidate1

    candidate2 = os.path.join(DIAG_DIR, f"{doc_id}_diag_{index+1}_{h}.png")
    if os.path.exists(candidate2) and os.path.getsize(candidate2) > 1000:
        return candidate2

    for f in os.listdir(DIAG_DIR):
        if (f.startswith(f"{base_name}_diag_{index+1}_") or f.startswith(f"{doc_id}_diag_{index+1}_")) and f.endswith(".png"):
            fp = os.path.join(DIAG_DIR, f)
            if os.path.getsize(fp) > 1000:
                return fp

    return None

def preprocess_markdown_apa7(src_path, doc_info):
    """
    Preprocesa el Markdown para dar cumplimiento estricto a las Normas APA 7ma Edición:
    1. Reemplaza bloques Mermaid por la estructura formal APA 7:
       - **Figura X**
       - *Título de la Figura*
       - Imagen centrada
       - *Nota.* Explicación técnica objetiva y detallada
    2. Elimina títulos redundantes al inicio del cuerpo para respetar la Portada APA 7.
    3. Normaliza las secciones a Heading 1 (# 1.) y subsecciones a Heading 2 (## 1.1).
    """
    with open(src_path, "r", encoding="utf-8") as f:
        content = f.read()

    doc_id = doc_info["id"]
    base_name = os.path.splitext(os.path.basename(src_path))[0]
    diag_list = DIAGRAM_METADATA.get(base_name, [])

    # 1. Sustitución de bloques Mermaid con estructura formal APA 7
    blocks = list(re.finditer(r"```mermaid(.*?)```", content, re.DOTALL))
    if blocks:
        new_content = ""
        last_end = 0
        for idx, match in enumerate(blocks):
            start, end = match.span()
            new_content += content[last_end:start]
            code_text = match.group(1)
            png_path = find_diagram_png(src_path, doc_id, idx, code_text)

            meta = diag_list[idx] if idx < len(diag_list) else {
                "title": f"Diagrama Arquitectónico del Módulo {doc_id}",
                "note": f"Diagrama técnico oficial del sistema LeoFit Solutions conforme al entregable {doc_id} (2026)."
            }

            if png_path and os.path.exists(png_path):
                norm_png = png_path.replace("\\", "/")
                apa_figure_block = (
                    f"\n\n"
                    f"**Figura {idx+1}**\n\n"
                    f"*{meta['title']}*\n\n"
                    f"![{meta['title']}]({norm_png})\n\n"
                    f"*Nota.* {meta['note']}\n\n"
                )
                new_content += apa_figure_block
            else:
                new_content += f"\n\n```text\n[Diagrama Arquitectónico {doc_id} #{idx+1}]\n```\n\n"
            last_end = end
        new_content += content[last_end:]
        content = new_content

    # 2. Eliminar encabezado inicial repetitivo previo a la Sección 1
    lines = content.splitlines()
    body_lines = []
    found_first_section = False

    for line in lines:
        if not found_first_section:
            if re.match(r"^#{1,3}\s+\d+\.", line):
                found_first_section = True
                body_lines.append(line)
            else:
                continue
        else:
            body_lines.append(line)

    restructured_text = "\n".join(body_lines)

    # 3. Normalizar niveles de encabezado
    restructured_text = re.sub(r"^#{2,3}\s+(\d+\..*)$", r"# \1", restructured_text, flags=re.MULTILINE)
    restructured_text = re.sub(r"^#{3,4}\s+(\d+\.\d+\..*)$", r"## \1", restructured_text, flags=re.MULTILINE)

    return restructured_text

def generate_formal_html(doc_info, processed_md):
    """
    Compila el Markdown procesado a una versión HTML formal con maquetación APA 7.
    """
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as tf:
        tf.write(processed_md)
        temp_md = tf.name

    try:
        cmd = ["pandoc", temp_md, "--from=gfm", "--to=html5"]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        body_html = res.stdout
    finally:
        if os.path.exists(temp_md):
            os.remove(temp_md)

    html_template = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{doc_info['id']} - {doc_info['title']}</title>
  <style>
{CSS_CONTENT}
  </style>
</head>
<body>
  <div class="document-container">
    <div class="executive-cover">
      <div class="institutional-bar">
        <div class="institutional-title">Universidad Tecnológica del Perú &bull; Facultad de Ingeniería</div>
        <div class="institutional-meta">Curso Integrador II: Sistemas de Información &bull; Ciclo 2026-I</div>
      </div>
      <div class="doc-hero">
        <div class="doc-badge-pill">{doc_info['category']} &bull; {doc_info['id']}</div>
        <h1 class="doc-main-title">{doc_info['title']}</h1>
        <div class="doc-subtitle">{doc_info['subtitle']}</div>
      </div>
      <div class="metadata-grid">
        <div class="metadata-item">
          <div class="metadata-label">PROYECTO</div>
          <div class="metadata-value">LeoFit - Gestión de Pedidos Multicanal</div>
        </div>
        <div class="metadata-item">
          <div class="metadata-label">LÍDER DE ARQUITECTURA</div>
          <div class="metadata-value">Lady Luz Loayza Rodríguez (Lead Architect)</div>
        </div>
        <div class="metadata-item">
          <div class="metadata-label">EQUIPO DE INGENIERÍA</div>
          <div class="metadata-value">Grupo 01 (Loayza, Cárdenas, Roman, Dávila, Rojas)</div>
        </div>
        <div class="metadata-item">
          <div class="metadata-label">DOCENTE ASESOR EVALUADOR</div>
          <div class="metadata-value">Ing. Enrique Lee Huamani Uriarte</div>
        </div>
        <div class="metadata-item">
          <div class="metadata-label">VERSIÓN / FECHA</div>
          <div class="metadata-value">{doc_info['version']} &bull; {doc_info['date']}</div>
        </div>
        <div class="metadata-item">
          <div class="metadata-label">ESTÁNDAR EDITORIAL</div>
          <div class="metadata-value">Normas APA 7ma Edición (Oficial UTP)</div>
        </div>
      </div>
    </div>
    <div class="document-body">
{body_html}
    </div>
  </div>
</body>
</html>
"""
    with open(doc_info["html_dest"], "w", encoding="utf-8") as f:
        f.write(html_template)

    return doc_info["html_dest"]

def convert_md_to_docx_via_pandoc(processed_md, dest_docx):
    """
    Compila el Markdown procesado a documento Word nativo vía Pandoc.
    """
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as tf:
        tf.write(processed_md)
        temp_md = tf.name

    try:
        cmd = [
            "pandoc",
            temp_md,
            "-o", dest_docx,
            "--from=gfm",
            "--to=docx"
        ]
        subprocess.run(cmd, capture_output=True, text=True, check=True)
    finally:
        if os.path.exists(temp_md):
            os.remove(temp_md)

def apply_table_cell_margins(table, top_dxa=100, bottom_dxa=100, left_dxa=140, right_dxa=140):
    """Configura márgenes celulares generosos para evitar texto pegado a los bordes."""
    tblPr = table._tbl.tblPr
    tblCellMar = parse_xml(r'''
        <w:tblCellMar {} >
            <w:top w:w="{}" w:type="dxa"/>
            <w:bottom w:w="{}" w:type="dxa"/>
            <w:left w:w="{}" w:type="dxa"/>
            <w:right w:w="{}" w:type="dxa"/>
        </w:tblCellMar>
    '''.format(nsdecls('w'), top_dxa, bottom_dxa, left_dxa, right_dxa))
    tblPr.append(tblCellMar)

def insert_apa7_title_page(doc, doc_info):
    """
    Construye la Portada Académica y Profesional Oficial bajo Normas APA 7ma Edición (Página 1):
    1. Banner institucional superior con los dos tonos de la UTP (#0F172A y #2563EB).
    2. Badge pill estilizado con categoría documental y código identificador.
    3. Título del Proyecto empresarial (LeoFit Solutions) y Título Principal en negrita y alto contraste.
    4. Subtítulo técnico formal y línea divisoria decorativa Cobalt.
    5. Tarjeta ejecutiva de metadatos del proyecto y autores (Grupo 01) con roles y docente asesor.
    6. Pie de página institucional formal con ubicación geográfica ("Lima, Perú") y fecha oficial.
    7. Salto de página y Ficha Técnica de Control Documental al inicio de la Página 2.
    """
    if not doc.paragraphs:
        doc.add_paragraph()
    p_first = doc.paragraphs[0]

    # --- 1. BANNER INSTITUCIONAL SUPERIOR UTP ---
    tbl_inst = doc.add_table(rows=2, cols=2)
    tbl_inst.alignment = WD_TABLE_ALIGNMENT.CENTER
    apply_table_cell_margins(tbl_inst, top_dxa=40, bottom_dxa=40, left_dxa=60, right_dxa=60)
    tbl_inst._tbl.tblPr.append(parse_xml(r'<w:tblLayout {} w:type="fixed"/>'.format(nsdecls('w'))))
    col_w_inst = [Inches(4.5), Inches(2.0)]
    tbl_inst._tbl.append(parse_xml(r'<w:tblGrid {}><w:gridCol w:w="6480"/><w:gridCol w:w="2880"/></w:tblGrid>'.format(nsdecls('w'))))

    r0 = tbl_inst.rows[0]
    r0._tr.get_or_add_trPr().append(parse_xml(r'<w:cantSplit {}/>'.format(nsdecls('w'))))
    c00, c01 = r0.cells[0], r0.cells[1]
    c00.width = col_w_inst[0]
    c01.width = col_w_inst[1]

    # Sin bordes exteriores en fila de texto
    bdr_none = parse_xml(r'''
        <w:tcBorders {} >
            <w:top w:val="none"/>
            <w:left w:val="none"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
        </w:tcBorders>
    '''.format(nsdecls('w')))
    c00._tc.get_or_add_tcPr().append(bdr_none)
    c01._tc.get_or_add_tcPr().append(parse_xml(r'''
        <w:tcBorders {} >
            <w:top w:val="none"/>
            <w:left w:val="none"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
        </w:tcBorders>
    '''.format(nsdecls('w'))))

    p00 = c00.paragraphs[0]
    p00.paragraph_format.space_before = Pt(0)
    p00.paragraph_format.space_after = Pt(2)
    p00.paragraph_format.line_spacing = 1.15
    r_u1 = p00.add_run("UNIVERSIDAD TECNOLÓGICA DEL PERÚ\n")
    r_u1.font.name = "Calibri"
    r_u1.font.size = Pt(11)
    r_u1.font.bold = True
    r_u1.font.color.rgb = RGBColor(15, 23, 42)
    r_u2 = p00.add_run("FACULTAD DE INGENIERÍA\n")
    r_u2.font.name = "Calibri"
    r_u2.font.size = Pt(9.5)
    r_u2.font.bold = True
    r_u2.font.color.rgb = RGBColor(71, 85, 105)
    r_u3 = p00.add_run("Carrera Profesional de Ingeniería de Sistemas e Informática")
    r_u3.font.name = "Calibri"
    r_u3.font.size = Pt(8.5)
    r_u3.font.color.rgb = RGBColor(100, 116, 139)

    p01 = c01.paragraphs[0]
    p01.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p01.paragraph_format.space_before = Pt(0)
    p01.paragraph_format.space_after = Pt(2)
    p01.paragraph_format.line_spacing = 1.15
    r_c1 = p01.add_run("CURSO INTEGRADOR II\n")
    r_c1.font.name = "Calibri"
    r_c1.font.size = Pt(9.5)
    r_c1.font.bold = True
    r_c1.font.color.rgb = RGBColor(30, 64, 175)
    r_c2 = p01.add_run("SISTEMAS DE INFORMACIÓN\n")
    r_c2.font.name = "Calibri"
    r_c2.font.size = Pt(8.5)
    r_c2.font.bold = True
    r_c2.font.color.rgb = RGBColor(71, 85, 105)
    r_c3 = p01.add_run("Sección 35374 — Ciclo 2026-I")
    r_c3.font.name = "Calibri"
    r_c3.font.size = Pt(8)
    r_c3.font.color.rgb = RGBColor(100, 116, 139)

    # Fila 1: Línea decorativa dual institucional (Navy + Cobalt)
    r1 = tbl_inst.rows[1]
    r1._tr.get_or_add_trPr().append(parse_xml(r'<w:cantSplit {}/>'.format(nsdecls('w'))))
    r1._tr.get_or_add_trPr().append(parse_xml(r'<w:trHeight {} w:val="30" w:hRule="exact"/>'.format(nsdecls('w'))))
    c10, c11 = r1.cells[0], r1.cells[1]
    c10.width = col_w_inst[0]
    c11.width = col_w_inst[1]
    c10._tc.get_or_add_tcPr().append(parse_xml(r'<w:shd {} w:fill="0F172A"/>'.format(nsdecls('w'))))
    c11._tc.get_or_add_tcPr().append(parse_xml(r'<w:shd {} w:fill="2563EB"/>'.format(nsdecls('w'))))
    c10.paragraphs[0].paragraph_format.space_before = Pt(0)
    c10.paragraphs[0].paragraph_format.space_after = Pt(0)
    c11.paragraphs[0].paragraph_format.space_before = Pt(0)
    c11.paragraphs[0].paragraph_format.space_after = Pt(0)

    p_first._p.addprevious(tbl_inst._tbl)

    # --- 2. ESPACIADOR ---
    p_sp1 = p_first.insert_paragraph_before("")
    p_sp1.paragraph_format.space_before = Pt(14)
    p_sp1.paragraph_format.space_after = Pt(0)

    # --- 3. BADGE PILL (IDENTIFICADOR DEL DOCUMENTO) ---
    tbl_pill = doc.add_table(rows=1, cols=1)
    tbl_pill.alignment = WD_TABLE_ALIGNMENT.CENTER
    apply_table_cell_margins(tbl_pill, top_dxa=40, bottom_dxa=40, left_dxa=90, right_dxa=90)
    tbl_pill._tbl.tblPr.append(parse_xml(r'<w:tblLayout {} w:type="fixed"/>'.format(nsdecls('w'))))
    tbl_pill._tbl.append(parse_xml(r'<w:tblGrid {}><w:gridCol w:w="7920"/></w:tblGrid>'.format(nsdecls('w'))))
    cpill = tbl_pill.rows[0].cells[0]
    cpill.width = Inches(5.5)
    cpill._tc.get_or_add_tcPr().append(parse_xml(r'<w:shd {} w:fill="EFF6FF"/>'.format(nsdecls('w'))))
    bdr_pill = parse_xml(r'''
        <w:tcBorders {} >
            <w:top w:val="single" w:sz="4" w:space="0" w:color="93C5FD"/>
            <w:left w:val="single" w:sz="4" w:space="0" w:color="93C5FD"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="93C5FD"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="93C5FD"/>
        </w:tcBorders>
    '''.format(nsdecls('w')))
    cpill._tc.get_or_add_tcPr().append(bdr_pill)
    ppill = cpill.paragraphs[0]
    ppill.alignment = WD_ALIGN_PARAGRAPH.CENTER
    ppill.paragraph_format.space_before = Pt(0)
    ppill.paragraph_format.space_after = Pt(0)
    rp = ppill.add_run(f"PROYECTO FINAL  |  {doc_info.get('category', 'ENTREGABLE OFICIAL')}  |  {doc_info['id']}")
    rp.font.name = "Calibri"
    rp.font.size = Pt(8.5)
    rp.font.bold = True
    rp.font.color.rgb = RGBColor(30, 64, 175)

    p_first._p.addprevious(tbl_pill._tbl)

    # --- 4. ESPACIADOR ---
    p_sp2 = p_first.insert_paragraph_before("")
    p_sp2.paragraph_format.space_before = Pt(16)
    p_sp2.paragraph_format.space_after = Pt(0)

    # --- 5. OVERTITLE (NOMBRE DEL PROYECTO) ---
    p_over = p_first.insert_paragraph_before("SISTEMA DE GESTIÓN DE PEDIDOS MULTICANAL — LEOFIT SOLUTIONS")
    p_over.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_over.paragraph_format.space_before = Pt(0)
    p_over.paragraph_format.space_after = Pt(6)
    ro = p_over.runs[0]
    ro.font.name = "Calibri"
    ro.font.size = Pt(10)
    ro.font.bold = True
    ro.font.color.rgb = RGBColor(30, 58, 138)

    # --- 6. TÍTULO PRINCIPAL DEL DOCUMENTO ---
    p_title = p_first.insert_paragraph_before(doc_info["title"])
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(6)
    p_title.paragraph_format.line_spacing = 1.15
    rt = p_title.runs[0]
    rt.font.name = "Calibri"
    rt.font.size = Pt(19)
    rt.font.bold = True
    rt.font.color.rgb = RGBColor(15, 23, 42)

    # --- 7. SUBTÍTULO ---
    p_sub = p_first.insert_paragraph_before(doc_info["subtitle"])
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(14)
    rsub = p_sub.runs[0]
    rsub.font.name = "Calibri"
    rsub.font.size = Pt(11)
    rsub.font.italic = True
    rsub.font.color.rgb = RGBColor(71, 85, 105)

    # --- 8. LÍNEA DIVISORIA COBALT ---
    rule_tbl = doc.add_table(rows=1, cols=1)
    rule_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    rcell = rule_tbl.rows[0].cells[0]
    rcell.width = Inches(3.2)
    rcell._tc.get_or_add_tcPr().append(parse_xml(r'<w:shd {} w:fill="2563EB"/>'.format(nsdecls('w'))))
    rule_tbl.rows[0]._tr.get_or_add_trPr().append(parse_xml(r'<w:trHeight {} w:val="25" w:hRule="exact"/>'.format(nsdecls('w'))))
    rcell.paragraphs[0].paragraph_format.space_before = Pt(0)
    rcell.paragraphs[0].paragraph_format.space_after = Pt(0)
    p_first._p.addprevious(rule_tbl._tbl)

    # --- 9. ESPACIADOR ANTES DE LA TARJETA ---
    p_sp3 = p_first.insert_paragraph_before("")
    p_sp3.paragraph_format.space_before = Pt(18)
    p_sp3.paragraph_format.space_after = Pt(0)

    # --- 10. TARJETA EJECUTIVA DE METADATOS Y AUTORES ---
    card_tbl = doc.add_table(rows=3, cols=2)
    card_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    apply_table_cell_margins(card_tbl, top_dxa=60, bottom_dxa=60, left_dxa=110, right_dxa=110)
    card_tbl._tbl.tblPr.append(parse_xml(r'<w:tblLayout {} w:type="fixed"/>'.format(nsdecls('w'))))
    card_tbl._tbl.append(parse_xml(r'<w:tblGrid {}><w:gridCol w:w="3312"/><w:gridCol w:w="6048"/></w:tblGrid>'.format(nsdecls('w'))))

    card_widths = [Inches(2.3), Inches(4.2)]
    card_data = [
        (
            [("AUTORES / GRUPO 01", True, 7.5, RGBColor(100, 116, 139)),
             ("Equipo de Ingeniería de Software", True, 9, RGBColor(15, 23, 42)),
             ("Facultad de Ingeniería — UTP", False, 8, RGBColor(100, 116, 139))],
            [("INTEGRANTES Y ROLES ASIGNADOS:", True, 7.5, RGBColor(100, 116, 139)),
             ("• Lady Luz Loayza Rodríguez — Scrum Master & DevSecOps Lead\n"
              "• Víctor Leandro Cárdenas Fernández — Product Owner & DBA Lead\n"
              "• Harley Anthony Roman Delgado — Frontend Lead & UI/UX Specialist\n"
              "• Jim Alessandro Dávila Morales — QA Lead & Backend Developer\n"
              "• Daniel Enrique Rojas Sánchez — Business Analyst & Cloud DevOps", False, 8.5, RGBColor(30, 41, 59))]
        ),
        (
            [("DOCENTE ASESOR EVALUADOR", True, 7.5, RGBColor(100, 116, 139)),
             ("Ing. Enrique Lee Huamani Uriarte", True, 9, RGBColor(15, 23, 42)),
             ("Docente Titular del Curso", False, 8, RGBColor(100, 116, 139))],
            [("INFORMACIÓN ACADÉMICA Y TÉCNICA:", True, 7.5, RGBColor(100, 116, 139)),
             (f"• Asignatura: Curso Integrador II — Sistemas de Información (100000S12F)\n"
              f"• Código Documental: {doc_info['id']} | Versión Evaluada: {doc_info['version']}\n"
              f"• Tipo de Documento: {doc_info.get('doc_type', 'Especificación Técnica')}", False, 8.5, RGBColor(30, 41, 59))]
        ),
        (
            [("ENTORNO EMPRESARIAL", True, 7.5, RGBColor(100, 116, 139)),
             ("LeoFit Solutions S.A.C.", True, 9, RGBColor(15, 23, 42)),
             ("Gestión de Pedidos Multicanal", False, 8, RGBColor(100, 116, 139))],
            [("ESTÁNDAR EDITORIAL Y EVALUACIÓN:", True, 7.5, RGBColor(100, 116, 139)),
             ("• Estándar Editorial: Normas APA 7ma Edición (Estándar Académico UTP)\n"
              "• Estado del Entregable: Aprobado para Sustentación Final de Arquitectura", False, 8.5, RGBColor(30, 41, 59))]
        )
    ]

    for row_idx, row_content in enumerate(card_data):
        row = card_tbl.rows[row_idx]
        row._tr.get_or_add_trPr().append(parse_xml(r'<w:cantSplit {}/>'.format(nsdecls('w'))))
        for col_idx in range(2):
            cell = row.cells[col_idx]
            cell.width = card_widths[col_idx]
            cell._tc.get_or_add_tcPr().append(parse_xml(r'<w:shd {} w:fill="F8FAFC"/>'.format(nsdecls('w'))))
            bdr = parse_xml(r'''
                <w:tcBorders {} >
                    <w:top w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                    <w:left w:val="{}" w:sz="6" w:space="0" w:color="CBD5E1"/>
                    <w:bottom w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                    <w:right w:val="{}" w:sz="6" w:space="0" w:color="CBD5E1"/>
                </w:tcBorders>
            '''.format(nsdecls('w'), "single" if col_idx == 0 else "none", "single" if col_idx == 1 else "none"))
            cell._tc.get_or_add_tcPr().append(bdr)

            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.15
            items = row_content[col_idx]
            for text, is_bold, sz, color in items:
                r_item = p.add_run(text + "\n" if text != items[-1][0] else text)
                r_item.font.name = "Calibri"
                r_item.font.size = Pt(sz)
                r_item.font.bold = is_bold
                r_item.font.color.rgb = color

    p_first._p.addprevious(card_tbl._tbl)

    # --- 11. ESPACIADOR ---
    p_sp4 = p_first.insert_paragraph_before("")
    p_sp4.paragraph_format.space_before = Pt(16)
    p_sp4.paragraph_format.space_after = Pt(0)

    # --- 12. FECHA Y CIUDAD ---
    p_city = p_first.insert_paragraph_before("Lima, Perú  —  Noviembre de 2026")
    p_city.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_city.paragraph_format.space_before = Pt(0)
    p_city.paragraph_format.space_after = Pt(2)
    rc = p_city.runs[0]
    rc.font.name = "Calibri"
    rc.font.size = Pt(9.5)
    rc.font.bold = True
    rc.font.color.rgb = RGBColor(15, 23, 42)

    p_subcity = p_first.insert_paragraph_before("Sustentación de Proyecto Final de Carrera  •  Semana 18")
    p_subcity.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_subcity.paragraph_format.space_before = Pt(0)
    p_subcity.paragraph_format.space_after = Pt(0)
    rsc = p_subcity.runs[0]
    rsc.font.name = "Calibri"
    rsc.font.size = Pt(8)
    rsc.font.color.rgb = RGBColor(100, 116, 139)

    # --- 13. SALTO DE PÁGINA FORMAL DE PORTADA (TERMINA PÁGINA 1) ---
    p_break = p_first.insert_paragraph_before()
    p_break.paragraph_format.space_before = Pt(0)
    p_break.paragraph_format.space_after = Pt(0)
    p_break.add_run().add_break(WD_BREAK.PAGE)

    # --- PÁGINA 2: FICHA TÉCNICA DE CONTROL DOCUMENTAL APA 7 ---
    f_tbl = doc.add_table(rows=2, cols=4)
    f_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    apply_table_cell_margins(f_tbl, top_dxa=70, bottom_dxa=70, left_dxa=100, right_dxa=100)

    tblPr = f_tbl._tbl.tblPr
    tblPr.append(parse_xml(r'<w:tblLayout {} w:type="fixed"/>'.format(nsdecls('w'))))

    col_widths = [Inches(1.625), Inches(1.625), Inches(1.625), Inches(1.625)]
    grid_cols = ''.join([r'<w:gridCol {} w:w="2340"/>'.format(nsdecls('w')) for _ in range(4)])
    f_tbl._tbl.append(parse_xml(r'<w:tblGrid {}>{}</w:tblGrid>'.format(nsdecls('w'), grid_cols)))

    headers = ["CÓDIGO OFICIAL", "ESTADO TÉCNICO", "VERSIÓN EVALUADA", "CLASIFICACIÓN"]
    values = [doc_info["id"], "APROBADO", doc_info["version"], "OFICIAL UTP"]

    row_hdr = f_tbl.rows[0]
    row_hdr._tr.get_or_add_trPr().append(parse_xml(r'<w:cantSplit {}/>'.format(nsdecls('w'))))
    for idx, cell in enumerate(row_hdr.cells):
        cell.width = col_widths[idx]
        cell._tc.get_or_add_tcPr().append(parse_xml(r'<w:tcW {} w:w="2340" w:type="dxa"/>'.format(nsdecls('w'))))
        cell._tc.get_or_add_tcPr().append(parse_xml(r'<w:shd {} w:fill="0F172A"/>'.format(nsdecls('w'))))
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(headers[idx])
        r.font.name = "Calibri"
        r.font.size = Pt(7.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    row_val = f_tbl.rows[1]
    row_val._tr.get_or_add_trPr().append(parse_xml(r'<w:cantSplit {}/>'.format(nsdecls('w'))))
    for idx, cell in enumerate(row_val.cells):
        cell.width = col_widths[idx]
        cell._tc.get_or_add_tcPr().append(parse_xml(r'<w:tcW {} w:w="2340" w:type="dxa"/>'.format(nsdecls('w'))))
        cell._tc.get_or_add_tcPr().append(parse_xml(r'<w:shd {} w:fill="F8FAFC"/>'.format(nsdecls('w'))))
        bdr = parse_xml(r'''
            <w:tcBorders {} >
                <w:bottom w:val="single" w:sz="8" w:space="0" w:color="0F172A"/>
            </w:tcBorders>
        '''.format(nsdecls('w')))
        cell._tc.get_or_add_tcPr().append(bdr)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(values[idx])
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(30, 64, 175)

    p_first._p.addprevious(f_tbl._tbl)

    # Espaciador antes de la Sección 1
    p_sp_sec = p_first.insert_paragraph_before("")
    p_sp_sec.paragraph_format.space_before = Pt(16)
    p_sp_sec.paragraph_format.space_after = Pt(0)

    # Limpiar p_first si quedó como párrafo en blanco
    if not p_first.text.strip():
        p_first._p.getparent().remove(p_first._p)

def setup_apa7_headers_and_footers(section, doc_info):
    """
    Configura encabezados y pies de página conforme a APA 7ma Edición:
    - Portada aislada (different_first_page_header_footer = True) sin cornisa ni pie.
    - Cornisa (Running head) a la izquierda en mayúsculas sostenidas desde la Página 2.
    - Paginación dinámica en la esquina superior derecha (Página X de Y).
    - Pie de página formal confidencial UTP en páginas interiores.
    """
    section.different_first_page_header_footer = True

    # 1. Limpiar encabezado y pie de página en la primera página (Portada formal sin cornisa ni paginación)
    first_h = section.first_page_header
    first_h.is_linked_to_previous = False
    for p in first_h.paragraphs:
        p.text = ""

    first_f = section.first_page_footer
    first_f.is_linked_to_previous = False
    for p in first_f.paragraphs:
        p.text = ""

    # 2. Encabezado a partir de la Página 2
    header = section.header
    header.is_linked_to_previous = False
    hp = header.paragraphs[0]
    hp.text = ""

    tbl_h = header.add_table(rows=1, cols=2, width=Inches(6.5))
    tbl_h.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_hl, c_hr = tbl_h.rows[0].cells[0], tbl_h.rows[0].cells[1]
    c_hl.width = Inches(4.8)
    c_hr.width = Inches(1.7)

    bdr_h = parse_xml(r'''
        <w:tcBorders {} >
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
        </w:tcBorders>
    '''.format(nsdecls('w')))
    c_hl._tc.get_or_add_tcPr().append(bdr_h)
    c_hr._tc.get_or_add_tcPr().append(parse_xml(r'''
        <w:tcBorders {} >
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
        </w:tcBorders>
    '''.format(nsdecls('w'))))

    p_hl = c_hl.paragraphs[0]
    p_hl.paragraph_format.space_before = Pt(0)
    p_hl.paragraph_format.space_after = Pt(3)
    r_hl = p_hl.add_run(doc_info.get("running_head", f"LEOFIT SOLUTIONS: {doc_info['id']}"))
    r_hl.font.name = "Calibri"
    r_hl.font.size = Pt(8.5)
    r_hl.font.color.rgb = RGBColor(100, 116, 139)

    p_hr = c_hr.paragraphs[0]
    p_hr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_hr.paragraph_format.space_before = Pt(0)
    p_hr.paragraph_format.space_after = Pt(3)
    r_hr_pre = p_hr.add_run("Página ")
    r_hr_pre.font.name = "Calibri"
    r_hr_pre.font.size = Pt(8.5)
    r_hr_pre.font.color.rgb = RGBColor(100, 116, 139)

    fld1 = parse_xml(r'<w:fldChar {} w:fldCharType="begin"/>'.format(nsdecls('w')))
    instr1 = parse_xml(r'<w:instrText {} xml:space="preserve"> PAGE </w:instrText>'.format(nsdecls('w')))
    fld2 = parse_xml(r'<w:fldChar {} w:fldCharType="separate"/>'.format(nsdecls('w')))
    fld3 = parse_xml(r'<w:fldChar {} w:fldCharType="end"/>'.format(nsdecls('w')))
    p_hr._p.append(fld1)
    p_hr._p.append(instr1)
    p_hr._p.append(fld2)
    p_hr._p.append(fld3)

    r_hr_mid = p_hr.add_run(" de ")
    r_hr_mid.font.name = "Calibri"
    r_hr_mid.font.size = Pt(8.5)
    r_hr_mid.font.color.rgb = RGBColor(100, 116, 139)

    fld4 = parse_xml(r'<w:fldChar {} w:fldCharType="begin"/>'.format(nsdecls('w')))
    instr2 = parse_xml(r'<w:instrText {} xml:space="preserve"> NUMPAGES </w:instrText>'.format(nsdecls('w')))
    fld5 = parse_xml(r'<w:fldChar {} w:fldCharType="separate"/>'.format(nsdecls('w')))
    fld6 = parse_xml(r'<w:fldChar {} w:fldCharType="end"/>'.format(nsdecls('w')))
    p_hr._p.append(fld4)
    p_hr._p.append(instr2)
    p_hr._p.append(fld5)
    p_hr._p.append(fld6)

    # 3. Pie de página en páginas interiores
    footer = section.footer
    footer.is_linked_to_previous = False
    fp = footer.paragraphs[0]
    fp.text = ""
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fp.paragraph_format.space_before = Pt(4)
    fp.paragraph_format.space_after = Pt(0)
    rf = fp.add_run("Universidad Tecnológica del Perú  |  Sustentación de Proyecto Final (Semana 18)  |  Confidencial")
    rf.font.name = "Calibri"
    rf.font.size = Pt(8)
    rf.font.color.rgb = RGBColor(148, 163, 184)

def format_apa7_tables(doc):
    """
    Aplica el formato estricto de tablas de las Normas APA 7ma Edición:
    1. CERO bordes verticales.
    2. Borde horizontal superior sólido de 1.0 pt (#0F172A).
    3. Borde horizontal inferior en la fila de cabecera de 1.0 pt (#0F172A).
    4. Borde horizontal inferior al final de la tabla de 1.0 pt (#0F172A).
    5. Bordes horizontales interiores sutiles (#E2E8F0) para delimitar filas.
    6. Distribución de anchos proporcionales inteligentes (fijo a 6.5 pulgadas / 9,360 dxa).
    """
    total_table_inches = 6.5

    for table in doc.tables:
        row_count = len(table.rows)
        if row_count == 0:
            continue

        first_cell_text = table.rows[0].cells[0].text.strip()
        # Omitir tablas que forman parte de la portada o ficha técnica
        if (
            "UNIVERSIDAD TECNOLÓGICA DEL PERÚ" in first_cell_text
            or "PROYECTO FINAL" in first_cell_text
            or "CÓDIGO OFICIAL" in first_cell_text
            or "AUTORES" in first_cell_text
            or (len(table.rows) == 1 and len(table.columns) == 1)
        ):
            continue

        col_count = len(table.columns)
        if col_count == 0:
            continue

        # 1. Calcular anchos proporcionales inteligentes
        cols_lengths = [[] for _ in range(col_count)]
        for row in table.rows:
            for c_idx, cell in enumerate(row.cells):
                if c_idx < col_count:
                    cols_lengths[c_idx].append(len(cell.text.strip()))

        weights = []
        for c_idx in range(col_count):
            lens = cols_lengths[c_idx]
            if lens:
                avg_len = sum(lens) / len(lens)
                max_len = max(lens)
                w = math.sqrt(max(1, max_len)) + (avg_len ** 0.55)
            else:
                w = 1.0
            weights.append(max(1.0, w))

        sum_w = sum(weights)
        col_widths_in = [round((w / sum_w) * total_table_inches, 2) for w in weights]
        diff = total_table_inches - sum(col_widths_in)
        col_widths_in[-1] += round(diff, 2)
        col_widths_dxa = [int(w * 1440) for w in col_widths_in]

        # 2. Configurar layout de tabla fijo
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        apply_table_cell_margins(table, top_dxa=100, bottom_dxa=100, left_dxa=140, right_dxa=140)

        tblPr = table._tbl.tblPr
        tblPr.append(parse_xml(r'<w:tblLayout {} w:type="fixed"/>'.format(nsdecls('w'))))

        grid_cols_xml = ''.join([r'<w:gridCol {} w:w="{}"/>'.format(nsdecls('w'), w) for w in col_widths_dxa])
        table._tbl.append(parse_xml(r'<w:tblGrid {}>{}</w:tblGrid>'.format(nsdecls('w'), grid_cols_xml)))

        # BORDES APA 7: Superior e inferior sólidos, CERO bordes verticales
        tblBorders = parse_xml(r'''
            <w:tblBorders {} >
                <w:top w:val="single" w:sz="8" w:space="0" w:color="0F172A"/>
                <w:bottom w:val="single" w:sz="8" w:space="0" w:color="0F172A"/>
                <w:left w:val="none"/>
                <w:right w:val="none"/>
                <w:insideH w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                <w:insideV w:val="none"/>
            </w:tblBorders>
        '''.format(nsdecls('w')))
        tblPr.append(tblBorders)

        # 3. Fila de Cabecera APA 7
        hdr_row = table.rows[0]
        hdr_row._tr.get_or_add_trPr().append(parse_xml(r'<w:tblHeader {}/>'.format(nsdecls('w'))))
        hdr_row._tr.get_or_add_trPr().append(parse_xml(r'<w:cantSplit {}/>'.format(nsdecls('w'))))

        for c_idx, cell in enumerate(hdr_row.cells):
            cell.width = Inches(col_widths_in[c_idx])
            cell._tc.get_or_add_tcPr().append(parse_xml(r'<w:tcW {} w:w="{}" w:type="dxa"/>'.format(nsdecls('w'), col_widths_dxa[c_idx])))
            cell._tc.get_or_add_tcPr().append(parse_xml(r'<w:shd {} w:fill="F8FAFC"/>'.format(nsdecls('w'))))
            bdr = parse_xml(r'''
                <w:tcBorders {} >
                    <w:bottom w:val="single" w:sz="8" w:space="0" w:color="0F172A"/>
                    <w:left w:val="none"/>
                    <w:right w:val="none"/>
                </w:tcBorders>
            '''.format(nsdecls('w')))
            cell._tc.get_or_add_tcPr().append(bdr)

            for p in cell.paragraphs:
                p.paragraph_format.space_before = Pt(3)
                p.paragraph_format.space_after = Pt(3)
                for r in p.runs:
                    r.font.name = "Calibri"
                    r.font.size = Pt(9.5)
                    r.font.bold = True
                    r.font.color.rgb = RGBColor(15, 23, 42)

        # 4. Filas de Datos APA 7
        for r_idx in range(1, row_count):
            row = table.rows[r_idx]
            row._tr.get_or_add_trPr().append(parse_xml(r'<w:cantSplit {}/>'.format(nsdecls('w'))))

            for c_idx, cell in enumerate(row.cells):
                cell.width = Inches(col_widths_in[c_idx])
                cell._tc.get_or_add_tcPr().append(parse_xml(r'<w:tcW {} w:w="{}" w:type="dxa"/>'.format(nsdecls('w'), col_widths_dxa[c_idx])))
                bdr_cell = parse_xml(r'''
                    <w:tcBorders {} >
                        <w:left w:val="none"/>
                        <w:right w:val="none"/>
                    </w:tcBorders>
                '''.format(nsdecls('w')))
                cell._tc.get_or_add_tcPr().append(bdr_cell)

                for p in cell.paragraphs:
                    p.paragraph_format.space_before = Pt(2)
                    p.paragraph_format.space_after = Pt(2)
                    p.paragraph_format.line_spacing = 1.15
                    for r in p.runs:
                        r.font.name = "Calibri"
                        r.font.size = Pt(9)
                        r.font.color.rgb = RGBColor(30, 41, 59)

def polish_apa7_document_elements(doc, doc_info):
    """
    Aplica la jerarquía formal de títulos APA 7, figuras y párrafos:
    - Nivel 1: Centrado, Negrita, Mayúsculas y Minúsculas.
    - Nivel 2: Alineado a la izquierda, Negrita.
    - Nivel 3: Alineado a la izquierda, Negrita y Cursiva.
    - Figuras: Centradas, con 'Figura X' en negrita (izquierda) y 'Nota.' descriptiva.
    - Párrafos: Calibri 11 pt, interlineado 1.15, alineación justificada.
    """
    for p in doc.paragraphs:
        txt = p.text.strip()
        style_name = p.style.name if p.style else ""

        # Heading 1 (APA 7 Nivel 1: Centrado, Negrita, Mayúsculas y Minúsculas)
        if style_name.startswith("Heading 1"):
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(20)
            p.paragraph_format.space_after = Pt(8)
            p.paragraph_format.keep_with_next = True

            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(13.5)
                r.font.bold = True
                r.font.color.rgb = RGBColor(15, 23, 42)

        # Heading 2 (APA 7 Nivel 2: Alineado a la izquierda, Negrita)
        elif style_name.startswith("Heading 2"):
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(11.5)
                r.font.bold = True
                r.font.color.rgb = RGBColor(30, 64, 175)

        # Heading 3 (APA 7 Nivel 3: Alineado a la izquierda, Negrita y Cursiva)
        elif style_name.startswith("Heading 3"):
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.keep_with_next = True
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(11)
                r.font.bold = True
                r.font.italic = True
                r.font.color.rgb = RGBColor(51, 65, 85)

        # Número de Figura y Título APA 7 (Inicia con "Figura " o "**Figura ")
        elif txt.startswith("Figura ") or txt.startswith("**Figura ") or re.match(r"^\*?\*?Figura\s+\d+", txt):
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(16)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.color.rgb = RGBColor(15, 23, 42)
                if "Figura " in r.text or "Figura" in r.text:
                    r.font.size = Pt(10)
                    r.font.bold = True
                else:
                    r.font.size = Pt(10)
                    r.font.italic = True

        # Nota de Figura o Tabla APA 7 (Inicia con "Nota." o "*Nota.")
        elif txt.startswith("Nota.") or txt.startswith("*Nota."):
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(18)
            p.paragraph_format.line_spacing = 1.15
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(8.5)
                r.font.color.rgb = RGBColor(71, 85, 105)

        # Citas y Callouts de texto
        elif style_name in ["Quote", "Block Text"]:
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.left_indent = Inches(0.5)
            p.paragraph_format.line_spacing = 1.15
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(10)
                r.font.color.rgb = RGBColor(30, 41, 59)

        # Párrafos regulares
        else:
            # Omitir párrafos especiales de portada si se detectaran
            if txt in [doc_info.get("title", ""), doc_info.get("subtitle", "")] or "LEOFIT SOLUTIONS" in txt or "Lima, Perú" in txt:
                continue

            if len(p._p.xpath('.//w:drawing')) > 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_before = Pt(6)
                p.paragraph_format.space_after = Pt(4)
            else:
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(5)
                p.paragraph_format.line_spacing = 1.15
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                for r in p.runs:
                    r.font.name = "Calibri"
                    r.font.size = Pt(11)
                    r.font.color.rgb = RGBColor(30, 41, 59)

def main():
    print("======================================================================")
    print("COMPILADOR MAESTRO APA 7ma EDICIÓN — ENTREGABLES OFICIALES UTP")
    print("======================================================================")
    print(f"Directorio HTML: {HTML_DIR}")
    print(f"Directorio DOCX: {DOCX_DIR}")
    print(f"Directorio Diagramas: {DIAG_DIR}")
    print("")

    success_count = 0
    total = len(DOCUMENTS)

    for doc_info in DOCUMENTS:
        doc_id = doc_info["id"]
        doc_name = os.path.basename(doc_info["docx_dest"])
        html_name = os.path.basename(doc_info["html_dest"])
        print(f"Procesando [{doc_id}]: {os.path.basename(doc_info['src'])}")

        try:
            processed_md = preprocess_markdown_apa7(doc_info["src"], doc_info)

            html_path = generate_formal_html(doc_info, processed_md)
            html_size_kb = os.path.getsize(html_path) / 1024.0
            print(f"  [OK] HTML formal generado: {html_name} ({html_size_kb:.1f} KB)")

            docx_path = doc_info["docx_dest"]
            convert_md_to_docx_via_pandoc(processed_md, docx_path)

            doc = docx.Document(docx_path)
            sec = doc.sections[0]
            sec.top_margin = Inches(1.0)
            sec.bottom_margin = Inches(1.0)
            sec.left_margin = Inches(1.0)
            sec.right_margin = Inches(1.0)

            setup_apa7_headers_and_footers(sec, doc_info)
            polish_apa7_document_elements(doc, doc_info)
            insert_apa7_title_page(doc, doc_info)
            format_apa7_tables(doc)

            doc.save(docx_path)
            docx_size_kb = os.path.getsize(docx_path) / 1024.0
            print(f"  [OK] Word (.docx) APA 7 finalizada: {doc_name} ({docx_size_kb:.1f} KB)")

            v = docx.Document(docx_path)
            img_count = sum(1 for p in v.paragraphs if len(p._p.xpath('.//w:drawing')) > 0)
            print(f"  [OK] Integridad verificada: {len(v.paragraphs)} párrafos, {len(v.tables)} tablas, {img_count} diagramas insertados.\n")
            success_count += 1

        except Exception as e:
            print(f"  [ERROR] Falló procesamiento de {doc_name}: {e}\n")
            import traceback
            traceback.print_exc()
            sys.exit(1)

    print("======================================================================")
    print(f"EXPORTACION COMPLETADA EXITOSAMENTE: {success_count}/{total} DOCUMENTOS")
    print("Versiones Word bajo Normas APA 7ma Edición listas en _PROYECTO_FINAL_LOCAL.")
    print("======================================================================")

if __name__ == "__main__":
    main()
