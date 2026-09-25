# -*- coding: utf-8 -*-
"""
Script de enriquecimiento y consolidación definitiva para DOCUMENTO_MAESTRO_INTEGRAL_LEOFIT.md
Integra los datos del Acta Formal N° 01, glosario técnico ampliado, desglose de 35 pruebas
y corrige el nombre del docente evaluador.
"""

import os

def enrich():
    md_path = os.path.abspath('docs/DOCUMENTO_MAESTRO_INTEGRAL_LEOFIT.md')
    if not os.path.exists(md_path):
        print(f"Error: {md_path} no existe.")
        return

    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Corregir docente si tiene placeholder
    text = text.replace('Mg. Ing. Docente Asignado UTP', 'Ing. Enrique Lee Huamani Uriarte')

    # 2. Enriquecer Sección 12.1 con Acta Formal N° 01 y DoD
    idx_12_1 = text.find('## 12.1.')
    idx_12_2 = text.find('## 12.2.')

    if idx_12_1 != -1 and idx_12_2 != -1:
        new_12_1 = """## 12.1. Gobernanza Ágil de Equipo y Acta Formal de Reunión N° 01

### A. Políticas de Gobernanza y Ritmo de Desarrollo Ágil
A lo largo del ciclo académico, el equipo sostuvo reuniones periódicas de alineamiento:
- **Daily Standups (15 minutos)**: Reuniones virtuales diarias de lunes a viernes a las 20:00 horas para responder las tres preguntas clásicas de Scrum: ¿Qué se logró ayer? ¿Qué se hará hoy? ¿Existen bloqueos técnicos?
- **Sprint Planning y Sprint Reviews**: Sesiones bisemanales con presencia del Product Owner y revisión de entregables frente a las rúbricas académicas de la UTP.
- **Políticas de Calidad y Revisión de Código**: Obligatoriedad de aprobación de al menos 1 desarrollador antes de fusionar cualquier Pull Request hacia la rama `dev` o `main`.
- **Criterios de Terminado (Definition of Done - DoD)**: Para considerar concluida cualquier tarea o historia de usuario se exige:
  1. Código tipado estricto en TypeScript sin advertencias ni errores en `tsc --noEmit`.
  2. Cobertura de pruebas unitarias y de integración con Vitest o Jest $\\ge 80\\%$.
  3. Revisión y aprobación formal mediante Pull Request por al menos un desarrollador par.
  4. Despliegue automatizado y validado en el entorno de staging/producción mediante GitHub Actions.

### B. Acta Formal de Reunión N° 01 con el Stakeholder (LeoFit)
* **Proyecto:** Sistema Web PWA de Gestión y Toma de Pedidos Multicanal para LeoFit.
* **Fecha y Horario:** 15 de Agosto de 2026 | 10:00 AM – 11:30 AM.
* **Lugar / Modalidad:** Presencial (Taller y Almacén de LeoFit, Lima) con soporte virtual.
* **Participantes y Control de Asistencia:**
  - **Víctor Raúl Cárdenas Ramírez** (Gerente General / Dueño del Negocio, LeoFit Indumentaria Deportiva) — Presente.
  - **Lady Luz Loayza Rodriguez** (Scrum Master / Líder de Proyecto, Grupo 01 - UTP) — Presente.
  - **Víctor Leandro Cárdenas Fernández** (Product Owner / Arquitecto Back-End, Grupo 01 - UTP) — Presente.
  - **Harley Anthony Roman Delgado** (Front-End Lead / Diseñador UI, Grupo 01 - UTP) — Presente.
  - **Jim Alessandro Dávila Morales** (Especialista QA / Testing, Grupo 01 - UTP) — Presente.
  - **Daniel Enrique Rojas Sanchez** (Analista de Negocio / Procesos, Grupo 01 - UTP) — Presente.
* **Agenda Formal Tratada:**
  1. Presentación formal del equipo de desarrollo de la UTP y objetivos estratégicos del proyecto.
  2. Descripción del modelo comercial actual y canales de atención (WhatsApp, Instagram y presencial).
  3. Diagnóstico de cuellos de botella: demoras de hasta 45 minutos por pedido, quiebres de inventario por ventas cruzadas y pérdida de notas manuales.
  4. Definición de la solución tecnológica: Progressive Web App (PWA) con catálogo en tiempo real y reserva de stock inmediata.
  5. Acuerdos de colaboración, cronograma de reuniones de Sprint y entrega de insumos fotográficos.
* **Acuerdos y Compromisos Formalizados:**
| N° | Descripción del Acuerdo / Entregable | Responsable Asignado | Fecha Límite |
| :---: | :--- | :--- | :---: |
| **1** | Redacción formal de la Ficha de Mapeo de Empresa y Problema | Grupo 01 (Daniel Rojas / Lady Loayza) | 20/08/2026 |
| **2** | Entrega de catálogo fotográfico de prendas y datos anonimizados de pedidos | Víctor Raúl Cárdenas (LeoFit) | 22/08/2026 |
| **3** | Elaboración de wireframes y primeros prototipos interactivos en Figma | Harley Roman / Lady Loayza | 25/08/2026 |
| **4** | Diseño del modelo relacional normalizado y especificación ERS IEEE 830 | Víctor Cárdenas / Jim Dávila | 28/08/2026 |

"""
        text = text[:idx_12_1] + new_12_1 + text[idx_12_2:]
        print("[OK] Sección 12.1 enriquecida con Acta N° 01 y DoD.")

    # 3. Enriquecer Glosario (12.2) con términos técnicos
    glosario_items = [
        ("AS-IS (Estado Actual)", "Metodología de modelado que describe el flujo operativo tradicional tal como se ejecuta en el presente, visibilizando cuellos de botella y pérdidas."),
        ("BPMN 2.0", "Business Process Model and Notation. Estándar internacional gráfico para el modelado formal de flujos de trabajo mediante carriles y eventos."),
        ("Bundle", "Conjunto empaquetado y minificado de activos JavaScript, CSS y recursos estáticos listos para su distribución y ejecución en el navegador."),
        ("Ciclo de Pedido", "Intervalo de tiempo total transcurrido desde que el cliente inicia la interacción de compra hasta que la orden es entregada en su domicilio."),
        ("Clean Architecture", "Patrón arquitectónico propuesto por Robert C. Martin que promueve la separación concéntrica de capas desacopladas, haciendo la lógica independiente de frameworks."),
        ("Code-Splitting", "Técnica de optimización que fragmenta el paquete de código fuente en chunks independientes que se descargan bajo demanda al navegar a cada ruta."),
        ("Core Web Vitals", "Conjunto de métricas estandarizadas por Google para evaluar la experiencia de usuario: FCP, LCP, CLS e INP."),
        ("HMR", "Hot Module Replacement. Característica de Vite que actualiza módulos en el navegador en tiempo real sin recargar la página completa ni perder estado."),
        ("Inventario Crítico", "Nivel de existencias de una prenda que se encuentra por debajo del umbral de seguridad (< 5 unidades), requiriendo alerta de reposición."),
        ("MVP", "Producto Mínimo Viable. Versión funcional inicial del software que satisface las necesidades centrales de los usuarios para validar hipótesis con clientes reales."),
        ("Quiebre de Stock", "Situación operativa en la que la demanda de una prenda no puede ser atendida por agotamiento imprevisto de existencias en almacén."),
        ("SLI", "Service Level Indicator. Medición cuantitativa directa del nivel de servicio brindado en tiempo real (ej. tasa de peticiones HTTP exitosas)."),
        ("TO-BE (Estado Propuesto)", "Representación del flujo de procesos rediseñado y optimizado mediante la integración de software para eliminar ineficiencias del AS-IS."),
        ("Tree-Shaking", "Proceso de optimización ejecutado por empaquetadores (Rollup) que analiza el árbol de dependencias y elimina código muerto o no utilizado."),
        ("TypeScript", "Superconjunto tipado estático de JavaScript desarrollado por Microsoft que añade verificación formal de tipos en tiempo de compilación."),
        ("Vitest", "Marco de pruebas unitarias de última generación optimizado para entornos Vite, de alta velocidad y soporte nativo para TypeScript.")
    ]

    for term, definition in glosario_items:
        row_str = f"| **{term}** | {definition} |\n"
        if f"| **{term}** |" not in text:
            anchor = "| **WPO** |"
            pos = text.find(anchor)
            if pos != -1:
                end_line = text.find("\n", pos) + 1
                text = text[:end_line] + row_str + text[end_line:]

    print("[OK] Glosario ampliado con términos técnicos y de negocio.")

    # 4. Añadir Pregunta 16 sobre la batería de 35 pruebas automatizadas
    if "### 16. ¿Qué estrategia y batería de pruebas automatizadas" not in text:
        q16 = """
### 16. ¿Qué estrategia y batería de pruebas automatizadas se implementó para garantizar la fiabilidad del software?
- **Respuesta**: Se implementó una estrategia piramidal con **35 pruebas automatizadas continuas** que cubren de extremo a extremo la lógica del sistema:
  1. **Frontend (17 pruebas unitarias y de integración con Vitest)**: Ubicadas en `frontend/src/__tests__/`, validando reactividad del estado del carrito, consistencia de inventario en memoria, validación de formularios de checkout, generación vectorial de recibos PDF y navegación fluida entre pestañas.
  2. **Backend (18 pruebas de integración con Jest & Supertest)**: Ubicadas en `backend/src/__tests__/`, evaluando la transaccionalidad ACID con bloqueos pesimistas `SELECT ... FOR UPDATE`, autenticación JWT, autorización RBAC por roles, sanitización contra inyección SQL y XSS, y endpoints de analítica de pedidos.
  Toda la batería se ejecuta automáticamente en el pipeline de Integración Continua (`.github/workflows/ci-cd.yml`) ante cada `push` y `pull request` hacia `main`, impidiendo regresiones en el entorno productivo.
"""
        idx_cap13 = text.find("# CAPÍTULO 13: CONCLUSIONES")
        if idx_cap13 != -1:
            text = text[:idx_cap13] + q16 + "\n---\n\n" + text[idx_cap13:]
            print("[OK] Pregunta técnica 16 sobre batería de 35 pruebas agregada.")

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"[EXITO] Documento Maestro actualizado: {len(text)} caracteres, {len(text.splitlines())} lineas.")

if __name__ == '__main__':
    enrich()
