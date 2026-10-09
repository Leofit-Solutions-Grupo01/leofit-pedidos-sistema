# PLAN DE PRESENTACIONES ACADÉMICAS - PROYECTO LEOFIT PWA
**Curso:** Curso Integrador II: Software (100000S12F) - UTP
**Equipo:** Grupo 01 (Lady, Víctor, Harley, Jim, Daniel)
**Stack Tecnológico:** React 19 + TypeScript + Node.js + Express + PostgreSQL (GitHub Pages / Render)

> **Instrucción para el LLM (Claude/GPT):** Utiliza la siguiente estructura y datos de contexto para generar el contenido detallado de los slides de presentación. Tu objetivo es redactar los *speaker notes* (lo que el presentador dirá) y el texto exacto que irá en cada diapositiva, basándote en esta planificación instruccional.

---

## 1. APF1: PROPUESTA, REQUERIMIENTOS Y ARQUITECTURA INICIAL
**Objetivo:** Demostrar entendimiento del negocio, alcance funcional y cimientos arquitectónicos.
**Tiempo Estimado:** 15 minutos.

| # Slide | Título | Tipo | Puntos clave a cubrir | Evidencia que la respalda |
| :---: | :--- | :---: | :--- | :--- |
| 1 | Portada LeoFit | Portada | • Nombre del proyecto<br>• Identidad Grupo 01<br>• Título del curso | Logotipo LeoFit |
| 2 | El Problema Operativo | Contenido | • Cuadernos manuales<br>• Pérdida de pedidos<br>• Descuadre de inventario | Flujograma AS-IS (`03_Acta_Reunion.md`) |
| 3 | Alcance y Solución (PWA) | Contenido | • Definición del TO-BE<br>• Beneficios PWA (Mobile-first)<br>• Principales RFs (Carrito, Inventario) | Lean Canvas / Matriz de Requerimientos |
| 4 | Requisitos No Funcionales | Métrica | • ISO 25010 (Usabilidad, Rendimiento)<br>• SLA de disponibilidad<br>• Trazabilidad y Seguridad | Tabla RNF (`02_Requerimientos.md`) |
| 5 | Arquitectura y Stack (C4) | Contenido | • React 19 + TypeScript<br>• Node.js + Express<br>• PostgreSQL Relacional | Diagrama Nivel 1 y 2 (`07_Arquitectura_Sistema.md`) |
| 6 | Mockups Alta Fidelidad | Contenido | • Interfaz UI/UX propuesta<br>• Modo Accesibilidad A11y | Capturas Figma / Wireframes |
| 7 | Cierre y Próximos Pasos | Cierre | • Hitos logrados<br>• Objetivos para el APF2 | Diagrama de Gantt |

---

## 2. APF2: IMPLEMENTACIÓN, BASE DE DATOS Y CALIDAD
**Objetivo:** Validar la normalización de la base de datos, el avance del código y el ecosistema de pruebas.
**Tiempo Estimado:** 15 minutos.

| # Slide | Título | Tipo | Puntos clave a cubrir | Evidencia que la respalda |
| :---: | :--- | :---: | :--- | :--- |
| 1 | Avance APF2 | Portada | • Hito de codificación<br>• Foco en Backend | N/A |
| 2 | Normalización BCNF | Contenido | • Diseño Físico PostgreSQL 16<br>• 12 tablas principales<br>• Integridad Referencial | Modelo ERD (`08_Normalizacion_Base_Datos.md`) |
| 3 | Trazabilidad y Roles | Contenido | • Trigger de Auditoría Forense<br>• RBAC (Admin vs Operador) | Script DDL (`schema.sql`) |
| 4 | Desarrollo del Frontend | Contenido | • Estructura de Context API<br>• Consumo de API REST | Árbol de directorios de Vite |
| 5 | Seguridad Base (OWASP) | Métrica | • Hash Bcrypt ($2b$)<br>• Cero vulnerabilidades `npm audit` | Captura Terminal / `security.test.ts` |
| 6 | Demo Funcional (Local) | Demo | • Login básico<br>• Navegación en el catálogo | Entorno `localhost:5173` o capturas |
| 7 | Plan de Cierre APF3 | Cierre | • CI/CD Pendiente<br>• Despliegue en la nube | Matriz de deuda técnica |

