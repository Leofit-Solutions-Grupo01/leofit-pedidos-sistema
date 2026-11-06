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

OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "02_PPTX"))
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
    txt(s1, 1.2, 2.9, 11.0, 0.4, "Sustentacion Final de Ingenieria (Semana 18) - Calidad ISO/IEC 25010 y Arquitectura Cloud", size=15, color=LGRAY)
    
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
        "- Despliegue: Render Docker API + GitHub Pages CDN", 
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
    # SLIDE 15: BATERÍA DE 190 PRUEBAS AUTOMATIZADAS
    # =========================================================================
    s15 = prs.slides.add_slide(BLANK)
    add_header(s15, "Aseguramiento de Calidad: 190 Pruebas Automatizadas (100% OK)", "8. TESTING Y CALIDAD (QA)")

    # Metricas grandes
    box(s15, 0.5, 1.5, 3.8, 1.8, fill=NAVY, line=None)
    txt(s15, 0.5, 1.7, 3.8, 0.5, "190", size=36, bold=True, color=WHITE, align="c")
    txt(s15, 0.5, 2.3, 3.8, 0.4, "TOTAL PRUEBAS APROBADAS (0 FALLOS)", size=11, bold=True, color=ACCENT, align="c")

    box(s15, 4.7, 1.5, 3.9, 1.8, fill=BLUE, line=None)
    txt(s15, 4.7, 1.7, 3.9, 0.5, "121", size=36, bold=True, color=WHITE, align="c")
    txt(s15, 4.7, 2.3, 3.9, 0.4, "PRUEBAS BACKEND (JEST + SUPERTEST)", size=11, bold=True, color=LGRAY, align="c")

    box(s15, 9.0, 1.5, 3.8, 1.8, fill=DARK, line=None)
    txt(s15, 9.0, 1.7, 3.8, 0.5, "69", size=36, bold=True, color=WHITE, align="c")
    txt(s15, 9.0, 2.3, 3.8, 0.4, "PRUEBAS FRONTEND (VITEST + RTL)", size=11, bold=True, color=LGRAY, align="c")

    # Detalle de suites
    box(s15, 0.5, 3.6, 12.333, 3.2, fill=LGRAY, line=GRAY)
    txt(s15, 0.8, 3.8, 11.5, 0.4, "Distribucion de Suites de Prueba Automatizadas", size=14, bold=True, color=NAVY)
    txt(s15, 0.8, 4.2, 11.5, 2.4, 
        "- Seguridad y OWASP Top 10 (security.test.ts): Inyeccion SQL, XSS, headers Helmet y validacion Zod.\n"
        "- Autenticacion y Matriz RBAC (auth.test.ts): Control estricto de roles admin y operador (401/403).\n"
        "- Integracion e Interoperabilidad (integration_external.test.ts): Contrato OpenAPI y webhooks HMAC.\n"
        "- Transaccionalidad de Pedidos (orders.test.ts): Bloqueo FOR UPDATE y decremento atomico de stock.\n"
        "- Usabilidad y Accesibilidad (usability_iso25010.test.ts): Navegacion por teclado y renderizado WCAG.\n"
        "- Generacion de Documentos (pdfGenerator.test.ts): Creacion de rotulos de envio y comprobantes PDF.",
        size=12, color=DARK)

    add_notes(s15,
        "NOTAS DEL ORADOR (SLIDE 15 - TESTING QA):\n"
        "La confiabilidad de LeoFit no es declarativa; esta demostrada con 190 pruebas automatizadas con 100% de exito. "
        "En el backend corremos 121 pruebas con Jest que validan seguridad OWASP, inyeccion SQL, tokens manipulados y concurrencia. "
        "En el frontend ejecutamos 69 pruebas con Vitest y Testing Library que certifican el renderizado de formularios, "
        "generacion de PDFs de despacho y guardas de autenticacion en la interfaz.")

    # =========================================================================
    # SLIDE 16: CALIDAD ISO 25010 Y ACCESIBILIDAD
    # =========================================================================
    s16 = prs.slides.add_slide(BLANK)
    add_header(s16, "Evaluacion de Calidad ISO/IEC 25010 y Usabilidad WCAG", "8. TESTING Y CALIDAD (QA)")

    box(s16, 0.5, 1.4, 5.9, 5.4, fill=WHITE, line=BLUE)
    txt(s16, 0.8, 1.6, 5.3, 0.4, "Metricas del Estandar ISO/IEC 25010", size=16, bold=True, color=BLUE)
    txt(s16, 0.8, 2.1, 5.3, 4.4, 
        "- Adecuacion Funcional: 100.0% de completitud (10 de 10 requerimientos funcionales verificados).\n"
        "- Eficiencia de Desempeno: Tiempo de registro de pedido en 38.2 segundos (meta institucional < 90s).\n"
        "- Compatibilidad y Coexistencia: Benchmark experimental Docker con degradacion P95 < 25% y 0% errores.\n"
        "- Fiabilidad: Mecanismos de reintento en servicios externos y recuperacion automatica ante fallos.\n"
        "- Seguridad: Cero contrasenas en plano (Bcrypt 10 rounds) y sanitizacion estricta de datos PII.",
        size=13, color=DARK)

    box(s16, 6.9, 1.4, 5.9, 5.4, fill=LGRAY, line=GRAY)
    txt(s16, 7.2, 1.6, 5.3, 0.4, "Estudio de Usabilidad y Accesibilidad WCAG", size=16, bold=True, color=NAVY)
    txt(s16, 7.2, 2.1, 5.3, 4.4, 
        "- System Usability Scale (SUS): Puntaje obtenido de 88.5 / 100 (Grado A - Excelente, Percentil 96%).\n"
        "- Estudio Empirico: Evaluacion con 5 participantes reales en el stand comercial de LeoFit.\n"
        "- Accesibilidad WCAG 2.1 AA/AAA: Contrastes de color certificados desde 5.42:1 hasta 17.8:1.\n"
        "- Navegacion Accesible: 100% de acciones operables exclusivamente mediante teclado (Tab/Enter).\n"
        "- Diseno Responsivo: Adaptabilidad fluida probada en dispositivos moviles, tablets y pantallas desktop.",
        size=13, color=DARK)

    add_notes(s16,
        "NOTAS DEL ORADOR (SLIDE 16 - ISO 25010):\n"
        "Evaluamos el software bajo la norma internacional ISO/IEC 25010. "
        "En usabilidad aplicamos la metodologia estandar System Usability Scale (SUS) con usuarios reales, "
        "logrando un puntaje de 88.5 sobre 100, ubicando a LeoFit en el percentil 96 de excelencia. "
        "Cumplimos ademas con el estandar de accesibilidad web WCAG 2.1, con contrastes de hasta 17.8 a 1 "
        "que permiten utilizar el sistema en ambientes con luz solar directa como el emporio de Gamarra.")

    # =========================================================================
    # SLIDE 17: DEMOSTRACIÓN EN LA NUBE
    # =========================================================================
    s17 = prs.slides.add_slide(BLANK)
    add_header(s17, "Validacion y Despliegue en Vivo en la Nube (Cloud Staging)", "9. DESPLIEGUE Y OPERACION")

    # 3 Cajas de Despliegue
    box(s17, 0.5, 1.5, 3.8, 5.2, fill=LGRAY, line=GRAY)
    txt(s17, 0.8, 1.7, 3.2, 0.3, "FRONTEND PWA", size=14, bold=True, color=NAVY)
    txt(s17, 0.8, 2.1, 3.2, 4.3, 
        "- URL Publica: Enlace en GitHub Pages con certificado SSL global.\n"
        "- Edge CDN: Distribucion geografica rapida de activos.\n"
        "- Soporte PWA: Instalable en dispositivos Android, iOS y Windows.\n"
        "- Cache Estrategico: Service Workers almacenan catalogo base para consulta sin conexion.", size=12, color=DARK)

    box(s17, 4.7, 1.5, 3.9, 5.2, fill=LBLUE, line=BLUE)
    txt(s17, 5.0, 1.7, 3.3, 0.3, "BACKEND API", size=14, bold=True, color=BLUE)
    txt(s17, 5.0, 2.1, 3.3, 4.3, 
        "- Hosting: Render Cloud Platform con Dockerfile de produccion.\n"
        "- Endpoint Health: /api/health retorna HTTP 200 con estado de BD.\n"
        "- Documentacion Viva: OpenAPI y Swagger integrados en /api/docs.\n"
        "- Variables Cifradas: Inyeccion segura sin filtracion de secretos en Git.", size=12, color=DARK)

    box(s17, 9.0, 1.5, 3.8, 5.2, fill=LGRAY, line=GRAY)
    txt(s17, 9.3, 1.7, 3.2, 0.3, "BASE DE DATOS", size=14, bold=True, color=ACCENT)
    txt(s17, 9.3, 2.1, 3.2, 4.3, 
        "- Motor: Neon Serverless PostgreSQL 16.\n"
        "- SSL Enforcement: Conexiones forzadas con cifrado TLS en transito.\n"
        "- Timezone Configurado: Sesiones fijadas en America/Lima.\n"
        "- Backups Continuos: Point-in-Time Restore activo para recuperacion ante incidentes.", size=12, color=DARK)

    add_notes(s17,
        "NOTAS DEL ORADOR (SLIDE 17 - CLOUD EN VIVO):\n"
        "El sistema no es una maqueta local; esta desplegado y operativo en la nube. "
        "El frontend se sirve a traves de la CDN de GitHub Pages con soporte PWA instalable en celulares. "
        "La API REST corre en un contenedor Docker sobre Render con un health check activo en /api/health, "
        "y la base de datos PostgreSQL 16 en Neon opera con conexiones SSL forzadas y respaldos continuos.")

    # =========================================================================
    # SLIDE 18: MATRIZ DE TRAZABILIDAD ANTE EL JURADO
    # =========================================================================
    s18 = prs.slides.add_slide(BLANK)
    add_header(s18, "Matriz de Trazabilidad: Respuestas a las 5 Preguntas del Jurado", "10. DEFENSA ANTE EL JURADO")

    box(s18, 0.5, 1.4, 12.333, 5.4, fill=WHITE, line=GRAY)
    txt(s18, 0.8, 1.6, 11.5, 0.4, "Trazabilidad Directa entre Preguntas, Anexos y Codigo Fuente", size=15, bold=True, color=NAVY)

    txt(s18, 0.8, 2.2, 11.5, 4.3,
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

    add_notes(s18,
        "NOTAS DEL ORADOR (SLIDE 18 - TRAZABILIDAD JURADO):\n"
        "Esta lamina resume la preparacion del equipo ante la evaluacion del tribunal. "
        "Las cinco preguntas tipicas sobre eleccion de infraestructura, maquetacion AWS, SUNAT, pasarelas de pago y arquitectura de software "
        "estan formalmente documentadas en seis anexos tecnicos y cuentan con evidencia verificable linea a linea en el repositorio GitHub. "
        "No hay respuestas ambiguas: todo lo afirmado se sustenta en el codigo fuente.")

    # =========================================================================
    # SLIDE 19: CONCLUSIONES Y APORTES DE INGENIERÍA
    # =========================================================================
    s19 = prs.slides.add_slide(BLANK)
    add_header(s19, "Conclusiones del Proyecto y Aportes a la Empresa LeoFit", "11. CONCLUSIONES Y APORTES")

    box(s19, 0.5, 1.4, 5.9, 5.4, fill=LBLUE, line=BLUE)
    txt(s19, 0.8, 1.6, 5.3, 0.4, "Impacto Comercial y Operativo en LeoFit", size=16, bold=True, color=BLUE)
    txt(s19, 0.8, 2.1, 5.3, 4.4, 
        "- Eliminacion Total de Sobreventa: Bloqueo pesado en base de datos garantiza stock 100% certero.\n"
        "- Reduccion de Tiempo de Registro: De mas de 5 minutos por llamada/WhatsApp a 38.2 segundos en la PWA.\n"
        "- Cero Errores en Despacho: Automatizacion de guias locales y rotulos oficiales de agencia de transporte.\n"
        "- Facturacion Inmediata: Emision de boletas en menos de 3 segundos integrada al proceso de cobro.\n"
        "- Autonomia Operativa: Personal del stand capacitado y operando fluidamente en moviles.",
        size=13, color=DARK)

    box(s19, 6.9, 1.4, 5.9, 5.4, fill=LGRAY, line=GRAY)
    txt(s19, 7.2, 1.6, 5.3, 0.4, "Aportes Formativos de Ingenieria de Software", size=16, bold=True, color=NAVY)
    txt(s19, 7.2, 2.1, 5.3, 4.4, 
        "- Aplicacion Rigurosa de Estandares: Clean Architecture, ISO/IEC 25010, C4 Model y MADR para ADRs.\n"
        "- Cultura DevSecOps: 190 pruebas automatizadas en CI/CD, sanitizacion PII y escaneo de vulnerabilidades.\n"
        "- Enfoque Financiero Real: Demostracion de eficiencia de costos antes de sobre-arquitecturar en la nube.\n"
        "- Documentacion Defendible: Manuales tecnicos, diagramas compilados y matrices de trazabilidad auditables.",
        size=13, color=DARK)

    add_notes(s19,
        "NOTAS DEL ORADOR (SLIDE 19 - CONCLUSIONES):\n"
        "Como conclusiones finales, el proyecto LeoFit Solutions demostro viabilidad tecnica y valor comercial tangible. "
        "Para la empresa, redujo el tiempo de procesamiento de pedidos en un 87% y elimino las discrepancias de inventario. "
        "Para nuestro equipo de ingenieria, el proyecto represento la integracion integral de todas las competencias del curso: "
        "desde el modelado relacional BCNF hasta la seguridad criptografica, el testing automatizado y la gestion de infraestructura cloud.")

    # =========================================================================
    # SLIDE 20: CIERRE Y RONDA DE PREGUNTAS
    # =========================================================================
    s20 = prs.slides.add_slide(BLANK)
    box(s20, 0, 0, 13.333, 7.5, fill=NAVY, line=None, shape=MSO_SHAPE.RECTANGLE)
    box(s20, 0.8, 0.8, 11.733, 5.9, fill=NAVY, line=BLUE, lw=2.0)
    
    txt(s20, 1.2, 1.6, 11.0, 0.4, "PROYECTO FINAL COMPLETADO SATISFACTORIAMENTE", size=13, bold=True, color=ACCENT, align="c")
    txt(s20, 1.2, 2.1, 11.0, 0.8, "Muchas Gracias por su Atencion", size=32, bold=True, color=WHITE, align="c")
    txt(s20, 1.2, 2.9, 11.0, 0.4, "LeoFit Solutions - Grupo 01 | Seccion 35374 (Ciclo 2026-I)", size=16, color=LGRAY, align="c")
    
    box(s20, 2.0, 3.8, 9.333, 2.2, fill=DARK, line=GRAY, radius=0.03)
    txt(s20, 2.2, 4.0, 8.933, 1.8, 
        "PANEL DE PREGUNTAS Y DEFENSA TECNICA ABIERTO:\n\n"
        "- Repositorio Oficial: github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema\n"
        "- Documentacion de Anexos: docs/05_ANEXOS_TECNICOS_PROYECTO_FINAL/\n"
        "- Sistema en Vivo: leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/",
        size=13, color=WHITE, align="c")

    add_notes(s20,
        "NOTAS DEL ORADOR (SLIDE 20 - CIERRE):\n"
        "Con esto concluimos la exposicion formal de la arquitectura y resultados de LeoFit Solutions. "
        "Agradecemos profundamente al docente asesor Ing. Enrique Lee Huamani por el acompanamiento y exigencia academica a lo largo del ciclo. "
        "Quedamos a disposicion del jurado evaluador para absolver cualquier pregunta tecnica sobre el codigo, los diagramas, "
        "la base de datos o las decisiones de arquitectura presentadas. Muchas gracias.")

    prs.save(OUT_PPTX)
    size_kb = os.path.getsize(OUT_PPTX) / 1024.0
    print(f"[OK] Presentacion PPTX generada con exito:")
    print(f"     Ruta: {OUT_PPTX}")
    print(f"     Diapositivas: {len(prs.slides)} slides (Requisito >= 18 slides)")
    print(f"     Tamano: {size_kb:.1f} KB")
    return OUT_PPTX, len(prs.slides), size_kb

if __name__ == "__main__":
    create_deck()
