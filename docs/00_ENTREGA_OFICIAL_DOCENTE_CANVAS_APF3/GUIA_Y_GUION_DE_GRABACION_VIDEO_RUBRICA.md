# GUION MAESTRO DE GRABACIÓN DE VIDEO (16/16 PUNTOS)
## Proyecto: LeoFit Solutions (`v2.0.0`) — Calidad ISO/IEC 25010 y APF3
### Curso Integrador II: Software (100000S12F) — Ciclo 2026-I — UTP
**Docente Asesor:** **Ing. Enrique Lee Huamani Uriarte**  
**Equipo de Ingeniería (Grupo 01):**
* **Lady Luz Loayza Rodríguez** (`U22221489`) — Scrum Master / DevSecOps Lead
* **Víctor Leandro Cárdenas Fernández** (`U19217414`) — Product Owner / DBA
* **Harley Anthony Roman Delgado** (`U21313032`) — Frontend Lead / UI-UX
* **Jim Alessandro Dávila Morales** (`U18206081`) — QA Lead / Backend
* **Daniel Enrique Rojas Sánchez** (`U21214627`) — Business Analyst / Cloud DevOps

---

### Preparación Previa Antes de Empezar a Grabar (5 minutos)
Ten abiertas estas pestañas y ventanas para alternar con fluidez (`Alt + Tab`):
1. **VS Code:** Con el proyecto `leofit-pedidos-sistema` y terminal integrado listo.
2. **Navegador Web (Pestaña 1):** [Frontend PWA en GitHub Pages](https://leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/).
3. **Navegador Web (Pestaña 2):** [Healthcheck Render Cloud API](https://leofit-backend-api.onrender.com/api/health).
4. **Navegador Web (Pestaña 3):** [Repositorio GitHub del Grupo 01](https://github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema).
5. **Documentos Abiertos:**
   - PDF: `docs/00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3/01_INFORME_FINAL_APF3_LEOFIT.pdf` (abierto en Capítulo 11 - Pruebas).
   - PDF: `docs/00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3/02_INFORME_ISO25010_SEMANAS_10_11_LEOFIT.pdf` (abierto en Secciones 5, 6 y 7).
   - Excel: `docs/00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3/04_PLAN_AUDITORIA_SOFTWARE_DASHBOARD_LEOFIT.xlsx`.

---

## ESTRUCTURA CRONOMETRADA DEL VIDEO (10 A 12 MINUTOS)

### BLOQUE 0: INTRODUCCIÓN Y CONTEXTO (00:00 – 01:30)
* **Qué mostrar en pantalla:** La primera diapositiva de `03_PRESENTACION_SUSTENTACION_APF3_LEOFIT.pptx` y luego el Repositorio en GitHub.
* **Qué decir (Guion):**
> *"Estimado docente asesor, Ing. Enrique Lee Huamani Uriarte, y miembros del jurado evaluador, muy buenas tardes. En este video presentamos la sustentación formal y demostración en vivo del software **LeoFit v2.0.0**, una solución web PWA de gestión de pedidos multicanal y control transaccional de inventario para la empresa LeoFit Confecciones y Diseños Deportivos S.A.C., ubicada en el emporio comercial de Gamarra.  
> Nuestro equipo, el Grupo 01, está conformado por Lady Loayza como Scrum Master y DevSecOps, Víctor Cárdenas como Product Owner y DBA, Harley Roman como Frontend Lead, Jim Dávila como QA Lead y Daniel Rojas como Business Analyst y Cloud DevOps.  
> A continuación, demostraremos el cumplimiento exhaustivo de cada uno de los 5 criterios de la rúbrica oficial de evaluación del curso."*

---

### BLOQUE 1: EVALUACIÓN DE PRUEBAS FUNCIONALES (4 PUNTOS) (01:30 – 04:00)
**Requisito de Rúbrica:** Evalúa funcionalidad mediante automatización validando completitud, corrección e idoneidad (ISO 25010): 1) Frameworks; 2) Casos; 3) Capturas/Ejecución; 4) Cobertura; 5) Métricas y observaciones.

* **Qué mostrar en pantalla:**
  1. Terminal de VS Code ejecutando las pruebas.
  2. El informe PDF `01_INFORME_FINAL_APF3_LEOFIT.pdf` en la **Tabla 18 y 19** y la **Figura 17 (Pirámide de Pruebas)**.
