# Entregable Oficial Final (APF3) — Sistema de Gestión de Pedidos y Control de Inventario Multicanal LeoFit

> [!IMPORTANT]
> **PAQUETE OFICIAL DE SUSTENTACIÓN ACADÉMICA Y EJECUTIVA**
> Esta carpeta concentra los documentos maestros definitivos del **Avance de Proyecto Final 3 (APF3)** destinados a la evaluación del Docente Asesor de la **Universidad Tecnológica del Perú (UTP)** (*Curso Integrador II: Software — 100000S12F*) y a la **Alta Dirección de LeoFit Confecciones y Diseños Deportivos S.A.C.** (RUC `206089*****`).
> Todos los documentos se encuentran **100% extendidos, sin omisiones ni suposiciones**, con **27 diagramas y gráficos de alta resolución (220 DPI, accesibilidad universal WCAG 2.1 AA/AAA)** y **32 tablas técnicas y listados verificados**.

---

## 1. Inventario de Archivos del Paquete APF3

| Archivo / Recurso | Formato | Tamaño / Extensión | Propósito y Audiencia |
| :--- | :---: | :---: | :--- |
| [**`INFORME_FINAL_APF3_LEOFIT.docx`**](./INFORME_FINAL_APF3_LEOFIT.docx) | Microsoft Word (`.docx`) | ~6.6 MB (19 Capítulos + 8 Anexos) | **Libro Técnico Maestro Editable:** Incluye Portada oficial UTP, Índices dinámicos (TOC, Índice de Figuras e Índice de Tablas), 27 figuras a color y 32 tablas corporativas. |
| [**`INFORME_FINAL_APF3_LEOFIT.pdf`**](./INFORME_FINAL_APF3_LEOFIT.pdf) | Documento Portátil (`.pdf`) | Edición Oficial Paginada | **Versión Oficial Lista para Impresión y Entrega en Canvas UTP / Directorio:** Exportada directamente desde Microsoft Word con numeración romana en preliminares y arábiga en el cuerpo. |
| [**`INFORME_FINAL_APF3_LEOFIT.md`**](./INFORME_FINAL_APF3_LEOFIT.md) | Markdown Extendido (`.md`) | +1,150 líneas (Texto Íntegro) | **Edición Extendida de Lectura Directa en GitHub:** Contiene el texto completo de los 19 capítulos y 8 anexos, las 27 figuras embebidas y las 32 tablas sin resumir. |
| [**`presentacion_sustentacion/APF3_LEOFIT_Presentacion.html`**](./presentacion_sustentacion/APF3_LEOFIT_Presentacion.html) | Presentación Web Interactiva (`.html`) | 24 Diapositivas Full-HD | **Deck Ejecutivo de Sustentación (Reveal.js / HTML5):** Presentación interactiva para defensa ante el jurado y gerencia. |
| [**`presentacion_sustentacion/APF3_LEOFIT_Presentacion.md`**](./presentacion_sustentacion/APF3_LEOFIT_Presentacion.md) | Guion de Diapositivas (`.md`) | 24 Diapositivas + Notas | **Estructura y Notas del Orador:** Fuente Markdown de las 24 láminas con guion técnico para los 5 integrantes. |
| [**`presentacion_sustentacion/assets/`**](./presentacion_sustentacion/assets/) | Repositorio Gráfico (`.png`) | 22 Activos Visuales (220 DPI) | Diagramas de arquitectura, secuencia, máquina de estados, cobertura, CI/CD y capturas de interfaz en producción. |

---

## 2. Resumen Ejecutivo de Indicadores Clave (KPIs Auditados)

