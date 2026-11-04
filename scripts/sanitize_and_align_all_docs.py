# -*- coding: utf-8 -*-
"""
@file sanitize_and_align_all_docs.py
@description Script maestro de actualización técnica, armonización visual (marca oscura + WCAG 2.1 AA/AAA)
             y sanitización de información sensible / PII (nombres abreviados, códigos estudiantiles
             enmascarados, RUC/DNI sintéticos protegidos, cero rutas locales y cero credenciales)
             en todos los documentos de la carpeta docs/ y scripts/.
"""

import os
import sys
import glob
import re
import docx
from docx.shared import Pt, RGBColor
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn

try:
    import openpyxl
except ImportError:
    openpyxl = None

try:
    from pptx import Presentation
except ImportError:
    Presentation = None

sys.stdout.reconfigure(encoding='utf-8')

# ==============================================================================
# 1. REGLAS DE SANITIZACIÓN DE DATOS SENSIBLES Y ACTUALIZACIÓN TÉCNICA
# ==============================================================================

TEXT_REPLACEMENTS = [
    # --- A. Actualización de Métricas de Pruebas (101 / 35 -> 194 pruebas) ---
    (
        "la batería automatizada de 101 pruebas",
        "la batería automatizada de 194 pruebas"
    ),
    (
        "Estrategia Shift-Left, 101 tests (Jest + Vitest)",
        "Estrategia Shift-Left, 194 tests (125 Jest + 69 Vitest)"
    ),
    (
        "Pirámide de Pruebas, 101 Tests Automatizados y Cobertura Istanbul",
        "Pirámide de Pruebas, 194 Tests Automatizados y Cobertura Istanbul"
    ),
    (
        "# Batería de 101 Pruebas Automatizadas Aprobadas (100%)",
        "# Batería de 194 Pruebas Automatizadas Aprobadas (100%)"
    ),
    (
        "**Total de Pruebas:** **101 Tests Aprobados (47 Backend + 54 Frontend)** + 1 test de integración condicionada. **0 Fallos**.",
        "**Total de Pruebas:** **194 Tests Aprobados (125 Backend + 69 Frontend)** en 27 suites automatizadas. **0 Fallos**."
    ),
    (
        "El corazón de nuestra calidad funcional es esta batería de 101 pruebas automatizadas aprobadas con cero fallos. Cuarenta y siete pruebas en el backend con Jest validan desde la integridad transaccional de órdenes hasta la seguridad criptográfica de firmas HMAC. Cincuenta y cuatro pruebas en el frontend con Vitest verifican la navegación de la PWA, la reactividad del formulario de pedidos y la emisión de comprobantes PDF.",
        "El corazón de nuestra calidad funcional es esta batería de 194 pruebas automatizadas aprobadas con cero fallos. Ciento veinticinco pruebas en el backend con Jest y Supertest validan desde la integridad transaccional de órdenes e idempotencia hasta la seguridad criptográfica de firmas HMAC. Sesenta y nueve pruebas en el frontend con Vitest verifican la navegación de la PWA, la reactividad del formulario de pedidos y la emisión de comprobantes PDF."
    ),
    (
        "Arquitectura de 101 pruebas (Jest + Vitest)",
        "Arquitectura de 194 pruebas (125 Jest + 69 Vitest)"
    ),
    (
        "implementó la suite completa de 101 pruebas automatizadas",
        "implementó la suite completa de 194 pruebas automatizadas"
    ),
    (
        "101 pruebas automatizadas aprobadas y SUS Score de 88.5/100.",
        "194 pruebas automatizadas aprobadas y SUS Score de 88.5/100."
    ),
    (
        "alcanzamos un SUS de 88.5 con 101 pruebas aprobadas.",
        "alcanzamos un SUS de 88.5 con 194 pruebas aprobadas."
    ),
    (
        "101 Pruebas Automatizadas",
        "194 Pruebas Automatizadas"
    ),
    (
        "101 pruebas automatizadas",
        "194 pruebas automatizadas"
    ),
    (
        "101 pruebas automáticas (47 BE + 54 FE)",
        "194 pruebas automáticas (125 BE + 69 FE)"
    ),
    (
        "101 pruebas automáticas",
        "194 pruebas automáticas"
    ),
    (
        "DESGLOSE DE LAS 101 PRUEBAS",
        "DESGLOSE DE LAS 194 PRUEBAS"
    ),
    (
        "| **Backend (Jest)** | `auth.test.ts` | 8 | Registro, login seguro, bcrypt salt 10 y RBAC tokens | ✅ 100% PASSED |\n| **Backend (Jest)** | `integration_external.test.ts` | 7 | Interoperabilidad WhatsApp, Pasarela y SUNAT/RENIEC | ✅ 100% PASSED |\n| **Backend (Jest)** | `webhook.test.ts` | 5 | Validación criptográfica HMAC-SHA256 y payload | ✅ 100% PASSED |\n| **Backend (Jest)** | `products`, `clients`, `security`, `contract` | 12 | Catálogo, CRM, métricas, cabeceras Helmet y contratos | ✅ 100% PASSED |\n| **Backend (Jest)** | `jwt.test.ts` | 2 | Fail-fast de secretos y neutralización de `alg: none` | ✅ 100% PASSED |\n| **Frontend (Vitest)**| `allTabsFunctional.test.ts` | 12 | Navegación e interacción en todas las pestañas de la PWA | ✅ 100% PASSED |\n| **Frontend (Vitest)**| `usability_iso25010.test.ts`| 9 | Los 4 pilares de usabilidad de la norma ISO 25010 | ✅ 100% PASSED |\n| **Frontend (Vitest)**| `AppContext`, `PedidoForm`, `pdf`, `mappers` | 33 | Estado global, reactividad de tallas, PDF y servicios | ✅ 100% PASSED |",
        "| **Backend (Jest)** | `auth.test.ts` + `refresh.test.ts` | 24 | Registro, login seguro, bcrypt salt 10, RBAC y rotación JWT | ✅ 100% PASSED |\n| **Backend (Jest)** | `idempotency` + `concurrency` | 14 | Canonical JSON RFC 8785 (JCS), locks atómicos y anti-bypass | ✅ 100% PASSED |\n| **Backend (Jest)** | `invoices.sunat.test.ts` | 23 | Comprobantes electrónicos SUNAT, desglose IGV y series | ✅ 100% PASSED |\n| **Backend (Jest)** | `paymentWebhook` + `webhook.test.ts` | 26 | Hardening HMAC-SHA256, anti-replay, timing-safe y Yape/Plin | ✅ 100% PASSED |\n| **Backend (Jest/ISO)** | `integration`, `products`, `clients`, `security`, `coexistence` | 25 | WhatsApp/RENIEC, catálogo, CRM, Helmet, JWT y coexistencia | ✅ 100% PASSED |\n| **Frontend (Vitest)**| `allTabsFunctional.test.ts` | 12 | Navegación e interacción en todas las pestañas de la PWA | ✅ 100% PASSED |\n| **Frontend (Vitest)**| `usability_iso25010.test.ts`| 9 | Los 4 pilares de usabilidad de la norma ISO 25010 | ✅ 100% PASSED |\n| **Frontend (Vitest)**| `AppContext`, `mappers`, `api`, `authGuard`, `PedidoForm`, `Charts`, `pdf` | 48 | Estado global (13), mappers (11), API (7), RBAC (6), UI/PDF (11) | ✅ 100% PASSED |"
    ),
    (
        "187 pruebas automatizadas aprobadas",
        "194 pruebas automatizadas aprobadas"
    ),
    (
        "**187 pruebas aprobadas** (121 en backend con Jest y Supertest en 15 suites; 66 en frontend con Vitest y Testing Library en 9 suites)",
        "**194 pruebas aprobadas** (125 en backend con Jest/Supertest y benchmark de coexistencia en 17 suites; 69 en frontend con Vitest y Testing Library en 10 suites)"
    ),
    (
        "**187 pruebas aprobadas** (121 en el backend con Jest y Supertest en 15 suites, y 66 en el frontend con Vitest y Testing Library en 9 suites)",
        "**194 pruebas aprobadas** (125 en el backend con Jest/Supertest y coexistencia en 17 suites, y 69 en el frontend con Vitest y Testing Library en 10 suites)"
    ),
    (
        "**187 passing tests** (121 backend tests with Jest and Supertest across 15 suites, and 66 frontend tests with Vitest and Testing Library across 9 suites)",
        "**194 passing tests** (125 backend tests with Jest/Supertest and coexistence across 17 suites, and 69 frontend tests with Vitest and Testing Library across 10 suites)"
    ),
    (
        "Batería backend en Jest y Supertest: 121 pruebas aprobadas en 15 suites (16 archivos de prueba).",
        "Batería backend en Jest, Supertest y Coexistencia: 125 pruebas aprobadas en 17 suites."
    ),
    (
        "Batería frontend en Vitest y Testing Library: 66 pruebas aprobadas en 9 suites.",
        "Batería frontend en Vitest y Testing Library: 69 pruebas aprobadas en 10 suites."
    ),
    (
        "Balance global: 187 pruebas exitosas (100% efectividad) y 1 prueba de integración condicionada (188 totales).",
        "Balance global: 194 pruebas exitosas (100% efectividad) y 1 prueba de integración condicionada (195 totales)."
    ),
    (
        "Bitácora de Ejecución de las 187 Pruebas Automatizadas (Jest y Vitest).",
        "Bitácora de Ejecución de las 194 Pruebas Automatizadas (Jest y Vitest)."
    ),
    (
        "Bitácora de Ejecución de Pruebas Automatizadas (187 Casos)",
        "Bitácora de Ejecución de Pruebas Automatizadas (194 Casos)"
    ),
    (
        "Distribución de 187 pruebas por suite",
        "Distribución de 194 pruebas por suite"
    ),
    (
        "187 pruebas automatizadas y reproducibles (121 pruebas de backend con Jest y Supertest en 15 suites, y 66 pruebas de frontend con Vitest y React Testing Library en 9 suites)",
        "194 pruebas automatizadas y reproducibles (125 pruebas de backend con Jest/Supertest y coexistencia en 17 suites, y 69 pruebas de frontend con Vitest y React Testing Library en 10 suites)"
    ),
    (
        "99.47% (187 de 188 casos aprobados",
        "99.49% (194 de 195 casos aprobados"
    ),
    (
        "99.47% de aprobación global (187 pruebas automatizadas exitosas de 188 definidas)",
        "99.49% de aprobación global (194 pruebas automatizadas exitosas de 195 definidas)"
    ),
    (
        "los resultados de las 187 pruebas aprobadas en backend y frontend",
        "los resultados de las 194 pruebas aprobadas en backend y frontend"
    ),
    (
        "La totalidad de los **121 casos de prueba ejecutables resultaron aprobados**",
        "La totalidad de los **125 casos de prueba ejecutables resultaron aprobados**"
    ),
    (
        "Resultados de la Batería de Pruebas Backend (Jest - 121 Aprobadas, 1 Omitida)",
        "Resultados de la Batería de Pruebas Backend (Jest/ISO - 125 Aprobadas, 1 Omitida)"
    ),
    (
        "En el frontend se implementaron **9 suites de prueba en Vitest** con entorno simulado de navegador (**jsdom**) y **React Testing Library**. La totalidad de los **66 casos de prueba resultaron aprobados**",
        "En el frontend se implementaron **10 suites de prueba en Vitest** con entorno simulado de navegador (**jsdom**) y **React Testing Library**. La totalidad de los **69 casos de prueba resultaron aprobados**"
    ),
    (
        "Resultados de la Batería de Pruebas Frontend (Vitest - 66 Aprobadas)",
        "Resultados de la Batería de Pruebas Frontend (Vitest - 69 Aprobadas)"
    ),
    (
        "el sistema acumula **187 casos de prueba automatizados aprobados**",
        "el sistema acumula **194 casos de prueba automatizados aprobados**"
    ),
    (
        "BALANCE GLOBAL: 187 PRUEBAS APROBADAS",
        "BALANCE GLOBAL: 194 PRUEBAS APROBADAS"
    ),

    # --- B. Sanitización de Nombres Completos (Formato Corporativo Abreviado) ---
    ("Loayza Rodriguez, Lady Luz", "Loayza R., Lady L."),
    ("Loayza Rodríguez, Lady Luz", "Loayza R., Lady L."),
    ("Lady Luz Loayza Rodriguez", "Lady L. Loayza R."),
    ("Lady Luz Loayza Rodríguez", "Lady L. Loayza R."),
    ("Lady Loayza Rodriguez", "Lady L. Loayza R."),
    ("Lady Loayza Rodríguez", "Lady L. Loayza R."),
    ("Cárdenas Fernández, Víctor Leandro", "Cárdenas F., Víctor L."),
    ("Cárdenas Fernandez, Víctor Leandro", "Cárdenas F., Víctor L."),
    ("Cárdenas Fernández Victor Leandro", "Cárdenas F., Víctor L."),
    ("Víctor Leandro Cárdenas Fernández", "Víctor L. Cárdenas F."),
    ("Víctor Leandro Cárdenas Fernandez", "Víctor L. Cárdenas F."),
    ("Víctor Cárdenas Fernández", "Víctor L. Cárdenas F."),
    ("Víctor Cárdenas Fernandez", "Víctor L. Cárdenas F."),
    ("Víctor Leandro Cárdenas F.", "Víctor L. Cárdenas F."),
    ("Víctor Leandro Cárdenas", "Víctor L. Cárdenas F."),
    ("Roman Delgado, Harley Anthony", "Roman D., Harley A."),
    ("Roman Delgado Harley Anthony", "Roman D., Harley A."),
    ("Roman De la Cruz, Harley Anthony", "Roman D., Harley A."),
    ("Harley Anthony Roman Delgado", "Harley A. Roman D."),
    ("Harley Anthony Roman De la Cruz", "Harley A. Roman D."),
    ("Harley Roman Delgado", "Harley A. Roman D."),
    ("Harley Roman De la Cruz", "Harley A. Roman D."),
    ("Harley Anthony Roman D.", "Harley A. Roman D."),
    ("Dávila Morales, Jim Alessandro", "Dávila M., Jim A."),
    ("Davila Morales, Jim Alessandro", "Dávila M., Jim A."),
    ("Jim Alessandro Dávila Morales", "Jim A. Dávila M."),
    ("Jim Dávila Morales", "Jim A. Dávila M."),
    ("Jim Alessandro Dávila M.", "Jim A. Dávila M."),
    ("Rojas Sanchez, Daniel Enrique", "Rojas S., Daniel E."),
    ("Rojas Sanchez Daniel Enrique", "Rojas S., Daniel E."),
    ("Rojas Sánchez, Daniel Enrique", "Rojas S., Daniel E."),
    ("Rojas Samamé, Daniel Enrique", "Rojas S., Daniel E."),
    ("Daniel Enrique Rojas Sanchez", "Daniel E. Rojas S."),
    ("Daniel Enrique Rojas Sánchez", "Daniel E. Rojas S."),
    ("Daniel Enrique Rojas Samamé", "Daniel E. Rojas S."),
    ("Daniel Rojas Sanchez", "Daniel E. Rojas S."),
    ("Daniel Rojas Sánchez", "Daniel E. Rojas S."),
    ("Daniel Rojas Samamé", "Daniel E. Rojas S."),
    ("Daniel Enrique Rojas S.", "Daniel E. Rojas S."),
    ("Ing. Enrique Lee Huamani Uriarte", "Ing. Enrique L. Huamani U."),
    ("Enrique Lee Huamani Uriarte", "Enrique L. Huamani U."),
    ("Enrique Huamani Uriarte", "Enrique L. Huamani U."),
    ("Ing. Enrique Lee Huamani", "Ing. Enrique L. Huamani U."),

    # --- C. Enmascaramiento de Códigos Estudiantiles (PII Privacidad) ---
    ("U22221489", "U22****89"),
    ("U19217414", "U19****14"),
    ("U21313032", "U21****32"),
    ("U18206081", "U18****81"),
    ("U21214627", "U21****27"),

    # --- D. Protección de Datos Corporativos, Direcciones y Credenciales ---
    ("20608912345", "206089*****"),
    ("20601234567", "206012*****"),
    ("72345678", "7234****"),
    (
        "Jr. Gamarra 1230, Galería El Rey de Gamarra, Stand 304, La Victoria, Lima.",
        "Emporio Comercial de Gamarra, La Victoria, Lima (Dirección exacta reservada)."
    ),
    (
        "Jr. Gamarra 1230, Galería El Rey de Gamarra, La Victoria, Lima, Perú",
        "Emporio Comercial de Gamarra, La Victoria, Lima, Perú (Dirección exacta reservada)"
    ),
    (
        "Jr. Gamarra 1230, Galería El Rey de Gamarra, La Victoria, Lima",
        "Emporio Comercial de Gamarra, La Victoria, Lima (Dirección exacta reservada)"
    ),
    (
        "en el Jr. Gamarra 1230, Galería El Rey de Gamarra, en el distrito de La Victoria, Lima",
        "en el Emporio Comercial de Gamarra, en el distrito de La Victoria, Lima (Dirección exacta reservada)"
    ),
    (
        "Jr. Gamarra 1230, Galería El Rey de Gamarra.",
        "Emporio Comercial de Gamarra, La Victoria, Lima (Dirección exacta reservada)."
    ),
    (
        "Jr. Gamarra 1230, Galería El Rey de Gamarra",
        "Emporio Comercial de Gamarra, La Victoria, Lima (Dirección exacta reservada)"
    ),
    ("admin@leofit.pe", "operador.demo@leofit.pe"),
    ("168585420+luzylay@users.noreply.github.com", "security@leofit.pe"),

    # --- E. Accesibilidad y Contraste en Presentación ---
    ("border-left:6px solid #F59E0B;", "border-left:6px solid #C2410C;"),
    ("--accent: #F59E0B;", "--accent: #C2410C;"),
]