* **Qué hacer en vivo:**
  En la terminal, ejecuta:
  ```powershell
  npm test --prefix frontend
  ```
  *(Muestra cómo pasan los 69 tests de Vitest)*  
  Y luego corre el escáner de sincronización de auditoría:
  ```powershell
  python scripts/sync_audit_metrics.py
  ```
* **Qué decir (Guion):**
> *"Iniciamos con el Criterio 1: Evaluación de Pruebas Funcionales bajo la norma ISO/IEC 25010:2023.  
> **1) Frameworks utilizados:** Empleamos **Jest v29** y **Supertest** en el backend sobre Node.js 20 LTS, y **Vitest v4.1** con **React Testing Library** sobre React 19 en el frontend.  
> **2) Listado de casos de prueba:** Disponemos de 27 suites automatizadas y 195 casos de prueba diseñados a partir de los 10 Requisitos Funcionales del alcance (RF-01 al RF-10), abarcando desde control de acceso RBAC hasta transacciones atómicas con bloqueo pesimista `SELECT FOR UPDATE` para evitar sobreventas.  
> **3) Ejecución en vivo:** Como se observa en la terminal en tiempo real, las suites frontend de Vitest aprueban al 100% sus 69 casos en 10 suites.  
> **4) Cobertura:** Nuestra cobertura de código instrumentalizada con Istanbul y v8 alcanza el 76.16% en líneas y 100% en los módulos críticos de negocio como cálculo de órdenes, facturación SUNAT y deduplicación atómica.  
> **5) Métricas y nivel de cumplimiento:**  
> • **Completitud Funcional:** 10 de 10 RF del alcance implementados y evidenciados, alcanzando el **100.0%**.  
> • **Corrección Funcional:** 194 pruebas automatizadas aprobadas de 195 ejecutadas, con una tasa del **99.49%** (solo 1 caso omitido deliberadamente por aislamiento de PostgreSQL en CI).  
> • **Idoneidad:** El flujo de toma de pedidos redujo el tiempo operativo de 45 minutos manuales a **38.2 segundos**, cumpliendo sobradamente la meta de menos de 90 segundos."*

---

### BLOQUE 2: AUTOMATIZACIÓN DE PRUEBAS DE INTEGRACIÓN (4 PUNTOS) (04:00 – 06:30)
**Requisito de Rúbrica:** Interoperabilidad y coexistencia con sistemas externos: 1) Sistemas integrados; 2) Frameworks; 3) Casos; 4) Capturas/Ejecución; 5) Reportes; 6) Métricas y observaciones.

* **Qué mostrar en pantalla:**
  1. El archivo `backend/tests/integration_external.test.ts` en VS Code.
  2. El informe `02_INFORME_ISO25010_SEMANAS_10_11_LEOFIT.pdf` en la **Sección 6 (Interoperabilidad)** y **Sección 7 (Coexistencia)**.
  3. Las figuras de coexistencia: `fig_coexistencia_latencias.png` y `fig_coexistencia_p95.png`.
* **Qué decir (Guion):**
> *"Pasamos al Criterio 2: Pruebas de Integración, Interoperabilidad y Coexistencia.  
> **1) Sistemas externos integrados:** LeoFit se integra con: 1) WhatsApp Cloud API para notificaciones; 2) Pasarelas y billeteras Yape/Plin mediante Webhooks asíncronos; y 3) Padrón fiscal SUNAT / RENIEC para validación de RUC y DNI.  
> **2) Frameworks utilizados:** Jest, Supertest, librerías nativas de criptografía `node:crypto` para firmas HMAC-SHA256, ApacheBench y Docker cgroups para coexistencia.  
> **3) Casos de prueba:** Fichas PI-01 a PI-05 en interoperabilidad y PC-01 a PC-04 en coexistencia.  
> **4 y 5) Demostración y Reporte de Interoperabilidad:** Tal como exige la directriz del profesor Enrique Lee, **status 200 no es interoperabilidad**. Por ello, probamos no solo el intercambio sino el uso semántico: verificamos que un webhook con firma HMAC incorrecta devuelva 401 Unauthorized; que un payload corrupto devuelva 422; y que un webhook válido transicione el pedido a estado 'PAGADO' en PostgreSQL de manera idempotente sin duplicar eventos.  
> **6) Coexistencia bajo recursos compartidos:** Diseñamos un experimento riguroso de dos condiciones bajo un contenedor Docker restringido a 1 vCPU y 512 MB RAM compartiendo host con el Servicio B de reportes.  
> **Métricas:** En la Condición A (Línea base) obtuvimos una latencia media de 4.92 ms, y en la Condición A+B bajo contención simultánea se obtuvo 4.42 ms con un P95 de 9.1 ms y **0.0% de errores de conexión**. La degradación relativa se mantuvo muy por debajo del umbral del 25%, demostrando que ambos servicios coexisten armónicamente."*