---

## 3. APF3: SISTEMA COMPLETO, SEGURIDAD Y USABILIDAD (ISO 25010)
**Objetivo:** Demostrar que el sistema es auditable, seguro, maduro y cumple normativas de calidad.
**Tiempo Estimado:** 15 minutos.

| # Slide | Título | Tipo | Puntos clave a cubrir | Evidencia que la respalda |
| :---: | :--- | :---: | :--- | :--- |
| 1 | Hacia Producción | Portada | • Consolidación del Sistema<br>• Despliegue y Seguridad | N/A |
| 2 | Despliegue Cloud | Contenido | • Frontend en GitHub Pages (CDN)<br>• Backend en Render.com | Diagrama de Nube y Red |
| 3 | Integración Continua | Contenido | • Pipelines de GitHub Actions<br>• Inyección segura de Variables | Workflow `deploy.yml` y Secretos |
| 4 | Calidad y Usabilidad | Métrica | • Puntuación SUS (88.5)<br>• Lighthouse Performance (96/100) | Reporte Lighthouse |
| 5 | Interoperabilidad Externa | Contenido | • API de WhatsApp<br>• Rótulos PDF y Códigos QR | Captura Modal PDF y enlace WA |
| 6 | Demostración en Vivo | Demo | • Carga inicial, Privacidad de Montos<br>• PWA Manifest válido | URL en Producción |
| 7 | Levantamiento APF2 | Cierre | • 100% de subsanaciones<br>• Auditoría formal cerrada | Documento (`13_Evidencia...`) |

---

## 4. SUSTENTACIÓN FINAL: DEFENSA DEL PRODUCTO
**Objetivo:** Vender el sistema como una solución integral lista para el mercado, sustentando decisiones.
**Tiempo Estimado:** 20 minutos (4 min por alumno).

| # Slide | Título | Tipo | Puntos clave a cubrir | Evidencia que la respalda |
| :---: | :--- | :---: | :--- | :--- |
| 1 | LeoFit Solutions | Portada | • Presentación del equipo completo | Foto de equipo (opcional) |
| 2 | El Reto y la Solución | Contenido | • Contraste Antes/Después<br>• Flujo de Despacho Dual | Diagrama D5 |
| 3 | Decisiones Arquitectónicas | Contenido | • Por qué PWA (offline-first)<br>• Por qué PostgreSQL | Documento SAD (`07_Arquitectura...`) |
| 4 | Pruebas y Evidencia UAT | Métrica | • 100% Casos Aprobados<br>• Mitigación OWASP Top 10 | Matriz de Trazabilidad UAT |
| 5 | Live Demo (Flujo Crítico) | Demo | • Login > Generar Pedido > Validar Stock > Imprimir Ticket | URL en Producción |
| 6 | Lecciones y Deuda Técnica | Cierre | • Bug del Optional Chaining resuelto<br>• Migración futura a Cypress | `DEUDA_TECNICA.md` |
| 7 | Rueda de Preguntas | Panel | • Agradecimiento<br>• Disposición al jurado | Logotipo de cierre |

---

## 5. REGLAS DE TRANSICIÓN PARA EL LLM
Al generar los *speaker notes*, utiliza las siguientes transiciones temáticas para conectar a los expositores fluidamente:
* **De Negocio a Backend:** *"Habiendo definido que nuestro cuello de botella era la trazabilidad (RF-007), Víctor nos detallará cómo la base de datos BCNF resuelve este desafío..."*
* **De Backend a Frontend:** *"Con esta lógica transaccional asegurada en Render, Harley demostrará cómo la consumimos desde una PWA..."*
* **De Desarrollo a DevOps:** *"Para garantizar que esta interfaz no colapse en producción, Lady detallará los pipelines de CI/CD..."*
