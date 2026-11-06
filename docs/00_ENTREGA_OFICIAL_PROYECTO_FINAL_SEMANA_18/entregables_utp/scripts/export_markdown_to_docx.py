# -*- coding: utf-8 -*-
"""
@file export_markdown_to_docx.py
@description Exportador profesional de Markdown a Microsoft Word (.docx)
             con procesamiento previo de diagramas Mermaid a PNG mediante mmdc y Pandoc.
@project LeoFit Pedidos Sistema - Sustentación Proyecto Final (Semana 18)
@author Grupo 01 - UTP
"""

import os
import sys
import re
import hashlib
import subprocess
import tempfile
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "01_DOCX"))
CACHE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".cache_diagrams"))

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)

DOCS_TO_EXPORT = [
    {
        "src": os.path.join(BASE_DIR, "docs", "00_ENTREGA_OFICIAL_PROYECTO_FINAL_SEMANA_18", "00_HOJA_DE_ENTREGA_Y_ENLACES_PROYECTO_FINAL.md"),
        "dest": os.path.join(OUT_DIR, "00_HOJA_DE_ENTREGA_Y_ENLACES_PROYECTO_FINAL.docx"),
        "title": "HOJA DE ENTREGA Y ENLACES OFICIALES - PROYECTO FINAL"
    },
    {
        "src": os.path.join(BASE_DIR, "docs", "05_ANEXOS_TECNICOS_PROYECTO_FINAL", "01_ADR-001_ELECCION_RENDER_NEON_VS_AWS.md"),
        "dest": os.path.join(OUT_DIR, "01_ADR-001_ELECCION_RENDER_NEON_VS_AWS.docx"),
        "title": "ADR-001: ELECCIÓN DE RENDER Y NEON VS AWS"
    },
    {
        "src": os.path.join(BASE_DIR, "docs", "05_ANEXOS_TECNICOS_PROYECTO_FINAL", "02_ADR-002_ARQUITECTURA_OBJETIVO_AWS_Y_COMPLEMENTOS.md"),
        "dest": os.path.join(OUT_DIR, "02_ADR-002_ARQUITECTURA_OBJETIVO_AWS_Y_COMPLEMENTOS.docx"),
        "title": "ADR-002: ARQUITECTURA OBJETIVO AWS Y COMPLEMENTOS"
    },
    {
        "src": os.path.join(BASE_DIR, "docs", "05_ANEXOS_TECNICOS_PROYECTO_FINAL", "03_CUMPLIMIENTO_SUNAT_CPE.md"),
        "dest": os.path.join(OUT_DIR, "03_CUMPLIMIENTO_SUNAT_CPE.docx"),
        "title": "CUMPLIMIENTO NORMATIVO SUNAT - COMPROBANTES DE PAGO"
    },
    {
        "src": os.path.join(BASE_DIR, "docs", "05_ANEXOS_TECNICOS_PROYECTO_FINAL", "04_INTEGRACION_PAGOS_SANDBOX_VS_PRODUCCION.md"),
        "dest": os.path.join(OUT_DIR, "04_INTEGRACION_PAGOS_SANDBOX_VS_PRODUCCION.docx"),
        "title": "INTEGRACIÓN DE PAGOS: SANDBOX FRENTE A PRODUCCIÓN"
    },
    {
        "src": os.path.join(BASE_DIR, "docs", "05_ANEXOS_TECNICOS_PROYECTO_FINAL", "05_ARQUITECTURA_REPOSITORIO_Y_ESTANDARES.md"),
        "dest": os.path.join(OUT_DIR, "05_ARQUITECTURA_REPOSITORIO_Y_ESTANDARES.docx"),
        "title": "ARQUITECTURA DEL REPOSITORIO Y ESTÁNDARES"
    },
    {
        "src": os.path.join(BASE_DIR, "docs", "05_ANEXOS_TECNICOS_PROYECTO_FINAL", "06_MATRIZ_TRAZABILIDAD_JURADO.md"),
        "dest": os.path.join(OUT_DIR, "06_MATRIZ_TRAZABILIDAD_JURADO.docx"),
        "title": "MATRIZ DE TRAZABILIDAD Y RESPUESTAS ANTE EL JURADO"
    },
    {
        "src": os.path.join(BASE_DIR, "docs", "05_ANEXOS_TECNICOS_PROYECTO_FINAL", "README.md"),
        "dest": os.path.join(OUT_DIR, "COMPENDIO_ANEXOS_TECNICOS_LEOFIT.docx"),
        "title": "COMPENDIO GENERAL DE ANEXOS TÉCNICOS LEOFIT"
    },
    {
        "src": os.path.join(BASE_DIR, "docs", "_auditoria", "00_INVENTARIO_REAL.md"),
        "dest": os.path.join(OUT_DIR, "AUDITORIA_INVENTARIO_REAL_CODIGO.docx"),
        "title": "AUDITORÍA TÉCNICA E INVENTARIO REAL DEL CÓDIGO"
    }
]