| Dimensión de Ingeniería y Negocio | Línea Base Inicial (AS-IS) | Resultado Alcanzado (TO-BE — APF3) | Evidencia Documental en el Informe |
| :--- | :---: | :---: | :--- |
| **Tiempo Promedio de Registro de Pedido** | 45 a 120 minutos (WhatsApp manual) | **38.2 segundos** (-99.1% de reducción) | Capítulo 2 (§2.2–2.3) y Capítulo 13 (§13.3) |
| **Tasa de Errores en Despacho y Rótulos** | 14.2% (transcripción en libreta física) | **0.4%** (emisión automática PDF `jsPDF`) | Capítulo 2 (§2.5) y Capítulo 9 (§9.3) |
| **Sobreventas por Quiebre de Stock** | Frecuentes (22% de fuga comercial) | **0.0%** (`SELECT ... FOR UPDATE` + Trigger ACID) | Capítulo 7 (§7.3–7.4) y Figura 12 |
| **Pruebas Automatizadas Aprobadas** | 0 pruebas automatizadas | **194 aprobadas (125 Backend + 69 Frontend)** | Capítulo 11 (Tablas 18 y 19, Figuras 17 y 18) |
| **Cobertura de Código en Lógica de Negocio** | Sin medición | **76.16% en líneas** (100% en rutas, Zod y JWT) | Capítulo 11 (§11.4) y Figura 19 |
| **Coexistencia y Rendimiento (ISO/IEC 25010)** | Sin aislamiento | **4.42 ms lectura / 3.44 ms escritura / 0% error** | Capítulo 12 (§12.4, Tabla 20, Figuras 20–22) |
| **Usabilidad Certificada (Escala SUS)** | Proceso fragmentado | **88.5 / 100 (Grado A+ Excelente)** | Capítulo 13 (§13.3) y Anexo G |
| **Recuperación ante Desastres (DRP)** | Sin respaldos formales | **RTO = 3.2 segundos / RPO = 0 transacciones** | Capítulo 16 (§16.3, Tabla 22 y Figura 25) |
| **Saneamiento de Deuda Técnica** | 10 pasivos técnicos identificados | **100% Resuelta (0 deuda pendiente en Sprint 4)** | Capítulo 18 (§18.2, Tabla 24 y Figura 27) |
| **Vulnerabilidades de Seguridad (SAST)** | Cuadernos expuestos | **0 vulnerabilidades (`npm audit` + HMAC + RBAC)** | Capítulo 10 y Anexo D |

---

## 3. Estructura Capitular Completa del Informe Final APF3

### Preliminares
- Portada Oficial UTP, Control de Versiones (v1.0 a v3.2), Ficha Técnica del Proyecto, Dedicatoria y Agradecimientos, Resumen Ejecutivo, Abstract, Índice General, Índice de Figuras (27 Figuras), Índice de Tablas (32 Tablas) y Lista de Acrónimos.

### Parte I: Fundamentos y Contextualización Empresarial
- **Capítulo 1:** Introducción, Realidad Problemática en el Emporio de Gamarra, Justificación Cuádruple, Objetivos SMART (`OE-1` a `OE-5`) y Alcance.
- **Capítulo 2:** Diagnóstico Organizacional, Flujo BPMN AS-IS (*Figura 1*), Flujo BPMN TO-BE (*Figura 2*), Lean Canvas (*Figura 3*) y Análisis GAP.
- **Capítulo 3:** Gestión Estratégica y Metodológica (Project Charter, Cronograma de 16 Semanas, Matriz RACI, Tablero Kanban con límites WIP [*Figura 4*] e Historias de Usuario BDD en Gherkin).

### Parte II: Ingeniería de Requisitos y Diseño de Experiencia de Usuario
- **Capítulo 4:** Catálogo de Requisitos Funcionales (`RF-01` a `RF-10`), Requisitos No Funcionales ISO/IEC 25010 (`RNF-01` a `RNF-10`), Matriz de Trazabilidad (RTM) y Reglas de Negocio (`RN-01` a `RN-08`).
- **Capítulo 5:** Diseño UX/UI Mobile-First, User Flow (*Figura 5*), Wireframes (*Figura 6*), Evaluación de las 10 Heurísticas de Jakob Nielsen, Interfaz en Producción (*Figuras 7 y 8*) y Accesibilidad Universal WCAG 2.1 AA/AAA.

