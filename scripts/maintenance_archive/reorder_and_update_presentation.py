import zipfile
import os
import xml.etree.ElementTree as ET
import sys
import shutil

sys.stdout.reconfigure(encoding='utf-8')

src_backup = r"C:\Users\Loayza\Downloads\leofit-pedidos-sistema\docs\00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3\GRUP01-Curso_Integrador_II_Software_ORIGINAL_BACKUP.pptx"
temp_out = r"C:\Users\Loayza\Downloads\leofit-pedidos-sistema\docs\00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3\GRUP01-Curso_Integrador_II_Software_REORDERED.pptx"
dest_pptx = r"C:\Users\Loayza\Downloads\leofit-pedidos-sistema\docs\00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3\GRUP01-Curso_Integrador_II_Software.pptx"

# New order of slide indices (1-based from original presentation)
# Strictly aligned to rubric criteria and team assignments:
new_order_indices = [
    # PORTADA Y AGENDA (Lady Loayza)
    1,   # Slide 01: Portada oficial Grupo 01 (Datos completos UTP e Ing. Enrique Lee)
    2,   # Slide 02: Agenda Oficial alineada a la Rúbrica de 16 Puntos
    
    # CRITERIO 1: EVALUACIÓN DE PRUEBAS FUNCIONALES (4 PTS) - Jim Dávila [Slides 03 al 07]
    10,  # Slide 03: 194 Pruebas Automatizadas (100% Pass, Completitud, Corrección, Idoneidad)
    38,  # Slide 04: Plan de Pruebas Automatizadas (Shift-Left: Vitest, Supertest, TypeScript)
    39,  # Slide 05: Diagrama de la Pirámide de Pruebas y Quality Gate Automatizado
    32,  # Slide 06: Plan de Pruebas: 69 Frontend (Vitest) y 125 Backend (Jest/Supertest)
    13,  # Slide 07: Concurrencia Transaccional k6 (0% sobreventas, idoneidad 38.2s < 90s)
    
    # CRITERIO 2: AUTOMATIZACIÓN DE PRUEBAS DE INTEGRACIÓN (4 PTS) - Víctor Cárdenas [Slides 08 al 13]
    11,  # Slide 08: Interoperabilidad: WhatsApp Cloud API, Webhooks Yape/Plin, SUNAT y RENIEC
    9,   # Slide 09: Idempotencia RFC 8785 (JCS) y Protocolo Envelope JSON
    8,   # Slide 10: Control de Acceso Basado en Roles (RBAC) en Runtime
    7,   # Slide 11: Ciberseguridad Defensiva y Mitigación OWASP Top 10
    6,   # Slide 12: PostgreSQL: Trigger Atómico fn_decrement_stock_on_order()
    37,  # Slide 13: Control de Concurrencia y SELECT FOR UPDATE en Repository
    
    # CRITERIO 3: EVALUACIÓN DE LA USABILIDAD DEL SISTEMA (4 PTS) - Harley Roman [Slides 14 al 18]
    12,  # Slide 14: Usabilidad ISO 25010 y SUS Score 88.5 / 100 (Grado A, Excelente, 5 Usuarios)
    20,  # Slide 15: Captura UI: Catálogo Reactivo y Variantes de Producto
    21,  # Slide 16: Captura UI: Prevención de Errores Inline y Modales Descriptivos
    22,  # Slide 17: Captura UI: Checkout Rápido en 3 Pasos y Rótulo QR
    23,  # Slide 18: URL Oficial PWA en Producción (GitHub Pages Edge CDN)
    
    # CRITERIO 4: VALIDACIÓN EN LA PLATAFORMA CLOUD (2 PTS) - Daniel Rojas [Slides 19 al 26]
    14,  # Slide 19: Topología Multi-Cloud (GitHub Pages CDN + Render PaaS + Neon Serverless BD)
    36,  # Slide 20: URL Oficial y Validación en Plataforma Cloud
    40,  # Slide 21: Despliegue Multi-Cloud: Render Web Service + Neon PostgreSQL 16
    41,  # Slide 22: Diagrama de Arquitectura de Despliegue Multi-Cloud
    42,  # Slide 23: Monitoreo, Telemetría y Endpoint /api/health en Producción (HTTP 200)
    33,  # Slide 24: Manual de Despliegue (Pipeline CI/CD en GitHub Actions)
    34,  # Slide 25: Evidencia de Pruebas de Despliegue Automatizado
    35,  # Slide 26: Evidencias de Monitoreo y Administración de Base de Datos en Neon
    
    # CRITERIO 5: SUSTENTACIÓN Y CONCLUSIONES (2 PTS) - Lady Loayza [Slides 27 al 32]
    3,   # Slide 27: Proceso Informal Previo BPMN 2.0 AS-IS (Gamarra)
    4,   # Slide 28: Modelo de Contenedores C4 Nivel 2 y Clean Architecture
    5,   # Slide 29: Arquitectura de Datos: Normalización 3FN / BCNF
    15,  # Slide 30: Diagnóstico Cuantitativo de Brechas Operativas
    17,  # Slide 31: Lean Canvas: Modelo de Negocio LeoFit S.A.C.
    43,  # Slide 32: MUCHAS GRACIAS - Principales Aportes, Limitaciones y Cierre
    
    # ANEXOS TÉCNICOS / RESPALDO ANTE PREGUNTAS DEL JURADO [Slides 33 al 43]
    16,  # Slide 33: Evidencias Espacio de Trabajo
    18,  # Slide 34: Requerimientos Funcionales (Tabla completa RF-01 al RF-10)
    19,  # Slide 35: Requerimientos No Funcionales (Tabla completa RNF)
    24,  # Slide 36: Integración con Base de Datos
    25,  # Slide 37: Diseño físico de base de datos
    26,  # Slide 38: Implementación del Patrón de Acceso a Datos (Neon Serverless)
    27,  # Slide 39: Consistencia entre el modelo de BD y script SQL
    28,  # Slide 40: Medidas de Seguridad para la Aplicación
    29,  # Slide 41: Informe Técnico de Seguridad, Cifrado Bcrypt y AES-256
    30,  # Slide 42: Prueba de seguridad web
    31   # Slide 43: Catálogo de Controles de Seguridad (OWASP Top 10)
]

