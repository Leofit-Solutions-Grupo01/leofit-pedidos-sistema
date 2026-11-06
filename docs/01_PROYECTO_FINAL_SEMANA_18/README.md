# Entrega Oficial: Proyecto Final de Grado (Semana 18)
## LeoFit Solutions — Sistema de Gestión de Pedidos y Despacho Multicanal
### Curso Integrador II: Software (100000S12F) — Ciclo 2026-I — UTP
**Docente Asesor:** **Ing. Enrique Lee Huamani Uriarte** | **Sección:** 35374 | **Grupo:** 01  
**Integrantes:** Lady Loayza, Víctor Cárdenas, Harley Roman, Jim Dávila, Daniel Rojas.

---

## 1. Presentación y Propósito del Módulo

Esta carpeta centraliza el **Paquete Definitivo de Sustentación del Proyecto Final (Semana 18)** del sistema LeoFit. 

El contenido ha sido estructurado bajo estándares internacionales de ingeniería de software (Clean Architecture, C4 Model, arc42, MADR e ISO/IEC 25010) para permitir la evaluación inmediata y transparente por parte del docente asesor y el jurado calificador de la Universidad Tecnológica del Perú.

---

## 2. Índice del Directorio de Entrega

```text
docs/01_PROYECTO_FINAL_SEMANA_18/
│
├── README.md                                        # Este documento (Guía de evaluación y alcance)
├── 00_HOJA_DE_ENTREGA_Y_ENLACES_PROYECTO_FINAL.md   # Ficha técnica oficial con URLs cloud y credenciales
│
├── 01_ANEXOS_TECNICOS/                              # Los 6 Anexos Técnicos de Sustentación de Arquitectura
│   ├── README.md                                    # Índice maestro de anexos y matriz de trazabilidad
│   ├── 01_ADR-001_ELECCION_RENDER_NEON_VS_AWS.md    # ADR-001: Justificación técnica y económica Render+Neon vs AWS
│   ├── 02_ADR-002_ARQUITECTURA_OBJETIVO_AWS_Y_COMPLEMENTOS.md # ADR-002: Maquetación 100% AWS Well-Architected
│   ├── 03_CUMPLIMIENTO_SUNAT_CPE.md                 # Análisis normativo SUNAT UBL 2.1, INDECOPI y OSE
│   ├── 04_INTEGRACION_PAGOS_SANDBOX_VS_PRODUCCION.md# Pasarela Culqi, PCI-DSS SAQ A y webhooks HMAC
│   ├── 05_ARQUITECTURA_REPOSITORIO_Y_ESTANDARES.md  # C4 Model real, Clean Architecture y onboarding < 1 día
│   └── 06_MATRIZ_TRAZABILIDAD_JURADO.md             # Matriz de trazabilidad a líneas de código fuente (ruta:línea)
│
├── 02_ENTREGABLES_UTP/                              # Paquete compilado a Microsoft Office oficial
│   ├── 01_DOCX/                                     # 9 Documentos Word (.docx) con diagramas compilados
│   ├── 02_PPTX/                                     # Presentación oficial (.pptx) de 20 láminas con notas completas
│   ├── 03_XLSX/                                     # Libro de auditoría y trazabilidad (.xlsx) en 4 pestañas
│   ├── scripts/                                     # Cadena de exportación automática (build_all.ps1)
│   └── build_all.ps1                                # Invocador maestro de construcción Office
│
└── 03_AUDITORIA_READONLY/                           # Auditoría técnica e inventario del código fuente
    └── 00_INVENTARIO_REAL.md                        # Inspección línea por línea de APIs, BD y pasarelas
```

---

## 3. Alcance del Proyecto Evaluado (Release v2.0.0)

### 3.1. Qué se Evalúa y Está Implementado en el Sistema:
1. **Gestión Omnicanal de Pedidos:** Registro validado en menos de 40 segundos para canales WhatsApp, llamada y venta presencial.
2. **Control Transaccional de Existencias:** Decremento atómico de prendas mediante bloqueo pesimista (`SELECT FOR UPDATE`), eliminando sobreventa.
3. **Motor de Despacho Dual:** Módulo diferenciado para reparto local en Lima (hoja de ruta para motorizado) y encomienda provincial (agencias Shalom, Olva, Marvisur con DNI).
4. **Cumplimiento Tributario SUNAT (CPE):** Integración con OSE homologado (Nubefact) para emisión de Boletas y Facturas bajo estándar UBL 2.1, desglose exacto de IGV (18%) y generación de PDF con código Hash y QR.
5. **Pasarela de Pagos Digitales:** Procesamiento de tarjetas con SDK Culqi JS en el cliente (aislamiento de datos sensibles bajo PCI-DSS SAQ A) y confirmación asíncrona mediante webhooks firmados con HMAC-SHA256 (`crypto.timingSafeEqual`).
6. **Resolución de Zona Horaria Oficial:** Pool de base de datos fijado forzosamente en `America/Lima` (UTC-5), garantizando concordancia contable.
7. **Batería de Pruebas Automatizadas:** 190 pruebas automáticas aprobadas (121 backend Jest + 69 frontend Vitest) con 0 fallos.
8. **Despliegue Multi-Capa en la Nube:** Frontend desplegado en GitHub Pages Edge CDN y Backend API en Render Cloud Platform conectado a PostgreSQL 16 serverless en Neon.