---

### BLOQUE 3: EVALUACIÓN DE LA USABILIDAD DEL SISTEMA (4 PUNTOS) (06:30 – 08:30)
**Requisito de Rúbrica:** Criterios ISO 25010 / Usabilidad mediante pruebas automatizadas: 1) Informe de Usabilidad; 2) Frameworks; 3) Casos; 4) Capturas/Ejecución; 5) Reportes; 6) Métricas y observaciones.

* **Qué mostrar en pantalla:**
  1. La PWA en vivo en el navegador (`https://leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/`).
  2. Haz una acción en vivo: simula agregar un producto y muestra la alerta preventiva de stock o la validación reactiva del formulario.
  3. Muestra el código de `frontend/src/__tests__/usability_iso25010.test.ts`.
* **Qué decir (Guion):**
> *"Avanzamos al Criterio 3: Evaluación de la Usabilidad y Capacidad de Interacción bajo ISO/IEC 25010:2023.  
> **1) Informe de Usabilidad:** Documentado en el Capítulo 12 del Informe Final y en las suites de calidad de la Semana 12.  
> **2) Frameworks:** Vitest, React Testing Library, Axe-Core para auditoría de accesibilidad y Lighthouse.  
> **3) Casos de prueba:** Suite `usability_iso25010.test.ts` con 9 pruebas automatizadas que validan las 8 subcaracterísticas 2023: aprendibilidad, operabilidad, protección contra errores, asistencia al usuario y accesibilidad.  
> **4 y 5) Demostración en vivo:** Como pueden ver en la interfaz PWA, el sistema aplica el principio de 'prevenir antes que culpar'. Si un operario ingresa un stock no disponible o teléfono inválido, la interfaz muestra advertencias inline inmediatas y un modal descriptivo sin borrar los datos del carrito.  
> **6) Métricas y Resultados:**  
> • Realizamos un estudio formal con **5 usuarios externos representativos** de Gamarra.  
> • **Tasa de éxito en tareas críticas:** 100% de cumplimiento sin intervención técnica.  
> • **Escala de Usabilidad del Sistema (SUS):** Obtuvimos un puntaje promedio de **88.5 / 100**, equivalente a **Grado A (Excelente, Percentil 96%)**.  
> • **Accesibilidad WCAG 2.1 AA/AAA:** Contrastes de color certificados de 5.42:1 a 17.8:1, soporte total para navegación por teclado y etiquetas `aria-live` para lectores de pantalla."*

---

### BLOQUE 4: VALIDACIÓN EN LA PLATAFORMA CLOUD (2 PUNTOS) (08:30 – 10:30)
**Requisito de Rúbrica:** Valida el funcionamiento mediante pruebas funcionales y de integración en la plataforma cloud con usabilidad y automatización.

* **Qué mostrar en pantalla:**
  1. Navegador Web mostrando la URL real en producción: `https://leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/`.
  2. Abre DevTools (`F12`) y muestra la pestaña **Application -> Service Workers** (activado y corriendo).
  3. Pestaña con el endpoint `/api/health` en Render Cloud mostrando el JSON:
     ```json
     { "status": "ok", "version": "2.0.0", "database": "connected" }
     ```
  4. Realiza un inicio de sesión en vivo con `admin@leofit.pe` / `Admin123!` y muestra el Dashboard de Ventas y Rendimiento.