print(f"Total new order slides: {len(new_order_indices)}")
assert len(new_order_indices) == 43
assert set(new_order_indices) == set(range(1, 44))

# Text replacements mapping - PUNCHY, PRECISE, NO OVERFLOWS
text_replacements = {
    # AGENDA OFICIAL: EXACT FIT FOR CANVA'S 9 ROWS (ELEGANT AND CRISP)
    "ppt/slides/slide2.xml": [
        ("Agenda", "Agenda Oficial"),
        ("Bloque Temático", "Criterio de Evaluación"),
        ("Contenido Técnico Clave", "Artefactos y Responsable"),
        ("Levantamiento APF2", "1. Pruebas Funcionales"),
        ("Subsanación al 100% de observaciones previas de la rúbrica",
         "194 Tests (Vitest + Jest), Cobertura y Métricas · Jim Dávila"),
        ("I. Negocio y Alcance", "2. Pruebas Integración"),
        ("Contexto Gamarra, brechas AS-IS vs TO-BE, Lean Canvas y Requerimientos",
         "WhatsApp API, Webhooks HMAC y Coexistencia · Víctor Cárdenas"),
        ("II. Arquitectura y Datos", "3. Usabilidad ISO 25010"),
        ("C4 Nível 2, Clean Architecture, PostgreSQL 16, ACID y Concorrencia",
         "SUS 88.5/100 (Grado A), WCAG 2.1 AAA y 5 Usuarios · Harley Roman"),
        ("III. Seguridad OWASP", "4. Plataforma Cloud"),
        ("JWT fail-fast, RBAC, Bcrypt salt 10, HMAC SHA-256 y defensa en profundidad",
         "GitHub Pages + Render PaaS + Neon PostgreSQL · Daniel Rojas"),
        ("IV. Calidad y Pruebas", "5. Sustentación Final"),
        ("Estrategia Shift-Left, 101 tests (Jest + Vites), cobertura Istanbul y CI/CD",
         "Aportes al Negocio, BCNF, Arquitectura y Demo · Lady Loayza"),
        ("V. Interoperabilidad", "Seguridad Defensiva"),
        ("WhatsApp Cloud, Webhooks de pago (Yape/Plin), SUNAT/RENIEC y rótulos QR",
         "OWASP Top 10, JWT Fail-Fast, Bcrypt salt 10 y Middleware RBAC"),
        ("VI. Usabilidad ISO 25010", "Concurrencia y ACID"),
        ("4 Pilares, 9 tests automáticos, SUS Score 88.5/100 y Core Web Vitals",
         "Bloqueo SELECT FOR UPDATE, Cero Sobreventas y Pruebas k6"),
        ("VII. Cloud y Producción", "Auditoría de Calidad"),
        ("Topología Cloud V2, K6 (50 VUs), demo en vivo y gobernanza en GitHub",
         "Dashboard ISO 29119-3 / ISO 90003 al 100% en Excel"),
        ("VIII. Cierre y Defensa", "Demostración en Vivo"),
        ("Conclusiones, limitaciones transparentes, roadmap y preguntas del jurado",
         "Frontend PWA + Render Backend + Neon DB en Producción Real"),
    ],
    
    # CRITERIO 1: EVALUACIÓN DE PRUEBAS FUNCIONALES (JIM DÁVILA)
    "ppt/slides/slide10.xml": [
        ("Calidad de Software: 194 Pruebas Automatizadas (100% Pass)",
         "Criterio 1: Evaluación de Pruebas Funcionales (4 pts)"),
        ("Estrategia Shift-Left, Cobertura Istanbul y Pirámide de Pruebas",
         "ISO 25010 · 194 Tests Passing (Vitest + Jest) · Ponente: Jim Dávila"),
    ],
    "ppt/slides/slide32.xml": [
        ("Por parte del frontend, se definen 17 pruebas utilizando Vitest, buscando probar las funcionalidades de renderización, navegación, y integridad de datos.",
         "Frontend: 69 pruebas automatizadas con Vitest y React Testing Library (10 suites), validando renderización, navegación e integridad."),
        ("Por parte del backend, se definen 18 pruebas utilizando API Supertest y Jest, buscando probar servicios (pedidos, stock), autenticación (JTW), y seguridad (SQL, Zod).",
         "Backend: 125 pruebas con Jest y Supertest (17 suites, Total: 194 pruebas, 99.49% éxito), validando transaccionalidad ACID y OWASP."),
    ],
    
    # CRITERIO 2: PRUEBAS DE INTEGRACIÓN (VÍCTOR CÁRDENAS)
    "ppt/slides/slide11.xml": [
        ("Interoperabilidad: Servicios Externos y Gateways",
         "Criterio 2: Pruebas de Integración y Coexistencia (4 pts)"),
        ("SLA, Latencias Contractuales y Pruebas Automatizadas",
         "Interoperabilidad Externa y Coexistencia Docker · Ponente: Víctor Cárdenas"),
    ],
    
    # CRITERIO 3: EVALUACIÓN DE USABILIDAD (HARLEY ROMAN)
    "ppt/slides/slide12.xml": [
        ("Auditoría de Usabilidad y Calidad ISO/IEC 25010",
         "Criterio 3: Evaluación de la Usabilidad del Sistema (4 pts)"),
        ("Estudio Formal SUS (88.5/100), 4 Pilares del Estándar y Core Web Vitals",
         "ISO 25010 · SUS Score 88.5/100 (Grado A) · Ponente: Harley Roman"),
        ("System Usability Scale (SUS) · 10 Usuarios UAT",
         "System Usability Scale (SUS) · 5 Usuarios UAT"),
    ],
    
    # CRITERIO 4: VALIDACIÓN EN PLATAFORMA CLOUD (DANIEL ROJAS)
    "ppt/slides/slide14.xml": [
        ("Topología Cloud Desplegada, Demo en Vivo y Roadmap",
         "Criterio 4: Validación y Verificación en la Nube (2 pts)"),
        ("Infraestructura en Producción, Pipelines CI/CD y Evolución Tecnológica",
         "Topología Multi-Cloud: GitHub Pages + Render + Neon · Ponente: Daniel Rojas"),
        ("PostgreSQL 16 Serverless", "Neon PostgreSQL 16 Serverless"),
    ],
    "ppt/slides/slide33.xml": [
        ("PWA / Frontend → Netlify", "PWA / Frontend → GitHub Pages Edge CDN"),
        ("API /  Backend →  Render", "API / Backend → Render Cloud (Node.js 20) | BD → Neon PostgreSQL 16"),
    ],
    "ppt/slides/slide36.xml": [
        ("PostgreSQL 16 (12 Tablas)", "Neon PostgreSQL 16 Serverless"),
    ],
    "ppt/slides/slide40.xml": [
        ("Clúster PostgreSQL 16 administrado en Render con enlace cifrado SSL (sslmode=require).",
         "Clúster Serverless PostgreSQL 16 alojado en Neon (https://neon.tech) con enlace cifrado SSL y PgBouncer nativo."),
    ],
    
    # CRITERIO 5: SUSTENTACIÓN Y CONCLUSIONES (LADY LOAYZA)
    "ppt/slides/slide3.xml": [
        ("Diagnóstico Cuantitativo: Fricción Operativa y Brechas",
         "Criterio 5: Sustentación Técnica del Sistema v2 (2 pts)"),
        ("Modelado de Procesos BPMN 2.0 y Estudio de Campo UAT en Gamarra",
         "Aportes al Proyecto, Consistencia BCNF y Demo · Ponente: Lady Loayza"),
    ],
    "ppt/slides/slide4.xml": [
        ("Contenedor 3: Base de Datos Relacional (PostgreSQL 16)",
         "Contenedor 3: BD Relacional (PostgreSQL 16 en Neon Serverless)"),
    ],
    "ppt/slides/slide26.xml": [
        ("Conexión establecido con PostgreSQL 16 alojado en Render.",
         "Conexión establecida con clúster Serverless PostgreSQL 16 alojado en Neon (neon.tech) con cifrado SSL."),
    ],
}

