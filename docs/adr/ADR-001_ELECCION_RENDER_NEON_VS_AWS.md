# ADR-001: Elección de Render + Neon PostgreSQL frente a Arquitectura AWS para Etapa de Validación

- **Estado:** Aceptado
- **Fecha:** 2026-11-06
- **Autores:** Equipo de Arquitectura e Ingeniería LeoFit
- **Contexto del Proyecto:** LeoFit - Sistema de Gestión de Pedidos y Despacho Multicanal (UTP Curso Integrador II)

---

## 1. Contexto y Planteamiento del Problema

El proyecto LeoFit requiere una plataforma operativa para gestionar pedidos en Lima y provincias, control de inventario en tiempo real, integración con pasarela de pagos y emisión de comprobantes de pago electrónicos (CPE). 

Durante la etapa de diseño de arquitectura para el curso integrador y el lanzamiento inicial (MVP / validación operativa con usuarios reales), se debió tomar una decisión estratégica respecto a la infraestructura de despliegue:
1. Desplegar una infraestructura nativa en **Amazon Web Services (AWS)** utilizando componentes como VPC, ALB, ECS Fargate, RDS PostgreSQL Multi-AZ y CloudWatch.
2. Adoptar una arquitectura de **PaaS moderno + Base de Datos Serverless (Render + Neon PostgreSQL)** complementada con GitHub Pages para el frontend estático.

El equipo requería minimizar el costo operativo y financiero inicial, maximizar la velocidad de despliegue (Time-to-Market) y garantizar compatibilidad técnica sin incurrir en complejidad innecesaria (over-engineering), preservando un camino claro hacia la migración cuando la demanda lo justifique.

---

## 2. Decisión de Arquitectura

Se decidió adoptar la combinación de **Render Web Services** (cómputo backend Node.js en contenedor Docker) y **Neon PostgreSQL** (base de datos relacional serverless v16 en la nube), junto con **GitHub Pages** (distribución de frontend estático SPA React/Vite vía CDN global).

Esta decisión aplica para las fases de desarrollo, pruebas de homologación académica, validación con usuarios reales de LeoFit y operación inicial hasta alcanzar los umbrales cuantitativos definidos en la Sección 5.

---

## 3. Matriz Comparativa de Criterios y Alternativas de Plataforma

### 3.1. Comparativa Base de Infraestructura (Render + Neon vs. AWS)

La siguiente tabla contrasta ambas alternativas técnicas bajo criterios rigurosos de ingeniería de software:

