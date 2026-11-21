# -*- coding: utf-8 -*-
"""
@file generate_sustentacion_pptx.py
@description Generador maestro de la Presentación de Sustentación del Proyecto Final (Semana 18)
             en PowerPoint (.pptx) con 20 diapositivas de alta ingeniería y notas de orador completas.
@project LeoFit Pedidos Sistema (UTP - Curso Integrador II)
@author Grupo 01 - UTP
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PROYECTO_FINAL_DIR = os.path.join(BASE_DIR, "_PROYECTO_FINAL_LOCAL")

if not os.path.exists(PROYECTO_FINAL_DIR):
    raise FileNotFoundError("_PROYECTO_FINAL_LOCAL/ no encontrado. Ejecutar solo en maquina de desarrollo con los anexos presentes.")

OUT_DIR = os.path.abspath(os.path.join(PROYECTO_FINAL_DIR, "02_ENTREGABLES_UTP", "02_PPTX"))
os.makedirs(OUT_DIR, exist_ok=True)
OUT_PPTX = os.path.join(OUT_DIR, "03_PRESENTACION_OFICIAL_SUSTENTACION_PROYECTO_FINAL.pptx")

def C(h): return RGBColor.from_string(h)

# Paleta Corporativa LeoFit (Alto Contraste WCAG AAA - Cero Emojis)
NAVY    = "0F172A"  # Slate 900 Institucional
BLUE    = "1665D8"  # Azul Cobalto Primario
ACCENT  = "C2410C"  # Terracota Deportivo
GREEN   = "15803D"  # Verde Exito
DARK    = "1E293B"  # Slate 800
GRAY    = "64748B"  # Slate 500
LGRAY   = "F8FAFC"  # Slate 50 Fondo
LBLUE   = "EFF6FF"  # Azul Suave
WHITE   = "FFFFFF"

FONT_MAIN = "Calibri"
FONT_CODE = "Consolas"

def create_deck():
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5) # Widescreen 16:9
    BLANK = prs.slide_layouts[6]

    def add_header(s, title, category="PROYECTO FINAL - INGENIERIA DE SOFTWARE"):
        # Header banner
        box(s, 0.5, 0.35, 12.333, 0.9, fill=WHITE, line=None)
        txt(s, 0.5, 0.35, 10.0, 0.25, category.upper(), size=11, bold=True, color=ACCENT)
        txt(s, 0.5, 0.60, 10.5, 0.60, title, size=22, bold=True, color=NAVY)
        # Footer
        txt(s, 0.5, 7.1, 8.0, 0.3, "LeoFit Solutions - Grupo 01 | UTP Curso Integrador II", size=10, color=GRAY)
        txt(s, 10.0, 7.1, 2.8, 0.3, "Sustentacion Semana 18", size=10, align="r", color=GRAY)

    def txt(s, x, y, w, h, text, size=14, bold=False, color=DARK, align="l", anchor="t", italic=False, font=FONT_MAIN):
        tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.06)
        tf.margin_top = tf.margin_bottom = Inches(0.04)
        tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
        for i, line in enumerate(str(text).split("\n")):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[align]
            r = p.add_run()
            r.text = line
            r.font.size, r.font.bold, r.font.italic, r.font.name = Pt(size), bold, italic, font
            r.font.color.rgb = C(color)
        return tb

    def box(s, x, y, w, h, text="", fill=LBLUE, line=None, size=13, bold=False, color=DARK,
            align="c", anchor="m", shape=MSO_SHAPE.ROUNDED_RECTANGLE, lw=1.2, radius=0.04, font=FONT_MAIN):
        sh = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
        if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
            sh.adjustments[0] = radius
        if fill is None:
            sh.fill.background()
        else:
            sh.fill.solid()
            sh.fill.fore_color.rgb = C(fill)
        if line:
            sh.line.color.rgb = C(line)
            sh.line.width = Pt(lw)
        else:
            sh.line.fill.background()
        if text:
            tf = sh.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_right = Inches(0.08)
            tf.margin_top = tf.margin_bottom = Inches(0.06)
            tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
            for i, line in enumerate(str(text).split("\n")):
                p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[align]
                r = p.add_run()
                r.text = line
                r.font.size, r.font.bold, r.font.name = Pt(size), bold, font
                r.font.color.rgb = C(color)
        return sh

    def table(s, x, y, w, h, headers, rows, col_widths=None, header_bg=NAVY, row_bg=LGRAY):
        rows_count = len(rows) + 1
        cols_count = len(headers)
        table_shape = s.shapes.add_table(rows_count, cols_count, Inches(x), Inches(y), Inches(w), Inches(h))
        tbl = table_shape.table
        if col_widths:
            for idx, width in enumerate(col_widths):
                tbl.columns[idx].width = Inches(width)
        
        # Formatear encabezados
        for col_idx, header_text in enumerate(headers):
            cell = tbl.cell(0, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C(header_bg)
            cell.text = header_text
            for p in cell.text_frame.paragraphs:
                p.alignment = PP_ALIGN.CENTER
                for r in p.runs:
                    r.font.name = FONT_MAIN
                    r.font.size = Pt(10)
                    r.font.bold = True
                    r.font.color.rgb = C(WHITE)
        
        # Formatear filas
        for row_idx, row_data in enumerate(rows):
            bg_color = WHITE if row_idx % 2 == 0 else row_bg
            for col_idx, cell_value in enumerate(row_data):
                cell = tbl.cell(row_idx + 1, col_idx)
                cell.fill.solid()
                cell.fill.fore_color.rgb = C(bg_color)
                cell.text = str(cell_value)
                for p in cell.text_frame.paragraphs:
                    p.alignment = PP_ALIGN.CENTER if col_idx != 7 else PP_ALIGN.LEFT
                    for r in p.runs:
                        r.font.name = FONT_MAIN
                        r.font.size = Pt(9.5)
                        r.font.color.rgb = C(DARK)
        return table_shape

    def add_notes(s, notes_text):
        notes_slide = s.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text

    # =========================================================================
    # SLIDE 1: PORTADA OFICIAL
    # =========================================================================
    s1 = prs.slides.add_slide(BLANK)
    box(s1, 0, 0, 13.333, 7.5, fill=NAVY, line=None, shape=MSO_SHAPE.RECTANGLE)
    box(s1, 0.8, 0.8, 11.733, 5.9, fill=NAVY, line=BLUE, lw=2.0)
    
    txt(s1, 1.2, 1.2, 11.0, 0.4, "UNIVERSIDAD TECNOLOGICA DEL PERU (UTP) - CURSO INTEGRADOR II: SOFTWARE", size=13, bold=True, color=ACCENT)
    txt(s1, 1.2, 1.7, 11.0, 1.1, "LEOFIT SOLUTIONS: SISTEMA DE GESTION DE PEDIDOS\nY CONTROL DE INVENTARIO MULTICANAL", size=26, bold=True, color=WHITE)
    txt(s1, 1.2, 2.9, 11.0, 0.4, "Sustentacion Final de Ingenieria (Semana 18) - Calidad ISO/IEC 25010 (S14-S16) y Arquitectura Cloud", size=15, color=LGRAY)
    
    # Tarjeta de Datos
    box(s1, 1.2, 3.6, 10.933, 2.6, fill=DARK, line=GRAY, radius=0.03)
    txt(s1, 1.5, 3.8, 5.2, 2.2, 
        "EQUIPO DE INGENIERIA (GRUPO 01):\n"
        "- Lady Luz Loayza Rodriguez (Scrum Master / DevSecOps)\n"
        "- Victor Leandro Cardenas Fernandez (Product Owner / DBA)\n"
        "- Harley Anthony Roman Delgado (Frontend Lead / UI-UX)\n"
        "- Jim Alessandro Davila Morales (QA Lead / Backend)\n"
        "- Daniel Enrique Rojas Sanchez (Business Analyst / Cloud)", 
        size=12, color=WHITE)
    
    txt(s1, 6.9, 3.8, 5.0, 2.2, 
        "METRICAS Y PARAMETROS DEL PROYECTO:\n"
        "- Empresa Beneficiaria: LeoFit Confecciones S.A.C.\n"
        "- Docente Asesor: Ing. Enrique Lee Huamani Uriarte\n"
        "- Bateria QA: 190 Pruebas Automatizadas (100% OK)\n"
        "- Base de Datos: PostgreSQL 16 (BCNF / ACID / Lima)\n"
        "- Despliegue: Render Docker API + GitHub Pages CDN\n- ISO 25010: Rendimiento (p95 280ms), Mantenibilidad y HA", 
        size=12, color=LGRAY)
        
    add_notes(s1, 
        "NOTAS DEL ORADOR (SLIDE 1 - PORTADA):\n"
        "Buenas noches estimado docente asesor Ing. Enrique Lee Huamani y miembros del jurado evaluador. "
        "Hoy el Grupo 01 tiene el agrado de presentar la sustentacion final del proyecto LeoFit Solutions, un sistema de gestion "
        "de pedidos, facturacion electronica y despacho multicanal desarrollado para la empresa LeoFit Confecciones y Diseños Deportivos S.A.C. "
        "Esta presentacion sintetiza el rigor de ingenieria, las decisiones de arquitectura (ADRs), el cumplimiento normativo SUNAT, "
        "la integracion criptografica con pasarelas de pago y las 190 pruebas automatizadas que certifican la calidad del software.")

    # =========================================================================
    # SLIDE 2: CONTEXTO Y PROBLEMÁTICA
    # =========================================================================
    s2 = prs.slides.add_slide(BLANK)
    add_header(s2, "Contexto Operativo y Diagnostico de la Empresa LeoFit", "1. CONTEXTO DEL NEGOCIO")
    
    box(s2, 0.5, 1.4, 5.9, 5.4, fill=LGRAY, line=GRAY)
    txt(s2, 0.8, 1.6, 5.3, 0.4, "Situacion Operativa Inicial (AS-IS)", size=16, bold=True, color=NAVY)
    txt(s2, 0.8, 2.1, 5.3, 4.4, 
        "- Ubicacion: Galeria El Rey de Gamarra, La Victoria, Lima.\n"
        "- Canales Desconectados: Pedidos ingresados por WhatsApp, llamadas y ventas en tienda fisica.\n"
        "- Registro Manual: Cuadernos fisicos y hojas de calculo sin validacion transaccional.\n"
        "- Desfase de Stock: Venta de prendas inexistentes (sobreventa) con impacto reputacional grave.\n"
        "- Despacho Dual Ineficiente: Retrasos en envios locales (motorizado) y provinciales (agencias).\n"
        "- Falta de Trazabilidad Tributaria: Retrasos en la emision de boletas y facturas ante SUNAT.",
        size=13, color=DARK)

    box(s2, 6.9, 1.4, 5.9, 5.4, fill=LBLUE, line=BLUE)
    txt(s2, 7.2, 1.6, 5.3, 0.4, "Solucion Implementada (TO-BE LeoFit)", size=16, bold=True, color=BLUE)
    txt(s2, 7.2, 2.1, 5.3, 4.4, 
        "- Plataforma Unificada PWA: Registro omnicanal de pedidos en menos de 40 segundos.\n"
        "- Bloqueo Pesimista (FOR UPDATE): Garantia ACID en decremento de existencias textiles.\n"
        "- Motor de Despacho Dual: Generacion automatica de hojas de ruta local y rotulos de encomienda.\n"
        "- Integracion Fiscal Automatizada: Emision de comprobantes CPE conectados con OSE Nubefact.\n"
        "- Pagos Digitales Auditados: Yape, Plin, Transferencias y Tarjetas con webhook timing-safe.\n"
        "- Trazabilidad Publica: Tracking en tiempo real para el cliente final sin autenticacion pesada.",
        size=13, color=DARK)

    add_notes(s2,
        "NOTAS DEL ORADOR (SLIDE 2 - CONTEXTO):\n"
        "Comenzamos contextualizando la problematica real de la empresa LeoFit Confecciones en Gamarra. "
        "Antes de nuestro sistema, la gestion de pedidos se realizaba por canales informales y notas de papel, "
        "lo que generaba sobreventa de stock textil, perdida de encomiendas provinciales y retrasos tributarios. "
        "Nuestra solucion digitaliza el 100% de este ciclo mediante una Progressive Web App conectada a una API REST "
        "transaccional que garantiza consistencia ACID, eliminando la sobreventa y acelerando el despacho dual.")

    # =========================================================================
    # SLIDE 3: ARQUITECTURA LÓGICA DEL SISTEMA
    # =========================================================================
    s3 = prs.slides.add_slide(BLANK)
    add_header(s3, "Arquitectura Logica y Separacion de Capas (Clean Architecture)", "2. ARQUITECTURA DE SOFTWARE")
    
    # 4 Capas horizontales
    box(s3, 0.5, 1.5, 12.333, 1.1, fill=LBLUE, line=BLUE)
    txt(s3, 0.8, 1.6, 11.5, 0.3, "CAPA DE PRESENTACION (FRONTEND SPA / PWA)", size=13, bold=True, color=BLUE)
    txt(s3, 0.8, 1.9, 11.5, 0.6, "React 19 + Vite 6 + TailwindCSS | Service Workers PWA con cache offline | jsPDF para rotulos y comprobantes", size=12, color=DARK)

    box(s3, 0.5, 2.8, 12.333, 1.1, fill=LGRAY, line=GRAY)
    txt(s3, 0.8, 2.9, 11.5, 0.3, "CAPA DE INTERFAZ Y ENRUTAMIENTO (EXPRESS API REST)", size=13, bold=True, color=NAVY)
    txt(s3, 0.8, 3.2, 11.5, 0.6, "Middlewares Helmet, CORS, RateLimiter (express-rate-limit) | Controladores delgados | Validacion con Zod Schemas", size=12, color=DARK)

    box(s3, 0.5, 4.1, 12.333, 1.1, fill=LBLUE, line=BLUE)
    txt(s3, 0.8, 4.2, 11.5, 0.3, "CAPA DE DOMINIO Y APLICACION (CORE BUSINESS SERVICES)", size=13, bold=True, color=BLUE)
    txt(s3, 0.8, 4.5, 11.5, 0.6, "OrderService, InventoryService, CulqiPaymentService, NubefactSunatService | Reglas de despacho dual y promociones", size=12, color=DARK)

    box(s3, 0.5, 5.4, 12.333, 1.3, fill=LGRAY, line=GRAY)
    txt(s3, 0.8, 5.5, 11.5, 0.3, "CAPA DE INFRAESTRUCTURA Y PERSISTENCIA (POSTGRESQL 16)", size=13, bold=True, color=NAVY)
    txt(s3, 0.8, 5.8, 11.5, 0.8, "Pool nativo 'pg' | Consultas parametrizadas anti SQLi | Zona horaria America/Lima | 11 migraciones versionables", size=12, color=DARK)

    add_notes(s3,
        "NOTAS DEL ORADOR (SLIDE 3 - ARQUITECTURA LIMPIA):\n"
        "La arquitectura del sistema sigue estrictamente los principios de Clean Architecture y separacion de responsabilidades. "
        "En el frontend implementamos React 19 con soporte PWA offline para que los operadores en taller o stand comercial no dependan de una conexion permanente. "
        "La API en Node.js 20 utiliza controladores delgados protegidos por validacion de esquemas Zod en tiempo de ejecucion, "
        "mientras que la logica de negocio esta aislada de la persistencia relacional en PostgreSQL 16.")

    # =========================================================================
    # SLIDE 4: ADR-001 - ELECCIÓN RENDER + NEON VS AWS
    # =========================================================================
    s4 = prs.slides.add_slide(BLANK)
    add_header(s4, "ADR-001: Justificacion de Render + Neon PostgreSQL frente a AWS", "3. DECISIONES DE ARQUITECTURA (ADR)")

    box(s4, 0.5, 1.4, 5.9, 5.4, fill=LGRAY, line=GRAY)
    txt(s4, 0.8, 1.6, 5.3, 0.4, "Por que Render + Neon en Fase MVP?", size=16, bold=True, color=NAVY)
    txt(s4, 0.8, 2.1, 5.3, 4.4, 
        "- Eficiencia de Costos: $0.00 a $14.00 USD/mes vs $95-$140 USD en AWS desde el dia 1.\n"
        "- Time-to-Market Inmediato: Despliegue declarativo automatizado via render.yaml en < 2 horas.\n"
        "- Cero Sobrecarga DevOps: SSL administrado automaticamente, auto-heal de contenedores Docker.\n"
        "- Base de Datos Serverless: Neon v16 escala CPU y RAM por demanda con branching instantaneo.\n"
        "- Cero Vendor Lock-in: Persistencia ANSI PostgreSQL estandar; 100% portable a AWS Aurora/RDS.",
        size=13, color=DARK)

    box(s4, 6.9, 1.4, 5.9, 5.4, fill=WHITE, line=ACCENT)
    txt(s4, 7.2, 1.6, 5.3, 0.4, "El Desafio de AWS en Etapas Iniciales", size=16, bold=True, color=ACCENT)
    txt(s4, 7.2, 2.1, 5.3, 4.4, 
        "- Costo Fijo Ineludible: NAT Gateway ($32.40/mes) + ALB ($18.00/mes) + RDS base ($18.00/mes).\n"
        "- Complejidad de Red: Mantenimiento de VPC, subredes publicas/privadas, IGW, Route Tables e IAM.\n"
        "- Desperdicio en Tráfico Inicial: En fase de validacion academica o piloto comercial temprano, el costo de red no genera ROI directo.\n"
        "- Decision Formal: Se adopta Render y Neon para validacion y se fijan umbrales formales de migracion hacia AWS.",
        size=13, color=DARK)

    add_notes(s4,
        "NOTAS DEL ORADOR (SLIDE 4 - ADR-001):\n"
        "Esta lamina responde a la primera gran interrogante del jurado: ¿Por que Render y Neon y no AWS desde el inicio? "
        "La respuesta de ingenieria es contundente: costo operativo y velocidad de despliegue. "
        "En AWS, la sola existencia de componentes de red como el NAT Gateway y el Application Load Balancer imponen un costo base "
        "superior a los $95 dolares mensuales, incluso con tráfico cero. Para un MVP o validacion piloto, Render y Neon ofrecen "
        "el mismo motor PostgreSQL 16 con costo cero a 14 dolares, sin riesgo de vendor lock-in.")

    # =========================================================================
    # SLIDE 5: COMPARATIVA TÉCNICA Y FINANCIERA
    # =========================================================================
    s5 = prs.slides.add_slide(BLANK)
    add_header(s5, "Matriz Comparativa de Criterios y Escenarios de Costo", "3. DECISIONES DE ARQUITECTURA (ADR)")

    # Tabla de criterios
    box(s5, 0.5, 1.4, 12.333, 5.4, fill=WHITE, line=GRAY)
    txt(s5, 0.8, 1.6, 11.5, 0.4, "Comparacion Rigurosa de Infraestructura (Render+Neon vs AWS Nativo)", size=15, bold=True, color=NAVY)
    
    txt(s5, 0.8, 2.1, 11.5, 4.5,
        "CRITERIO                   | RENDER + NEON SERVERLESS          | AWS NATVO (ECS + AURORA)\n"
        "--------------------------------------------------------------------------------------------------------------------\n"
        "Tiempo de Despliegue       | < 2 horas (Declarativo en Git)    | 12 - 24 horas (Terraform / CloudFormation)\n"
        "Costo Mensual Inicial      | $0.00 a $14.00 USD / mes          | $95.00 a $140.00 USD / mes (Costo fijo)\n"
        "Carga Operativa (DevOps)   | Minima (PaaS administrado)        | Media-Alta (Gestion de parches, IAM, SG)\n"
        "SLA de Disponibilidad      | 99.9% (Admisible en MVP)          | 99.99% (Multi-AZ empresarial)\n"
        "Riesgo de Lock-in          | Nulo (PostgreSQL 16 nativo)       | Medio (Dependencia de Secrets/IAM roles)\n"
        "Backups y Restauracion     | Point-in-Time Restore (PITR)      | Automated Snapshots Multi-AZ\n"
        "Latencia de Red a Lima     | ~70 - 85 ms (US-East Edge CDN)    | ~65 - 75 ms (us-east-1 N. Virginia)\n"
        "\n"
        "ESCENARIOS ECONOMICOS:\n"
        "- Escenario 1 (MVP / Sustentacion): Render+Neon = $0.00 USD | AWS = $110.00 USD (Ahorro del 100%)\n"
        "- Escenario 2 (Crecimiento Comercial): Render+Neon = $26.00 USD | AWS = $195.00 USD\n"
        "- Escenario 3 (Alta Escala >25k usuarios): AWS resulta mas eficiente por economia de escala.",
        size=11, font=FONT_CODE, color=DARK)

    add_notes(s5,
        "NOTAS DEL ORADOR (SLIDE 5 - COMPARATIVA):\n"
        "En esta matriz demostramos que evaluamos ambas opciones con criterios formales de ingenieria. "
        "En tiempo de despliegue, Render y Neon nos permitieron iterar en minutos. "
        "En cuanto a latencia, la diferencia hacia Lima es de apenas 10 milisegundos, totalmente imperceptible frente al tiempo de red general. "
        "Demostramos ademas que la migracion hacia AWS esta planificada economicamente para cuando el negocio justifique el costo fijo.")

    # =========================================================================
    # SLIDE 6: UMBRALES CUANTITATIVOS DE MIGRACIÓN
    # =========================================================================
    s6 = prs.slides.add_slide(BLANK)
    add_header(s6, "Disparadores Cuantitativos para la Migracion hacia AWS", "3. DECISIONES DE ARQUITECTURA (ADR)")

    # 4 Tarjetas de Disparadores
    box(s6, 0.5, 1.5, 5.9, 2.5, fill=LBLUE, line=BLUE)
    txt(s6, 0.8, 1.7, 5.3, 0.3, "1. CONCURRENCIA Y TRAFICO", size=14, bold=True, color=BLUE)
    txt(s6, 0.8, 2.1, 5.3, 1.7, 
        "- Trafico sostenido superior a 50 RPS (solicitudes por segundo) durante mas de 15 minutos.\n"
        "- Base activa superior a 5,000 usuarios activos diarios (DAU).\n"
        "- Gatillo: Escalamiento horizontal masivo en ECS Fargate.", size=12, color=DARK)

    box(s6, 6.9, 1.5, 5.9, 2.5, fill=LGRAY, line=GRAY)
    txt(s6, 7.2, 1.7, 5.3, 0.3, "2. GOBERNANZA Y COMPLIANCE", size=14, bold=True, color=NAVY)
    txt(s6, 7.2, 2.1, 5.3, 1.7, 
        "- Exigencia corporativa de certificacion PCI-DSS Nivel 1 directa en servidores propios.\n"
        "- Cifrado con llaves administradas por hardware propio (AWS KMS CloudHSM).\n"
        "- Requisito de interconexion bancaria privada (AWS PrivateLink).", size=12, color=DARK)

    box(s6, 0.5, 4.3, 5.9, 2.5, fill=LGRAY, line=GRAY)
    txt(s6, 0.8, 4.5, 5.3, 0.3, "3. ACUERDOS DE NIVEL DE SERVICIO (SLA)", size=14, bold=True, color=NAVY)
    txt(s6, 0.8, 4.9, 5.3, 1.7, 
        "- Compromiso contractual B2B de disponibilidad superior al 99.95% con penalizacion financiera.\n"
        "- Necesidad de conmutacion por error automatica Multi-AZ en menos de 30 segundos.\n"
        "- Despliegue de replica de almacenamiento sincrono en Aurora.", size=12, color=DARK)

    box(s6, 6.9, 4.3, 5.9, 2.5, fill=LBLUE, line=BLUE)
    txt(s6, 7.2, 4.5, 5.3, 0.3, "4. EFICIENCIA FINANCIERA", size=14, bold=True, color=BLUE)
    txt(s6, 7.2, 4.9, 5.3, 1.7, 
        "- Cuando la factura combinada de Render y Neon supere los $300.00 USD/mes.\n"
        "- En ese punto de inflexion, los contratos de reserva (Savings Plans) de AWS ofrecen un costo menor por transaccion procesada.", size=12, color=DARK)

    add_notes(s6,
        "NOTAS DEL ORADOR (SLIDE 6 - UMBRALES DE MIGRACION):\n"
        "Un arquitecto senior no se casa con un proveedor; define disparadores cuantitativos. "
        "En el documento ADR-001 definimos que LeoFit migrara a AWS cuando ocurra cualquiera de cuatro eventos: "
        "superar 50 peticiones por segundo sostenidas, requerir certificacion PCI Nivel 1 con hardware HSM, "
        "exigir un SLA del 99.99% Multi-AZ, o cuando la facturacion de Render supere los 300 dolares al mes.")

    # =========================================================================
    # SLIDE 7: ADR-002 - ARQUITECTURA OBJETIVO EN AWS
    # =========================================================================
    s7 = prs.slides.add_slide(BLANK)
    add_header(s7, "ADR-002: Maquetacion Objetivo 100% Nativa en AWS", "4. ARQUITECTURA OBJETIVO AWS")

    box(s7, 0.5, 1.4, 12.333, 5.4, fill=WHITE, line=BLUE)
    txt(s7, 0.8, 1.6, 11.5, 0.4, "Diseno C4 Nivel Contenedor bajo el AWS Well-Architected Framework", size=15, bold=True, color=NAVY)

    # 3 Columnas
    box(s7, 0.8, 2.2, 3.6, 4.3, fill=LGRAY, line=GRAY)
    txt(s7, 1.0, 2.4, 3.2, 0.3, "Perimetro y CDN", size=13, bold=True, color=BLUE)
    txt(s7, 1.0, 2.8, 3.2, 3.5, 
        "- AWS WAF: Proteccion contra inyeccion SQL, XSS y Rate Limiting perimetral.\n"
        "- Amazon CloudFront: CDN global con terminacion TLS 1.3.\n"
        "- Amazon S3: Almacenamiento seguro del frontend estatico SPA React.\n"
        "- Certificados ACM: SSL administrado con renovacion automatica.", size=11, color=DARK)

    box(s7, 4.8, 2.2, 3.7, 4.3, fill=LBLUE, line=BLUE)
    txt(s7, 5.0, 2.4, 3.3, 0.3, "Computo y Balanceo", size=13, bold=True, color=NAVY)
    txt(s7, 5.0, 2.8, 3.3, 3.5, 
        "- Application Load Balancer: Health checks activos en /api/health.\n"
        "- Amazon ECS con Fargate: Contenedores Docker serverless en subredes privadas.\n"
        "- Auto Scaling: Escalado automatico por CPU y consumo de memoria.\n"
        "- Despliegue Multi-AZ: Distribucion en us-east-1a y us-east-1b.", size=11, color=DARK)

    box(s7, 8.9, 2.2, 3.6, 4.3, fill=LGRAY, line=GRAY)
    txt(s7, 9.1, 2.4, 3.2, 0.3, "Datos y Servicios", size=13, bold=True, color=ACCENT)
    txt(s7, 9.1, 2.8, 3.2, 3.5, 
        "- Amazon Aurora PostgreSQL: Motor relacional transaccional Multi-AZ con failover automatico.\n"
        "- ElastiCache Redis: Cache de sesiones y limite de tasa distribuido.\n"
        "- AWS Secrets Manager: Rotacion segura de credenciales de BD y API keys.\n"
        "- Amazon CloudWatch: Alarmas APM y centralizacion de logs.", size=11, color=DARK)

    add_notes(s7,
        "NOTAS DEL ORADOR (SLIDE 7 - ADR-002 ARQUITECTURA AWS):\n"
        "Esta lamina responde a la segunda pregunta del jurado: ¿Como maquetarian el sistema en una arquitectura 100% AWS? "
        "El diseno propuesto en el ADR-002 sigue los 6 pilares de AWS Well-Architected. "
        "En el perimetro colocamos CloudFront y AWS WAF para filtrar ataques DDoS y SQL injection antes de que lleguen a la red. "
        "En la capa de aplicacion usamos ECS Fargate en subredes privadas aisladas sin acceso directo a internet, "
        "y en la base de datos Aurora PostgreSQL Multi-AZ con replicacion sincronica de almacenamiento.")

    # =========================================================================
    # SLIDE 8: TOPOLOGÍA DE RED VPC Y RESILIENCIA
    # =========================================================================
    s8 = prs.slides.add_slide(BLANK)
    add_header(s8, "Topologia de Red VPC y Aislamiento por Zonas de Disponibilidad", "4. ARQUITECTURA OBJETIVO AWS")

    box(s8, 0.5, 1.4, 12.333, 5.4, fill=LGRAY, line=GRAY)
    txt(s8, 0.8, 1.6, 11.5, 0.4, "Segmentacion Estricta de Red (CIDR: 10.0.0.0/16 en Region us-east-1)", size=15, bold=True, color=NAVY)

    txt(s8, 0.8, 2.2, 11.5, 4.3,
        "TOPOLOGIA DE RED EN 2 AVAILABILITY ZONES (AZ-a y AZ-b):\n"
        "--------------------------------------------------------------------------------------------------------------------\n"
        "1. SUBREDES PUBLICAS (10.0.1.0/24 y 10.0.2.0/24):\n"
        "   - Alojan exclusivamente el Application Load Balancer (ALB) y el NAT Gateway.\n"
        "   - Unicas subredes con ruta directa hacia el Internet Gateway (IGW).\n"
        "\n"
        "2. SUBREDES PRIVADAS DE COMPUTO (10.0.10.0/24 y 10.0.11.0/24):\n"
        "   - Alojan los contenedores Docker de la API en AWS Fargate.\n"
        "   - Salida a internet unicamente para consumir APIs externas (Culqi, Nubefact) via NAT Gateway.\n"
        "   - Trafico entrante restringido exclusivamente al Security Group del ALB (Puerto 3001).\n"
        "\n"
        "3. SUBREDES PRIVADAS DE DATOS (10.0.20.0/24 y 10.0.21.0/24):\n"
        "   - Alojan la base de datos Aurora PostgreSQL y los nodos de ElastiCache Redis.\n"
        "   - Totalmente aisladas: SIN ruta a internet ni asignacion de IPs publicas.\n"
        "   - Trafico entrante admitido unicamente desde el Security Group de Fargate en el puerto 5432.",
        size=11, font=FONT_CODE, color=DARK)

    add_notes(s8,
        "NOTAS DEL ORADOR (SLIDE 8 - RED VPC):\n"
        "La seguridad de red se diseno bajo el principio de defensa en profundidad. "
        "Dividimos la VPC en tres niveles de subredes a traves de dos zonas de disponibilidad (us-east-1a y us-east-1b). "
        "Las tareas de Fargate nunca tienen direcciones IP publicas, y la base de datos se encuentra en subredes de datos "
        "sin salida a internet ni ruta al exterior, eliminando vectores de ataque directo por red.")

    # =========================================================================
    # SLIDE 9: LO QUE AWS NO CONVIENE CONSTRUIR
    # =========================================================================
    s9 = prs.slides.add_slide(BLANK)
    add_header(s9, "Ecosistema de Complementos: Lo que AWS NO Conviene Construir", "4. ARQUITECTURA OBJETIVO AWS")

    # 4 Tarjetas de Justificacion
    box(s9, 0.5, 1.5, 5.9, 2.5, fill=LBLUE, line=BLUE)
    txt(s9, 0.8, 1.7, 5.3, 0.3, "PASARELA DE PAGOS: CULQI / NIUBIZ", size=13, bold=True, color=BLUE)
    txt(s9, 0.8, 2.1, 5.3, 1.7, 
        "- Por que NO en AWS: AWS Payment Cryptography es hardware HSM para bancos, no es una pasarela adquirente en Peru.\n"
        "- Solucion: Culqi y Niubiz permiten cobro en Soles con Yape, Plin y tarjetas locales con liquidacion bancaria directa.", size=12, color=DARK)

    box(s9, 6.9, 1.5, 5.9, 2.5, fill=LGRAY, line=GRAY)
    txt(s9, 7.2, 1.7, 5.3, 0.3, "FACTURACION SUNAT: OSE NUBEFACT", size=13, bold=True, color=NAVY)
    txt(s9, 7.2, 2.1, 5.3, 1.7, 
        "- Por que NO en AWS: AWS no cuenta con homologacion ante SUNAT para UBL 2.1 ni firma digital INDECOPI.\n"
        "- Solucion: Un OSE autorizado (Nubefact/Efact) absorbe los cambios tributarios constantes y el riesgo legal.", size=12, color=DARK)

    box(s9, 0.5, 4.3, 5.9, 2.5, fill=LGRAY, line=GRAY)
    txt(s9, 0.8, 4.5, 5.3, 0.3, "AUTENTICACION Y ROLES: JWT PROPIO / AUTH0", size=13, bold=True, color=NAVY)
    txt(s9, 0.8, 4.9, 5.3, 1.7, 
        "- Por que NO AWS Cognito: Curva de complejidad excesiva para esquemas de roles simples (admin/operador).\n"
        "- Solucion: Manejo de JWT sin estado con verificacion fail-fast y bcrypt reduce complejidad y costo.", size=12, color=DARK)

    box(s9, 6.9, 4.3, 5.9, 2.5, fill=LBLUE, line=BLUE)
    txt(s9, 7.2, 4.5, 5.3, 0.3, "BUSQUEDA TEXTIL: POSTGRESQL NATIVO", size=13, bold=True, color=BLUE)
    txt(s9, 7.2, 4.9, 5.3, 1.7, 
        "- Por que NO OpenSearch: AWS OpenSearch tiene un costo base de ~$180 USD/mes inviable para <10,000 SKUs.\n"
        "- Solucion: Indices GIN y Trigram en PostgreSQL resuelven busqueda por codigo, color y talla con latencia <5ms.", size=12, color=DARK)

    add_notes(s9,
        "NOTAS DEL ORADOR (SLIDE 9 - COMPLEMENTOS NO AWS):\n"
        "Un buen arquitecto sabe que construir y que comprar o integrar. "
        "Reinventar una pasarela adquirente en AWS en lugar de usar Culqi o Niubiz es un grave error de negocio en Peru, "
        "porque AWS no procesa Yape ni liquida soles a cuentas del BCP. "
        "Del mismo modo, implementar la firma UBL 2.1 de SUNAT en AWS desde cero en lugar de delegar en un OSE como Nubefact "
        "implicaria certificar una entidad de firma digital ante INDECOPI, lo cual esta fuera del alcance de una empresa comercial.")

    # =========================================================================
    # SLIDE 10: CUMPLIMIENTO SUNAT CPE
    # =========================================================================
    s10 = prs.slides.add_slide(BLANK)
    add_header(s10, "Cumplimiento Normativo SUNAT para Comprobantes Electronicos", "5. INTEGRACION TRIBUTARIA SUNAT")

    box(s10, 0.5, 1.4, 12.333, 5.4, fill=WHITE, line=GRAY)
    txt(s10, 0.8, 1.6, 11.5, 0.4, "Matriz de Requisitos Legales y Marco Regulatorio Vigente", size=15, bold=True, color=NAVY)

    txt(s10, 0.8, 2.2, 11.5, 4.3,
        "REQUISITO LEGAL           | BASE LEGAL SUNAT         | IMPLEMENTACION TECNICA EN LEOFIT\n"
        "--------------------------------------------------------------------------------------------------------------------\n"
        "Estandar UBL 2.1          | RS 097-2012 y 117-2017   | Delegado al OSE Nubefact via payload JSON estructurado.\n"
        "Firma Digital INDECOPI    | Ley 27269 / RS 097-2012  | Certificado digital acreditado inyectado por Nubefact.\n"
        "Envio a OSE Homologado    | RS 117-2017 / 252-2019   | Endpoint POST /api/v1/invoice con token de seguridad.\n"
        "Plazo Maximo de Envio     | RS 193-2020 / 003-2023   | Emision sincrona al confirmar el pedido (< 3 segundos).\n"
        "Condicion de RUC          | TUO Codigo Tributario    | Validacion previa de RUC 'ACTIVO' y 'HABIDO'.\n"
        "Desglose de IGV (18%)     | Ley del IGV (D.S. 055)   | Calculo matematico exacto de Base Imponible + Impuesto.\n"
        "Representacion Impresa    | Anexo RS 097-2012        | Generacion PDF con Codigo Hash SHA-256 y Codigo QR oficial.\n"
        "Persistencia Tributaria   | Art. 87 Codigo Tribut.   | Tabla 'invoices' registra serie, correlativo, hash y CDR.",
        size=11, font=FONT_CODE, color=DARK)

    add_notes(s10,
        "NOTAS DEL ORADOR (SLIDE 10 - NORMATIVA SUNAT):\n"
        "Esta seccion responde a la tercera pregunta del jurado sobre el cumplimiento de comprobantes de pago electronicos (CPE). "
        "En el Peru, la emision esta regida por las Resoluciones de Superintendencia N.° 097-2012 y 117-2017. "
        "LeoFit cumple con el estandar internacional OASIS UBL 2.1 y la firma digital homologada ante INDECOPI a traves del OSE Nubefact. "
        "El sistema desglosa con precision el 18% del IGV y almacena el codigo hash y el CDR de recepcion en la tabla 'invoices'.")

    # =========================================================================
    # SLIDE 11: FLUJO TÉCNICO DE EMISIÓN DE FACTURAS
    # =========================================================================
    s11 = prs.slides.add_slide(BLANK)
    add_header(s11, "Flujo Tecnico de Emision y Respuestas de Error OSE/SUNAT", "5. INTEGRACION TRIBUTARIA SUNAT")

    # 4 Pasos secuenciales
    box(s11, 0.5, 1.5, 2.9, 5.2, fill=LGRAY, line=GRAY)
    txt(s11, 0.7, 1.7, 2.5, 0.3, "PASO 1: ORDEN", size=13, bold=True, color=NAVY)
    txt(s11, 0.7, 2.1, 2.5, 4.3, 
        "- Cliente confirma pedido.\n"
        "- Selecciona Boleta o Factura.\n"
        "- Ingresa DNI (8 digitos) o RUC (11 digitos).\n"
        "- Backend valida consistencia del documento receptor.\n"
        "- Se reserva correlativo en base de datos.", size=12, color=DARK)

    box(s11, 3.6, 1.5, 2.9, 5.2, fill=LBLUE, line=BLUE)
    txt(s11, 3.8, 1.7, 2.5, 0.3, "PASO 2: PAYLOAD", size=13, bold=True, color=BLUE)
    txt(s11, 3.8, 2.1, 2.5, 4.3, 
        "- Construccion JSON fiscal en nubefact.service.ts.\n"
        "- Desglose por items: valor unitario, total y tributos.\n"
        "- Inyeccion de token de seguridad de comercio.\n"
        "- Manejo de moneda (PEN) y tipo de operacion onerosa.", size=12, color=DARK)

    box(s11, 6.7, 1.5, 2.9, 5.2, fill=LGRAY, line=GRAY)
    txt(s11, 6.9, 1.7, 2.5, 0.3, "PASO 3: OSE Y SUNAT", size=13, bold=True, color=NAVY)
    txt(s11, 6.9, 2.1, 2.5, 4.3, 
        "- OSE valida esquema XSD y genera XML UBL 2.1.\n"
        "- Aplica firma digital con certificado INDECOPI.\n"
        "- Remite a servidores centrales de SUNAT.\n"
        "- Obtiene Constancia de Recepcion (CDR codigo 0).", size=12, color=DARK)

    box(s11, 9.8, 1.5, 3.0, 5.2, fill=LBLUE, line=BLUE)
    txt(s11, 10.0, 1.7, 2.6, 0.3, "PASO 4: ENTREGA", size=13, bold=True, color=ACCENT)
    txt(s11, 10.0, 2.1, 2.6, 4.3, 
        "- Backend guarda hash y enlaces en BD atómica.\n"
        "- Cliente recibe confirmacion en pantalla.\n"
        "- Descarga inmediata de PDF con Codigo QR oficial.\n"
        "- Modo simulado funcional en desarrollo sin llaves.", size=12, color=DARK)

    add_notes(s11,
        "NOTAS DEL ORADOR (SLIDE 11 - FLUJO FACTURACION):\n"
        "En esta lamina explicamos el flujo de datos exacto. "
        "Cuando el cliente registra su compra, el backend genera el payload en nubefact.service.ts y llama al OSE. "
        "El OSE valida las reglas tributarias, firma digitalmente el XML y obtiene la constancia CDR de SUNAT. "
        "Si el sistema no cuenta con credenciales en desarrollo, conmuta limpiamente a un simulador que genera "
        "un hash demostrativo para permitir la prueba funcional de punta a punta sin arrojar excepciones.")

    # =========================================================================
    # SLIDE 12: PASARELA DE PAGOS SANDBOX VS PRODUCCIÓN
    # =========================================================================
    s12 = prs.slides.add_slide(BLANK)
    add_header(s12, "Pasarela de Pagos: Operacion en Sandbox frente a Produccion", "6. PASARELA DE PAGOS Y PCI-DSS")

    box(s12, 0.5, 1.4, 5.9, 5.4, fill=LGRAY, line=GRAY)
    txt(s12, 0.8, 1.6, 5.3, 0.4, "Ambiente Sandbox (Pruebas - Estado Actual)", size=16, bold=True, color=NAVY)
    txt(s12, 0.8, 2.1, 5.3, 4.4, 
        "- Cargo Simulado: No hay debito real de fondos ni liquidacion interbancaria.\n"
        "- Tarjetas de Prueba: Numeros provistos por Culqi (4111...) con fechas futuras arbitrarias.\n"
        "- Credenciales de Prueba: Llaves publicas pk_test y privadas sk_test.\n"
        "- Fallback Inteligente: Si falta la llave secreta, culqi.ts conmuta a mock local (chr_mock_).\n"
        "- Cero Riesgo Financiero: Permite validar todo el flujo de cobro sin costo transaccional.",
        size=13, color=DARK)

    box(s12, 6.9, 1.4, 5.9, 5.4, fill=LBLUE, line=BLUE)
    txt(s12, 7.2, 1.6, 5.3, 0.4, "Pase a Produccion Comercial (En Vivo)", size=16, bold=True, color=BLUE)
    txt(s12, 7.2, 2.1, 5.3, 4.4, 
        "- Proceso KYC Bancario: RUC activo, ficha RUC y cuenta corriente de LeoFit en BCP o BBVA.\n"
        "- Emision de Llaves Live: Reemplazo de variables de entorno por pk_live y sk_live.\n"
        "- Descuento Real: Debito inmediato de fondos en cuentas de clientes con retencion legal.\n"
        "- Comision Comercial: Tarifa de adquirencia pactada (aprox. 3.44% + $0.30 USD + IGV).\n"
        "- Codigo 100% Preparado: Cero cambios de codigo requeridos; solo configuracion de entorno.",
        size=13, color=DARK)

    add_notes(s12,
        "NOTAS DEL ORADOR (SLIDE 12 - PAGOS SANDBOX VS PROD):\n"
        "La cuarta pregunta del jurado indaga sobre la realidad de los pagos y sus limitantes. "
        "En el repositorio implementamos la pasarela Culqi en modo Sandbox. "
        "Esto significa que el flujo logico de cobro y tokenizacion es 100% real, pero las transacciones utilizan tarjetas de prueba sin debitar dinero. "
        "El paso a produccion no requiere reescribir software: la logica ya contempla las llaves de produccion; solo se requiere "
        "culminar el tramite administrativo de KYC bancario de la empresa LeoFit para activar las llaves live.")

    # =========================================================================
    # SLIDE 13: SEGURIDAD CRIPTOGRÁFICA Y PCI-DSS
    # =========================================================================
    s13 = prs.slides.add_slide(BLANK)
    add_header(s13, "Seguridad Criptografica, Webhooks HMAC y Cumplimiento PCI-DSS", "6. PASARELA DE PAGOS Y PCI-DSS")

    box(s13, 0.5, 1.4, 5.9, 5.4, fill=WHITE, line=BLUE)
    txt(s13, 0.8, 1.6, 5.3, 0.4, "Cumplimiento PCI-DSS (Cuestionario SAQ A)", size=16, bold=True, color=BLUE)
    txt(s13, 0.8, 2.1, 5.3, 4.4, 
        "- Tokenizacion en el Cliente: El formulario web utiliza el SDK Culqi JS directamente en el navegador del usuario.\n"
        "- Aislamiento Total del PAN: Los 16 digitos de la tarjeta y el CVV NUNCA tocan el servidor de LeoFit.\n"
        "- Reduccion de Alcance: Al no almacenar datos de tarjetahabientes, LeoFit califica bajo el estandar SAQ A de PCI-DSS v4.0.\n"
        "- Esto exime a LeoFit de someter su infraestructura a costosas auditorias de certificacion de red Nivel 1.",
        size=13, color=DARK)

    box(s13, 6.9, 1.4, 5.9, 5.4, fill=LGRAY, line=GRAY)
    txt(s13, 7.2, 1.6, 5.3, 0.4, "Validacion de Webhooks con HMAC-SHA256", size=16, bold=True, color=NAVY)
    txt(s13, 7.2, 2.1, 5.3, 4.4, 
        "- Endpoint: POST /api/webhooks/payment en paymentWebhook.controller.ts.\n"
        "- Firma Criptografica: Se verifica la firma enviada por la pasarela con el secreto del comercio.\n"
        "- Proteccion contra Timing Attacks: Implementacion de crypto.timingSafeEqual en Node.js.\n"
        "- Idempotencia Transaccional: Verificacion de si la transaccion ya fue procesada antes de actualizar la BD.\n"
        "- Actualizacion Atomica: Transicion del pedido a 'CONFIRMADO' y estado de pago 'PAGADO'.",
        size=13, color=DARK)

    add_notes(s13,
        "NOTAS DEL ORADOR (SLIDE 13 - PCI-DSS Y HMAC):\n"
        "Desde la perspectiva de seguridad de la informacion, implementamos tokenizacion del lado del cliente. "
        "Esto nos permite acogernos al cuestionario SAQ A de PCI-DSS, garantizando que ningun dato confidencial de tarjeta "
        "quede registrado en logs o bases de datos de LeoFit. "
        "Adicionalmente, los webhooks asincronos son validados con firmas HMAC-SHA256 utilizando comparacion de tiempo constante "
        "mediante crypto.timingSafeEqual, neutralizando ataques de temporizacion.")

    # =========================================================================
    # SLIDE 14: MODELO DE DATOS Y TIMEZONE LIMA
    # =========================================================================
    s14 = prs.slides.add_slide(BLANK)
    add_header(s14, "Modelo Relacional (BCNF) y Resolucion de Zona Horaria", "7. BASE DE DATOS Y PERSISTENCIA")

    box(s14, 0.5, 1.4, 5.9, 5.4, fill=LGRAY, line=GRAY)
    txt(s14, 0.8, 1.6, 5.3, 0.4, "Normalizacion y Consistencia ACID", size=16, bold=True, color=NAVY)
    txt(s14, 0.8, 2.1, 5.3, 4.4, 
        "- Tercera Forma Normal (3FN / BCNF): Esquema relacional con 11 tablas maestras y de transaccion.\n"
        "- Tablas Clave: products, product_variants, orders, order_items, payments, invoices, audit_logs.\n"
        "- Integridad Referencial: Claves foraneas con eliminacion restringida (ON DELETE RESTRICT).\n"
        "- Bloqueo Pesimista (SELECT FOR UPDATE): Evita carreras criticas (race conditions) en compras concurrentes.\n"
        "- Migraciones Versionables: 11 migraciones secuenciales en TypeScript reproducibles en CI/CD.",
        size=13, color=DARK)

    box(s14, 6.9, 1.4, 5.9, 5.4, fill=LBLUE, line=BLUE)
    txt(s14, 7.2, 1.6, 5.3, 0.4, "Configuracion de Zona Horaria 'America/Lima'", size=16, bold=True, color=BLUE)
    txt(s14, 7.2, 2.1, 5.3, 4.4, 
        "- Problematica: En servidores cloud (Render/Neon en US-East), la hora por defecto es UTC (+00:00).\n"
        "- Impacto: Pedidos nocturnos en Lima se registraban con la fecha del dia siguiente, alterando auditorias y reportes contables.\n"
        "- Solucion en backend/src/config/database.ts: Inyeccion obligatoria de timezone al inicializar el pool:\n"
        "  client.query(\"SET timezone = 'America/Lima'\")\n"
        "- Garantia: 100% de marcas de tiempo (created_at) persisten en horario oficial peruano (UTC-5).",
        size=13, color=DARK)

    add_notes(s14,
        "NOTAS DEL ORADOR (SLIDE 14 - BASE DE DATOS):\n"
        "En la base de datos PostgreSQL 16 aplicamos estricta normalizacion en Forma Normal de Boyce-Codd. "
        "Un aporte tecnico critico que resolvimos fue la discrepancia de zona horaria: al estar los servidores de Neon en Estados Unidos, "
        "los pedidos se registraban en horario UTC, lo que causaba que pedidos hechos despues de las 7 pm tuvieran la fecha del dia siguiente. "
        "Configuramos el pool de conexiones para que cada sesion ejecute obligatoriamente 'SET timezone = America/Lima', "
        "garantizando concordancia contable con la SUNAT.")

    # =========================================================================
        # =========================================================================
    # SLIDE 15: CALIDAD DE RENDIMIENTO (ISO/IEC 25010:2023 - SEMANA 14)
    # =========================================================================
    s15 = prs.slides.add_slide(BLANK)
    add_header(s15, "Calidad de Rendimiento (ISO/IEC 25010:2023): Percentiles y Senales Doradas SRE", "8. CALIDAD DE RENDIMIENTO (SEMANA 14)")

    # 3 Cajas Superiores de Resumen de Metricas SRE
    box(s15, 0.5, 1.4, 3.8, 1.3, fill=NAVY, line=None)
    txt(s15, 0.5, 1.48, 3.8, 0.4, "p50: 120ms | p95: 280ms/480ms", size=17, bold=True, color=WHITE, align="c")
    txt(s15, 0.5, 2.0, 3.8, 0.4, "PERCENTIL 95 (P95) EN 1 Y 10 USUARIOS (SLO < 700 ms)", size=9, bold=True, color=ACCENT, align="c")

    box(s15, 4.7, 1.4, 3.9, 1.3, fill=BLUE, line=None)
    txt(s15, 4.7, 1.48, 3.9, 0.4, "0.00% ERRORES (SLO < 0.1%)", size=18, bold=True, color=WHITE, align="c")
    txt(s15, 4.7, 2.0, 3.9, 0.4, "TASA DE FALLOS EN PRUEBAS STEADY Y SOAK (4 HORAS)", size=9, bold=True, color=LGRAY, align="c")

    box(s15, 9.0, 1.4, 3.8, 1.3, fill=DARK, line=None)
    txt(s15, 9.0, 1.48, 3.8, 0.4, "CPU < 25% | RAM 185 MB", size=18, bold=True, color=WHITE, align="c")
    txt(s15, 9.0, 2.0, 3.8, 0.4, "SATURACION SRE < 70% EN CARGA COMERCIAL NOMINAL", size=9, bold=True, color=LGRAY, align="c")

    # Tabla de Resultados de los 4 Ensayos k6
    headers_s15 = ["Tipo de Ensayo", "Carga", "Duracion", "p50 (ms)", "p95 (ms)", "p99 (ms)", "RPS", "Errores %", "Saturacion SRE", "Evaluacion SLA"]
    rows_s15 = [
        ["Linea Base", "1 VU", "2 min", "120 ms", "280 ms", "410 ms", "2.8 r/s", "0.00%", "CPU: 8% | RAM: 145 MB", "Cumple (Holgado)"],
        ["Steady-State", "10 VU", "30 min", "240 ms", "480 ms", "720 ms", "19.0 r/s", "0.00%", "CPU: 24% | RAM: 185 MB", "Cumple (< 700 ms)"],
        ["Spike Test", "35 VU", "5 min", "620 ms", "1,400 ms", "1,820 ms", "45.2 r/s", "0.00%", "CPU: 58% | RAM: 230 MB", "Observado (Limite)"],
        ["Soak Test", "8 VU", "4 horas", "225 ms", "460 ms", "680 ms", "16.0 r/s", "0.00%", "CPU: 21% | RAM: 188 MB", "Cumple (Sin fugas)"]
    ]
    col_w_s15 = [1.6, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.1, 1.733]
    table(s15, 0.5, 2.85, 12.333, 1.95, headers_s15, rows_s15, col_w_s15)

    # Bloque Inferior: Las 4 Señales Doradas SRE y Diagnóstico de Cuello de Botella
    box(s15, 0.5, 4.95, 5.9, 1.9, fill=LBLUE, line=BLUE)
    txt(s15, 0.7, 5.05, 5.5, 0.3, "Las Cuatro Senales Doradas de SRE (Google)", size=13, bold=True, color=BLUE)
    txt(s15, 0.7, 5.4, 5.5, 1.35, 
        "- 1. Latencia por Percentiles: El promedio oculta la cola larga (GC V8 y locks). p95 = 480ms en carga comercial.\n"
        "- 2. Trafico: 19 req/s nominales; capacidad maxima demostrada de 45 req/s en tier base de Render.\n"
        "- 3. Errores: 0.00% fallos transaccionales en 34,200 solicitudes (meta SRE < 0.10%).\n"
        "- 4. Saturacion: CPU < 25% y memoria en 185 MB, respetando holgadamente el margen de saturacion (< 70%).",
        size=10.5, color=DARK)

    box(s15, 6.9, 4.95, 5.9, 1.9, fill=LGRAY, line=GRAY)
    txt(s15, 7.1, 5.05, 5.5, 0.3, "Diagnostico de Cola Larga (p99) y Optimizacion B-Tree", size=13, bold=True, color=NAVY)
    txt(s15, 7.1, 5.4, 5.5, 1.35, 
        "- Causa de p99 en Spike (1,820 ms): Latencia transfronteriza RTT hacia Neon PostgreSQL (EE. UU.) y limites del pool.\n"
        "- Optimizacion Inmediata: Creacion de indices compuestos B-Tree idx_orders_customer_created y idx_variants_stock.\n"
        "- Resultado Medible: Reduccion del 64.2% en costo EXPLAIN ANALYZE (de 14.8 ms a 5.3 ms en ejecucion SQL).\n"
        "- Accion Estructural AWS (ADR-002): Despliegue en misma VPC con RDS Multi-AZ, abatiendo RTT a < 1.5 ms.",
        size=10.5, color=DARK)

    add_notes(s15,
        "NOTAS DEL ORADOR (SLIDE 15 - RENDIMIENTO SEMANA 14):\n"
        "En la evaluacion de rendimiento bajo ISO/IEC 25010:2023 aplicamos el rigor de la ingenieria de confiabilidad de sitios (Google SRE). "
        "En primer lugar, demostramos por que el promedio aritmetico oculta la realidad: un promedio puede ser bajo mientras la cola larga p99 "
        "revela pausas de recoleccion de basura o contencion de bloqueos. Por ello medimos percentiles: mediana p50 de 120 ms, p95 de 280 ms con 1 usuario, "
        "y 480 ms con 10 usuarios concurrentes sostenidos en una prueba Steady-State de 30 minutos, manteniendo 0% de errores frente a un SLO de 700 ms. "
        "Ademas, ejecutamos una prueba Soak de 4 horas continuas que certifico la ausencia total de fugas de memoria en Node.js. "
        "En el ensayo de Spike identificamos que la latencia p99 se debio a la distancia con la base de datos en Estados Unidos; "
        "optimizamos indices B-Tree reduciendo el costo SQL en 64.2%, y dejamos justificada la arquitectura de baja latencia en AWS.")

    # =========================================================================
    # SLIDE 16: FLEXIBILIDAD: ADAPTABILIDAD, ESCALABILIDAD Y RESILIENCIA CLOUD
    # =========================================================================
    s16 = prs.slides.add_slide(BLANK)
    add_header(s16, "Flexibilidad (ISO/IEC 25010:2023): Adaptabilidad, Escalabilidad y Resiliencia", "8. CALIDAD DE RENDIMIENTO (SEMANA 14)")

    # Banner Central Distintivo
    box(s16, 0.5, 1.35, 12.333, 0.65, fill=NAVY, line=None)
    txt(s16, 0.5, 1.48, 12.333, 0.4, 
        "ISO/IEC 25010:2023 — FLEXIBILITY: ADAPTAR = CONTEXTO / ENTORNO  |  ESCALAR = DEMANDA ATENDIDA SIN DEGRADACION",
        size=11.5, bold=True, color=WHITE, align="c")

    # Columna Izquierda: Adaptabilidad
    box(s16, 0.5, 2.15, 5.9, 4.7, fill=WHITE, line=BLUE)
    txt(s16, 0.8, 2.3, 5.3, 0.35, "Adaptabilidad (Portabilidad de Entorno)", size=15, bold=True, color=BLUE)
    txt(s16, 0.8, 2.75, 5.3, 3.9, 
        "- Definicion ISO: Capacidad de ajustarse a diferentes entornos operativos y de red sin alterar el codigo fuente.\n\n"
        "- The Twelve-Factor App (Factor III - Configuracion):\n"
        "  * 100% de credenciales, puertos y endpoints inyectados como variables (.env, Render Secrets, AWS Parameter Store).\n\n"
        "- Clean Architecture Desacoplada:\n"
        "  * Capa Controller: Expone contratos REST OpenAPI.\n"
        "  * Capa Service: Encapsula 100% de logica comercial pura.\n"
        "  * Capa Repository: Interfaz agnostica de persistencia SQL.\n\n"
        "- Portabilidad Comprobada: Mismo codigo fuente opera en Local Docker Compose, Staging Render y AWS ECS Fargate.",
        size=11, color=DARK)

    # Columna Derecha: Escalabilidad y Resiliencia
    box(s16, 6.9, 2.15, 5.9, 4.7, fill=LGRAY, line=GRAY)
    txt(s16, 7.2, 2.3, 5.3, 0.35, "Escalabilidad Elastica y Patrones de Resiliencia", size=15, bold=True, color=NAVY)
    txt(s16, 7.2, 2.75, 5.3, 3.9, 
        "- Principio Rector: Optimizar consultas y bloqueos antes de escalar.\n\n"
        "- Patrones de Resiliencia Cloud Implementados:\n"
        "  * Circuit Breaker (Cortacircuito): Fail-fast en 5 fallos ante caidas de SUNAT o WhatsApp para no bloquear el Event Loop.\n"
        "  * Bulkhead (Aislamiento): Separacion de pools; ordenes transaccionales aisladas de lecturas de catalogo.\n"
        "  * Retry con Exponential Backoff y Jitter: Reintentos con dispersion aleatoria (+-20%) para evitar 'thundering herd'.\n"
        "  * Rate Limiting / Load Shedding: 100 req/min y descarte selectivo de carga no esencial al superar 75% CPU.\n\n"
        "- Auto-Scaling: Disparo a > 70% CPU, tiempo de provisionamiento 42s y enfriamiento (cooldown) de 300s para evitar flapping.",
        size=11, color=DARK)

    add_notes(s16,
        "NOTAS DEL ORADOR (SLIDE 16 - FLEXIBILIDAD Y RESILIENCIA):\n"
        "En la ISO/IEC 25010:2023, la caracteristica Flexibility unifica a la antigua portabilidad con la adaptabilidad y la escalabilidad. "
        "Adaptabilidad responde a mover el software entre entornos: lo resolvemos mediante Clean Architecture y Twelve-Factor App, "
        "donde cambiar de base de datos o de nube implica cero modificaciones en las reglas comerciales. "
        "Por otro lado, la escalabilidad no se limita a poner mas servidores: aplicamos el principio de optimizar antes de escalar, "
        "e implementamos patrones formales de resiliencia: Circuit Breakers que cortan llamadas a servicios externos lentos con fail-fast, "
        "Bulkhead para aislar el pool de compras respecto a reportes, Retry con backoff exponencial y jitter para evitar avalanchas, "
        "y Rate Limiting con Load Shedding que garantiza que el checkout transaccional nunca se caiga.")

    # =========================================================================
    # SLIDE 17: MANTENIBILIDAD: MODULARIDAD Y DIRECCIÓN DE DEPENDENCIAS (SEMANA 15)
    # =========================================================================
    s17 = prs.slides.add_slide(BLANK)
    add_header(s17, "Calidad de Mantenibilidad (ISO/IEC 25010:2023): Modularidad y Dependencias", "9. CALIDAD DE MANTENIBILIDAD (SEMANA 15)")

    # 3 Cajas de Modularidad y Clean Architecture
    box(s17, 0.5, 1.4, 3.8, 5.4, fill=WHITE, line=ACCENT)
    txt(s17, 0.7, 1.6, 3.4, 0.35, "Anti-Patron Monolitico", size=14, bold=True, color=ACCENT)
    txt(s17, 0.7, 2.05, 3.4, 4.6, 
        "- Archivo gigante tipo app.py que concentra:\n"
        "  * Rutas HTTP y endpoints\n"
        "  * Logica de negocio y descuentos\n"
        "  * Consultas SQL directas concatenadas\n"
        "  * Renderizado de vistas y plantillas\n\n"
        "- Graves Consecuencias:\n"
        "  * Alto acoplamiento espagueti\n"
        "  * Cambiar un precio rompe la facturacion\n"
        "  * Imposibilidad de probar con mocks\n"
        "  * Deuda tecnica inmanejable.",
        size=11, color=DARK)

    box(s17, 4.6, 1.4, 4.1, 5.4, fill=LBLUE, line=BLUE)
    txt(s17, 4.8, 1.6, 3.7, 0.35, "Direccion de Dependencias (Clean)", size=14, bold=True, color=BLUE)
    txt(s17, 4.8, 2.05, 3.7, 4.6, 
        "- Principio de Inversion de Dependencias (DIP):\n\n"
        "  [ Infraestructura (Express/SQL/Zod) ]\n"
        "                  | (depende de)\n"
        "                  v\n"
        "  [ Casos de Uso / Servicios (order.service) ]\n"
        "                  | (depende de)\n"
        "                  v\n"
        "  [ Dominio Puro (models/ - Sin Frameworks) ]\n\n"
        "- Beneficio Crucial:\n"
        "  El dominio comercial de LeoFit no importa nada de Express, Postgres ni librerias cloud.",
        size=11, color=DARK)

    box(s17, 9.0, 1.4, 3.8, 5.4, fill=LGRAY, line=GRAY)
    txt(s17, 9.2, 1.6, 3.4, 0.35, "Reusabilidad Transversal (DRY)", size=14, bold=True, color=NAVY)
    txt(s17, 9.2, 2.05, 3.4, 4.6, 
        "- Cero Duplicidad de Codigo:\n\n"
        "- Middleware RBAC (requireRole):\n"
        "  Protege 14 endpoints administrativos.\n\n"
        "- Idempotencia RFC 8785:\n"
        "  Blindaje en ordenes, cobros y anulaciones.\n\n"
        "- Motor PDF Vectorial:\n"
        "  Genera rotulos de despacho y boletas.\n\n"
        "- Esquemas Zod Reutilizables:\n"
        "  Validacion estricta en frontend y backend.",
        size=11, color=DARK)

    add_notes(s17,
        "NOTAS DEL ORADOR (SLIDE 17 - MANTENIBILIDAD SEMANA 15):\n"
        "En la Semana 15 analizamos la mantenibilidad segun ISO/IEC 25010:2023. "
        "Separar archivos en carpetas no basta si las dependencias estan desordenadas. En LeoFit aplicamos Clean Architecture "
        "con una regla de dependencia estricta: las dependencias apuntan hacia el centro, hacia el Dominio Puro. "
        "Nuestras entidades y reglas de negocio no conocen Express, ni PostgreSQL, ni bibliotecas externas. "
        "Superamos por completo el anti-patron monolitico tipo app.py, y logramos una reusabilidad comprobada: "
        "un unico middleware de roles protege 14 rutas, la idempotencia RFC 8785 blinda toda operacion transaccional, "
        "y el generador de PDF atiende tanto a logistica como a tesoreria.")

    # =========================================================================
    # SLIDE 18: MANTENIBILIDAD: MODIFICABILIDAD, MÉTRICAS Y TESTABILIDAD TDD
    # =========================================================================
    s18 = prs.slides.add_slide(BLANK)
    add_header(s18, "Mantenibilidad: Modificabilidad, Metricas Objetivas y Testabilidad TDD", "9. CALIDAD DE MANTENIBILIDAD (SEMANA 15)")

    # Columna Izquierda: Modificabilidad y Blast Radius
    box(s18, 0.5, 1.4, 5.9, 5.4, fill=WHITE, line=BLUE)
    txt(s18, 0.8, 1.6, 5.3, 0.35, "Modificabilidad y Analisis de 'Blast Radius'", size=15, bold=True, color=BLUE)
    txt(s18, 0.8, 2.05, 5.3, 4.6, 
        "- Definicion ISO: Efectividad y eficiencia con que el software se modifica sin introducir defectos colaterales.\n\n"
        "- Caso Real CHG-01 en LeoFit:\n"
        "  * Requerimiento: Descuento textil del 10% en compras al por mayor (>= 6 prendas).\n"
        "  * Archivo Modificado: Exclusivamente src/services/order.service.ts (calculateOrderTotals).\n"
        "  * Impacto en Controladores y Rutas: 0 lineas modificadas.\n"
        "  * Impacto en Esquema de BD: 0 alteraciones en tablas relacionales.\n\n"
        "- Metrica de 'Blast Radius' (Radio de Impacto):\n"
        "  * Solo 2 archivos tocados: el servicio de negocio y su suite de pruebas unitarias.\n"
        "  * Trazabilidad inmutable en Git con commit semantico feat(orders).",
        size=11.5, color=DARK)

    # Columna Derecha: Métricas Objetivas y Testabilidad TDD
    box(s18, 6.9, 1.4, 5.9, 5.4, fill=LGRAY, line=GRAY)
    txt(s18, 7.2, 1.6, 5.3, 0.35, "Metricas Objetivas y Piramide de Pruebas (TDD)", size=15, bold=True, color=NAVY)
    txt(s18, 7.2, 2.05, 5.3, 4.6, 
        "- Piramide de Pruebas Automatizadas (194 Tests Totales):\n"
        "  * Base: 140 pruebas unitarias rapidas (< 50ms) con mocks en memoria.\n"
        "  * Centro: 44 pruebas de integracion con Supertest y base de datos.\n"
        "  * Cupide: 10 pruebas end-to-end y de contrato OpenAPI.\n\n"
        "- Metricas de Mantenibilidad Auditadas:\n"
        "  * Complejidad Ciclomatica (McCabe): Valores de 1 a 3 en metodos core (umbral maximo optimo <= 4).\n"
        "  * Cobertura de Pruebas: 84.6% en servicios y 92.1% en calculos con Decimal.js.\n\n"
        "- Comprobacion Automatizada en CI/CD:\n"
        "  * Bateria completa ejecuta en 42 segundos en GitHub Actions.",
        size=11.5, color=DARK)

    add_notes(s18,
        "NOTAS DEL ORADOR (SLIDE 18 - MODIFICABILIDAD, METRICAS Y TDD):\n"
        "En modificabilidad y testabilidad presentamos evidencia con metricas cuantitativas. "
        "Para evaluar la modificabilidad, medimos el radio de impacto o 'blast radius': ante un cambio comercial real de descuentos por volumen, "
        "solo se modificaron 2 archivos en todo el repositorio: el archivo del servicio y su prueba unitaria, con cero impacto en controladores o base de datos. "
        "En mantenibilidad objetiva reportamos la complejidad ciclomatica de McCabe, situandonos en valores de 1 a 3, dentro del rango optimo menor a 4. "
        "Nuestra piramide de pruebas cuenta con 194 pruebas automatizadas con 100% de exito y una cobertura superior al 80% en las reglas de negocio criticas, "
        "ejecutandose de forma automatizada en el pipeline de GitHub Actions en 42 segundos.")

    # =========================================================================
    # SLIDE 19: CONFIABILIDAD: ALTA DISPONIBILIDAD (HA VS HPC) (SEMANA 16)
    # =========================================================================
    s19 = prs.slides.add_slide(BLANK)
    add_header(s19, "Calidad de Confiabilidad: Alta Disponibilidad (HA vs HPC) y Tolerancia a Fallos", "10. PROYECCION DE CONFIABILIDAD (SEMANA 16)")

    # Banner Comparativo HA vs HPC
    box(s19, 0.5, 1.4, 5.9, 2.4, fill=WHITE, line=BLUE)
    txt(s19, 0.8, 1.55, 5.3, 0.35, "HA: Alta Disponibilidad (High Availability)", size=15, bold=True, color=BLUE)
    txt(s19, 0.8, 1.95, 5.3, 1.75, 
        "- Enfoque: Operacion continua 24/7 sin caidas de servicio.\n"
        "- Casos de Aplicacion: Banca digital, pasarelas de pago, comercio electronico y LeoFit.\n"
        "- Mecanismos Clave: Redundancia activa, clúster de nodos, balanceo de carga y failover automatico ante contingencias.\n"
        "- Meta LeoFit: Uptime proyectado del 99.9% anual.",
        size=11.5, color=DARK)

    box(s19, 6.9, 1.4, 5.9, 2.4, fill=LGRAY, line=GRAY)
    txt(s19, 7.2, 1.55, 5.3, 0.35, "HPC: Computacion de Alto Rendimiento", size=15, bold=True, color=NAVY)
    txt(s19, 7.2, 1.95, 5.3, 1.75, 
        "- Enfoque: Maxima velocidad de procesamiento y calculo intensivo.\n"
        "- Casos de Aplicacion: Entrenamiento de modelos IA (LLMs), bioinformatica, simulaciones sismicas.\n"
        "- Arquitectura: Miles de GPUs/CPUs trabajando en paralelo sobre grandes volumenes (Petabytes).\n"
        "- Diferencia: HPC prioriza calculo; HA prioriza tiempo activo 24/7.",
        size=11.5, color=DARK)

    # Bloque Inferior: Tolerancia a Fallos y PITR en LeoFit
    box(s19, 0.5, 4.0, 5.9, 2.8, fill=LBLUE, line=BLUE)
    txt(s19, 0.8, 4.15, 5.3, 0.35, "Tolerancia a Fallos en LeoFit", size=14, bold=True, color=BLUE)
    txt(s19, 0.8, 4.55, 5.3, 2.15, 
        "- PWA con Modo Offline: Service Workers almacenan cache estatico y catalogo textil para consultas sin conexion en Gamarra.\n"
        "- Circuit Breakers y Reintentos: En colas de notificaciones WhatsApp y SUNAT ante indisponibilidad externa.\n"
        "- Degradacion Elegante: Mensajes claros al usuario sin bloqueos de pantalla ni caidas fatales.",
        size=11.5, color=DARK)

    box(s19, 6.9, 4.0, 5.9, 2.8, fill=LGRAY, line=GRAY)
    txt(s19, 7.2, 4.15, 5.3, 0.35, "Respaldo y Recuperacion (PITR)", size=14, bold=True, color=NAVY)
    txt(s19, 7.2, 4.55, 5.3, 2.15, 
        "- Respaldo Continuo en Neon PostgreSQL: Registro ininterrumpido de Write-Ahead Logs (WAL) en almacenamiento duradero.\n"
        "- Point-in-Time Restore (PITR): Restauracion exacta a cualquier segundo previo ante corrupcion o incidente humano.\n"
        "- Metricas de Continuidad: RPO (Recovery Point Objective) < 5 min; RTO (Recovery Time Objective) < 15 min.",
        size=11.5, color=DARK)

    add_notes(s19,
        "NOTAS DEL ORADOR (SLIDE 19 - CONFIABILIDAD SEMANA 16):\n"
        "Proyectando hacia la Semana 16, abordamos la calidad de confiabilidad segun ISO 25010. "
        "El docente nos planteo una distincion clave: servidores HPC frente a servidores HA. Mientras que HPC resuelve calculo intensivo masivo para modelos de IA con GPUs, "
        "sistemas de comercio y pedidos como LeoFit requieren arquitectura HA de Alta Disponibilidad 24/7, garantizando que el servicio nunca se detenga. "
        "En LeoFit aplicamos tolerancia a fallos mediante la PWA con Service Workers que permite operar offline en las galerias de Gamarra, "
        "y garantizamos recuperacion ante desastres con copias continuas Point-in-Time Restore en PostgreSQL, con un objetivo de punto de recuperacion menor a 5 minutos.")

    # SLIDE 20: BATERÍA DE 194 PRUEBAS AUTOMATIZADAS
    # =========================================================================
    s20 = prs.slides.add_slide(BLANK)
    add_header(s20, "Aseguramiento de Calidad: 194 Pruebas Automatizadas (100% OK)", "11. TESTING Y CALIDAD (QA)")

    # Metricas grandes
    box(s20, 0.5, 1.5, 3.8, 1.8, fill=NAVY, line=None)
    txt(s20, 0.5, 1.7, 3.8, 0.5, "194", size=36, bold=True, color=WHITE, align="c")
    txt(s20, 0.5, 2.3, 3.8, 0.4, "TOTAL PRUEBAS APROBADAS (0 FALLOS)", size=11, bold=True, color=ACCENT, align="c")

    box(s20, 4.7, 1.5, 3.9, 1.8, fill=BLUE, line=None)
    txt(s20, 4.7, 1.7, 3.9, 0.5, "125", size=36, bold=True, color=WHITE, align="c")
    txt(s20, 4.7, 2.3, 3.9, 0.4, "PRUEBAS BACKEND (JEST + SUPERTEST)", size=11, bold=True, color=LGRAY, align="c")

    box(s20, 9.0, 1.5, 3.8, 1.8, fill=DARK, line=None)
    txt(s20, 9.0, 1.7, 3.8, 0.5, "69", size=36, bold=True, color=WHITE, align="c")
    txt(s20, 9.0, 2.3, 3.8, 0.4, "PRUEBAS FRONTEND (VITEST + RTL)", size=11, bold=True, color=LGRAY, align="c")

    # Detalle de suites
    box(s20, 0.5, 3.6, 12.333, 3.2, fill=LGRAY, line=GRAY)
    txt(s20, 0.8, 3.8, 11.5, 0.4, "Distribucion de Suites de Prueba Automatizadas", size=14, bold=True, color=NAVY)
    txt(s20, 0.8, 4.2, 11.5, 2.4, 
        "- Seguridad y OWASP Top 10 (security.test.ts): Inyeccion SQL, XSS, headers Helmet y validacion Zod.\n"
        "- Autenticacion y Matriz RBAC (auth.test.ts): Control estricto de roles admin y operador (401/403).\n"
        "- Integracion e Interoperabilidad (integration_external.test.ts): Contrato OpenAPI y webhooks HMAC.\n"
        "- Transaccionalidad de Pedidos (orders.test.ts): Bloqueo FOR UPDATE y decremento atomico de stock.\n"
        "- Usabilidad y Accesibilidad (usability_iso25010.test.ts): Navegacion por teclado y renderizado WCAG.\n"
        "- Generacion de Documentos (pdfGenerator.test.ts): Creacion de rotulos de envio y comprobantes PDF.",
        size=12, color=DARK)

    add_notes(s20,
        "NOTAS DEL ORADOR (SLIDE 20 - TESTING QA):\n"
        "La confiabilidad de LeoFit no es declarativa; esta demostrada con 194 pruebas automatizadas con 100% de exito. "
        "En el backend corremos 125 pruebas con Jest que validan seguridad OWASP, inyeccion SQL, tokens manipulados y concurrencia. "
        "En el frontend ejecutamos 69 pruebas con Vitest y Testing Library que certifican el renderizado de formularios, "
        "generacion de PDFs de despacho y guardas de autenticacion en la interfaz.")

    # =========================================================================
    # SLIDE 21: MARCO DE CALIDAD ISO/IEC 25010:2023 Y CAPACIDAD DE INTERACCIÓN
    # =========================================================================
    s21 = prs.slides.add_slide(BLANK)
    add_header(s21, "Marco Integral ISO/IEC 25010:2023 y Capacidad de Interaccion (SUS)", "11. TESTING Y CALIDAD (QA)")

    box(s21, 0.5, 1.4, 5.9, 5.4, fill=WHITE, line=BLUE)
    txt(s21, 0.8, 1.6, 5.3, 0.4, "Las 9 Caracteristicas de ISO/IEC 25010:2023", size=15, bold=True, color=BLUE)
    txt(s21, 0.8, 2.1, 5.3, 4.4, 
        "- 1. Functional Suitability: 100% completitud (10 RF verificados).\n"
        "- 2. Performance Efficiency: p95 = 480 ms y sat. < 25% (SLA < 700 ms).\n"
        "- 3. Compatibility: Coexistencia Docker certificada sin degradacion.\n"
        "- 4. Interaction Capability: Evaluacion SUS 88.5/100 y WCAG 2.1 AA.\n"
        "- 5. Reliability: Tolerancia a fallos PWA y DRP con RTO de 3.2s.\n"
        "- 6. Security: Autenticacion JWT HS256, Bcrypt y HMAC-SHA256.\n"
        "- 7. Maintainability: Clean Architecture, complejidad 1-3 y TDD.\n"
        "- 8. Flexibility: Adaptabilidad multi-entorno y escalabilidad.\n"
        "- 9. Safety: Ausencia de dano financiero (cero sobreventas ACID).",
        size=11.5, color=DARK)

    box(s21, 6.9, 1.4, 5.9, 5.4, fill=LGRAY, line=GRAY)
    txt(s21, 7.2, 1.6, 5.3, 0.4, "Capacidad de Interaccion y Accesibilidad WCAG", size=15, bold=True, color=NAVY)
    txt(s21, 7.2, 2.1, 5.3, 4.4, 
        "- System Usability Scale (SUS): Puntaje obtenido de 88.5 / 100 (Grado A - Excelente, Percentil 96%).\n"
        "- Estudio Empirico en Gamarra: Evaluacion con 5 participantes reales en el stand comercial de LeoFit.\n"
        "- Agilidad Operativa: Reduccion del tiempo de pedido de 310s a 38.2s (mejora del 87.6%).\n"
        "- Accesibilidad WCAG 2.1 AA/AAA: Contrastes de color certificados desde 5.42:1 hasta 17.8:1.\n"
        "- Navegacion Accesible: 100% de acciones operables exclusivamente mediante teclado (Tab/Enter).\n"
        "- Diseno Responsivo: Adaptabilidad probada en moviles Android, iOS y pantallas desktop.",
        size=11.5, color=DARK)

    add_notes(s21,
        "NOTAS DEL ORADOR (SLIDE 21 - ISO 25010:2023):\n"
        "Cerramos el modulo de calidad respaldando la totalidad del software bajo las 9 caracteristicas de la ISO/IEC 25010:2023. "
        "Destacamos la incorporacion de Safety, que garantiza la ausencia de danos economicos para la empresa mediante consistencia ACID estricta. "
        "En Interaction Capability, nuestro estudio con la metodologia estandar SUS alcanzo 88.5 sobre 100 con usuarios reales de Gamarra, "
        "reduciendo el tiempo de atencion en 87.6%. Cumplimos ademas con accesibilidad web WCAG 2.1 con contrastes de hasta 17.8 a 1, "
        "optimizados para operar en condiciones de alta luminosidad en el stand comercial.")

    # =========================================================================
    # SLIDE 22: DEMOSTRACIÓN EN LA NUBE
    # =========================================================================
    s22 = prs.slides.add_slide(BLANK)
    add_header(s22, "Validacion y Despliegue en Vivo en la Nube (Cloud Staging)", "12. DESPLIEGUE Y OPERACION")

    # 3 Cajas de Despliegue
    box(s22, 0.5, 1.5, 3.8, 5.2, fill=LGRAY, line=GRAY)
    txt(s22, 0.8, 1.7, 3.2, 0.3, "FRONTEND PWA", size=14, bold=True, color=NAVY)
    txt(s22, 0.8, 2.1, 3.2, 4.3, 
        "- URL Publica: Enlace en GitHub Pages con certificado SSL global.\n"
        "- Edge CDN: Distribucion geografica rapida de activos.\n"
        "- Soporte PWA: Instalable en dispositivos Android, iOS y Windows.\n"
        "- Cache Estrategico: Service Workers almacenan catalogo base para consulta sin conexion.", size=12, color=DARK)

    box(s22, 4.7, 1.5, 3.9, 5.2, fill=LBLUE, line=BLUE)
    txt(s22, 5.0, 1.7, 3.3, 0.3, "BACKEND API", size=14, bold=True, color=BLUE)
    txt(s22, 5.0, 2.1, 3.3, 4.3, 
        "- Hosting: Render Cloud Platform con Dockerfile de produccion.\n"
        "- Endpoint Health: /api/health retorna HTTP 200 con estado de BD.\n"
        "- Documentacion Viva: OpenAPI y Swagger integrados en /api/docs.\n"
        "- Variables Cifradas: Inyeccion segura sin filtracion de secretos en Git.", size=12, color=DARK)

    box(s22, 9.0, 1.5, 3.8, 5.2, fill=LGRAY, line=GRAY)
    txt(s22, 9.3, 1.7, 3.2, 0.3, "BASE DE DATOS", size=14, bold=True, color=ACCENT)
    txt(s22, 9.3, 2.1, 3.2, 4.3, 
        "- Motor: Neon Serverless PostgreSQL 16.\n"
        "- SSL Enforcement: Conexiones forzadas con cifrado TLS en transito.\n"
        "- Timezone Configurado: Sesiones fijadas en America/Lima.\n"
        "- Backups Continuos: Point-in-Time Restore activo para recuperacion ante incidentes.", size=12, color=DARK)

    add_notes(s22,
        "NOTAS DEL ORADOR (SLIDE 22 - CLOUD EN VIVO):\n"
        "El sistema no es una maqueta local; esta desplegado y operativo en la nube. "
        "El frontend se sirve a traves de la CDN de GitHub Pages con soporte PWA instalable en celulares. "
        "La API REST corre en un contenedor Docker sobre Render con un health check activo en /api/health, "
        "y la base de datos PostgreSQL 16 en Neon opera con conexiones SSL forzadas y respaldos continuos.")

    # =========================================================================
    # SLIDE 23: MATRIZ DE TRAZABILIDAD ANTE EL JURADO
    # =========================================================================
    s23 = prs.slides.add_slide(BLANK)
    add_header(s23, "Matriz de Trazabilidad: Respuestas a las 5 Preguntas del Jurado", "13. DEFENSA ANTE EL JURADO")

    box(s23, 0.5, 1.4, 12.333, 5.4, fill=WHITE, line=GRAY)
    txt(s23, 0.8, 1.6, 11.5, 0.4, "Trazabilidad Directa entre Preguntas, Anexos y Codigo Fuente", size=15, bold=True, color=NAVY)

    txt(s23, 0.8, 2.2, 11.5, 4.3,
        "PREGUNTA DEL JURADO              | DOCUMENTO TECNICO | EVIDENCIA EN CODIGO (`ruta:linea`)    | ESTADO\n"
        "--------------------------------------------------------------------------------------------------------------------\n"
        "1. ¿Por que Render+Neon vs AWS?  | Anexo ADR-001     | render.yaml:1-70 / database.ts:16-55  | LISTO\n"
        "2. Maquetacion 100% AWS?         | Anexo ADR-002     | culqi.ts:57 / nubefact.service.ts:1   | LISTO\n"
        "3. Cumplimiento Normativo SUNAT? | Anexo DOC-SUNAT   | nubefact.service.ts:171 / 008_inv.ts  | LISTO\n"
        "4. Pagos reales o simulados?     | Anexo DOC-PAY     | culqi.ts:85 / paymentWebhook.ts:61    | LISTO\n"
        "5. Arquitectura del Repositorio? | Anexo DOC-ARCH    | backend/src/ / 190 tests unitarios    | LISTO\n"
        "\n"
        "SINTESIS DEFENSIBLE:\n"
        "- Cada afirmacion técnica del equipo está respaldada por una linea verificable en el repositorio.\n"
        "- Toda la documentacion cuenta con referencias normativas y fuentes oficiales citadas.\n"
        "- Cero suposiciones: lo implementado esta probado y lo planificado tiene hoja de ruta cuantitativa.",
        size=11, font=FONT_CODE, color=DARK)

    add_notes(s23,
        "NOTAS DEL ORADOR (SLIDE 23 - TRAZABILIDAD JURADO):\n"
        "Esta lamina resume la preparacion del equipo ante la evaluacion del tribunal. "
        "Las cinco preguntas tipicas sobre eleccion de infraestructura, maquetacion AWS, SUNAT, pasarelas de pago y arquitectura de software "
        "estan formalmente documentadas en seis anexos tecnicos y cuentan con evidencia verificable linea a linea en el repositorio GitHub. "
        "No hay respuestas ambiguas: todo lo afirmado se sustenta en el codigo fuente.")

    # =========================================================================
    # SLIDE 24: CONCLUSIONES Y APORTES DE INGENIERÍA
    # =========================================================================
    s24 = prs.slides.add_slide(BLANK)
    add_header(s24, "Conclusiones del Proyecto y Aportes a la Empresa LeoFit", "14. CONCLUSIONES Y APORTES")

    box(s24, 0.5, 1.4, 5.9, 5.4, fill=LBLUE, line=BLUE)
    txt(s24, 0.8, 1.6, 5.3, 0.4, "Impacto Comercial y Operativo en LeoFit", size=16, bold=True, color=BLUE)
    txt(s24, 0.8, 2.1, 5.3, 4.4, 
        "- Eliminacion Total de Sobreventa: Bloqueo pesado en base de datos garantiza stock 100% certero.\n"
        "- Reduccion de Tiempo de Registro: De mas de 5 minutos por llamada/WhatsApp a 38.2 segundos en la PWA.\n"
        "- Cero Errores en Despacho: Automatizacion de guias locales y rotulos oficiales de agencia de transporte.\n"
        "- Facturacion Inmediata: Emision de boletas en menos de 3 segundos integrada al proceso de cobro.\n"
        "- Autonomia Operativa: Personal del stand capacitado y operando fluidamente en moviles.",
        size=13, color=DARK)

    box(s24, 6.9, 1.4, 5.9, 5.4, fill=LGRAY, line=GRAY)
    txt(s24, 7.2, 1.6, 5.3, 0.4, "Aportes Formativos de Ingenieria de Software", size=16, bold=True, color=NAVY)
    txt(s24, 7.2, 2.1, 5.3, 4.4, 
        "- Aplicacion Rigurosa de Estandares: Clean Architecture, ISO/IEC 25010, C4 Model y MADR para ADRs.\n"
        "- Cultura DevSecOps: 190 pruebas automatizadas en CI/CD, sanitizacion PII y escaneo de vulnerabilidades.\n"
        "- Enfoque Financiero Real: Demostracion de eficiencia de costos antes de sobre-arquitecturar en la nube.\n"
        "- Documentacion Defendible: Manuales tecnicos, diagramas compilados y matrices de trazabilidad auditables.",
        size=13, color=DARK)

    add_notes(s24,
        "NOTAS DEL ORADOR (SLIDE 24 - CONCLUSIONES):\n"
        "Como conclusiones finales, el proyecto LeoFit Solutions demostro viabilidad tecnica y valor comercial tangible. "
        "Para la empresa, redujo el tiempo de procesamiento de pedidos en un 87% y elimino las discrepancias de inventario. "
        "Para nuestro equipo de ingenieria, el proyecto represento la integracion integral de todas las competencias del curso: "
        "desde el modelado relacional BCNF hasta la seguridad criptografica, el testing automatizado y la gestion de infraestructura cloud.")

    # =========================================================================
    # SLIDE 25: CIERRE Y RONDA DE PREGUNTAS
    # =========================================================================
    s25 = prs.slides.add_slide(BLANK)
    box(s25, 0, 0, 13.333, 7.5, fill=NAVY, line=None, shape=MSO_SHAPE.RECTANGLE)
    box(s25, 0.8, 0.8, 11.733, 5.9, fill=NAVY, line=BLUE, lw=2.0)
    
    txt(s25, 1.2, 1.6, 11.0, 0.4, "PROYECTO FINAL COMPLETADO SATISFACTORIAMENTE", size=13, bold=True, color=ACCENT, align="c")
    txt(s25, 1.2, 2.1, 11.0, 0.8, "Muchas Gracias por su Atencion", size=32, bold=True, color=WHITE, align="c")
    txt(s25, 1.2, 2.9, 11.0, 0.4, "LeoFit Solutions - Grupo 01 | Seccion 35374 (Ciclo 2026-I)", size=16, color=LGRAY, align="c")
    
    box(s25, 2.0, 3.8, 9.333, 2.2, fill=DARK, line=GRAY, radius=0.03)
    txt(s25, 2.2, 4.0, 8.933, 1.8, 
        "PANEL DE PREGUNTAS Y DEFENSA TECNICA ABIERTO:\n\n"
        "- Repositorio Oficial: github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema\n"
        "- Documentacion de Anexos: _PROYECTO_FINAL_LOCAL/01_ANEXOS_TECNICOS/\n"
        "- Sistema en Vivo: leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/",
        size=13, color=WHITE, align="c")

    add_notes(s25,
        "NOTAS DEL ORADOR (SLIDE 25 - CIERRE):\n"
        "Con esto concluimos la exposicion formal de la arquitectura y resultados de LeoFit Solutions. "
        "Agradecemos profundamente al docente asesor Ing. Enrique Lee Huamani por el acompanamiento y exigencia academica a lo largo del ciclo. "
        "Quedamos a disposicion del jurado evaluador para absolver cualquier pregunta tecnica sobre el codigo, los diagramas, "
        "la base de datos o las decisiones de arquitectura presentadas. Muchas gracias.")

    prs.save(OUT_PPTX)
    DOCS_PPTX_DIR = os.path.join(BASE_DIR, "docs", "05_SUSTENTACION_PROYECTO_FINAL_SEMANA_18")
    os.makedirs(DOCS_PPTX_DIR, exist_ok=True)
    DOCS_PPTX = os.path.join(DOCS_PPTX_DIR, "03_PRESENTACION_OFICIAL_SUSTENTACION_PROYECTO_FINAL.pptx")
    prs.save(DOCS_PPTX)
    size_kb = os.path.getsize(OUT_PPTX) / 1024.0
    print(f"[OK] Presentacion PPTX generada con exito:")
    print(f"     Ruta: {OUT_PPTX}")
    print(f"     Diapositivas: {len(prs.slides)} slides (Requisito >= 18 slides)")
    print(f"     Tamano: {size_kb:.1f} KB")
    return OUT_PPTX, len(prs.slides), size_kb

if __name__ == "__main__":
    create_deck()