* **Qué decir (Guion):**
> *"En el Criterio 4: Validación y Verificación en la Plataforma Cloud.  
> **Arquitectura Desacoplada en la Nube:**  
> • **Frontend:** Desplegado en **GitHub Pages Edge CDN** bajo protocolo HTTPS TLS 1.3 con Service Worker PWA activo, lo que permite funcionamiento offline con persistencia en IndexedDB.  
> • **Backend:** Desplegado en **Render Cloud Platform** (Node.js 20 LTS en contenedor) conectado de forma segura mediante SSL a una base de datos relacional gestionada **PostgreSQL 16 Cloud**.  
> **Validación en Vivo:**  
> Mostramos en pantalla el endpoint `api/health`, que responde HTTP 200 confirmando la versión `2.0.0` y la conexión activa a la base de datos PostgreSQL.  
> Iniciamos sesión con el usuario Administrador y observamos cómo el sistema carga los KPIs operativos, el catálogo textil y los gráficos reactivos de ventas y SLA sin demoras.  
> Todo el ciclo está automatizado mediante un pipeline de **CI/CD en GitHub Actions**, donde cada commit a la rama `main` compila el código, ejecuta las pruebas de frontend y backend, y si todo aprueba, despliega automáticamente a producción."*

---

### BLOQUE 5: SUSTENTACIÓN Y CONCLUSIONES (2 PUNTOS) (10:30 – 12:00)
**Requisito de Rúbrica:** Argumenta con claridad, coherencia técnica y dominio conceptual: 1) Principales aportes; 2) Orden lógico y síntesis; 3) Dominio y sustento de artefactos; 4) Funcionamiento de v2 en cloud.

* **Qué mostrar en pantalla:**
  1. El archivo Excel `docs/00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3/04_PLAN_AUDITORIA_SOFTWARE_DASHBOARD_LEOFIT.xlsx` mostrando el avance del 100% en las 8 fases de auditoría.
  2. La lámina final de la presentación PPTX con los aportes y limitaciones.
* **Qué decir (Guion):**
> *"Para concluir con el Criterio 5: Sustentación Técnica.  
> **1) Principales aportes al proyecto:**  
> • Eliminación del 100% de sobreventas mediante concurrencia pesimista en PostgreSQL.  
> • Reducción del tiempo de toma de pedidos en un **98.6%** (de 45 min a 38.2 s).  
> • Reducción de fallas humanas mediante auditoría criptográfica HMAC y deduplicación atómica.  
> **2) Dominio de los artefactos elaborados:**  
> Presentamos un expediente integral compuesto por:  
> • El Informe Final APF3 tipo libro de 77 páginas con 21 diagramas.  
> • El Informe Técnico de Calidad ISO 25010 Semanas 10-11 basado en la plantilla oficial.  
> • El Dashboard de Auditoría en Excel alineado con ISO 29119-3 e ISO 90003 al 100% de avance.  
> • 194 pruebas automatizadas con 613 aserciones.  
> **3) Honestidad Técnica y Limitaciones (Criterio Lee Huamani):**  
> Reconocemos con rigor que nuestro informe evalúa atributos específicos de producto y no constituye una certificación comercial ISO. Asimismo, la muestra de usabilidad de 5 usuarios valida el flujo operativo de Gamarra pero requerirá muestras mayores ante expansiones regionales.  
> El sistema LeoFit v2.0.0 se encuentra en producción, auditado, probado y listo para operar. Muchas gracias."*

---

### CHEATSHEET RÁPIDO PARA LA SEGUNDA PANTALLA

| Recurso | Valor Exacto |
| :--- | :--- |
| **URL Frontend:** | `https://leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/` |
| **URL Backend:** | `https://leofit-backend-api.onrender.com/api/health` |
| **URL Swagger:** | `https://leofit-backend-api.onrender.com/api/docs` |
| **URL Repositorio:** | `https://github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema` |
| **Usuario Admin:** | `admin@leofit.pe` / `Admin123!` |
| **Usuario Operador:** | `operador@leofit.pe` / `Operador123!` |
| **Pruebas Aprobadas:** | **194 pruebas aprobadas** (125 Jest Backend + 69 Vitest Frontend), 0 fallos |
| **Métrica SUS:** | **88.5 / 100** (Grado A - Excelente) |
| **Coexistencia:** | Latencia **4.42 ms**, P95 **9.1 ms**, Degradación \(< 25\%\), **0.0% errores** |
| **Comando Tests:** | `npm test --prefix frontend` y `python scripts/sync_audit_metrics.py` |
