# UNIVERSIDAD TECNOLÓGICA DEL PERÚ
## FACULTAD DE INGENIERÍA DE SISTEMAS E INFORMÁTICA
### CURSO INTEGRADOR II: SOFTWARE (100000S12F)

---

# GLOSARIO FORMAL DE TÉRMINOS TÉCNICOS Y DE NEGOCIO
## PROYECTO: SISTEMA WEB PWA DE GESTIÓN Y TOMA DE PEDIDOS MULTICANAL PARA LEOFIT

---

## 1. TÉRMINOS DE NEGOCIO Y MODELADO DE PROCESOS

* **AS-IS (Estado Actual):** Metodología de modelado que describe el flujo operativo y los procedimientos de una organización tal como se ejecutan en el presente, permitiendo identificar ineficiencias, cuellos de botella y costos ocultos.
* **BPMN 2.0 (Business Process Model and Notation):** Estándar internacional gráfico para el modelado formal de procesos de negocio mediante eventos, actividades, compuertas lógicas y carriles de responsabilidad.
* **Ciclo de Pedido (Order Lead Time):** Intervalo de tiempo total transcurrido desde que el cliente inicia la interacción de compra hasta que la orden es entregada físicamente en su domicilio.
* **Flete / Costo de Delivery:** Importe monetario cobrado por el servicio logístico motorizado para trasladar los paquetes desde el almacén hasta la dirección del cliente.
* **Inventario Crítico:** Nivel de existencias de un producto que se encuentra por debajo del umbral de seguridad (en LeoFit, $< 5$ unidades), requiriendo reabastecimiento prioritario.
* **Lean Canvas:** Herramienta estratégica de modelado de negocios creada por Ash Maurya, compuesta por 9 bloques enfocados en la resolución de problemas para startups y productos innovadores.
* **MoSCoW:** Técnica ágil de priorización de requerimientos basada en cuatro categorías: Must have (Imprescindible), Should have (Debería tener), Could have (Podría tener) y Won't have (No tendrá en esta iteración).
* **MVP (Producto Mínimo Viable):** Versión funcional de un producto de software que incluye el conjunto mínimo indispensable de características requeridas para validar hipótesis de valor con usuarios reales.
* **Quiebre de Stock (Stockout):** Situación operativa en la que la demanda de un producto no puede ser satisfecha debido al agotamiento no previsto de las existencias en inventario.
* **SKU (Stock Keeping Unit):** Identificador alfanumérico único asignado a un producto y sus variantes específicas (tipo de prenda, talla, color) para su control y seguimiento en almacén.
* **TO-BE (Estado Propuesto):** Representación del flujo de procesos rediseñado y optimizado mediante la integración de la solución de software, orientada a eliminar las ineficiencias del modelo AS-IS.

---

## 2. TÉRMINOS TÉCNICOS, ARQUITECTURA Y DESARROLLO DE SOFTWARE

* **Bundle:** Archivo o conjunto de archivos compilados y minificados que contienen el código JavaScript, CSS y recursos estáticos de una aplicación web listos para su distribución a producción.
* **Clean Architecture (Arquitectura Limpia):** Patrón arquitectónico propuesto por Robert C. Martin que promueve la separación de responsabilidades en capas concéntricas desacopladas, haciendo la lógica de negocio independiente de frameworks, interfaces y bases de datos.
* **Code-Splitting (División de Código):** Técnica de optimización que fragmenta el paquete de código fuente en chunks independientes que se descargan de forma asíncrona únicamente cuando la vista o componente es requerido.
* **Core Web Vitals:** Conjunto de métricas estandarizadas por Google para evaluar la experiencia de usuario en la web: First Contentful Paint (FCP), Largest Contentful Paint (LCP), Cumulative Layout Shift (CLS) e Interaction to Next Paint (INP).
* **Gherkin:** Lenguaje formal y legible para el ser humano utilizado en el desarrollo guiado por comportamiento (BDD), estructurado mediante cláusulas Given-When-Then (Dado-Cuando-Entonces) para definir criterios de aceptación.
* **Hot Module Replacement (HMR):** Característica de los empaquetadores modernos (como Vite) que actualiza módulos en el navegador en tiempo real durante el desarrollo sin necesidad de recargar la página completa ni perder el estado.
* **PWA (Progressive Web App):** Aplicación web construida con tecnologías estándar que ofrece capacidades avanzadas similares a las aplicaciones móviles nativas, tales como funcionamiento offline, instalación en pantalla de inicio y alto rendimiento de carga.
* **Service Worker:** Script en JavaScript que el navegador ejecuta en segundo plano, independiente de la página web, permitiendo interceptar peticiones de red, gestionar estrategias de caché offline y recibir notificaciones.
* **SLA (Service Level Agreement):** Acuerdo formal y contractual que define los niveles de servicio comprometidos entre el proveedor de software y el cliente (ejemplo: $99.5\%$ de disponibilidad).
* **SLI (Service Level Indicator):** Medición cuantitativa directa del nivel de servicio que se está brindando en tiempo real (ejemplo: porcentaje de peticiones exitosas).
* **SLO (Service Level Objective):** Meta cuantitativa interna establecida por el equipo de ingeniería para un indicador SLI específico (ejemplo: tiempo de respuesta P95 $< 800$ ms).
* **Tree-Shaking:** Proceso de optimización ejecutado por empaquetadores (como Rollup) que analiza el árbol de dependencias estático y elimina de forma automática el código muerto o no utilizado.
* **TypeScript:** Superconjunto tipado estático de JavaScript desarrollado por Microsoft que añade verificación formal de tipos en tiempo de compilación, mejorando la robustez y mantenibilidad del software.
* **Vitest:** Marco de pruebas unitarias de última generación optimizado para entornos Vite, caracterizado por su velocidad de ejecución y compatibilidad nativa con TypeScript y módulos ES.
* **WPO (Web Performance Optimization):** Disciplina de la ingeniería de software enfocada en la aplicación de técnicas y estrategias para maximizar la velocidad de carga, eficiencia de recursos y rendimiento general de aplicaciones web.