### 3.2. Qué Está Fuera del Alcance (Exclusiones Justificadas):
- **Emisión de Guías de Remisión Electrónicas (GRE Remitente):** El sistema emite los rótulos físicos de embalaje y despacho, pero no emite el documento fiscal GRE de SUNAT (planificado para roadmap posterior).
- **Certificación PCI-DSS Nivel 1 en Servidores Propios:** LeoFit no almacena números de tarjeta (PAN) ni CVV en su base de datos; la tokenización se delega en la pasarela certificada Culqi bajo el cuestionario SAQ A.
- **Débito Bancario Real en Cuentas Comerciales:** La pasarela opera en modo Sandbox académico. La activación a dinero real requiere el trámite bancario KYC de la razón social de LeoFit.
- **Infraestructura Multi-Region Distribuida:** Para la etapa de validación y sustentación se utiliza la región US-East con CDN Anycast perimetral; no se justifica el costo de redundancia transcontinental en etapa MVP.

---

## 4. Matriz de Preguntas de Sustentación del Jurado

| # | Pregunta Clave del Jurado | Anexo Técnico de Sustentación | Evidencia Verificable en Código |
| :-: | :--- | :--- | :--- |
| **1** | ¿Por qué Render + Neon y no AWS desde el inicio? | [**`01_ADR-001`**](./01_ANEXOS_TECNICOS/01_ADR-001_ELECCION_RENDER_NEON_VS_AWS.md) | `render.yaml:1-70` · `database.ts:16-55` |
| **2** | ¿Cómo sería la maquetación en una arquitectura 100% AWS y qué no reinventar? | [**`02_ADR-002`**](./01_ANEXOS_TECNICOS/02_ADR-002_ARQUITECTURA_OBJETIVO_AWS_Y_COMPLEMENTOS.md) | `culqi.ts:57` · `nubefact.service.ts:1-295` |
| **3** | ¿Cómo cumple el sistema la normativa SUNAT de facturación electrónica? | [**`03_CUMPLIMIENTO_SUNAT`**](./01_ANEXOS_TECNICOS/03_CUMPLIMIENTO_SUNAT_CPE.md) | `nubefact.service.ts:171` · `008_invoices.ts:1-75` |
| **4** | ¿Los pagos son reales o simulados, cuáles son sus limitantes y cómo se pasa a producción? | [**`04_INTEGRACION_PAGOS`**](./01_ANEXOS_TECNICOS/04_INTEGRACION_PAGOS_SANDBOX_VS_PRODUCCION.md) | `culqi.ts:85` · `paymentWebhook.controller.ts:61-114` |
| **5** | ¿La arquitectura del repositorio es correcta, comprensible y bajo qué estándares? | [**`05_ARQUITECTURA_REPO`**](./01_ANEXOS_TECNICOS/05_ARQUITECTURA_REPOSITORIO_Y_ESTANDARES.md) | `backend/src/` · 190 tests en `tests/` |

---

## 5. Acceso Rápido a los Entregables de Oficina

Para la revisión directa en Microsoft Office, la carpeta [**`02_ENTREGABLES_UTP/`**](./02_ENTREGABLES_UTP/) contiene:
- [**`01_DOCX/`**](./02_ENTREGABLES_UTP/01_DOCX/): 9 documentos Word con diagramas incrustados y formato APA/Corporativo.
- [**`02_PPTX/`**](./02_ENTREGABLES_UTP/02_PPTX/): Presentación oficial de sustentación de 20 diapositivas widescreen con notas del orador integradas.
- [**`03_XLSX/`**](./02_ENTREGABLES_UTP/03_XLSX/): Plan de auditoría y matriz de trazabilidad en Excel con 4 pestañas de datos.
