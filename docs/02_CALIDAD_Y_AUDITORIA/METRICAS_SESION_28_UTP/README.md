# Taller Práctico: Métricas de Funcionalidad y Pruebas de Software
**Asignatura:** Calidad de Software — Unidad 05: Técnicas de Prueba de Errores del Software (Sesión 28)  
**Universidad Tecnológica del Perú (UTP)** — Facultad de Ingeniería  
**Estudiante:** Loayza Rodríguez, Lady Luz | **Código UTP:** `U22221489`  
**Proyecto:** Sistema Web de Gestión de Pedidos y Facturación Electrónica (LeoFit)

---

## 1. Documentos del Entregable

* **Documento Word Formal (2 Páginas):** [`METRICAS_FUNCIONALIDAD_Y_PRUEBAS_LOAYZA_U22221489.docx`](./METRICAS_FUNCIONALIDAD_Y_PRUEBAS_LOAYZA_U22221489.docx)
* **Documento PDF Referencial:** [`METRICAS_FUNCIONALIDAD_Y_PRUEBAS_LOAYZA_U22221489.pdf`](./METRICAS_FUNCIONALIDAD_Y_PRUEBAS_LOAYZA_U22221489.pdf)
* **Script Generador Automatizado:** [`scripts/generators/generate_metricas_funcionalidad_pruebas.py`](../../../scripts/generators/generate_metricas_funcionalidad_pruebas.py)

---

## 2. Cuatro (4) Métricas de Funcionalidad (Sesión 28)

| Código | Métrica y Objetivo | Fórmula / Medición | Criterio / Umbral | Resultado Real en LeoFit |
| :--- | :--- | :--- | :--- | :--- |
| **MF-01** | **Métrica de Éxito de Funcionalidades (MEF)**<br>Evalúa completitud de módulos según pesos formales: 0 (no hecha), 0.5 (a medio realizar), 1.0 (realizada y operativa). | $$\text{MEF} = \left[\frac{\sum (P_i \times F_i)}{F_{\text{total}}}\right] \times 100\%$$ | Óptimo $\ge 95\%$<br>Aceptable $\ge 85\%$ | **100.0% de Éxito**<br>(14 de 14 funcionalidades completas con peso 1.0). |
| **MF-02** | **Índice de Funcionalidad Estructural vs Servidor (IFS)**<br>Proporción entre lógica funcional de servidor vs. componentes estructurales UI (Slide 19). | $$\text{IFS} = \left[\frac{N_{\text{func}}}{N_{\text{func}} + N_{\text{estruc}}}\right] \times 100\%$$ | Balanceado:<br>60% a 75% | **70.0% de Lógica de Negocio**<br>(42 archivos backend vs. 18 de interfaz). |
| **MF-03** | **Latencia Operativa de Acceso Rápido (LOAR)**<br>Cumplimiento de límites de interacción humana (Lafuente, 2000 adaptado a SLAs de API REST). | $\text{LOAR}_{p95} =$ Tiempo de respuesta en percentil 95 bajo concurrencia de 50 VUs. | Visual $\le 1.5$ s<br>API crítica $\le 500$ ms | **$p95 = 215$ ms (Óptimo)**<br>(Catálogo: 180 ms, Checkout: 215 ms, Webhook Culqi: 145 ms). |
| **MF-04** | **Grado de Validación de Requisitos IEEE 830 (GVR)**<br>Determinación de requisitos no ambiguos, trazables y verificados empíricamente. | $$\text{GVR} = \left[\frac{\text{RF}_{\text{validados}}}{\text{RF}_{\text{especificados}}}\right] \times 100\%$$ | Requerido: 100% | **100.0% de Validación**<br>(14/14 RFs cubiertos con casos de prueba CP-F01 al CP-F14). |

---

## 3. Cuatro (4) Métricas para Pruebas de Software (Sesión 28 - Slide 22)

| Código | Métrica y Objetivo | Fórmula / Medición | Criterio / Umbral | Resultado Real en LeoFit |
| :--- | :--- | :--- | :--- | :--- |
| **MP-01** | **Exhaustividad de las Pruebas (EP)**<br>Completitud de la suite automatizada respecto al plan maestro de pruebas QA. | $$\text{EP} = \left[\frac{\text{CP}_{\text{ejecutados}}}{\text{CP}_{\text{planificados}}}\right] \times 100\%$$ | Meta $\ge 98\%$<br>Mínimo $\ge 90\%$ | **99.18% de Cobertura**<br>(121 pruebas pasadas en CI/CD; 1 prueba live). |
| **MP-02** | **Densidad de Defectos por KLOC (DD)**<br>Cuantificación de fallos por cada mil líneas de código fuente (calidad intrínseca). | $$\text{DD} = \frac{\text{Defectos Detectados}}{\text{KLOC}}$$ | Excelente: $< 1.0$<br>Aceptable: $1.0 - 3.0$ | **0.47 defectos / KLOC**<br>(4 fallos en 8.5 KLOC TypeScript; 100% resueltos). |
| **MP-03** | **Control de Pruebas Unitarias (CPU)**<br>Efectividad y estabilidad de las pruebas automatizadas de componentes (Slide 22). | $$\text{CPU} = \left[\frac{\text{Pruebas Aprobadas (Pass)}}{\text{Total Pruebas Ejecutadas}}\right] \times 100\%$$ | Mandatorio:<br>100% pass | **100.0% Pass Rate**<br>(121/121 pruebas unitarias aprobadas en 8.57 s en Jest). |
| **MP-04** | **Índice de Madurez del Software (SMI)**<br>Estabilidad del software ante refactorizaciones y cambios (Software Maturity Index). | $$\text{SMI} = \frac{M_T - (F_a + F_c + F_d)}{M_T}$$ | Estable: $\ge 0.85$ | **$\text{SMI} = 0.889$ (88.9%)**<br>(45 módulos totales, 3 añadidos, 2 modificados, 0 eliminados). |

---

## 4. Cuadro Resumen y Dictamen de Calidad

| Dimensión | Métrica Principal | Valor Obtenido | Umbral Exigido | Estado / Dictamen |
| :--- | :--- | :--- | :--- | :--- |
| **Funcionalidad** | Éxito Funcional (MEF) / Latencia $p95$ (LOAR) | 100.0% completitud / 215 ms latencia API | $\ge 95\%$ éxito / $< 500$ ms latencia | **CONFORME (Excelente)** |
| **Pruebas / QA** | Control Unitario (CPU) / Densidad Defectos (DD) | 100.0% Pass (121/121) / 0.47 def / KLOC | 100% aprobadas / $< 1.0$ def / KLOC | **CONFORME (Excelente)** |