# Open source backup zip, modify, and write to temp_out
with zipfile.ZipFile(src_backup, 'r') as zin, zipfile.ZipFile(temp_out, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        
        # 1. Reorder slides in presentation.xml
        if item.filename == "ppt/presentation.xml":
            xml_str = data.decode("utf-8")
            root = ET.fromstring(xml_str)
            ns = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main",
                  "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
            sldIdLst = root.find("p:sldIdLst", ns)
            
            id_map = {}
            for elem in list(sldIdLst):
                sid = int(elem.attrib["id"]) - 255 # original 1-based index
                id_map[sid] = elem
                sldIdLst.remove(elem)
                
            for new_idx in new_order_indices:
                elem = id_map[new_idx]
                sldIdLst.append(elem)
                
            data = ET.tostring(root, encoding="utf-8", xml_declaration=True)
            print("Successfully reordered presentation.xml sldIdLst!")

        # 2. Text replacements in specific slides
        elif item.filename in text_replacements:
            text_str = data.decode("utf-8")
            for old_text, new_text in text_replacements[item.filename]:
                if old_text in text_str:
                    text_str = text_str.replace(old_text, new_text)
                    print(f"Replaced text in {item.filename}: {old_text[:30]}... -> {new_text[:30]}...")
                else:
                    print(f"WARNING: Target text not found in {item.filename}: {old_text[:30]}...")
            data = text_str.encode("utf-8")

        zout.writestr(item, data)

print(f"Wrote updated presentation to {temp_out}")
shutil.copy2(temp_out, dest_pptx)
print(f"Copied to {dest_pptx}")