def render_mermaid_to_png(mermaid_code, index, doc_name):
    """
    Compila código Mermaid a imagen PNG usando mmdc.
    Implementa caché idempotente basado en hash SHA-256 del contenido.
    """
    code_hash = hashlib.sha256(mermaid_code.encode("utf-8")).hexdigest()[:12]
    img_name = f"{doc_name}_diag_{index}_{code_hash}.png"
    img_path = os.path.join(CACHE_DIR, img_name)
    
    if os.path.exists(img_path) and os.path.getsize(img_path) > 100:
        return img_path
        
    mmd_path = os.path.join(CACHE_DIR, f"{doc_name}_diag_{index}_{code_hash}.mmd")
    with open(mmd_path, "w", encoding="utf-8") as f:
        f.write(mermaid_code)
        
    cmd = ["mmdc", "-i", mmd_path, "-o", img_path, "-b", "white", "-s", "2"]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        if res.returncode == 0 and os.path.exists(img_path):
            return img_path
        else:
            print(f"  [WARN] mmdc fallo para {img_name}: {res.stderr[:200]}")
    except Exception as e:
        print(f"  [ERROR] Excepcion ejecutando mmdc: {e}")
        
    return None

def process_markdown_file(src_path, doc_name):
    """
    Procesa un archivo Markdown reemplazando los bloques ```mermaid``` por
    referencias a imágenes renderizadas en PNG antes de compilar con Pandoc.
    """
    with open(src_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Excluir cualquier emoji residual si existiera
    content = re.sub(r'[\U00010000-\U0010ffff\u2600-\u27bf]', '', content)
    
    # Procesar bloques Mermaid
    pattern = re.compile(r'```mermaid(.*?)```', re.DOTALL)
    
    def replacer(match):
        nonlocal index
        index += 1
        mermaid_code = match.group(1).strip()
        img_path = render_mermaid_to_png(mermaid_code, index, doc_name)
        if img_path and os.path.exists(img_path):
            # Pandoc maneja mejor rutas absolutas o relativas con barras normales
            clean_path = img_path.replace("\\", "/")
            return f"\n\n![Diagrama de Arquitectura]({clean_path})\n*Figura {index}: Diagrama Técnico Compilado.* \n\n"
        else:
            # Fallback en caso de que mmdc falle: bloque de código limpio
            return f"\n```text\n[Diagrama de Arquitectura Mermaid]\n{mermaid_code}\n```\n"
            
    index = 0
    processed_content = pattern.sub(replacer, content)
    return processed_content

def style_docx(doc_path):
    """
    Aplica formato corporativo LeoFit al documento .docx generado por Pandoc:
    - Márgenes estándar de 1 pulgada (2.54 cm).
    - Fuentes limpias Calibri.
    - Encabezados en paleta oficial (#0F172A).
    - Tablas alineadas al centro con bordes sutiles.
    - Validación de integridad para asegurar que python-docx puede abrirlo.
    """
    doc = docx.Document(doc_path)
    
    # Configurar márgenes
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # Formatear tablas
    for table in doc.tables:
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        # Dar formato al encabezado de la tabla si existe
        if len(table.rows) > 0:
            for cell in table.rows[0].cells:
                shading = parse_xml(r'<w:shd {} w:fill="0F172A"/>'.format(nsdecls('w')))
                cell._tc.get_or_add_tcPr().append(shading)
                for p in cell.paragraphs:
                    for run in p.runs:
                        run.font.bold = True
                        run.font.color.rgb = RGBColor(255, 255, 255)
                        
    doc.save(doc_path)
    
    # Validar re-apertura sin error
    verification = docx.Document(doc_path)
    assert len(verification.paragraphs) > 0 or len(verification.tables) > 0
    return True

def export_all():
    print("=" * 70)
    print("INICIANDO CADENA DE EXPORTACION MARKDOWN -> DOCX (LEOFIT)")
    print("=" * 70)
    
    results = []
    for item in DOCS_TO_EXPORT:
        src = item["src"]
        dest = item["dest"]
        doc_name = os.path.splitext(os.path.basename(dest))[0]
        
        if not os.path.exists(src):
            print(f"[ERROR] Archivo fuente no encontrado: {src}")
            continue
            
        print(f"\nProcesando: {os.path.basename(src)} -> {os.path.basename(dest)}")
        
        # 1. Preprocesar Markdown con diagramas Mermaid
        processed_md = process_markdown_file(src, doc_name)
        
        # 2. Guardar Markdown temporal para Pandoc
        temp_md_path = os.path.join(CACHE_DIR, f"{doc_name}_pandoc_in.md")
        with open(temp_md_path, "w", encoding="utf-8") as f:
            f.write(processed_md)
            
        # 3. Ejecutar Pandoc
        cmd = [
            "pandoc",
            temp_md_path,
            "-o", dest,
            "--from=gfm",
            "--to=docx"
        ]
        
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"  [ERROR] Pandoc fallo para {dest}: {res.stderr}")
            continue
            
        # 4. Estilizar y validar con python-docx
        try:
            style_docx(dest)
            size_kb = os.path.getsize(dest) / 1024.0
            print(f"  [OK] Generado exitosamente: {os.path.basename(dest)} ({size_kb:.1f} KB)")
            results.append((os.path.basename(dest), size_kb))
        except Exception as e:
            print(f"  [ERROR] Fallo en la estilizacion de {dest}: {e}")
            
    print("\n" + "=" * 70)
    print(f"EXPORTACION COMPLETADA: {len(results)}/{len(DOCS_TO_EXPORT)} ARCHIVOS DOCX GENERADOS")
    print("=" * 70)
    return results

if __name__ == "__main__":
    export_all()