### Parte III: Arquitectura del Sistema y Diseño Técnico
- **Capítulo 6:** Clean Architecture en 3 Capas (*Figura 9*), Patrón `RepositoryFactory` (*Figura 10*) y Protocolo de Comunicación Envelope JSON.
- **Capítulo 7:** Modelado Relacional en PostgreSQL 16 (3FN/BCNF, 14 Tablas, *Figura 11*), Trigger PL/pgSQL, Control de Concurrencia Pesimista (*Figura 12*) y Máquina de Estados (*Figura 13*).
- **Capítulo 8:** Diseño de la API Backend v2.0.0 (*Figura 14*), Catálogo Exhaustivo de los **27 Endpoints RESTful**, Idempotencia RFC 8785 (JCS) y Pipeline de Seguridad.
- **Capítulo 9:** Implementación Frontend PWA en React 19, `AppContext` con Caché Inteligente, Motor PDF `jsPDF` y Pantallas Operativas (*Figuras 15 y 16*).
- **Capítulo 10:** Seguridad Integral, Matriz RBAC (`ADMIN` / `OPERATOR`), Derivación `bcryptjs`, Mitigación de Timing Attacks, Rotación de Refresh Tokens y Firmas `HMAC-SHA256`.

### Parte IV: Verificación, Validación y Aseguramiento de la Calidad
- **Capítulo 11:** Pirámide de Pruebas (*Figura 17*), Desglose de las **17 Suites Backend (125 aprobadas)** y **10 Suites Frontend (69 aprobadas)** (*Figura 18*) y Cobertura de Código (*Figura 19*).
- **Capítulo 12:** Interoperabilidad Externa (WhatsApp, Yape/Plin, RENIEC/SUNAT) y Evaluación Experimental de Coexistencia ISO/IEC 25010 (*Figuras 20, 21 y 22*).
- **Capítulo 13:** Evaluación de Usabilidad ISO/IEC 25010 y Estudio de Campo System Usability Scale (**SUS = 88.5 / 100**).
- **Capítulo 14:** Desempeño, Core Web Vitals (`LCP = 1.4 s`, `INP = 45 ms`, `CLS = 0.01`) y Optimización WPO.

### Parte V: Operaciones, Despliegue Cloud y Gobernanza
- **Capítulo 15:** Topología de Despliegue Multi-Cloud en GitHub Pages CDN + Render Cloud (*Figura 23*) y Pipelines CI/CD en GitHub Actions (*Figura 24*).
- **Capítulo 16:** Observabilidad en `/api/health`, Acuerdos SLA/SLO y Simulacro Empírico de Recuperación ante Desastres (**DRP con RTO = 3.2 s y RPO = 0**, *Figura 25*).
- **Capítulo 17:** Matriz de Gestión de Riesgos 5x5 (*Figura 26*) y Planes de Tratamiento (`R1` a `R8`).

### Parte VI: Evolución, Conclusiones y Trabajo Futuro
- **Capítulo 18:** Trayectoria Evolutiva (APF1 -> APF2 -> APF3) y Saneamiento del **100% de la Deuda Técnica (`DT-01` a `DT-10`)** (*Figura 27*).
- **Capítulo 19:** Conclusiones Generales de Ingeniería, Reconocimiento Transparente de Limitaciones Técnicas y Roadmap hacia la Versión 4.0.

### Anexos Técnicos y Referencias
- **Glosario Técnico** y **Anexos A al H** (DDL SQL, Middlewares, Bitácora de 194 Pruebas, Auditoría SAST, Contratos Zod, Payload Webhook, Instrumento SUS, Trazabilidad de Ramas Git) y **Referencias Bibliográficas APA 7ma Edición**.
