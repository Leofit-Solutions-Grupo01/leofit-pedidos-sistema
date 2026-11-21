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

    IMG_DIR = os.path.join(BASE_DIR, "docs", "05_SUSTENTACION_PROYECTO_FINAL_SEMANA_18", "graficos")

    def pic(s, filename, x, y, w, h=None):
        path = os.path.join(IMG_DIR, filename)
        if os.path.exists(path):
            if h is not None:
                return s.shapes.add_picture(path, Inches(x), Inches(y), Inches(w), Inches(h))
            else:
                return s.shapes.add_picture(path, Inches(x), Inches(y), Inches(w))
        return None

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
        "   - Alojan la base de datos Aurora PostgreSQL 16 (BCNF, 11 tablas) y nodos ElastiCache Redis.\n"
        "   - Totalmente aisladas: SIN ruta a internet ni asignacion de IPs publicas.\n"
        "   - Trafico entrante admitido unicamente desde el Security Group de Fargate en el puerto 5432.\n"
        "   - Pool configurado con 'SET timezone = America/Lima' para consistencia fiscal SUNAT.",
        size=11, font=FONT_CODE, color=DARK)

    add_notes(s8,
        "NOTAS DEL ORADOR (SLIDE 8 - RED VPC Y DATOS):\n"
        "La seguridad de red se diseno bajo el principio de defensa en profundidad. "
        "Dividimos la VPC en tres niveles de subredes a traves de dos zonas de disponibilidad (us-east-1a y us-east-1b). "
        "Las tareas de Fargate nunca tienen direcciones IP publicas, y la base de datos PostgreSQL 16 estructurada en BCNF "
        "se encuentra en subredes de datos sin salida a internet ni ruta al exterior. "
        "El pool inyecta obligatoriamente la zona horaria America/Lima para asegurar consistencia contable con SUNAT.")

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
    # SLIDE 14: MARCO DE CALIDAD ISO 9126 Y EVOLUCIÓN A ISO/IEC 25010:2023
    # =========================================================================
    s14 = prs.slides.add_slide(BLANK)
    add_header(s14, "Marco de Calidad: Fundamentos ISO 9126 y Transicion a ISO/IEC 25010:2023", "7. MARCO DE CALIDAD DE SOFTWARE")

    # Columna Izquierda: Estructura ISO 9126 (Partes 1-4) y Fórmulas
    box(s14, 0.5, 1.4, 5.8, 5.4, fill=WHITE, line=BLUE)
    txt(s14, 0.8, 1.6, 5.2, 0.35, "Norma ISO/IEC 9126: Estructura y Metricas de Clase", size=15, bold=True, color=BLUE)
    txt(s14, 0.8, 2.05, 5.2, 4.6, 
        "- Estructura Cuatripartita de la Norma ISO 9126:\n"
        "  * ISO 9126-1: Modelo de calidad (interna, externa y en uso).\n"
        "  * ISO 9126-2 (Metricas Externas - Runtime): Cobertura 100%, Tiempo analisis 8.5m, Exito causas 100%, Confiabilidad 100% (p95=480ms, 0% fallas k6).\n"
        "  * ISO 9126-3 (Metricas Internas - Estatico): Completitud 100%, Suficiencia de pruebas 129% (194 tests), UI evidente 100%, McCabe 1-3, Trazabilidad 100%.\n"
        "  * ISO 9126-4 (Calidad en Uso): Efectividad 100%, Productividad 8.2x (38.2s vs 310s), Dano Economico S/ 0.00, SUS 88.5/100.\n\n"
        "- Formulacion Matematica de Clase:\n"
        "  * Adecuacion Funcional (Diapo 17):\n"
        "    X = 1 - (A / B) = 1 - (0 / 10) = 1.0 (100% de adecuacion)\n"
        "    (A = 0 funciones deficientes | B = 10 funciones requeridas)\n"
        "  * Madurez de Fiabilidad (Diapo 19):\n"
        "    X = A / B = 194 / 194 = 1.0 (100% de madurez)\n"
        "    (A = 194 pruebas aprobadas | B = 194 pruebas requeridas)",
        size=10.0, color=DARK)

    # Columna Derecha: Las 6 Características y Evolución
    box(s14, 6.5, 1.4, 6.3, 5.4, fill=LGRAY, line=GRAY)
    txt(s14, 6.8, 1.6, 5.7, 0.35, "Las 6 Caracteristicas ISO 9126 vs ISO 25010:2023", size=15, bold=True, color=NAVY)
    txt(s14, 6.8, 2.05, 5.7, 4.6, 
        "- Taxonomia Original ISO 9126-1 (6 Caracteristicas):\n"
        "  1. Funcionalidad: Adecuacion (100%), Exactitud (Decimal.js), Interoperabilidad (SUNAT/WhatsApp), Seguridad y Conformidad.\n"
        "  2. Fiabilidad: Madurez (X=A/B), Tolerancia a fallos (PWA offline, FOR UPDATE) y Recuperabilidad (PITR 3.2s).\n"
        "  3. Usabilidad: Entendimiento, Aprendizaje, Operabilidad, Atraccion.\n"
        "  4. Eficiencia: Comportamiento temporal (p50=120ms) y Recursos.\n"
        "  5. Mantenibilidad: Capacidad de analisis, Cambiabilidad (CHG-01 en 2 archivos), Estabilidad y Testabilidad (TDD).\n"
        "  6. Portabilidad: Adaptabilidad (Clean Arch), Instalacion, Coexistencia.\n\n"
        "- Evolucion Normativa hacia ISO/IEC 25010:2023 (9 Caracteristicas):\n"
        "  * Seguridad: Pasa de subcaracteristica a caracteristica de 1° nivel.\n"
        "  * Safety (Seguridad Funcional): Nueva caracteristica (ACID).\n"
        "  * Portabilidad: Absorbida en Flexibility (formalizando Scalability).\n"
        "  * Usabilidad: Evoluciona a Interaction Capability (WCAG 2.1 AAA).",
        size=10.5, color=DARK)

    add_notes(s14,
        "NOTAS DEL ORADOR (SLIDE 14 - MARCO DE CALIDAD ISO 9126):\n"
        "Iniciamos el bloque de calidad fundamentando la evolucion teorica desde la norma ISO/IEC 9126. "
        "El docente explico en clase que la ISO 9126 se divide en 4 partes fundamentales: "
        "la parte 1 con el modelo conceptual de 6 caracteristicas maestras y 27 subcaracteristicas; "
        "la parte 2 de metricas externas en ejecucion, cuyos 3 objetivos son validar cumplimiento externo, predecir calidad en uso y describir respuesta ante requisitos, logrando 100% de cobertura y 8.5 minutos en diagnostico; "
        "la parte 3 de metricas internas estaticas de codigo sin ejecucion, midiendo completitud (100%), suficiencia de pruebas (129% con 194 tests) y complejidad McCabe de 1 a 3; "
        "y la parte 4 para calidad en uso en produccion, abarcando efectividad, productividad, seguridad física y económica con S/ 0.00 de daño, y satisfaccion SUS. "
        "En LeoFit aplicamos rigurosamente las formulas de la clase: en adecuacion de la diapositiva 17, X = 1 - (A/B) alcanza 1.0 (100%) al cumplir los 10 requisitos funcionales; "
        "y en madurez de la diapositiva 19, X = A/B logra 194 pruebas aprobadas sobre 194 requeridas sin defectos abiertos. "
        "Mostramos ademas la genealogia hacia la ISO/IEC 25010:2023 vigente con sus 9 caracteristicas.")

    # =========================================================================
        # =========================================================================
    # SLIDE 15: CALIDAD DE RENDIMIENTO (ISO/IEC 25010 - SEMANA 14)
    # =========================================================================
    s15 = prs.slides.add_slide(BLANK)
    add_header(s15, "Calidad de Rendimiento (ISO/IEC 25010): Latencia p50/p95/p99 y SRE", "8. CALIDAD DE RENDIMIENTO (SEMANA 14)")

    # Columna Izquierda: Metricas y Analisis
    box(s15, 0.5, 1.4, 5.8, 1.25, fill=NAVY, line=None)
    txt(s15, 0.7, 1.45, 5.4, 0.4, "280 ms / 480 ms", size=22, bold=True, color=WHITE)
    txt(s15, 0.7, 1.95, 5.4, 0.4, "PERCENTIL 95 (P95) EN 1 Y 10 VU (META SLO < 700 ms)", size=9.5, bold=True, color=ACCENT)

    # 2 Mini Cajas
    box(s15, 0.5, 2.75, 2.8, 1.05, fill=BLUE, line=None)
    txt(s15, 0.6, 2.85, 2.6, 0.35, "0.0% ERRORES", size=15, bold=True, color=WHITE, align="c")
    txt(s15, 0.6, 3.25, 2.6, 0.35, "TASA DE FALLOS EN CARGA", size=8.5, bold=True, color=LGRAY, align="c")

    box(s15, 3.5, 2.75, 2.8, 1.05, fill=DARK, line=None)
    txt(s15, 3.6, 2.85, 2.6, 0.35, "45 req / seg", size=15, bold=True, color=WHITE, align="c")
    txt(s15, 3.6, 3.25, 2.6, 0.35, "CAPACIDAD MAXIMA TIER BASE", size=8.5, bold=True, color=LGRAY, align="c")

    # Tarjeta de Analisis SRE
    box(s15, 0.5, 3.9, 5.8, 2.9, fill=WHITE, line=BLUE)
    txt(s15, 0.7, 4.05, 5.4, 0.3, "Evaluacion de Latencia y Senales Doradas SRE", size=13, bold=True, color=BLUE)
    txt(s15, 0.7, 4.4, 5.4, 2.3, 
        "- Operacion Critica: POST /api/orders (verificacion y reserva atomica de stock).\n"
        "- Mediana p50: 120 ms (1 VU) y 240 ms (10 VU) - Experiencia tipica excelente.\n"
        "- Percentil 95: 480 ms en carga nominal (SLA < 700 ms superado con holgura).\n"
        "- Cola Larga (p99 = 720 ms): Causada por contencion en pool y RTT hacia Neon.\n"
        "- Optimizacion: Indices B-Tree redujeron costo de consulta en 64.2%.\n"
        "- Soak Test 60 min: Cero fugas de memoria (RAM estable < 185 MB).",
        size=10.5, color=DARK)

    # Columna Derecha: Grafico Cientifico de Percentiles
    pic(s15, "fig02_percentiles_latencia_k6.png", 6.5, 1.4, 6.3, 5.4)

    add_notes(s15,
        "NOTAS DEL ORADOR (SLIDE 15 - RENDIMIENTO SEMANA 14):\n"
        "En la Semana 14 evaluamos cuantitativamente el rendimiento del software bajo la norma ISO/IEC 25010:2023. "
        "A la derecha pueden observar el grafico cientifico de barras horizontales de percentiles. "
        "Superando el promedio simple, medimos p50, p90, p95 y p99. La experiencia tipica de la mediana p50 es de solo 120 a 240 ms. "
        "En carga nominal de 10 usuarios virtuales, el percentil 95 responde en 480 ms, muy por debajo de la linea roja de corte del SLO de 700 ms. "
        "La cola larga de p99 refleja la contencion del pool de conexiones hacia Neon, la cual mitigamos en un 64% creando indices B-Tree compuestos.")

    # =========================================================================
    # SLIDE 16: CURVA DE CARGA Y SATURACIÓN (SEMANA 14)
    # =========================================================================
    s16 = prs.slides.add_slide(BLANK)
    add_header(s16, "Curva de Carga k6: Capacidad Maxima y Punto de Saturacion", "8. CALIDAD DE RENDIMIENTO (SEMANA 14)")

    # Columna Izquierda: Explicacion de Capacidad y Punto de Saturacion
    box(s16, 0.5, 1.4, 5.8, 5.4, fill=WHITE, line=BLUE)
    txt(s16, 0.8, 1.6, 5.2, 0.35, "Analisis de Capacidad, Limites y Auto-Scaling", size=15, bold=True, color=NAVY)
    txt(s16, 0.8, 2.05, 5.2, 4.6, 
        "- Zona de Crecimiento Lineal (1 a 25 VU):\n"
        "  * Throughput (TPS) escala proporcionalmente hasta 45.6 TPS.\n"
        "  * CPU permanece por debajo del 50% y latencia contenida (< 600 ms).\n\n"
        "- Punto de Inflexion y Saturacion (~33 a 35 VU):\n"
        "  * Throughput se ameseta en ~47 TPS por contencion del pool PostgreSQL.\n"
        "  * Utilizacion de CPU cruza el umbral critico del 70% sostenido.\n"
        "  * Latencia p95 entra en regimen exponencial no lineal (> 2,000 ms).\n\n"
        "- Parametros de Disparo de Auto-Scaling (AWS ECS):\n"
        "  * Trigger: CPU > 70% sostenido durante 60 segundos.\n"
        "  * Aprovisionamiento: 42 segundos en nuevo contenedor Fargate.\n"
        "  * Cooldown: 300 segundos para evitar oscilaciones destructivas (flapping).\n\n"
        "- Respaldo Normativo: ISO/IEC 25010:2023 - Flexibility - Scalability.",
        size=11, color=DARK)

    # Columna Derecha: Grafico Combinado Carga vs Throughput vs CPU vs Latencia
    pic(s16, "fig04_saturacion_capacidad_throughput_cpu.png", 6.5, 1.4, 6.3, 5.4)

    add_notes(s16,
        "NOTAS DEL ORADOR (SLIDE 16 - SATURACION Y CAPACIDAD):\n"
        "En esta diapositiva presentamos el grafico combinado de saturacion y capacidad, el cual responde con rigor cientifico donde esta el limite del sistema. "
        "A la derecha vemos que hasta los 25 usuarios virtuales el throughput crece de forma lineal y la CPU se mantiene en rangos seguros. "
        "Entre los 33 y 35 usuarios virtuales identificamos con precision el punto de saturacion: el throughput se ameseta en 47 transacciones por segundo, "
        "la CPU supera el 70% del limite seguro de Google SRE, y la latencia entra en regimen no lineal. "
        "Este grafico justifica empiricamente el parametro de disparo del autoescalado en ECS Fargate para aprovisionar nuevas instancias antes de degradar la experiencia de compra.")

    # =========================================================================
    # SLIDE 17: MANTENIBILIDAD: MODULARIDAD Y REUSABILIDAD (SEMANA 15)
    # =========================================================================
    s17 = prs.slides.add_slide(BLANK)
    add_header(s17, "Calidad de Mantenibilidad (ISO/IEC 25010): Modularidad y Reusabilidad", "9. CALIDAD DE MANTENIBILIDAD (SEMANA 15)")

    # Comparativa Antes vs Despues (Anti-patron vs Clean Architecture)
    box(s17, 0.5, 1.4, 4.0, 5.4, fill=WHITE, line=ACCENT)
    txt(s17, 0.8, 1.6, 3.4, 0.35, "El Anti-Patron Monolitico", size=15, bold=True, color=ACCENT)
    txt(s17, 0.8, 2.05, 3.4, 4.6, 
        "- Archivo gigante (tipo app.py / server.js) que mezcla todo:\n"
        "  * Rutas HTTP y endpoints\n"
        "  * Renderizado de pantallas\n"
        "  * Reglas de negocio hardcodeadas\n"
        "  * Consultas SQL directas\n"
        "  * Validaciones de entrada\n\n"
        "- Consecuencias Graves:\n"
        "  * Alto acoplamiento\n"
        "  * Un cambio rompe modulos no relacionados\n"
        "  * Imposible hacer pruebas unitarias aisladas\n"
        "  * Deuda tecnica exponencial y dificil incorporacion de nuevos desarrolladores.",
        size=11.5, color=DARK)

    # Estructura Modular de LeoFit
    box(s17, 4.8, 1.4, 4.0, 5.4, fill=LBLUE, line=BLUE)
    txt(s17, 5.1, 1.6, 3.4, 0.35, "Modularidad en LeoFit (Clean)", size=15, bold=True, color=BLUE)
    txt(s17, 5.1, 2.05, 3.4, 4.6, 
        "- Separacion Estricta de Responsabilidades:\n"
        "  * src/routes/ : Definicion de rutas HTTP y contratos REST.\n"
        "  * src/controllers/ : Mapeo de requests, codigos de estado y DTOs.\n"
        "  * src/services/ : Logica de negocio pura (descuentos, stock, estados).\n"
        "  * src/repositories/ : Consultas SQL parametrizadas.\n"
        "  * src/tests/ : Suites de pruebas automatizadas aisladas.\n\n"
        "- Beneficio Concreto:\n"
        "  Modificar la logica de pedidos no toca la base de datos ni los endpoints HTTP.",
        size=11.5, color=DARK)

    # Reusabilidad de Componentes
    box(s17, 9.1, 1.4, 3.7, 5.4, fill=LGRAY, line=GRAY)
    txt(s17, 9.3, 1.6, 3.3, 0.35, "Reusabilidad Comprobada", size=15, bold=True, color=NAVY)
    txt(s17, 9.3, 2.05, 3.3, 4.6, 
        "- Cero Codigo Duplicado:\n\n"
        "- Middleware RBAC (requireRole):\n"
        "  Reutilizado en 14 endpoints administrativos y de venta.\n\n"
        "- Middleware Idempotencia (RFC 8785):\n"
        "  Reutilizado en creacion de pedidos, cobros y anulaciones.\n\n"
        "- Motor PDF (pdfGenerator):\n"
        "  Consumido para rotulos de agencia y boletas de venta.\n\n"
        "- Componentes UI PWA:\n"
        "  Botones accesibles, modales y tablas paginadas compartidas en 12 vistas.",
        size=11.5, color=DARK)

    add_notes(s17,
        "NOTAS DEL ORADOR (SLIDE 17 - MANTENIBILIDAD SEMANA 15):\n"
        "En la Semana 15 analizamos la mantenibilidad segun ISO/IEC 25010, evaluando modularidad y reusabilidad. "
        "Evitamos a toda costa el anti-patron del archivo monolitico donde se mezclan rutas, SQL y logica. En LeoFit estructuramos el backend siguiendo Clean Architecture: "
        "las rutas estan en src/routes, los controladores validan con schemas Zod, los servicios encapsulan las reglas comerciales y los repositorios ejecutan SQL parametrizado. "
        "En reusabilidad, demostramos componentes transversales consumidos en multiples puntos sin una sola linea duplicada: "
        "el middleware de roles protege 14 endpoints, el generador de PDF emite tanto rotulos de envio como comprobantes, y el validador de idempotencia asegura consistencia en todas las operaciones transaccionales.")

    # =========================================================================
    # SLIDE 18: MANTENIBILIDAD: MODIFICABILIDAD Y COMPLEJIDAD (SEMANA 15)
    # =========================================================================
    s18 = prs.slides.add_slide(BLANK)
    add_header(s18, "Calidad de Mantenibilidad: Modificabilidad y Complejidad McCabe", "9. CALIDAD DE MANTENIBILIDAD (SEMANA 15)")

    # Columna Izquierda: Modificabilidad y Blast Radius
    box(s18, 0.5, 1.4, 5.8, 5.4, fill=WHITE, line=BLUE)
    txt(s18, 0.8, 1.6, 5.2, 0.35, "Modificabilidad y Radio de Impacto (Blast Radius)", size=15, bold=True, color=BLUE)
    txt(s18, 0.8, 2.05, 5.2, 4.6, 
        "- Definicion ISO/IEC 25010:2023: Eficacia y eficiencia con que el software se modifica sin introducir defectos ni degradar la calidad.\n\n"
        "- Caso Practico Aplicado en LeoFit (CHG-01):\n"
        "  * Requerimiento Comercial: Aplicar 10% de descuento en compras textiles >= 6 unidades.\n"
        "  * Archivo Afectado: Exclusivamente src/services/order.service.ts (calculateOrderTotal).\n"
        "  * Blast Radius Minimo: Solo 2 archivos modificados (servicio y test unitario).\n"
        "  * Impacto en Controladores y Rutas: 0 lineas de cambio en Express.\n"
        "  * Impacto en Base de Datos: 0 alteraciones en esquemas relacionales.\n\n"
        "- Auditoria de Complejidad Ciclomatica (McCabe):\n"
        "  * 100% de los modulos en la zona optima de 1 a 3 (estandar <= 4).\n"
        "  * Modulo order.service.ts: Complejidad promedio de 2.8 en 380 LOC.\n"
        "  * Garantiza bajo costo cognitivo y ausencia de regresiones.",
        size=11, color=DARK)

    # Columna Derecha: Grafico Treemap / Complejidad Ciclomatica
    pic(s18, "fig05_treemap_complejidad_ciclomatica.png", 6.5, 1.4, 6.3, 5.4)

    add_notes(s18,
        "NOTAS DEL ORADOR (SLIDE 18 - MODIFICABILIDAD Y COMPLEJIDAD):\n"
        "En esta diapositiva demostramos la mantenibilidad mediante metricas de complejidad ciclomatica y analisis de radio de impacto. "
        "A la derecha se visualiza la auditoria estatica de McCabe: todos los modulos del backend se situan entre 1 y 3, dentro de la franja verde optima. "
        "Esto se traduce en que realizar un cambio de negocio real, como la regla de descuento por volumen textil CHG-01, solo toco 2 archivos: el servicio de pedidos y su prueba unitaria, con cero impacto en controladores o base de datos.")

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

    # =========================================================================
    # SLIDE 20: BATERÍA DE 194 PRUEBAS AUTOMATIZADAS Y PIRÁMIDE
    # =========================================================================
    s20 = prs.slides.add_slide(BLANK)
    add_header(s20, "Aseguramiento de Calidad: 194 Pruebas Automatizadas y Piramide", "11. TESTING Y CALIDAD (QA)")

    # Columna Izquierda: Metricas y Suites
    box(s20, 0.5, 1.4, 5.8, 1.35, fill=NAVY, line=None)
    txt(s20, 0.7, 1.5, 5.4, 0.45, "194 TESTS APROBADOS (100% OK)", size=20, bold=True, color=WHITE)
    txt(s20, 0.7, 2.05, 5.4, 0.4, "125 BACKEND (JEST) + 69 FRONTEND (VITEST) - CERO FALLOS", size=9.5, bold=True, color=ACCENT)

    box(s20, 0.5, 2.95, 5.8, 3.85, fill=LGRAY, line=GRAY)
    txt(s20, 0.7, 3.1, 5.4, 0.3, "Distribucion de Suites y Cobertura por Capa", size=13, bold=True, color=NAVY)
    txt(s20, 0.7, 3.5, 5.4, 3.2, 
        "- Capa Dominio (98.4% Cobertura): Entidades puras, validacion Zod, reglas de stock y calculo monetario con Decimal.js.\n"
        "- Capa Aplicacion (94.2% Cobertura): Servicios de pedidos, autenticacion JWT, RBAC y logica de negocio.\n"
        "- Capa Infraestructura (86.5% Cobertura): Repositorios SQL, pooling de conexiones y clientes externos.\n"
        "- Capa Frontend PWA (91.5% Cobertura): Componentes React 19, navegacion accesible WCAG y Service Workers offline.\n"
        "- Inversion de Dependencias: Dependencias apuntan estrictamente hacia el dominio (0 violaciones de acoplamiento).",
        size=10.5, color=DARK)

    # Columna Derecha: Grafico de Piramide y Cobertura por Capa
    pic(s20, "fig06_cobertura_por_capa.png", 6.5, 1.4, 6.3, 5.4)

    add_notes(s20,
        "NOTAS DEL ORADOR (SLIDE 20 - TESTING QA):\n"
        "La confiabilidad de LeoFit esta respaldada por 194 pruebas automatizadas con 100% de exito. "
        "A la derecha pueden observar el grafico de cobertura por capas bajo Clean Architecture: la cobertura supera el 98% en el dominio y 94% en aplicacion, "
        "demostrando que el esfuerzo de pruebas se enfoca donde reside el valor comercial. Todas las dependencias apuntan hacia el interior del sistema sin violaciones de acoplamiento.")

    # =========================================================================
    # SLIDE 21: EVALUACIÓN INTEGRAL ISO/IEC 25010:2023 Y CALIDAD EN USO (ISO 9126-4)
    # =========================================================================
    s21 = prs.slides.add_slide(BLANK)
    add_header(s21, "Evaluacion Integral ISO/IEC 25010:2023 y Calidad en Uso (ISO 9126-4)", "11. TESTING Y CALIDAD (QA)")

    box(s21, 0.5, 1.4, 5.8, 5.4, fill=WHITE, line=BLUE)
    txt(s21, 0.8, 1.6, 5.2, 0.35, "Perfil de Calidad Global y Calidad en Uso", size=15, bold=True, color=NAVY)
    txt(s21, 0.8, 2.05, 5.2, 4.6, 
        "- Modelo ISO/IEC 25010:2023 (9 Caracteristicas):\n"
        "  * Adecuacion Funcional: 98.0% | Desempeno (p95=480ms): 94.0%\n"
        "  * Seguridad Informacion: 97.0% | Mantenibilidad (McCabe 1-3): 95.5%\n"
        "  * Confiabilidad: 96.5% | Safety (Cero sobreventas ACID): 91.0%\n"
        "  * Puntaje Sintetico Global: 94.6 / 100 (Nivel Sobresaliente).\n\n"
        "- Calidad en Uso (ISO 9126-4) y Metricas de Clase:\n"
        "  * Efectividad: 100% tareas completas, 0.08 errores/tarea.\n"
        "  * Productividad: 38.2s vs 310s (-87.6%), 1.57 ped/min (8.2x),\n"
        "    costo $0.0056 USD (S/ 0.021)/pedido, 92.4% tiempo productivo.\n"
        "  * Seguridad y Dano Economico: S/ 0.00 soles perdidos en inventario.\n"
        "  * Satisfaccion: SUS 88.5 / 100 (Grado A, Percentil 96%).\n\n"
        "- Accesibilidad WCAG 2.1 AA/AAA: Contrastes de hasta 17.8:1.",
        size=10.0, color=DARK)

    # Columna Derecha: Grafico Radial ISO 25010:2023 + Score Gauge
    pic(s21, "fig01_radar_iso25010_2023.png", 6.5, 1.4, 6.3, 5.4)

    add_notes(s21,
        "NOTAS DEL ORADOR (SLIDE 21 - ISO 25010 Y CALIDAD EN USO ISO 9126-4):\n"
        "Para cerrar el bloque de calidad presentamos la sintesis entre el estandar vigente ISO/IEC 25010:2023 y la calidad en uso de ISO 9126-4. "
        "A la derecha observan el grafico radial con las 9 caracteristicas tecnicas, superando holgadamente el 90% con un puntaje global de 94.6 sobre 100. "
        "En cuanto a calidad en uso segun la norma ISO 9126-4 explicada por el profesor: "
        "en efectividad logramos 100% de tareas completadas; en productividad reducimos el tiempo operativo de 310 segundos a 38.2 segundos, multiplicando la velocidad por 8.2x y elevando el tiempo comercial activo al 92.4%; "
        "en seguridad fisica y operativa prevenimos el riesgo de dano con S/ 0.00 soles de perdida economica gracias a la concurrencia ACID con FOR UPDATE; "
        "y en satisfaccion alcanzamos 88.5 puntos SUS en el percentil 96 con accesibilidad universal WCAG 2.1 AAA.")

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
