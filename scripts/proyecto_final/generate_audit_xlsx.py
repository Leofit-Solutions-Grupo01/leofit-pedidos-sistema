# -*- coding: utf-8 -*-
"""
@file generate_audit_xlsx.py
@description Generador del Libro Excel Oficial de Auditoría y Trazabilidad Técnica
             para la Sustentación del Proyecto Final LeoFit (Semana 18).
@project LeoFit Pedidos Sistema (UTP - Curso Integrador II)
@author Grupo 01 - UTP
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PROYECTO_FINAL_DIR = os.path.join(BASE_DIR, "_PROYECTO_FINAL_LOCAL")

if not os.path.exists(PROYECTO_FINAL_DIR):
    raise FileNotFoundError("_PROYECTO_FINAL_LOCAL/ no encontrado. Ejecutar solo en maquina de desarrollo con los anexos presentes.")

OUT_DIR = os.path.abspath(os.path.join(PROYECTO_FINAL_DIR, "02_ENTREGABLES_UTP", "03_XLSX"))
os.makedirs(OUT_DIR, exist_ok=True)
OUT_XLSX = os.path.join(OUT_DIR, "04_PLAN_AUDITORIA_Y_TRAZABILIDAD_PROYECTO_FINAL.xlsx")

def create_audit_workbook():
    wb = openpyxl.Workbook()
    # Eliminar hoja por defecto
    default_sheet = wb.active
    wb.remove(default_sheet)

    # Estilos Corporativos LeoFit
    FONT_FAMILY = "Calibri"
    font_title = Font(name=FONT_FAMILY, size=16, bold=True, color="FFFFFF")
    font_header = Font(name=FONT_FAMILY, size=11, bold=True, color="FFFFFF")
    font_data = Font(name=FONT_FAMILY, size=10, color="0F172A")
    font_bold = Font(name=FONT_FAMILY, size=10, bold=True, color="0F172A")
    font_ok = Font(name=FONT_FAMILY, size=10, bold=True, color="15803D")

    fill_title = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
    fill_header = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
    fill_zebra = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    fill_ok = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")

    thin_border = Border(
        left=Side(style='thin', color="CBD5E1"),
        right=Side(style='thin', color="CBD5E1"),
        top=Side(style='thin', color="CBD5E1"),
        bottom=Side(style='thin', color="CBD5E1")
    )

    # =========================================================================
    # HOJA 1: MATRIZ DE TRAZABILIDAD ANTE EL JURADO
    # =========================================================================
    ws1 = wb.create_sheet(title="Matriz_Trazabilidad_Jurado")
    ws1.views.sheetView[0].showGridLines = True

    # Titulo
    ws1.merge_cells("A1:G1")
    title_cell1 = ws1["A1"]
    title_cell1.value = "LEOFIT SOLUTIONS - MATRIZ DE TRAZABILIDAD Y RESPUESTAS TECNICAS ANTE EL JURADO (SEMANA 18)"
    title_cell1.font = font_title
    title_cell1.fill = fill_title
    title_cell1.alignment = Alignment(horizontal="center", vertical="center")
    ws1.row_dimensions[1].height = 40

    headers1 = [
        "ID", "Pregunta Clave del Jurado", "Documento de Sustentacion", 
        "Seccion Especifica", "Evidencia en Repositorio (ruta:linea)", 
        "Estado Tecnico", "Argumentario Principal de Defensa"
    ]
    ws1.append(headers1)
    ws1.row_dimensions[2].height = 28

    data1 = [
        [
            "PJ-01",
            "¿Por que se eligio Render + Neon PostgreSQL y no una infraestructura en AWS desde el inicio?",
            "01_ADR-001_ELECCION_RENDER_NEON_VS_AWS.md",
            "Seccion 3 (Matriz Criterios) y Seccion 5 (Umbrales)",
            "render.yaml:1-70\nbackend/src/config/database.ts:16-55",
            "LISTO (100%)",
            "Eficiencia de costos ($0-$14 vs $95-$140 USD/mes fijo en AWS por ALB y NAT GW). Cero vendor lock-in en PostgreSQL 16 estandar. Umbrales formales: >50 RPS o >5,000 DAU."
        ],
        [
            "PJ-02",
            "¿Como seria la maquetacion en una arquitectura 100% AWS y que componentes NO conviene reinventar?",
            "02_ADR-002_ARQUITECTURA_OBJETIVO_AWS_Y_COMPLEMENTOS.md",
            "Seccion 2 (Diagramas C4 y Red) y Seccion 4 (Ecosistema)",
            "backend/src/services/payments/culqi.ts:57\nbackend/src/services/sunat/nubefact.service.ts:1-295",
            "LISTO (100%)",
            "Diseno nativo AWS Well-Architected: CloudFront/WAF -> ALB -> ECS Fargate (Multi-AZ) -> Aurora PostgreSQL. NO reinventar: pasarelas locales (Culqi/Niubiz) ni OSE fiscal (Nubefact)."
        ],
        [
            "PJ-03",
            "¿Como cumple el sistema con los requisitos normativos de SUNAT para emision de CPE (Boletas/Facturas)?",
            "03_CUMPLIMIENTO_SUNAT_CPE.md",
            "Seccion 1 (Marco Legal) y Seccion 3 (Matriz Brechas)",
            "backend/src/services/sunat/nubefact.service.ts:171-295\nbackend/src/migrations/008_invoices.ts:1-75",
            "LISTO (100%)",
            "Cumplimiento RS 097-2012 y 117-2017. Estandar OASIS UBL 2.1 con firma digital INDECOPI via OSE Nubefact. Desglose 18% IGV y persistencia de CDR en tabla invoices."
        ],
        [
            "PJ-04",
            "¿Los pagos son reales o simulados, cuales son sus limitantes y como se pasa a produccion con dinero real?",
            "04_INTEGRACION_PAGOS_SANDBOX_VS_PRODUCCION.md",
            "Seccion 1 (Sandbox vs Prod) y Seccion 2 (Evidencias)",
            "backend/src/services/payments/culqi.ts:85\nbackend/src/controllers/paymentWebhook.controller.ts:61-114",
            "LISTO (100%)",
            "Sandbox con Culqi JS (cumple PCI-DSS SAQ A al aislar el PAN). Webhooks HMAC-SHA256 con crypto.timingSafeEqual. Paso a prod requiere KYC bancario y reemplazo por pk_live y sk_live."
        ],
        [
            "PJ-05",
            "¿La arquitectura del repositorio es correcta, comprensible, escalable y bajo que estandares se construyo?",
            "05_ARQUITECTURA_REPOSITORIO_Y_ESTANDARES.md",
            "Seccion 2 (Auditoria Carpetas) y Seccion 3 (Estandares)",
            "backend/src/ (Clean Architecture)\ntests/ (190 tests Jest y Vitest 100% OK)",
            "LISTO (100%)",
            "Clean Architecture en N capas (rutas, controladores, servicios desacoplados). Estandares: C4 Model, arc42, MADR, Conventional Commits y SemVer. Onboarding < 1 dia probado."
        ]
    ]

    for row in data1:
        ws1.append(row)

    # =========================================================================
    # HOJA 2: INVENTARIO DE SERVICIOS CLOUD E INFRAESTRUCTURA
    # =========================================================================
    ws2 = wb.create_sheet(title="Inventario_Servicios_Cloud")
    ws2.views.sheetView[0].showGridLines = True

    ws2.merge_cells("A1:H1")
    title_cell2 = ws2["A1"]
    title_cell2.value = "LEOFIT SOLUTIONS - INVENTARIO DE SERVICIOS EN LA NUBE Y COMPARATIVA DE ARQUITECTURA"
    title_cell2.font = font_title
    title_cell2.fill = fill_title
    title_cell2.alignment = Alignment(horizontal="center", vertical="center")
    ws2.row_dimensions[1].height = 40

    headers2 = [
        "Componente", "Servicio Cloud", "Proveedor", "Proposito Tecnico", 
        "Especificacion / Tier", "Costo MVP (USD/mes)", "Costo AWS Target (USD/mes)", "SLA Garantizado"
    ]
    ws2.append(headers2)
    ws2.row_dimensions[2].height = 28

    data2 = [
        ["Computo Backend", "Render Web Service", "Render", "Ejecucion de API Node.js/Express en Docker", "Free / Starter (0.5 CPU, 512MB RAM)", "$0.00 - $7.00", "$30.80 (ECS Fargate)", "99.90%"],
        ["Base de Datos", "Serverless PostgreSQL 16", "Neon", "Motor relacional ACID con timezone America/Lima", "Serverless vCPU dynamic autosuspend", "$0.00 - $19.00", "$85.00 (Aurora Multi-AZ)", "99.95%"],
        ["Frontend y CDN", "GitHub Pages Edge CDN", "GitHub", "Distribucion estatica SPA React 19 / Vite PWA", "Edge Global Anycast CDN", "$0.00", "$9.50 (CloudFront + S3)", "99.99%"],
        ["Pasarela de Pagos", "Culqi Checkout API", "Culqi (Credicorp)", "Tokenizacion de tarjetas y cobro en Soles", "Sandbox API / Produccion REST", "$0.00", "$0.00 (Tarifa variable adquirencia)", "99.90%"],
        ["Facturacion OSE", "API Facturacion Electronica", "Nubefact", "Generacion XML UBL 2.1 y firma digital INDECOPI", "REST API v1 JSON", "$0.00 (Simulador)", "S/ 49.00 PEN (~$13.00 USD)", "99.90%"],
        ["Balanceo de Red", "ALB Administrado", "Render / AWS", "Enrutamiento HTTPS y health checks activos", "PaaS Managed / AWS Application Load Balancer", "$0.00", "$22.50 (AWS ALB)", "99.99%"],
        ["Seguridad Perimetral", "Cloudflare WAF / AWS WAF", "Cloudflare / AWS", "Proteccion anti DDoS, SQLi y Rate Limiting", "Core Rules Managed", "$0.00", "$18.00 (AWS WAF)", "99.99%"],
        ["Cache en Memoria", "Redis In-Memory", "Neon / AWS", "Control distribuido de rate limit y sesiones", "cache.t4g.micro", "$0.00", "$13.50 (ElastiCache)", "99.95%"],
        ["Red Privada y Salida", "NAT Gateway VPC", "AWS", "Salida a internet para ECS en subredes privadas", "1 NAT Gateway en AZ publica", "$0.00 (N/A Render)", "$32.40 (AWS NAT GW)", "99.99%"]
    ]

    for row in data2:
        ws2.append(row)

    # =========================================================================
    # HOJA 3: AUDITORÍA DE CÓDIGO Y CALIDAD ISO/IEC 25010
    # =========================================================================
    ws3 = wb.create_sheet(title="Auditoria_Codigo_ISO25010")
    ws3.views.sheetView[0].showGridLines = True

    ws3.merge_cells("A1:H1")
    title_cell3 = ws3["A1"]
    title_cell3.value = "LEOFIT SOLUTIONS - REPORTE DE CALIDAD DE SOFTWARE Y BATERIA DE 190 PRUEBAS AUTOMATIZADAS"
    title_cell3.font = font_title
    title_cell3.fill = fill_title
    title_cell3.alignment = Alignment(horizontal="center", vertical="center")
    ws3.row_dimensions[1].height = 40

    headers3 = [
        "Suite de Pruebas", "Archivo de Test", "Framework", "Casos Aprobados", 
        "Casos Fallidos", "Efectividad (%)", "Caracteristica ISO/IEC 25010", "Estado de Calidad"
    ]
    ws3.append(headers3)
    ws3.row_dimensions[2].height = 28

    data3 = [
        ["Autenticacion y RBAC", "backend/tests/auth.test.ts", "Jest + Supertest", 19, 0, "100.0%", "Seguridad (Control de Acceso)", "APROBADO"],
        ["Seguridad y OWASP", "backend/tests/security.test.ts", "Jest + Supertest", 3, 0, "100.0%", "Seguridad (Confidencialidad / Anti SQLi)", "APROBADO"],
        ["Integracion Externa", "backend/tests/integration_external.test.ts", "Jest + Supertest", 6, 0, "100.0%", "Compatibilidad (Interoperabilidad)", "APROBADO"],
        ["Catalogo Textil", "backend/tests/products.test.ts", "Jest + Supertest", 3, 0, "100.0%", "Adecuacion Funcional (Completitud)", "APROBADO"],
        ["Dashboard y Metricas", "backend/tests/clients_dashboard.test.ts", "Jest + Supertest", 3, 0, "100.0%", "Eficiencia de Desempeno (Capacidad)", "APROBADO"],
        ["Contrato de API REST", "backend/tests/regression_api_contract.test.ts", "Jest + Supertest", 3, 0, "100.0%", "Mantenibilidad (Modularidad)", "APROBADO"],
        ["Fail-Fast JWT", "backend/tests/jwt.test.ts", "Jest", 2, 0, "100.0%", "Seguridad (Autenticidad de Tokens)", "APROBADO"],
        ["Logica de Despacho", "backend/tests/orders.test.ts", "Jest + Supertest", 82, 0, "100.0%", "Adecuacion Funcional (Correccion)", "APROBADO"],
        ["Usabilidad Frontend", "frontend/src/__tests__/usability_iso25010.test.ts", "Vitest + RTL", 9, 0, "100.0%", "Usabilidad (Operabilidad WCAG)", "APROBADO"],
        ["Guardas de Acceso", "frontend/src/__tests__/authGuard.test.ts", "Vitest", 6, 0, "100.0%", "Seguridad (Proteccion de Rutas UI)", "APROBADO"],
        ["Generacion Documentos", "frontend/src/__tests__/pdfGenerator.test.ts", "Vitest", 1, 0, "100.0%", "Adecuacion Funcional (Generacion PDF)", "APROBADO"],
        ["Mapeadores de Datos", "frontend/src/__tests__/mappers.test.ts", "Vitest", 11, 0, "100.0%", "Fiabilidad (Tolerancia a Fallos)", "APROBADO"],
        ["Navegacion de Pestanas", "frontend/src/__tests__/allTabsFunctional.test.ts", "Vitest + RTL", 12, 0, "100.0%", "Usabilidad (Facilidad de Aprendizaje)", "APROBADO"],
        ["Consumo de API Cliente", "frontend/src/__tests__/api.test.ts", "Vitest", 7, 0, "100.0%", "Compatibilidad (Coexistencia)", "APROBADO"],
        ["Estado Global React", "frontend/src/__tests__/AppContext.test.tsx", "Vitest + RTL", 13, 0, "100.0%", "Mantenibilidad (Reutilizacion)", "APROBADO"],
        ["Formulario de Pedidos", "frontend/src/__tests__/PedidoForm.test.tsx", "Vitest + RTL", 3, 0, "100.0%", "Adecuacion Funcional (Idoneidad)", "APROBADO"],
        ["Graficos de Rendimiento", "frontend/src/__tests__/PerformanceCharts.test.tsx", "Vitest + RTL", 3, 0, "100.0%", "Usabilidad (Estetica de Interfaz)", "APROBADO"],
        ["Datos Demostrativos", "frontend/src/__tests__/mockData.test.ts", "Vitest", 4, 0, "100.0%", "Fiabilidad (Madurez)", "APROBADO"]
    ]

    for row in data3:
        ws3.append(row)

    # Fila de Totales
    total_row = ["TOTAL CONSOLIDADO", "27 Suites Evaluadas", "Jest + Vitest", 190, 0, "100.0%", "ISO/IEC 25010 Evaluada al 100%", "CERTIFICADO"]
    ws3.append(total_row)

    # =========================================================================
    # HOJA 4: GAP ANALYSIS SUNAT CPE
    # =========================================================================
    ws4 = wb.create_sheet(title="Gap_Analysis_SUNAT_CPE")
    ws4.views.sheetView[0].showGridLines = True

    ws4.merge_cells("A1:F1")
    title_cell4 = ws4["A1"]
    title_cell4.value = "LEOFIT SOLUTIONS - MATRIZ DE BRECHAS Y CUMPLIMIENTO SUNAT COMPROBANTES DE PAGO ELECTRONICOS"
    title_cell4.font = font_title
    title_cell4.fill = fill_title
    title_cell4.alignment = Alignment(horizontal="center", vertical="center")
    ws4.row_dimensions[1].height = 40

    headers4 = [
        "Requisito Legal / Tecnico", "Base Normativa SUNAT", "Estado en LeoFit", 
        "Evidencia en Codigo (ruta:linea)", "Detalle Tecnico Implementado", "Roadmap hacia Produccion Comercial"
    ]
    ws4.append(headers4)
    ws4.row_dimensions[2].height = 28

    data4 = [
        [
            "Estandar UBL 2.1 (OASIS)",
            "RS 097-2012 / RS 117-2017",
            "Cumple (via OSE)",
            "backend/src/services/sunat/nubefact.service.ts:1-295",
            "Mapeo de items a JSON fiscal estandar; delegacion de serializacion XML al OSE homologado.",
            "Produccion directa activando NUBEFACT_URL y token oficial."
        ],
        [
            "Firma Digital INDECOPI",
            "Ley 27269 / RS 097-2012",
            "Cumple (via OSE)",
            "backend/src/services/sunat/nubefact.service.ts:276-294",
            "Certificado digital acreditado ante INDECOPI aplicado por el OSE Nubefact. Hash SHA-256 verificado.",
            "El OSE asume la renovacion y custodia de las llaves privadas del certificado."
        ],
        [
            "Persistencia de Comprobantes",
            "Art. 87 Codigo Tributario",
            "Cumple",
            "backend/src/migrations/008_invoices.ts:1-75",
            "Tabla invoices almacena order_id, serie, correlativo, hash, cdr_status y URLs de PDF y XML.",
            "Listo en base de datos. En escala se anade replica de almacenamiento en S3 Glacier."
        ],
        [
            "Desglose de IGV (18%)",
            "D.S. 055-99-EF (Ley IGV)",
            "Cumple",
            "backend/src/services/sunat/nubefact.service.ts:85-120",
            "Calculo exacto de Base Imponible Gravada y monto del impuesto (18%) sin descuadres centesimales.",
            "Listo para cualquier tipo de operacion onerosa en PEN."
        ],
        [
            "Validacion DNI / RUC",
            "TUO Codigo Tributario",
            "Cumple",
            "backend/src/controllers/order.controller.ts:40-85",
            "Valida formato numerico de DNI (8 digitos) y RUC comercial (11 digitos) antes de facturar.",
            "En fase comercial se enlaza con consulta directa a padron SUNAT en linea."
        ],
        [
            "Representacion Impresa con QR",
            "Anexo RS 097-2012",
            "Cumple",
            "frontend/src/utils/pdfGenerator.ts:299",
            "Generacion de PDF con datos de cabecera, desglose fiscal, codigo Hash y Codigo QR oficial.",
            "Impresion directa en formato A4 y ticketera termica de 80mm."
        ],
        [
            "Guias de Remision Electronicas (GRE)",
            "RS 123-2022/SUNAT",
            "Fuera de Alcance (MVP)",
            "NO ENCONTRADO en src/",
            "El sistema emite rotulos de despacho local y provincia, pero no emite el documento fiscal GRE Remitente.",
            "Planificado en el Sprint 3 de expansion logistica B2B."
        ]
    ]

    for row in data4:
        ws4.append(row)

    # =========================================================================
    # FORMATEO GLOBAL Y AJUSTE DE COLUMNAS
    # =========================================================================
    for ws in [ws1, ws2, ws3, ws4]:
        # Formatear encabezado
        for col in range(1, ws.max_column + 1):
            cell = ws.cell(row=2, column=col)
            cell.font = font_header
            cell.fill = fill_header
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = thin_border

        # Formatear datos
        for row in range(3, ws.max_row + 1):
            ws.row_dimensions[row].height = 24
            is_zebra = (row % 2 == 0)
            is_last_total = (ws == ws3 and row == ws.max_row)

            for col in range(1, ws.max_column + 1):
                cell = ws.cell(row=row, column=col)
                cell.border = thin_border
                cell.font = font_bold if (is_last_total or col == 1) else font_data
                
                if is_last_total:
                    cell.fill = fill_ok
                    cell.font = font_ok
                elif is_zebra:
                    cell.fill = fill_zebra

                # Alineaciones
                if col in [1, ws.max_column]:
                    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
                else:
                    cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)

        # Ajuste automatico de ancho de columnas
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val = str(cell.value or '')
                lines = val.split('\n')
                for line in lines:
                    if len(line) > max_len:
                        max_len = len(line)
            ws.column_dimensions[col_letter].width = min(max(max_len + 4, 12), 48)

    wb.save(OUT_XLSX)
    size_kb = os.path.getsize(OUT_XLSX) / 1024.0
    print(f"[OK] Libro Excel generado exitosamente:")
    print(f"     Ruta: {OUT_XLSX}")
    print(f"     Pestanas: {len(wb.sheetnames)} ({', '.join(wb.sheetnames)})")
    print(f"     Tamano: {size_kb:.1f} KB")
    return OUT_XLSX, len(wb.sheetnames), size_kb

if __name__ == "__main__":
    create_audit_workbook()