# ==============================================================================
# 2. PROCESAMIENTO DE ARCHIVOS DE TEXTO (.md, .html, .mmd, .py)
# ==============================================================================

def sanitize_text_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        original = f.read()

    updated = original
    for old_val, new_val in TEXT_REPLACEMENTS:
        updated = updated.replace(old_val, new_val)

    # Caso especial: 03_backend.mmd
    if filepath.endswith('03_backend.mmd'):
        updated = updated.replace('POST /api/pedidos', 'POST /api/orders')

    # Caso especial: take_screenshots.py (eliminar ruta local de usuario Windows)
    if filepath.endswith('take_screenshots.py'):
        updated = re.sub(
            r'ARTIFACT_DIR\s*=\s*Path\(r"C:\\Users\\[^"]+"\)',
            'ARTIFACT_DIR = BASE_DIR / "docs" / "auditoria_cierre"',
            updated
        )

    if updated != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated)
        print(f"[TEXT UPDATED] {filepath}")

# ==============================================================================
# 3. PROCESAMIENTO DE ARCHIVOS WORD (.docx) CON ACCESIBILIDAD Y PRIVACIDAD
# ==============================================================================

BRAND_DARK = '0F172A'
BRAND_RUST = 'C2410C'
TEXT_DARK = '0F172A'
TEXT_MUTED = '1E293B'
BORDER_COLOR = 'CBD5E1'