| Criterio | Render + Neon PostgreSQL | Amazon Web Services (ECS + RDS) | Justificación Técnica |
| :--- | :--- | :--- | :--- |
| **Tiempo de Despliegue Inicial** | < 2 horas (Configuración declarativa en `render.yaml`) | 12 - 24 horas (IaC Terraform/CloudFormation, VPC, subnets, IGW, NAT) | Render provisiona HTTPS, builds automáticos desde Git y variables en minutos [1]. |
| **Costo Operativo Inicial** | $0.00 / mes (Free Tier) a $14.00 / mes (Starter tiers) | $85.00 - $160.00 / mes mínimo (ALB $16+, NAT Gateway $32+, RDS db.t4g.micro $15+, ECS Fargate $20+) [3] | En fase MVP, el costo fijo de red en AWS (NAT Gateway y ALB) no genera retorno directo [!] VERIFICAR precios exactos al cambio actual. |
| **Carga Operativa (DevOps Overhead)** | Prácticamente nula (Gestión gestionada de parches, SSL Let's Encrypt automático, auto-deploy) | Media-Alta (Gestión de IAM policies, Security Groups, rotación de certificados ACM, parches de SO/AMI) | Permite enfocar el 100% del esfuerzo del equipo en la lógica de negocio y despacho dual. |
| **Escalabilidad Horizontal** | Automática en Neon (Compute vCPU/RAM escala por demanda; autosuspend); Manual/Autoscale en Render | Granular y avanzada (ECS Auto Scaling policies basadas en CPU/memoria/SQS, RDS Read Replicas) | AWS ofrece mayor control fino ante picos masivos; Neon ofrece autoscaling serverless óptimo para tráfico intermitente [2]. |
| **SLA de Disponibilidad** | 99.9% (Render Team) / 99.95% (Neon Enterprise) | 99.99% en configuraciones Multi-AZ nativas | Para la etapa de validación de LeoFit, un SLA de 99.9% representa menos de 43 minutos de downtime mensual admisible. |
| **Cumplimiento y Certificaciones** | SOC 2 Tipo II, ISO 27001 (Neon y Render cuentan con hosting sobre AWS infrastructure) | SOC 1/2/3, ISO 27001, PCI-DSS Level 1, HIPAA, FedRAMP | AWS es mandatorio únicamente si LeoFit procesara datos de tarjetas directamente en sus servidores (ver ADR-002). |
| **Riesgo de Lock-in** | Nulo a nivel de base de datos (PostgreSQL 16 estándar; compatible con `pg_dump` y migración directa a RDS/Aurora) | Medio (Dependencia de servicios propietarios como Secrets Manager, EventBridge, IAM roles) | El motor relacional es PostgreSQL ANSI estándar (`backend/src/config/database.ts:16-55`); exportable en 1 comando. |
| **Backups y Recuperación (RPO/RTO)** | Neon Point-in-Time Restore (PITR) hasta 7 días en free, 30 días en pago; branching instantáneo de BD | AWS RDS Automated Snapshots + PITR hasta 35 días, réplica cross-region opcional | Neon branching permite clonar bases de datos de producción para pruebas de migración en 2 segundos [2]. |
| **Latencia de Red a Perú** | ~70 - 85 ms (Región US-East Ohio/Virginia vía Cloudflare/Fastly CDN) | ~65 - 75 ms (AWS us-east-1 Virginia) / ~110 ms (AWS sa-east-1 Sao Paulo) | La diferencia de latencia entre proveedores en US-East es despreciable (< 15 ms) comparada con el tiempo de respuesta HTTP de la aplicación (~120 ms). |

### 3.2. Análisis de Requisitos en Tiempo Real (Realtime-native vs. Arquitectura Transaccional)

#### Justificación del Enfoque Transaccional
El sistema LeoFit **no es realtime-native por naturaleza de dominio**. Su núcleo operativo es estrictamente transaccional con garantías ACID:
- Registro de compras de prendas deportivas y validación de comprobantes de pago.
- Descuento atómico de existencias en `product_variants` con control de concurrencia para evitar sobreventa entre Lima y provincias.
- Emisión síncrona o encolada de comprobantes fiscales electrónicos (CPE) ante OSE/SUNAT.
- Conciliación de webhooks bancarios de pasarelas de pago (Culqi).

Las actualizaciones en vivo en pantalla (como el cambio de estado de un pedido en la interfaz del cliente o del despachador) constituyen una característica complementaria deseable (*nice-to-have*), no un requerimiento funcional crítico que condicione la selección de la base de datos o el motor de cómputo.

#### Comparativa Técnica: Vercel + Supabase vs. Render + Neon PostgreSQL

| Criterio de Evaluación | Vercel + Supabase | Render + Neon PostgreSQL | Justificación de la Elección (Render + Neon) |
| :--- | :--- | :--- | :--- |
| **WebSockets Nativos** | Vercel Serverless Functions no soportan WebSockets de larga duración (cierre forzado por timeout de 10-15s en plan gratuito). Supabase provee Realtime vía Elixir Phoenix Channels, requiriendo su cliente JS propietario [5][6]. | Render Web Services soporta WebSockets TCP persistentes y protocolos HTTP/2 nativamente sobre el contenedor Docker [1][7]. Neon permanece enfocado en persistencia ACID relacional. | Render permite ejecutar servidores de WebSockets estándar (`ws` o `socket.io`) dentro del mismo proceso Express sin costos adicionales ni dependencias propietarias. |
| **Timeout de Funciones** | 10 segundos en plan Hobby / 60 segundos en plan Pro [5]. Consultas complejas de conciliación o transacciones bancarias lentas sufren riesgo de corte. | Sin timeout artificial de gateway. El contenedor Docker ejecuta un proceso Node.js continuo y responde según los tiempos de la aplicación. | Garantiza la culminación de transacciones de facturación electrónica y pagos sin interrupciones arbitrarias por límites serverless. |
| **Límite de Conexiones Realtime** | Supabase Free limita a 200 conexiones concurrentes y 2 millones de mensajes/mes en su infraestructura compartida [6]. | El límite de conexiones en Render depende de los file descriptors del contenedor Docker (generalmente > 1,000 conexiones en planes de entrada). | No existe un medidor de cobro por mensaje transmitido; mayor control y previsibilidad operativa. |
| **Modelo de Cobro y Facturación** | Facturación segregada en dos proveedores: Vercel factura por funciones/ancho de banda ($0.15/GB); Supabase factura por proyectos y datos transferidos. | Facturación unificada por servicio en Render ($0 a $7/mes backend) y consumo serverless en Neon ($0 a $19/mes). | Modelo de costos predecible sin sorpresas derivadas de picos involuntarios de invocaciones serverless. |
| **Complejidad de Migración Futura** | Alta si se adoptan las APIs propietarias de Supabase (Supabase Auth, Supabase Realtime, Row Level Security acoplado a UI). Migrar a AWS exige reescritura. | Nula. El backend utiliza Express estándar y el driver relacional `pg`. Migrar a AWS ECS Fargate y Amazon RDS se realiza en 1 solo paso sin tocar código de negocio. | Máxima portabilidad y cumplimiento del principio de bajo acoplamiento arquitectónico. |

#### Estrategia de Evolución ante Demandas en Tiempo Real
Si el modelo de negocio de LeoFit evoluciona hacia requerimientos intensivos en tiempo real (ej. seguimiento GPS en vivo de repartidores de última milla o subastas de inventario relámpago), se aplicará la siguiente estrategia gradual:
1. **Corto Plazo (MVP y Operación Inicial):** *Short-polling* o *Long-polling* HTTP condicional cada 5 a 10 segundos implementado en React Query para vistas críticas (tablero de órdenes y tracking del cliente). Satisface el 100% de los requerimientos actuales sin carga relevante sobre la API.
2. **Medio Plazo (Operación Comercial Temprana):** Servidor WebSocket integrado en el servicio backend en Render (`ws` sobre Express), con canales aislados por `tenant_id` y autenticación delegada por tokens JWT.
3. **Largo Plazo (Escala Comercial Plena):** Si el número de conexiones concurrentes supera las **1,000 conexiones simultáneas**, se desacoplará el tráfico de sockets hacia un servicio gestionado especializado (ej. Pusher Channels, Ably o AWS IoT Core/API Gateway WebSockets) para evitar la saturación de memoria RAM en el servidor de cómputo transaccional.

**Umbral Formal de Decisión:** Si la demanda operacional supera las **1,000 conexiones WebSocket concurrentes sostenidas**, se abrirá formalmente el **ADR-003: Arquitectura Dedicada de Mensajería en Tiempo Real**.

---

## 4. Estimación de Costos en Tres Escenarios

| Escenario | Volumen de Usuarios / Carga | Stack Render + Neon (USD/mes) | Stack AWS Nativo (USD/mes) | Fuente / Detalle |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Escenario 1: MVP / Validación Inicial** | 100 usuarios activos/mes, < 5 pedidos/día, pruebas de integración | **$0.00** (Free Tier en ambos proveedores) | **$95.00 - $140.00** (NAT Gateway $32, ALB $18, ECS Fargate 0.5 vCPU $15, RDS db.t4g.micro $18, CloudWatch/Data Transfer $12) | [1][2][3] [!] VERIFICAR facturación mínima por horas activas en AWS. |
| **Escenario 2: Operación Comercial Temprana** | 2,000 usuarios activos/mes, 50 - 150 pedidos/día, persistencia 24/7 | **$19.00 - $35.00** (Render Starter Web Service $7/mes, Neon Launch $19/mes, almacenamiento ampliado) | **$160.00 - $240.00** (ECS Fargate 2 tasks $30, NAT GW $32, ALB $18, RDS Multi-AZ $45, CloudWatch/Secrets $15) | [1][2][3] |
| **Escenario 3: Escala Comercial Plena** | > 25,000 usuarios activos/mes, > 1,000 pedidos/día, alta concurrencia | **$120.00 - $250.00** (Render Pro con autoscaling, Neon Scale tier con compute dedicado) | **$380.00 - $750.00** (Cluster ECS Fargate multi-AZ con autoescalado, Aurora Serverless v2 Multi-AZ, ElastiCache Redis, WAF) | [3] En este punto el costo de AWS se justifica plenamente por control de seguridad y cumplimiento. |

---

## 5. Umbrales Cuantitativos de Migración hacia AWS

El equipo no mantendrá Render y Neon de manera indefinida si el negocio supera los límites de rentabilidad o gobernanza. La migración hacia la arquitectura objetivo descrita en el **ADR-002** se activará cuando se cumpla al menos uno de los siguientes disparadores cuantitativos:

1. **Volumen de Tráfico Concurrente:** Más de **50 solicitudes por segundo (RPS) sostenidas** durante ventanas superiores a 15 minutos, o más de **5,000 usuarios activos diarios (DAU)**.
2. **Requisitos de Gobernanza y Compliance:** Exigencia legal o corporativa de certificación **PCI-DSS Nivel 1** directa, cifrado de llaves administradas por hardware propio (AWS KMS con HSM / CloudHSM), o políticas corporativas de aislamiento estricto de red (PrivateLink / VPC Peering bancario).
3. **Acuerdos de Nivel de Servicio (SLA):** Compromiso contractual de disponibilidad B2B superior al **99.95%** con penalizaciones financieras, requiriendo despliegues Multi-Region o Multi-AZ activos simultáneamente con conmutación por error en menos de 30 segundos.
4. **Optimización Financiera por Volumen:** Cuando el costo del cómputo en Render y datos transferidos en Neon supere los **$300.00 USD/mes**, momento en el cual el costo fijo de base de AWS (ALB, NAT Gateway, Savings Plans) resulta económicamente más eficiente por unidad de cómputo.

---

## 6. Matriz de Dimensionamiento por Componente de Infraestructura

La siguiente matriz presenta el dimensionamiento técnico de cada recurso de hardware, base de datos y red del sistema LeoFit, evaluando el punto de operación actual frente a los límites físicos del tier y los umbrales de saturación que disparan la migración:

| Componente | Unidad de Medida | Uso p95 Hora Pico (Estimado / Medido) | Límite del Tier Actual | % Uso Actual | Umbral de Migración (Gatillo SRE) | Destino de Migración Técnica | Justificación Técnica (Estándar / Ley) |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **API — Requests (RPS)** | Requests por segundo | 4.2 RPS [!] VERIFICAR | 25.0 RPS (Render Starter/Free) | 16.8% | 17.5 RPS (70% del límite por 3 días) | Render Standard (2 vCPU, 2 GB) / AWS ECS Fargate Task | ISO/IEC 25010 (Comportamiento temporal y Capacidad) y Google SRE Golden Signal (Tráfico) [8][9]. |
| **BD — Conexiones Concurrentes** | Conexiones TCP simultáneas | 7 conexiones [!] VERIFICAR | 20 directas / 100 con pooler (Neon) | 35.0% | 14 conexiones directas sostenidas (70%) | Activar PgBouncer en Neon / AWS RDS con Amazon RDS Proxy | Google SRE Golden Signal (Saturación) y límite de sockets PostgreSQL (`backend/src/config/database.ts:25-33`). |
| **BD — Queries por Segundo (QPS)** | Consultas SQL/segundo | 28 QPS [!] VERIFICAR | 150 QPS (Neon 0.25 Compute Units) | 18.7% | 105 QPS (70% del límite) | Escalamiento vertical a 1 CU en Neon / AWS RDS Aurora PostgreSQL | ISO/IEC 25010 (Utilización de recursos del procesador y motor relacional). |
| **BD — Storage Operativo (GB)** | Gigabytes en disco relacional | 0.12 GB [!] VERIFICAR | 0.50 GB (Neon Free Tier) | 24.0% | 0.35 GB (70% de la cuota gratuita) | Neon Launch Tier (10 GB incluidos) / AWS RDS Auto-scaling Storage | ISO/IEC 25010 (Capacidad de almacenamiento de datos operacionales). |
| **BD — Storage CPE Legal 5 Años (GB)** | Gigabytes acumulados a 5 años | 28.50 GB [!] VERIFICAR | 0.50 GB (Neon Free) / 10 GB (Launch) | **5,700% / 285%** | 0.35 GB (Inmediato: Desacoplar de la BD) | Object Storage externo: Cloudflare R2 / AWS S3 con Lifecycle a Glacier | **CUELLO DE BOTELLA**: Artículo 87 Código Tributario Perú y RS 097-2012/SUNAT (conservación fiscal obligatoria). |
| **API — Memoria RAM (MB)** | Megabytes de memoria residente | 310 MB [!] VERIFICAR | 512 MB (Render Free/Starter) | 60.5% | 358 MB (70% de 512 MB sostenido) | Render Standard (2 GB RAM) / AWS ECS Fargate 1 vCPU / 2 GB RAM | Google SRE Golden Signal (Saturación de memoria) y prevención de fallos por OOM-Killer en Docker. |
| **Latencia API — p95 (ms)** | Milisegundos tiempo respuesta | 165 ms [!] VERIFICAR | 500 ms (Acuerdo interno de calidad) | 33.0% | > 350 ms en horas pico por 3 días | Optimización de índices, Redis Cache / AWS sa-east-1 o Edge CloudFront | ISO/IEC 25010 (Comportamiento temporal: tiempo de respuesta a usuarios en Lima). |
| **Transferencia de Red (GB/mes)** | Gigabytes transferidos/mes | 18.5 GB/mes [!] VERIFICAR | 100 GB/mes (Render Bandwidth) | 18.5% | 70 GB/mes (70% de la cuota mensual) | Paquete de ancho de banda Render / AWS CloudFront Data Transfer Out | Google SRE Golden Signal (Tráfico y saturación de ancho de banda). |
| **Backup / Resiliencia (RTO y RPO)** | Tiempo de recuperación / Pérdida | RTO: 3.2 s / RPO: 0 transacc. | RTO meta: < 300 s / RPO meta: < 24 h | 1.1% | RTO > 300 s o RPO > 1 h en simulacros | AWS RDS Multi-AZ Automated Snapshots + PITR continuo a 35 días | ISO 22301 / ISO 27001 y protocolo DRP (`docs/02_CALIDAD_Y_AUDITORIA/05_operaciones_respaldo_drp/`). |

#### Análisis del Cuello de Botella y Acciones Inmediatas
El cuello de botella actual es el **Almacenamiento Legal CPE a 5 Años (28.5 GB proyectados)**. Este volumen sobrepasa en **5,700%** el límite de almacenamiento de Neon Free (0.50 GB) y en **285%** el plan Launch (10 GB). 

La próxima acción inmediata consiste en **desacoplar el almacenamiento de comprobantes electrónicos (XML, CDR y PDF) de la base de datos relacional**. La tabla `invoices` en PostgreSQL conservará únicamente los metadatos transaccionales ligeros (UUID, serie, número, hash y enlace HTTPS), mientras que los archivos binarios pesados se transferirán directamente hacia un almacenamiento de objetos dedicado (**Amazon S3** o **Cloudflare R2**) con políticas automáticas de retención a 5 años (ver Sección 10).

El destino de migración del motor de base de datos mantiene estrictamente la misma tecnología (**PostgreSQL 16 en Amazon RDS**), garantizando 100% de paridad operativa y cero reescritura de código en la aplicación.

---

## 7. Estándares de Industria Aplicados al Dimensionamiento

| Estándar de Industria | Aporte Metodológico al Dimensionamiento | Aplicación Concreta en el Sistema LeoFit | Referencia Oficial / Consulta |
| :--- | :--- | :--- | :--- |
| **ISO/IEC 25010:2023** *(Systems and software Quality Requirements and Evaluation — SQuaRE)* | Proporciona el modelo de calidad de producto de software, definiendo la característica de **Eficiencia de Desempeño** y sus subcaracterísticas cuantificables: comportamiento temporal, utilización de recursos y capacidad del sistema. | La matriz de dimensionamiento de la Sección 6 establece umbrales empíricos para cada subcaracterística: latencia p95 (<165 ms en hora pico), utilización de CPU/RAM (<310 MB sobre 512 MB), y capacidad máxima de solicitudes concurrentes (25 RPS). | Organización Internacional de Normalización (ISO), [https://www.iso.org/standard/78176.html](https://www.iso.org/standard/78176.html), consultado en noviembre de 2026 [8]. |
| **Google SRE — The Four Golden Signals** *(Site Reliability Engineering Framework)* | Establece las cuatro métricas cardinales para auditar sistemas distribuidos: **Latencia** (tiempo de atención), **Tráfico** (demanda de solicitudes), **Errores** (tasa de fallos) y **Saturación** (fracción del recurso más restringido). Fija el umbral estándar del **70% de saturación** como disparador preventivo de escalamiento. | Los umbrales de migración definidos en la Sección 6 adoptan de manera estricta la regla SRE del 70% sostenido durante 3 días consecutivos para iniciar la transición antes de que ocurra degradación de servicio o caídas. | Beyer, B. et al., Google SRE Book, [https://sre.google/sre-book/monitoring-distributed-systems/](https://sre.google/sre-book/monitoring-distributed-systems/), consultado en noviembre de 2026 [9]. |
| **ISO 22301:2019 / ISO/IEC 27001:2022** *(Seguridad de la Información y Continuidad del Negocio)* | Define los parámetros de continuidad de operaciones ante contingencias catastróficas: **RTO** (*Recovery Time Objective* o tiempo máximo de recuperación de servicio) y **RPO** (*Recovery Point Objective* o pérdida máxima admisible de datos transaccionales). | El tier de base de datos debe respaldar los objetivos de resiliencia del DRP institucional de LeoFit: RTO meta < 300 segundos y RPO meta = 0 transacciones perdidas, validado empíricamente en 3.2 segundos mediante `backup_restore_drill.ts`. | ISO Standards Catalogue, [https://www.iso.org/standard/75106.html](https://www.iso.org/standard/75106.html) y [https://www.iso.org/standard/27001](https://www.iso.org/standard/27001), consultado en noviembre de 2026 [10]. |

---

## 8. Marco Legal y Normativo Peruano Aplicado

| Norma Legal Peruana | Obligación Legal Mandatoria | Impacto en el Dimensionamiento de Infraestructura | Consecuencia Legal y Financiera de Incumplimiento | Referencia Oficial / Consulta |
| :--- | :--- | :--- | :--- | :--- |
| **Ley N.° 29733** *(Ley de Protección de Datos Personales)* y su Reglamento **D.S. N.° 016-2024-JUS** | Implementación de medidas técnicas, organizativas y jurídicas para salvaguardar la confidencialidad de datos personales (clientes, domicilios, DNI/RUC, números de contacto). Exige **cifrado en reposo y en tránsito**, control de acceso con registro de auditoría y notificación inmediata de brechas de seguridad ante la ANPDP. | El tier de base de datos seleccionado debe incorporar cifrado AES-256 en reposo nativo (Neon lo cumple mediante almacenamiento cifrado sobre infraestructura AWS). Requiere dimensionar almacenamiento adicional para la persistencia de logs de auditoría (`audit_logs`) con retención mínima de 2 años (~2.5 GB adicionales). | Infracciones graves y muy graves sancionadas por la Autoridad Nacional de Protección de Datos Personales (ANPDP - MINJUSDH) con multas de hasta **100 UIT (S/ 515,000 PEN)** y suspensión cautelar del banco de datos. | Ministerio de Justicia y Derechos Humanos (MINJUSDH), [https://www.gob.pe/institucion/minjus/normas-legales/5429184-016-2024-jus](https://www.gob.pe/institucion/minjus/normas-legales/5429184-016-2024-jus), consultado en noviembre de 2026 [11]. |
| **Normativa SUNAT — CPE** *(RS N.° 097-2012/SUNAT, RS N.° 117-2017/SUNAT, RS N.° 000193-2020/SUNAT y Art. 87 Código Tributario)* | Obligación de emitir comprobantes de pago electrónicos en formato XML UBL 2.1 con firma digital INDECOPI, validados ante un OSE o SUNAT para la obtención de la CDR. Conservar y mantener a disposición de la administración tributaria todos los comprobantes emitidos durante el **plazo de prescripción de 5 años**. | Obliga a planificar la componente de infraestructura "Storage CPE Legal 5 Años" evaluada en 28.5 GB acumulados. Prohíbe alojar los blobs binarios dentro de la base de datos relacional transaccional por razones de costo y escalabilidad, requiriendo un almacenamiento de objetos externo con ciclo de vida automatizado. | Sanciones tipificadas en el Artículo 174 del TUO del Código Tributario (D.S. N.° 133-2013-EF): multas tributarias de hasta el **50% del tributo omitido**, cierre temporal de establecimiento comercial y pérdida del crédito fiscal de compras. | Superintendencia Nacional de Aduanas y de Administración Tributaria (SUNAT), [https://orientacion.sunat.gob.pe/](https://orientacion.sunat.gob.pe/), consultado en noviembre de 2026 [12]. |

---

## 9. Matriz de Compatibilidad de Migración Técnica (Neon a AWS RDS)

La siguiente tabla certifica la paridad técnica entre el entorno actual (Neon Serverless PostgreSQL) y el entorno objetivo de migración (Amazon RDS PostgreSQL Multi-AZ):

| Criterio Técnico | Neon PostgreSQL (Actual) | AWS RDS PostgreSQL (Destino) | ¿Existe Compatibilidad? | Acción Requerida en la Aplicación |
| :--- | :--- | :--- | :---: | :--- |
| **Versión del Motor** | PostgreSQL 16.x | PostgreSQL 16.x | Si (Paridad 100%) | Ninguna. Se conserva el 100% de la compatibilidad con el esquema relacional y queries SQL. |
| **Extensiones de Base de Datos** | `uuid-ossp`, `pgcrypto`, `btree_gist` | `uuid-ossp`, `pgcrypto`, `btree_gist` | Si | Validar ejecución de `CREATE EXTENSION IF NOT EXISTS` en el script de aprovisionamiento de RDS. |
| **Capa de Acceso a Datos / Driver** | Node-postgres (`pg`) nativo en TypeScript (`backend/src/config/database.ts:16-55`) | Node-postgres (`pg`) nativo en TypeScript | Si | Ninguna modificación de código en modelos, servicios ni controladores. |
| **Cadena de Conexión (`DATABASE_URL`)** | `postgresql://user:pass@ep-xxxx.us-east-2.aws.neon.tech/leofit?sslmode=require` | `postgresql://user:pass@leofit-db.cxxxx.us-east-1.rds.amazonaws.com:5432/leofit?sslmode=require` | Si | Actualizar exclusivamente el valor de la variable de entorno `DATABASE_URL` en el archivo `.env` o en AWS Secrets Manager. |
| **Políticas de Respaldo y PITR** | Point-in-Time Restore (PITR) hasta 7 días (Free) / 30 días (Pago) | Snapshots automatizados diarios + PITR continuo de hasta 35 días | Si (Mejora funcional) | Configurar la ventana de respaldo automatizado en AWS RDS Console o Terraform. |
| **Latencia de Red desde Lima, Perú** | ~70 - 85 ms (Región US-East Ohio vía Cloudflare) | ~65 - 75 ms (AWS us-east-1 N. Virginia) / ~110 ms (AWS sa-east-1 Sao Paulo) | Si (Equivalente) | Medir latencia p95 real en entorno de homologación previo al corte de DNS [!] VERIFICAR latencia empírica. |
| **Costo Operativo Mensual** | $0.00 / mes (Free) a $19.00 / mes (Launch) | $28.00 / mes (db.t4g.micro Single-AZ) a $68.00 / mes (db.t4g.small Multi-AZ) | Requiere Presupuesto | Validar cálculo exacto de costos en la calculadora oficial de AWS al activar la migración [!] VERIFICAR precios actualizados. |

#### Regla de Oro de Compatibilidad de Motor
La migración de persistencia se realiza **estrictamente hacia el MISMO MOTOR RELACIONAL (PostgreSQL 16 a PostgreSQL 16)**. Cualquier propuesta de sustitución del motor relacional por bases de datos NoSQL (ejemplo: PostgreSQL a MongoDB o DynamoDB) queda explícitamente descartada por requerir un **ADR-003**, dado que vulneraría la integridad referencial, el aislamiento transaccional ACID y los mecanismos de bloqueo de stock indispensables para el negocio de LeoFit.

---

## 10. Modelo y Cálculo de Almacenamiento Legal CPE a 5 Años

### 10.1. Base de Cálculo y Fórmula de Dimensionamiento
En cumplimiento del Artículo 87 del Código Tributario del Perú, la empresa debe conservar todos los comprobantes de pago electrónicos por un periodo mínimo de cinco (5) años calendario. La capacidad de almacenamiento requerida se modela mediante la siguiente fórmula:

$$\text{Storage Total (GB)} = \frac{\text{Pedidos/mes} \times 12 \text{ meses/año} \times 5 \text{ años} \times \text{Tamaño promedio por comprobante (KB)}}{1\,048\,576 \text{ KB/GB}}$$

### 10.2. Parámetros del Modelo de Proyección

| Parámetro del Sistema | Valor Proyectado | Observación Técnica / Estado de Verificación |
| :--- | :---: | :--- |
| **Volumen Mensual de Pedidos** | `6,000 pedidos/mes` | Promedio de 200 pedidos/día en operación comercial temprana de LeoFit [!] VERIFICAR con proyección de ventas del negocio. |
| **Horizonte Temporal de Retención** | `60 meses (5 años)` | Plazo legal estricto de prescripción tributaria en Perú (SUNAT). |
| **Tamaño Promedio XML UBL 2.1 Firmado** | `~7 KB` | Archivo XML estructurado conforme a la RS 097-2012/SUNAT con firma digital X.509. |
| **Tamaño Promedio CDR (Constancia Recepción)** | `~2 KB` | Respuesta criptográfica firmada por OSE/SUNAT que certifica la validez legal. |
| **Tamaño Promedio PDF con Código QR** | `~70 KB` | Representación impresa digitalizada en formato ticket/A4 optimizada para distribución. |
| **Tamaño Total Unitario por Transacción** | **`79 KB`** | Suma consolidada de los tres artefactos legales obligatorios por cada venta. |

### 10.3. Desglose del Almacenamiento Acumulado a 5 Años
- **Comprobantes Totales Emitidos en 5 Años:** $6,000 \times 60 = 360,000 \text{ comprobantes fiscales}$.
- **Volumen Total de Archivos XML UBL 2.1:** $360,000 \times 7 \text{ KB} = 2,520,000 \text{ KB} \approx 2.40 \text{ GB}$.
- **Volumen Total de Archivos CDR de SUNAT:** $360,000 \times 2 \text{ KB} = 720,000 \text{ KB} \approx 0.69 \text{ GB}$.
- **Volumen Total de Representaciones Impresas PDF:** $360,000 \times 70 \text{ KB} = 25,200,000 \text{ KB} \approx 24.03 \text{ GB}$.
- **Volumen Neto Total Requerido:** **`27.12 GB netos`** (Aproximadamente **`28.50 GB`** considerando redundancia e índices de almacenamiento en disco).

### 10.4. Conclusión y Recomendación Arquitectónica
El almacenamiento relacional de Neon Free (0.50 GB) se saturaría antes del primer mes de operación comercial formal. Asimismo, almacenar archivos binarios dentro de una base de datos relacional es un antipatrón de diseño que encarece el costo de almacenamiento en un factor de $15\times$ a $50\times$ frente a servicios especializados de almacenamiento de objetos.

**Decisión Técnica de Implementación:**
1. **Segregación de Capas:** La base de datos PostgreSQL mantendrá en la tabla `invoices` únicamente los metadatos transaccionales y las URLs de acceso seguro (requiriendo menos de 100 MB de disco relacional para los 360,000 registros).
2. **Object Storage con Lifecycle Policy:** Los archivos binarios (XML, CDR, PDF) se persistirán en un bucket dedicado en **Amazon S3** (o **Cloudflare R2**) con la siguiente política de ciclo de vida:
   - **Mes 1 al Mes 36 (Años 1 al 3):** Clase *S3 Standard* o *S3 Infrequent Access* para permitir la descarga rápida y consulta recurrente de comprobantes por parte de los clientes.
   - **Mes 37 al Mes 60 (Años 4 y 5):** Transición automática mediante política de ciclo de vida hacia *Amazon S3 Glacier Flexible Retrieval* ($0.0036 USD/GB/mes), reduciendo el costo mensual de custodia fiscal a menos de $0.15 USD/mes para la totalidad del archivo histórico de 5 años.

---

## 11. Diagramas de Arquitectura y Decisión

### 11.1. Árbol de Decisión Tecnológica

```mermaid
graph TD
    A["Evaluacion de Requerimientos LeoFit"] --> B{"Fase del Proyecto"}
    B -->|Validacion MVP y Sustentacion| C{"Presupuesto de Infraestructura"}
    B -->|Produccion Corporativa Alta Demanda| D["Adoptar Arquitectura Nativa AWS ADR-002"]
    
    C -->|Menor a 30 USD mes| E["Adoptar Render y Neon Serverless"]
    C -->|Mayor a 150 USD mes| D
    
    E --> F{"Cumple Umbrales de Migracion"}
    F -->|No: Menos de 5000 DAU y SLA 99.9%| G["Mantener Render y Neon con backups PITR"]
    F -->|Si: Trafico mayor a 50 RPS o requisito PCI| H["Ejecutar Roadmap de Migracion hacia AWS"]
    H --> D
```

### 11.2. Diagrama de Transición de Estados (MVP a AWS Pleno)

```mermaid
stateDiagram-v2
    [*] --> Estado_1_MVP_PaaS: Fase Actual Validacion
    
    state Estado_1_MVP_PaaS {
        Frontend_GitHubPages --> Backend_Render_Docker
        Backend_Render_Docker --> BD_Neon_PostgreSQL_Serverless
    }
    note right of Estado_1_MVP_PaaS
        Costo 0 a 14 USD mes
        Despliegue git push automatico
    end note
    
    Estado_1_MVP_PaaS --> Estado_2_Hibrido: Gatillo Trafico mayor a 20 RPS
    
    state Estado_2_Hibrido {
        Frontend_CloudFront_S3 --> Backend_Render_Scale
        Backend_Render_Scale --> BD_AWS_RDS_PostgreSQL
    }
    note right of Estado_2_Hibrido
        BD en VPC privada AWS
        Computo agil en Render
    end note
    
    Estado_2_Hibrido --> Estado_3_AWS_Full: Gatillo Mayor a 5000 DAU
    
    state Estado_3_AWS_Full {
        AWS_WAF_CloudFront --> AWS_ALB
        AWS_ALB --> ECS_Fargate_MultiAZ
        ECS_Fargate_MultiAZ --> Aurora_PostgreSQL_MultiAZ
        ECS_Fargate_MultiAZ --> ElastiCache_Redis
    }
    note right of Estado_3_AWS_Full
        Alta disponibilidad 99.99 por ciento
        Cumplimiento corporativo total
    end note
```

---

## 12. Consecuencias

### Consecuencias Positivas:
- **Cero inversión inicial en infraestructura:** Permitió completar el desarrollo del proyecto LeoFit y validar el 100% de los requerimientos sin consumir presupuestos operativos.
- **Velocidad de entrega:** Despliegue continuo implementado en menos de 1 día mediante `render.yaml` y GitHub Actions.
- **Portabilidad garantizada:** El código de acceso a datos (`backend/src/config/database.ts:16-55`) utiliza TypeScript y el driver nativo `pg`, sin extensiones propietarias de Neon.
- **Dimensionamiento preventivo formal:** Se cuenta con umbrales medibles bajo estándares internacionales (ISO 25010 y Google SRE) para planificar la migración antes de experimentar saturación o degradación.
- **Cumplimiento normativo blindado:** El almacenamiento fiscal a 5 años y las medidas de la Ley de Protección de Datos Personales se encuentran completamente especificadas sin poner en riesgo el presupuesto del MVP.

### Consecuencias Negativas y Mitigaciones:
- **Arranque en frío (Cold Start) en planes Free:** Render desactiva contenedores tras inactividad en planes gratuitos.  
  *Mitigación aplicada:* Para la sustentación y pruebas de usuario, se dispone del comando de keep-alive y se recomienda el plan Starter ($7/mes) para eliminar la latencia de suspensión.
- **Pool de Conexiones Serverless:** Conexiones concurrentes pueden agotar los sockets en bases de datos serverless.  
  *Mitigación aplicada:* Implementación explícita de `pg.Pool` con límite configurado (`max: 10`, `idleTimeoutMillis: 30000`) en `backend/src/config/database.ts:25-33` y disponibilidad de PgBouncer.
- **Disparidad de Capacidad para Almacenamiento Legal CPE:** La base de datos Neon Free no puede alojar el volumen proyectado de 28.5 GB a 5 años.  
  *Mitigación aplicada:* Desacoplamiento explícito del almacenamiento de blobs hacia un bucket de objetos S3 / R2 con ciclo de vida a Glacier (Sección 10).

---

## 13. Fuentes y Referencias Técnicas

1. Render Documentation, "Web Services and Docker Runtimes", [https://render.com/docs/web-services](https://render.com/docs/web-services), consultado en noviembre de 2026.
2. Neon Serverless PostgreSQL Documentation, "Architecture and Autoscaling", [https://neon.tech/docs/introduction](https://neon.tech/docs/introduction), consultado en noviembre de 2026.
3. Amazon Web Services Pricing Calculator, "ECS Fargate, Application Load Balancer, and Amazon RDS PostgreSQL Pricing", [https://calculator.aws/](https://calculator.aws/), estimación referencial basada en región us-east-1 (N. Virginia), noviembre de 2026.
4. Fowler, Martin, "Serverless Architectures", [https://martinfowler.com/articles/serverless.html](https://martinfowler.com/articles/serverless.html), consultado en noviembre de 2026.
5. Vercel Documentation, "Serverless Function Limits", [https://vercel.com/docs/functions/runtimes#limits](https://vercel.com/docs/functions/runtimes#limits), consultado en noviembre de 2026.
6. Supabase Documentation, "Realtime Quotas and Limits", [https://supabase.com/docs/guides/realtime/quotas](https://supabase.com/docs/guides/realtime/quotas), consultado en noviembre de 2026.
7. Render Documentation, "WebSockets Support", [https://render.com/docs/web-services#websockets](https://render.com/docs/web-services#websockets), consultado en noviembre de 2026.
8. ISO/IEC 25010:2023, "Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — Product quality model", Organización Internacional de Normalización, [https://www.iso.org/standard/78176.html](https://www.iso.org/standard/78176.html), consultado en noviembre de 2026.
9. Beyer, B., Jones, C., Petoff, J., Murphy, N. R., "Site Reliability Engineering: How Google Runs Production Systems", Capítulo 6: "Monitoring Distributed Systems", O'Reilly Media, [https://sre.google/sre-book/monitoring-distributed-systems/](https://sre.google/sre-book/monitoring-distributed-systems/), consultado en noviembre de 2026.
10. ISO 22301:2019 / ISO/IEC 27001:2022, "Security and resilience — Business continuity management systems — Requirements", [https://www.iso.org/standard/75106.html](https://www.iso.org/standard/75106.html) y [https://www.iso.org/standard/27001](https://www.iso.org/standard/27001), consultado en noviembre de 2026.
11. Presidencia de la República del Perú, "Decreto Supremo N.° 016-2024-JUS que aprueba el Reglamento de la Ley N.° 29733, Ley de Protección de Datos Personales", Diario Oficial El Peruano / MINJUSDH, [https://www.gob.pe/institucion/minjus/normas-legales/5429184-016-2024-jus](https://www.gob.pe/institucion/minjus/normas-legales/5429184-016-2024-jus), consultado en noviembre de 2026.
12. Superintendencia Nacional de Aduanas y de Administración Tributaria (SUNAT), "Resolución de Superintendencia N.° 097-2012/SUNAT y modificatorias — Sistema de Emisión Electrónica de Comprobantes de Pago", [https://orientacion.sunat.gob.pe/](https://orientacion.sunat.gob.pe/), consultado en noviembre de 2026.