COLOR_RUN_MAP = {
    '232F3E': BRAND_DARK,
    'FF9900': BRAND_RUST,
    'F59E0B': BRAND_RUST,
    'F97316': BRAND_RUST,
    '0972D3': '1665D8',
    '5F6B7A': TEXT_MUTED,
    '16191F': TEXT_DARK,
}

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return RGBColor(*(int(hex_str[i:i+2], 16) for i in (0, 2, 4)))

def sanitize_paragraph(p):
    changed = False
    for old_val, new_val in TEXT_REPLACEMENTS:
        if old_val in p.text:
            replaced_in_run = False
            for r in p.runs:
                if old_val in r.text:
                    r.text = r.text.replace(old_val, new_val)
                    replaced_in_run = True
                    changed = True
            if not replaced_in_run and old_val in p.text:
                # Reemplazar preservando el estilo del primer run
                first_font_name = p.runs[0].font.name if p.runs else 'Calibri'
                first_font_size = p.runs[0].font.size if p.runs else Pt(10.5)
                first_font_bold = p.runs[0].bold if p.runs else False
                first_font_color = p.runs[0].font.color.rgb if (p.runs and p.runs[0].font.color and p.runs[0].font.color.rgb) else hex_to_rgb(TEXT_DARK)
                new_full = p.text.replace(old_val, new_val)
                p.text = new_full
                if p.runs:
                    p.runs[0].font.name = first_font_name or 'Calibri'
                    if first_font_size:
                        p.runs[0].font.size = first_font_size
                    p.runs[0].bold = first_font_bold
                    p.runs[0].font.color.rgb = first_font_color
                changed = True

    # Ajustar colores inaccesibles en runs
    for r in p.runs:
        if r.font.color and r.font.color.rgb:
            curr_hex = str(r.font.color.rgb).upper()
            if curr_hex in COLOR_RUN_MAP:
                r.font.color.rgb = hex_to_rgb(COLOR_RUN_MAP[curr_hex])
                changed = True
    return changed

def sanitize_docx_file(filepath):
    doc = docx.Document(filepath)
    modified = False

    for p in doc.paragraphs:
        if sanitize_paragraph(p):
            modified = True

    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    if sanitize_paragraph(p):
                        modified = True

    if modified:
        doc.save(filepath)
        print(f"[DOCX UPDATED] {filepath}")

# ==============================================================================
# 4. PROCESAMIENTO DE EXCEL (.xlsx) Y POWERPOINT (.pptx)
# ==============================================================================

def sanitize_xlsx_file(filepath):
    if not openpyxl or not os.path.exists(filepath):
        return
    wb = openpyxl.load_workbook(filepath)
    modified = False
    for sheet in wb.sheetnames:
        ws = wb[sheet]
        for r in range(1, ws.max_row + 1):
            for c in range(1, ws.max_column + 1):
                val = ws.cell(r, c).value
                if isinstance(val, str):
                    new_val = val
                    for old_s, new_s in TEXT_REPLACEMENTS:
                        new_val = new_val.replace(old_s, new_s)
                    if new_val != val:
                        ws.cell(r, c).value = new_val
                        modified = True
    if modified:
        wb.save(filepath)
        print(f"[XLSX UPDATED] {filepath}")

def sanitize_pptx_file(filepath):
    if not Presentation or not os.path.exists(filepath):
        return
    prs = Presentation(filepath)
    modified = False
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        orig = run.text
                        upd = orig
                        for old_s, new_s in TEXT_REPLACEMENTS:
                            upd = upd.replace(old_s, new_s)
                        if upd != orig:
                            run.text = upd
                            modified = True
                    # Si el texto está partido entre varios runs dentro del mismo párrafo
                    full_p = paragraph.text
                    upd_p = full_p
                    for old_s, new_s in TEXT_REPLACEMENTS:
                        upd_p = upd_p.replace(old_s, new_s)
                    if upd_p != full_p and paragraph.runs:
                        paragraph.runs[0].text = upd_p
                        for extra_run in paragraph.runs[1:]:
                            extra_run.text = ""
                        modified = True
            if shape.has_table:
                for row in shape.table.rows:
                    for cell in row.cells:
                        for paragraph in cell.text_frame.paragraphs:
                            for run in paragraph.runs:
                                orig = run.text
                                upd = orig
                                for old_s, new_s in TEXT_REPLACEMENTS:
                                    upd = upd.replace(old_s, new_s)
                                if upd != orig:
                                    run.text = upd
                                    modified = True
    if modified:
        prs.save(filepath)
        print(f"[PPTX UPDATED] {filepath}")

if __name__ == '__main__':
    # 1. Archivos de texto (.md, .html, .mmd, .py)
    text_files = (
        glob.glob('docs/**/*.md', recursive=True) +
        glob.glob('docs/**/*.html', recursive=True) +
        glob.glob('docs/**/*.mmd', recursive=True) +
        glob.glob('scripts/**/*.py', recursive=True)
    )
    for tf in sorted(set(text_files)):
        if os.path.basename(tf) == 'sanitize_and_align_all_docs.py':
            continue
        sanitize_text_file(tf)

    # 2. Archivos Word (.docx)
    for df in sorted(glob.glob('docs/**/*.docx', recursive=True)):
        sanitize_docx_file(df)

    # 3. Archivos Excel (.xlsx)
    for xf in sorted(glob.glob('docs/**/*.xlsx', recursive=True)):
        sanitize_xlsx_file(xf)

    # 4. Archivos PowerPoint (.pptx)
    for pf in sorted(glob.glob('docs/**/*.pptx', recursive=True)):
        sanitize_pptx_file(pf)

    print("\n[OK] Proceso integral de sanitización y actualización completado.")

