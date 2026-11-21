# LeoFit Solutions — Presentación Oficial de Sustentación Final de Ingeniería
## Sistema de Gestión de Pedidos y Control de Inventario Multicanal (Ciclo 2026-I)
**Asignatura:** Curso Integrador II: Software (100000S12F) · **Docente Asesor:** Ing. Enrique Lee Huamani Uriarte  
**Equipo de Ingeniería:** Grupo 01 (Lady Loayza, Victor Cardenas, Harley Roman, Jim Davila, Daniel Rojas)  
**Entregable Oficial:** Semana 18 · Sustentación Final de Grado · Formato Widescreen 16:9 (25 Diapositivas)  

---

## Diapositiva 01
### UNIVERSIDAD TECNOLOGICA DEL PERU (UTP) - CURSO INTEGRADOR II: SOFTWARE

LEOFIT SOLUTIONS: SISTEMA DE GESTION DE PEDIDOS  
Y CONTROL DE INVENTARIO MULTICANAL  

Sustentacion Final de Ingenieria (Semana 18) - Calidad ISO/IEC 25010 (S14-S16) y Arquitectura Cloud  

EQUIPO DE INGENIERIA (GRUPO 01):  
- Lady Luz Loayza Rodriguez (Scrum Master / DevSecOps)
- Victor Leandro Cardenas Fernandez (Product Owner / DBA)
- Harley Anthony Roman Delgado (Frontend Lead / UI-UX)
- Jim Alessandro Davila Morales (QA Lead / Backend)
- Daniel Enrique Rojas Sanchez (Business Analyst / Cloud)

METRICAS Y PARAMETROS DEL PROYECTO:  
- Empresa Beneficiaria: LeoFit Confecciones S.A.C.
- Docente Asesor: Ing. Enrique Lee Huamani Uriarte
- Bateria QA: 190 Pruebas Automatizadas (100% OK)
- Base de Datos: PostgreSQL 16 (BCNF / ACID / Lima)
- Despliegue: Render Docker API + GitHub Pages CDN
- ISO 25010: Rendimiento (p95 280ms), Mantenibilidad y HA

> **Notas del Orador:**  
> NOTAS DEL ORADOR (SLIDE 1 - PORTADA):  
> Buenas noches estimado docente asesor Ing. Enrique Lee Huamani y miembros del jurado evaluador. Hoy el Grupo 01 tiene el agrado de presentar la sustentacion final del proyecto LeoFit Solutions, un sistema de gestion de pedidos, facturacion electronica y despacho multicanal desarrollado para la empresa LeoFit Confecciones y Diseños Deportivos S.A.C. Esta presentacion sintetiza el rigor de ingenieria, las decisiones de arquitectura (ADRs), el cumplimiento normativo SUNAT, la integracion criptografica con pasarelas de pago y las 190 pruebas automatizadas que certifican la calidad del software.  

---

## Diapositiva 02
### 1. CONTEXTO DEL NEGOCIO

### Contexto Operativo y Diagnostico de la Empresa LeoFit

### LeoFit Solutions - Grupo 01 | UTP Curso Integrador II

### Sustentacion Semana 18

### Situacion Operativa Inicial (AS-IS)

- Ubicacion: Galeria El Rey de Gamarra, La Victoria, Lima.
- Canales Desconectados: Pedidos ingresados por WhatsApp, llamadas y ventas en tienda fisica.
- Registro Manual: Cuadernos fisicos y hojas de calculo sin validacion transaccional.
- Desfase de Stock: Venta de prendas inexistentes (sobreventa) con impacto reputacional grave.
- Despacho Dual Ineficiente: Retrasos en envios locales (motorizado) y provinciales (agencias).
- Falta de Trazabilidad Tributaria: Retrasos en la emision de boletas y facturas ante SUNAT.

### Solucion Implementada (TO-BE LeoFit)

- Plataforma Unificada PWA: Registro omnicanal de pedidos en menos de 40 segundos.
- Bloqueo Pesimista (FOR UPDATE): Garantia ACID en decremento de existencias textiles.
- Motor de Despacho Dual: Generacion automatica de hojas de ruta local y rotulos de encomienda.
- Integracion Fiscal Automatizada: Emision de comprobantes CPE conectados con OSE Nubefact.
- Pagos Digitales Auditados: Yape, Plin, Transferencias y Tarjetas con webhook timing-safe.
- Trazabilidad Publica: Tracking en tiempo real para el cliente final sin autenticacion pesada.

> **Notas del Orador:**  
> NOTAS DEL ORADOR (SLIDE 2 - CONTEXTO):  
> Comenzamos contextualizando la problematica real de la empresa LeoFit Confecciones en Gamarra. Antes de nuestro sistema, la gestion de pedidos se realizaba por canales informales y notas de papel, lo que generaba sobreventa de stock textil, perdida de encomiendas provinciales y retrasos tributarios. Nuestra solucion digitaliza el 100% de este ciclo mediante una Progressive Web App conectada a una API REST transaccional que garantiza consistencia ACID, eliminando la sobreventa y acelerando el despacho dual.  

---

## Diapositiva 03
### 2. ARQUITECTURA DE SOFTWARE

### Arquitectura Logica y Separacion de Capas (Clean Architecture)

### LeoFit Solutions - Grupo 01 | UTP Curso Integrador II

### Sustentacion Semana 18

### CAPA DE PRESENTACION (FRONTEND SPA / PWA)

React 19 + Vite 6 + TailwindCSS | Service Workers PWA con cache offline | jsPDF para rotulos y comprobantes  

### CAPA DE INTERFAZ Y ENRUTAMIENTO (EXPRESS API REST)

Middlewares Helmet, CORS, RateLimiter (express-rate-limit) | Controladores delgados | Validacion con Zod Schemas  

### CAPA DE DOMINIO Y APLICACION (CORE BUSINESS SERVICES)

OrderService, InventoryService, CulqiPaymentService, NubefactSunatService | Reglas de despacho dual y promociones  

### CAPA DE INFRAESTRUCTURA Y PERSISTENCIA (POSTGRESQL 16)

Pool nativo 'pg' | Consultas parametrizadas anti SQLi | Zona horaria America/Lima | 11 migraciones versionables  

> **Notas del Orador:**  
> NOTAS DEL ORADOR (SLIDE 3 - ARQUITECTURA LIMPIA):  
> La arquitectura del sistema sigue estrictamente los principios de Clean Architecture y separacion de responsabilidades. En el frontend implementamos React 19 con soporte PWA offline para que los operadores en taller o stand comercial no dependan de una conexion permanente. La API en Node.js 20 utiliza controladores delgados protegidos por validacion de esquemas Zod en tiempo de ejecucion, mientras que la logica de negocio esta aislada de la persistencia relacional en PostgreSQL 16.  

---

## Diapositiva 04
### 3. DECISIONES DE ARQUITECTURA (ADR)

### ADR-001: Justificacion de Render + Neon PostgreSQL frente a AWS

### LeoFit Solutions - Grupo 01 | UTP Curso Integrador II

### Sustentacion Semana 18

### Por que Render + Neon en Fase MVP?

- Eficiencia de Costos: $0.00 a $14.00 USD/mes vs $95-$140 USD en AWS desde el dia 1.
- Time-to-Market Inmediato: Despliegue declarativo automatizado via render.yaml en < 2 horas.
- Cero Sobrecarga DevOps: SSL administrado automaticamente, auto-heal de contenedores Docker.
- Base de Datos Serverless: Neon v16 escala CPU y RAM por demanda con branching instantaneo.
- Cero Vendor Lock-in: Persistencia ANSI PostgreSQL estandar; 100% portable a AWS Aurora/RDS.

### El Desafio de AWS en Etapas Iniciales

- Costo Fijo Ineludible: NAT Gateway ($32.40/mes) + ALB ($18.00/mes) + RDS base ($18.00/mes).
- Complejidad de Red: Mantenimiento de VPC, subredes publicas/privadas, IGW, Route Tables e IAM.
- Desperdicio en Tráfico Inicial: En fase de validacion academica o piloto comercial temprano, el costo de red no genera ROI directo.
- Decision Formal: Se adopta Render y Neon para validacion y se fijan umbrales formales de migracion hacia AWS.

> **Notas del Orador:**  
> NOTAS DEL ORADOR (SLIDE 4 - ADR-001):  
> Esta lamina responde a la primera gran interrogante del jurado: ¿Por que Render y Neon y no AWS desde el inicio? La respuesta de ingenieria es contundente: costo operativo y velocidad de despliegue. En AWS, la sola existencia de componentes de red como el NAT Gateway y el Application Load Balancer imponen un costo base superior a los $95 dolares mensuales, incluso con tráfico cero. Para un MVP o validacion piloto, Render y Neon ofrecen el mismo motor PostgreSQL 16 con costo cero a 14 dolares, sin riesgo de vendor lock-in.  

---

## Diapositiva 05
### 3. DECISIONES DE ARQUITECTURA (ADR)

### Matriz Comparativa de Criterios y Escenarios de Costo

### LeoFit Solutions - Grupo 01 | UTP Curso Integrador II

### Sustentacion Semana 18

### Comparacion Rigurosa de Infraestructura (Render+Neon vs AWS Nativo)

CRITERIO                   | RENDER + NEON SERVERLESS          | AWS NATVO (ECS + AURORA)  
--------------------------------------------------------------------------------------------------------------------
Tiempo de Despliegue       | < 2 horas (Declarativo en Git)    | 12 - 24 horas (Terraform / CloudFormation)  
Costo Mensual Inicial      | $0.00 a $14.00 USD / mes          | $95.00 a $140.00 USD / mes (Costo fijo)  
Carga Operativa (DevOps)   | Minima (PaaS administrado)        | Media-Alta (Gestion de parches, IAM, SG)  
SLA de Disponibilidad      | 99.9% (Admisible en MVP)          | 99.99% (Multi-AZ empresarial)  
Riesgo de Lock-in          | Nulo (PostgreSQL 16 nativo)       | Medio (Dependencia de Secrets/IAM roles)  
Backups y Restauracion     | Point-in-Time Restore (PITR)      | Automated Snapshots Multi-AZ  
Latencia de Red a Lima     | ~70 - 85 ms (US-East Edge CDN)    | ~65 - 75 ms (us-east-1 N. Virginia)  
  
ESCENARIOS ECONOMICOS:  
- Escenario 1 (MVP / Sustentacion): Render+Neon = $0.00 USD | AWS = $110.00 USD (Ahorro del 100%)
- Escenario 2 (Crecimiento Comercial): Render+Neon = $26.00 USD | AWS = $195.00 USD
- Escenario 3 (Alta Escala >25k usuarios): AWS resulta mas eficiente por economia de escala.

> **Notas del Orador:**  
> NOTAS DEL ORADOR (SLIDE 5 - COMPARATIVA):  
> En esta matriz demostramos que evaluamos ambas opciones con criterios formales de ingenieria. En tiempo de despliegue, Render y Neon nos permitieron iterar en minutos. En cuanto a latencia, la diferencia hacia Lima es de apenas 10 milisegundos, totalmente imperceptible frente al tiempo de red general. Demostramos ademas que la migracion hacia AWS esta planificada economicamente para cuando el negocio justifique el costo fijo.  

---

## Diapositiva 06
### 3. DECISIONES DE ARQUITECTURA (ADR)

### Disparadores Cuantitativos para la Migracion hacia AWS

### LeoFit Solutions - Grupo 01 | UTP Curso Integrador II

### Sustentacion Semana 18

### 1. CONCURRENCIA Y TRAFICO

- Trafico sostenido superior a 50 RPS (solicitudes por segundo) durante mas de 15 minutos.
- Base activa superior a 5,000 usuarios activos diarios (DAU).
- Gatillo: Escalamiento horizontal masivo en ECS Fargate.

### 2. GOBERNANZA Y COMPLIANCE

- Exigencia corporativa de certificacion PCI-DSS Nivel 1 directa en servidores propios.
- Cifrado con llaves administradas por hardware propio (AWS KMS CloudHSM).
- Requisito de interconexion bancaria privada (AWS PrivateLink).

### 3. ACUERDOS DE NIVEL DE SERVICIO (SLA)

- Compromiso contractual B2B de disponibilidad superior al 99.95% con penalizacion financiera.
- Necesidad de conmutacion por error automatica Multi-AZ en menos de 30 segundos.
- Despliegue de replica de almacenamiento sincrono en Aurora.

### 4. EFICIENCIA FINANCIERA

- Cuando la factura combinada de Render y Neon supere los $300.00 USD/mes.
- En ese punto de inflexion, los contratos de reserva (Savings Plans) de AWS ofrecen un costo menor por transaccion procesada.

> **Notas del Orador:**  
> NOTAS DEL ORADOR (SLIDE 6 - UMBRALES DE MIGRACION):  
> Un arquitecto senior no se casa con un proveedor; define disparadores cuantitativos. En el documento ADR-001 definimos que LeoFit migrara a AWS cuando ocurra cualquiera de cuatro eventos: superar 50 peticiones por segundo sostenidas, requerir certificacion PCI Nivel 1 con hardware HSM, exigir un SLA del 99.99% Multi-AZ, o cuando la facturacion de Render supere los 300 dolares al mes.  

---

## Diapositiva 07
### 4. ARQUITECTURA OBJETIVO AWS

### ADR-002: Maquetacion Objetivo 100% Nativa en AWS

### LeoFit Solutions - Grupo 01 | UTP Curso Integrador II

### Sustentacion Semana 18

### Diseno C4 Nivel Contenedor bajo el AWS Well-Architected Framework

### Perimetro y CDN

- AWS WAF: Proteccion contra inyeccion SQL, XSS y Rate Limiting perimetral.
- Amazon CloudFront: CDN global con terminacion TLS 1.3.
- Amazon S3: Almacenamiento seguro del frontend estatico SPA React.
- Certificados ACM: SSL administrado con renovacion automatica.

### Computo y Balanceo

- Application Load Balancer: Health checks activos en /api/health.
- Amazon ECS con Fargate: Contenedores Docker serverless en subredes privadas.
- Auto Scaling: Escalado automatico por CPU y consumo de memoria.
- Despliegue Multi-AZ: Distribucion en us-east-1a y us-east-1b.

### Datos y Servicios

- Amazon Aurora PostgreSQL: Motor relacional transaccional Multi-AZ con failover automatico.
- ElastiCache Redis: Cache de sesiones y limite de tasa distribuido.
- AWS Secrets Manager: Rotacion segura de credenciales de BD y API keys.
- Amazon CloudWatch: Alarmas APM y centralizacion de logs.

> **Notas del Orador:**  
> NOTAS DEL ORADOR (SLIDE 7 - ADR-002 ARQUITECTURA AWS):  
> Esta lamina responde a la segunda pregunta del jurado: ¿Como maquetarian el sistema en una arquitectura 100% AWS? El diseno propuesto en el ADR-002 sigue los 6 pilares de AWS Well-Architected. En el perimetro colocamos CloudFront y AWS WAF para filtrar ataques DDoS y SQL injection antes de que lleguen a la red. En la capa de aplicacion usamos ECS Fargate en subredes privadas aisladas sin acceso directo a internet, y en la base de datos Aurora PostgreSQL Multi-AZ con replicacion sincronica de almacenamiento.  

---

## Diapositiva 08
### 4. ARQUITECTURA OBJETIVO AWS

### Topologia de Red VPC y Aislamiento por Zonas de Disponibilidad

### LeoFit Solutions - Grupo 01 | UTP Curso Integrador II

### Sustentacion Semana 18

### Segmentacion Estricta de Red (CIDR: 10.0.0.0/16 en Region us-east-1)

TOPOLOGIA DE RED EN 2 AVAILABILITY ZONES (AZ-a y AZ-b):  
--------------------------------------------------------------------------------------------------------------------
1. SUBREDES PUBLICAS (10.0.1.0/24 y 10.0.2.0/24):  
   - Alojan exclusivamente el Application Load Balancer (ALB) y el NAT Gateway.  
   - Unicas subredes con ruta directa hacia el Internet Gateway (IGW).  
  
2. SUBREDES PRIVADAS DE COMPUTO (10.0.10.0/24 y 10.0.11.0/24):  
   - Alojan los contenedores Docker de la API en AWS Fargate.  
   - Salida a internet unicamente para consumir APIs externas (Culqi, Nubefact) via NAT Gateway.  
   - Trafico entrante restringido exclusivamente al Security Group del ALB (Puerto 3001).  
  
3. SUBREDES PRIVADAS DE DATOS (10.0.20.0/24 y 10.0.21.0/24):  
   - Alojan la base de datos Aurora PostgreSQL y los nodos de ElastiCache Redis.  
   - Totalmente aisladas: SIN ruta a internet ni asignacion de IPs publicas.  
   - Trafico entrante admitido unicamente desde el Security Group de Fargate en el puerto 5432.  

> **Notas del Orador:**  
> NOTAS DEL ORADOR (SLIDE 8 - RED VPC):  
> La seguridad de red se diseno bajo el principio de defensa en profundidad. Dividimos la VPC en tres niveles de subredes a traves de dos zonas de disponibilidad (us-east-1a y us-east-1b). Las tareas de Fargate nunca tienen direcciones IP publicas, y la base de datos se encuentra en subredes de datos sin salida a internet ni ruta al exterior, eliminando vectores de ataque directo por red.  

---

## Diapositiva 09
### 4. ARQUITECTURA OBJETIVO AWS

### Ecosistema de Complementos: Lo que AWS NO Conviene Construir

### LeoFit Solutions - Grupo 01 | UTP Curso Integrador II

### Sustentacion Semana 18

### PASARELA DE PAGOS: CULQI / NIUBIZ

- Por que NO en AWS: AWS Payment Cryptography es hardware HSM para bancos, no es una pasarela adquirente en Peru.
- Solucion: Culqi y Niubiz permiten cobro en Soles con Yape, Plin y tarjetas locales con liquidacion bancaria directa.

### FACTURACION SUNAT: OSE NUBEFACT

- Por que NO en AWS: AWS no cuenta con homologacion ante SUNAT para UBL 2.1 ni firma digital INDECOPI.
- Solucion: Un OSE autorizado (Nubefact/Efact) absorbe los cambios tributarios constantes y el riesgo legal.

### AUTENTICACION Y ROLES: JWT PROPIO / AUTH0

- Por que NO AWS Cognito: Curva de complejidad excesiva para esquemas de roles simples (admin/operador).
- Solucion: Manejo de JWT sin estado con verificacion fail-fast y bcrypt reduce complejidad y costo.

### BUSQUEDA TEXTIL: POSTGRESQL NATIVO

- Por que NO OpenSearch: AWS OpenSearch tiene un costo base de ~$180 USD/mes inviable para <10,000 SKUs.
- Solucion: Indices GIN y Trigram en PostgreSQL resuelven busqueda por codigo, color y talla con latencia <5ms.

> **Notas del Orador:**  
> NOTAS DEL ORADOR (SLIDE 9 - COMPLEMENTOS NO AWS):  
> Un buen arquitecto sabe que construir y que comprar o integrar. Reinventar una pasarela adquirente en AWS en lugar de usar Culqi o Niubiz es un grave error de negocio en Peru, porque AWS no procesa Yape ni liquida soles a cuentas del BCP. Del mismo modo, implementar la firma UBL 2.1 de SUNAT en AWS desde cero en lugar de delegar en un OSE como Nubefact implicaria certificar una entidad de firma digital ante INDECOPI, lo cual esta fuera del alcance de una empresa comercial.  

---

## Diapositiva 10
### 5. INTEGRACION TRIBUTARIA SUNAT

### Cumplimiento Normativo SUNAT para Comprobantes Electronicos

### LeoFit Solutions - Grupo 01 | UTP Curso Integrador II

### Sustentacion Semana 18

### Matriz de Requisitos Legales y Marco Regulatorio Vigente

REQUISITO LEGAL           | BASE LEGAL SUNAT         | IMPLEMENTACION TECNICA EN LEOFIT  
--------------------------------------------------------------------------------------------------------------------
Estandar UBL 2.1          | RS 097-2012 y 117-2017   | Delegado al OSE Nubefact via payload JSON estructurado.  
Firma Digital INDECOPI    | Ley 27269 / RS 097-2012  | Certificado digital acreditado inyectado por Nubefact.  
Envio a OSE Homologado    | RS 117-2017 / 252-2019   | Endpoint POST /api/v1/invoice con token de seguridad.  
Plazo Maximo de Envio     | RS 193-2020 / 003-2023   | Emision sincrona al confirmar el pedido (< 3 segundos).  
Condicion de RUC          | TUO Codigo Tributario    | Validacion previa de RUC 'ACTIVO' y 'HABIDO'.  
Desglose de IGV (18%)     | Ley del IGV (D.S. 055)   | Calculo matematico exacto de Base Imponible + Impuesto.  
Representacion Impresa    | Anexo RS 097-2012        | Generacion PDF con Codigo Hash SHA-256 y Codigo QR oficial.  
Persistencia Tributaria   | Art. 87 Codigo Tribut.   | Tabla 'invoices' registra serie, correlativo, hash y CDR.  

> **Notas del Orador:**  
> NOTAS DEL ORADOR (SLIDE 10 - NORMATIVA SUNAT):  
> Esta seccion responde a la tercera pregunta del jurado sobre el cumplimiento de comprobantes de pago electronicos (CPE). En el Peru, la emision esta regida por las Resoluciones de Superintendencia N.° 097-2012 y 117-2017. LeoFit cumple con el estandar internacional OASIS UBL 2.1 y la firma digital homologada ante INDECOPI a traves del OSE Nubefact. El sistema desglosa con precision el 18% del IGV y almacena el codigo hash y el CDR de recepcion en la tabla 'invoices'.  

---

## Diapositiva 11
### 5. INTEGRACION TRIBUTARIA SUNAT

### Flujo Tecnico de Emision y Respuestas de Error OSE/SUNAT

### LeoFit Solutions - Grupo 01 | UTP Curso Integrador II

### Sustentacion Semana 18

### PASO 1: ORDEN

- Cliente confirma pedido.
- Selecciona Boleta o Factura.
- Ingresa DNI (8 digitos) o RUC (11 digitos).
- Backend valida consistencia del documento receptor.
- Se reserva correlativo en base de datos.

### PASO 2: PAYLOAD

- Construccion JSON fiscal en nubefact.service.ts.
- Desglose por items: valor unitario, total y tributos.
- Inyeccion de token de seguridad de comercio.
- Manejo de moneda (PEN) y tipo de operacion onerosa.

### PASO 3: OSE Y SUNAT

- OSE valida esquema XSD y genera XML UBL 2.1.
- Aplica firma digital con certificado INDECOPI.
- Remite a servidores centrales de SUNAT.
- Obtiene Constancia de Recepcion (CDR codigo 0).

### PASO 4: ENTREGA

- Backend guarda hash y enlaces en BD atómica.
- Cliente recibe confirmacion en pantalla.
- Descarga inmediata de PDF con Codigo QR oficial.
- Modo simulado funcional en desarrollo sin llaves.

> **Notas del Orador:**  
> NOTAS DEL ORADOR (SLIDE 11 - FLUJO FACTURACION):  
> En esta lamina explicamos el flujo de datos exacto. Cuando el cliente registra su compra, el backend genera el payload en nubefact.service.ts y llama al OSE. El OSE valida las reglas tributarias, firma digitalmente el XML y obtiene la constancia CDR de SUNAT. Si el sistema no cuenta con credenciales en desarrollo, conmuta limpiamente a un simulador que genera un hash demostrativo para permitir la prueba funcional de punta a punta sin arrojar excepciones.  

---

## Diapositiva 12
### 6. PASARELA DE PAGOS Y PCI-DSS

### Pasarela de Pagos: Operacion en Sandbox frente a Produccion

### LeoFit Solutions - Grupo 01 | UTP Curso Integrador II

### Sustentacion Semana 18

### Ambiente Sandbox (Pruebas - Estado Actual)

- Cargo Simulado: No hay debito real de fondos ni liquidacion interbancaria.
- Tarjetas de Prueba: Numeros provistos por Culqi (4111...) con fechas futuras arbitrarias.
- Credenciales de Prueba: Llaves publicas pk_test y privadas sk_test.
- Fallback Inteligente: Si falta la llave secreta, culqi.ts conmuta a mock local (chr_mock_).
- Cero Riesgo Financiero: Permite validar todo el flujo de cobro sin costo transaccional.

### Pase a Produccion Comercial (En Vivo)

- Proceso KYC Bancario: RUC activo, ficha RUC y cuenta corriente de LeoFit en BCP o BBVA.
- Emision de Llaves Live: Reemplazo de variables de entorno por pk_live y sk_live.
- Descuento Real: Debito inmediato de fondos en cuentas de clientes con retencion legal.
- Comision Comercial: Tarifa de adquirencia pactada (aprox. 3.44% + $0.30 USD + IGV).
- Codigo 100% Preparado: Cero cambios de codigo requeridos; solo configuracion de entorno.

> **Notas del Orador:**  
> NOTAS DEL ORADOR (SLIDE 12 - PAGOS SANDBOX VS PROD):  
> La cuarta pregunta del jurado indaga sobre la realidad de los pagos y sus limitantes. En el repositorio implementamos la pasarela Culqi en modo Sandbox. Esto significa que el flujo logico de cobro y tokenizacion es 100% real, pero las transacciones utilizan tarjetas de prueba sin debitar dinero. El paso a produccion no requiere reescribir software: la logica ya contempla las llaves de produccion; solo se requiere culminar el tramite administrativo de KYC bancario de la empresa LeoFit para activar las llaves live.  

---

## Diapositiva 13
### 6. PASARELA DE PAGOS Y PCI-DSS

### Seguridad Criptografica, Webhooks HMAC y Cumplimiento PCI-DSS

### LeoFit Solutions - Grupo 01 | UTP Curso Integrador II

### Sustentacion Semana 18

### Cumplimiento PCI-DSS (Cuestionario SAQ A)

- Tokenizacion en el Cliente: El formulario web utiliza el SDK Culqi JS directamente en el navegador del usuario.
- Aislamiento Total del PAN: Los 16 digitos de la tarjeta y el CVV NUNCA tocan el servidor de LeoFit.
- Reduccion de Alcance: Al no almacenar datos de tarjetahabientes, LeoFit califica bajo el estandar SAQ A de PCI-DSS v4.0.
- Esto exime a LeoFit de someter su infraestructura a costosas auditorias de certificacion de red Nivel 1.

### Validacion de Webhooks con HMAC-SHA256

- Endpoint: POST /api/webhooks/payment en paymentWebhook.controller.ts.
- Firma Criptografica: Se verifica la firma enviada por la pasarela con el secreto del comercio.
- Proteccion contra Timing Attacks: Implementacion de crypto.timingSafeEqual en Node.js.
- Idempotencia Transaccional: Verificacion de si la transaccion ya fue procesada antes de actualizar la BD.
- Actualizacion Atomica: Transicion del pedido a 'CONFIRMADO' y estado de pago 'PAGADO'.

> **Notas del Orador:**  
> NOTAS DEL ORADOR (SLIDE 13 - PCI-DSS Y HMAC):  
> Desde la perspectiva de seguridad de la informacion, implementamos tokenizacion del lado del cliente. Esto nos permite acogernos al cuestionario SAQ A de PCI-DSS, garantizando que ningun dato confidencial de tarjeta quede registrado en logs o bases de datos de LeoFit. Adicionalmente, los webhooks asincronos son validados con firmas HMAC-SHA256 utilizando comparacion de tiempo constante mediante crypto.timingSafeEqual, neutralizando ataques de temporizacion.  

---

## Diapositiva 14
### 7. BASE DE DATOS Y PERSISTENCIA

### Modelo Relacional (BCNF) y Resolucion de Zona Horaria

### LeoFit Solutions - Grupo 01 | UTP Curso Integrador II

### Sustentacion Semana 18

### Normalizacion y Consistencia ACID

- Tercera Forma Normal (3FN / BCNF): Esquema relacional con 11 tablas maestras y de transaccion.
- Tablas Clave: products, product_variants, orders, order_items, payments, invoices, audit_logs.
- Integridad Referencial: Claves foraneas con eliminacion restringida (ON DELETE RESTRICT).
- Bloqueo Pesimista (SELECT FOR UPDATE): Evita carreras criticas (race conditions) en compras concurrentes.
- Migraciones Versionables: 11 migraciones secuenciales en TypeScript reproducibles en CI/CD.

### Configuracion de Zona Horaria 'America/Lima'

- Problematica: En servidores cloud (Render/Neon en US-East), la hora por defecto es UTC (+00:00).
- Impacto: Pedidos nocturnos en Lima se registraban con la fecha del dia siguiente, alterando auditorias y reportes contables.
- Solucion en backend/src/config/database.ts: Inyeccion obligatoria de timezone al inicializar el pool:
  client.query("SET timezone = 'America/Lima'")  
- Garantia: 100% de marcas de tiempo (created_at) persisten en horario oficial peruano (UTC-5).

> **Notas del Orador:**  
> NOTAS DEL ORADOR (SLIDE 14 - BASE DE DATOS):  
> En la base de datos PostgreSQL 16 aplicamos estricta normalizacion en Forma Normal de Boyce-Codd. Un aporte tecnico critico que resolvimos fue la discrepancia de zona horaria: al estar los servidores de Neon en Estados Unidos, los pedidos se registraban en horario UTC, lo que causaba que pedidos hechos despues de las 7 pm tuvieran la fecha del dia siguiente. Configuramos el pool de conexiones para que cada sesion ejecute obligatoriamente 'SET timezone = America/Lima', garantizando concordancia contable con la SUNAT.  

---

## Diapositiva 15
### 8. CALIDAD DE RENDIMIENTO (SEMANA 14)

### Calidad de Rendimiento (ISO/IEC 25010:2023): Percentiles y Senales Doradas SRE

### LeoFit Solutions - Grupo 01 | UTP Curso Integrador II

### Sustentacion Semana 18

### p50: 120ms | p95: 280ms/480ms

### PERCENTIL 95 (P95) EN 1 Y 10 USUARIOS (SLO < 700 ms)

### 0.00% ERRORES (SLO < 0.1%)

### TASA DE FALLOS EN PRUEBAS STEADY Y SOAK (4 HORAS)

### CPU < 25% | RAM 185 MB

### SATURACION SRE < 70% EN CARGA COMERCIAL NOMINAL

### Las Cuatro Senales Doradas de SRE (Google)

- 1. Latencia por Percentiles: El promedio oculta la cola larga (GC V8 y locks). p95 = 480ms en carga comercial.
- 2. Trafico: 19 req/s nominales; capacidad maxima demostrada de 45 req/s en tier base de Render.
- 3. Errores: 0.00% fallos transaccionales en 34,200 solicitudes (meta SRE < 0.10%).
- 4. Saturacion: CPU < 25% y memoria en 185 MB, respetando holgadamente el margen de saturacion (< 70%).

### Diagnostico de Cola Larga (p99) y Optimizacion B-Tree

- Causa de p99 en Spike (1,820 ms): Latencia transfronteriza RTT hacia Neon PostgreSQL (EE. UU.) y limites del pool.
- Optimizacion Inmediata: Creacion de indices compuestos B-Tree idx_orders_customer_created y idx_variants_stock.
- Resultado Medible: Reduccion del 64.2% en costo EXPLAIN ANALYZE (de 14.8 ms a 5.3 ms en ejecucion SQL).
- Accion Estructural AWS (ADR-002): Despliegue en misma VPC con RDS Multi-AZ, abatiendo RTT a < 1.5 ms.

| Tipo de Ensayo | Carga | Duracion | p50 (ms) | p95 (ms) | p99 (ms) | RPS | Errores % | Saturacion SRE | Evaluacion SLA |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Linea Base | 1 VU | 2 min | 120 ms | 280 ms | 410 ms | 2.8 r/s | 0.00% | CPU: 8% | RAM: 145 MB | Cumple (Holgado) |
| Steady-State | 10 VU | 30 min | 240 ms | 480 ms | 720 ms | 19.0 r/s | 0.00% | CPU: 24% | RAM: 185 MB | Cumple (< 700 ms) |
| Spike Test | 35 VU | 5 min | 620 ms | 1,400 ms | 1,820 ms | 45.2 r/s | 0.00% | CPU: 58% | RAM: 230 MB | Observado (Limite) |
| Soak Test | 8 VU | 4 horas | 225 ms | 460 ms | 680 ms | 16.0 r/s | 0.00% | CPU: 21% | RAM: 188 MB | Cumple (Sin fugas) |

> **Notas del Orador:**  
> NOTAS DEL ORADOR (SLIDE 15 - RENDIMIENTO SEMANA 14):  
> En la evaluacion de rendimiento bajo ISO/IEC 25010:2023 aplicamos el rigor de la ingenieria de confiabilidad de sitios (Google SRE). En primer lugar, demostramos por que el promedio aritmetico oculta la realidad: un promedio puede ser bajo mientras la cola larga p99 revela pausas de recoleccion de basura o contencion de bloqueos. Por ello medimos percentiles: mediana p50 de 120 ms, p95 de 280 ms con 1 usuario, y 480 ms con 10 usuarios concurrentes sostenidos en una prueba Steady-State de 30 minutos, manteniendo 0% de errores frente a un SLO de 700 ms. Ademas, ejecutamos una prueba Soak de 4 horas continuas que certifico la ausencia total de fugas de memoria en Node.js. En el ensayo de Spike identificamos que la latencia p99 se debio a la distancia con la base de datos en Estados Unidos; optimizamos indices B-Tree reduciendo el costo SQL en 64.2%, y dejamos justificada la arquitectura de baja latencia en AWS.  

---

## Diapositiva 16
### 8. CALIDAD DE RENDIMIENTO (SEMANA 14)

### Flexibilidad (ISO/IEC 25010:2023): Adaptabilidad, Escalabilidad y Resiliencia

### LeoFit Solutions - Grupo 01 | UTP Curso Integrador II

### Sustentacion Semana 18

ISO/IEC 25010:2023 — FLEXIBILITY: ADAPTAR = CONTEXTO / ENTORNO  |  ESCALAR = DEMANDA ATENDIDA SIN DEGRADACION  

### Adaptabilidad (Portabilidad de Entorno)

- Definicion ISO: Capacidad de ajustarse a diferentes entornos operativos y de red sin alterar el codigo fuente.
  
- The Twelve-Factor App (Factor III - Configuracion):
  * 100% de credenciales, puertos y endpoints inyectados como variables (.env, Render Secrets, AWS Parameter Store).  
  
- Clean Architecture Desacoplada:
  * Capa Controller: Expone contratos REST OpenAPI.  
  * Capa Service: Encapsula 100% de logica comercial pura.  
  * Capa Repository: Interfaz agnostica de persistencia SQL.  
  
- Portabilidad Comprobada: Mismo codigo fuente opera en Local Docker Compose, Staging Render y AWS ECS Fargate.

### Escalabilidad Elastica y Patrones de Resiliencia

- Principio Rector: Optimizar consultas y bloqueos antes de escalar.
  
- Patrones de Resiliencia Cloud Implementados:
  * Circuit Breaker (Cortacircuito): Fail-fast en 5 fallos ante caidas de SUNAT o WhatsApp para no bloquear el Event Loop.  
  * Bulkhead (Aislamiento): Separacion de pools; ordenes transaccionales aisladas de lecturas de catalogo.  
  * Retry con Exponential Backoff y Jitter: Reintentos con dispersion aleatoria (+-20%) para evitar 'thundering herd'.  
  * Rate Limiting / Load Shedding: 100 req/min y descarte selectivo de carga no esencial al superar 75% CPU.  
  
- Auto-Scaling: Disparo a > 70% CPU, tiempo de provisionamiento 42s y enfriamiento (cooldown) de 300s para evitar flapping.

> **Notas del Orador:**  
> NOTAS DEL ORADOR (SLIDE 16 - FLEXIBILIDAD Y RESILIENCIA):  
> En la ISO/IEC 25010:2023, la caracteristica Flexibility unifica a la antigua portabilidad con la adaptabilidad y la escalabilidad. Adaptabilidad responde a mover el software entre entornos: lo resolvemos mediante Clean Architecture y Twelve-Factor App, donde cambiar de base de datos o de nube implica cero modificaciones en las reglas comerciales. Por otro lado, la escalabilidad no se limita a poner mas servidores: aplicamos el principio de optimizar antes de escalar, e implementamos patrones formales de resiliencia: Circuit Breakers que cortan llamadas a servicios externos lentos con fail-fast, Bulkhead para aislar el pool de compras respecto a reportes, Retry con backoff exponencial y jitter para evitar avalanchas, y Rate Limiting con Load Shedding que garantiza que el checkout transaccional nunca se caiga.  

---

## Diapositiva 17
### 9. CALIDAD DE MANTENIBILIDAD (SEMANA 15)

### Calidad de Mantenibilidad (ISO/IEC 25010:2023): Modularidad y Dependencias

### LeoFit Solutions - Grupo 01 | UTP Curso Integrador II

### Sustentacion Semana 18

### Anti-Patron Monolitico

- Archivo gigante tipo app.py que concentra:
  * Rutas HTTP y endpoints  
  * Logica de negocio y descuentos  
  * Consultas SQL directas concatenadas  
  * Renderizado de vistas y plantillas  
  
- Graves Consecuencias:
  * Alto acoplamiento espagueti  
  * Cambiar un precio rompe la facturacion  
  * Imposibilidad de probar con mocks  
  * Deuda tecnica inmanejable.  

### Direccion de Dependencias (Clean)

- Principio de Inversion de Dependencias (DIP):
  
  [ Infraestructura (Express/SQL/Zod) ]  
                  | (depende de)  
                  v  
  [ Casos de Uso / Servicios (order.service) ]  
                  | (depende de)  
                  v  
  [ Dominio Puro (models/ - Sin Frameworks) ]  
  
- Beneficio Crucial:
  El dominio comercial de LeoFit no importa nada de Express, Postgres ni librerias cloud.  

### Reusabilidad Transversal (DRY)

- Cero Duplicidad de Codigo:
  
- Middleware RBAC (requireRole):
  Protege 14 endpoints administrativos.  
  
- Idempotencia RFC 8785:
  Blindaje en ordenes, cobros y anulaciones.  
  
- Motor PDF Vectorial:
  Genera rotulos de despacho y boletas.  
  
- Esquemas Zod Reutilizables:
  Validacion estricta en frontend y backend.  

> **Notas del Orador:**  
> NOTAS DEL ORADOR (SLIDE 17 - MANTENIBILIDAD SEMANA 15):  
> En la Semana 15 analizamos la mantenibilidad segun ISO/IEC 25010:2023. Separar archivos en carpetas no basta si las dependencias estan desordenadas. En LeoFit aplicamos Clean Architecture con una regla de dependencia estricta: las dependencias apuntan hacia el centro, hacia el Dominio Puro. Nuestras entidades y reglas de negocio no conocen Express, ni PostgreSQL, ni bibliotecas externas. Superamos por completo el anti-patron monolitico tipo app.py, y logramos una reusabilidad comprobada: un unico middleware de roles protege 14 rutas, la idempotencia RFC 8785 blinda toda operacion transaccional, y el generador de PDF atiende tanto a logistica como a tesoreria.  

---

## Diapositiva 18
### 9. CALIDAD DE MANTENIBILIDAD (SEMANA 15)

### Mantenibilidad: Modificabilidad, Metricas Objetivas y Testabilidad TDD

### LeoFit Solutions - Grupo 01 | UTP Curso Integrador II

### Sustentacion Semana 18

### Modificabilidad y Analisis de 'Blast Radius'

- Definicion ISO: Efectividad y eficiencia con que el software se modifica sin introducir defectos colaterales.
  
- Caso Real CHG-01 en LeoFit:
  * Requerimiento: Descuento textil del 10% en compras al por mayor (>= 6 prendas).  
  * Archivo Modificado: Exclusivamente src/services/order.service.ts (calculateOrderTotals).  
  * Impacto en Controladores y Rutas: 0 lineas modificadas.  
  * Impacto en Esquema de BD: 0 alteraciones en tablas relacionales.  
  
- Metrica de 'Blast Radius' (Radio de Impacto):
  * Solo 2 archivos tocados: el servicio de negocio y su suite de pruebas unitarias.  
  * Trazabilidad inmutable en Git con commit semantico feat(orders).  

### Metricas Objetivas y Piramide de Pruebas (TDD)

- Piramide de Pruebas Automatizadas (194 Tests Totales):
  * Base: 140 pruebas unitarias rapidas (< 50ms) con mocks en memoria.  
  * Centro: 44 pruebas de integracion con Supertest y base de datos.  
  * Cupide: 10 pruebas end-to-end y de contrato OpenAPI.  
  
- Metricas de Mantenibilidad Auditadas:
  * Complejidad Ciclomatica (McCabe): Valores de 1 a 3 en metodos core (umbral maximo optimo <= 4).  
  * Cobertura de Pruebas: 84.6% en servicios y 92.1% en calculos con Decimal.js.  
  
- Comprobacion Automatizada en CI/CD:
  * Bateria completa ejecuta en 42 segundos en GitHub Actions.  

> **Notas del Orador:**  
> NOTAS DEL ORADOR (SLIDE 18 - MODIFICABILIDAD, METRICAS Y TDD):  
> En modificabilidad y testabilidad presentamos evidencia con metricas cuantitativas. Para evaluar la modificabilidad, medimos el radio de impacto o 'blast radius': ante un cambio comercial real de descuentos por volumen, solo se modificaron 2 archivos en todo el repositorio: el archivo del servicio y su prueba unitaria, con cero impacto en controladores o base de datos. En mantenibilidad objetiva reportamos la complejidad ciclomatica de McCabe, situandonos en valores de 1 a 3, dentro del rango optimo menor a 4. Nuestra piramide de pruebas cuenta con 194 pruebas automatizadas con 100% de exito y una cobertura superior al 80% en las reglas de negocio criticas, ejecutandose de forma automatizada en el pipeline de GitHub Actions en 42 segundos.  

---

## Diapositiva 19
### 10. PROYECCION DE CONFIABILIDAD (SEMANA 16)

### Calidad de Confiabilidad: Alta Disponibilidad (HA vs HPC) y Tolerancia a Fallos

### LeoFit Solutions - Grupo 01 | UTP Curso Integrador II

### Sustentacion Semana 18

### HA: Alta Disponibilidad (High Availability)

- Enfoque: Operacion continua 24/7 sin caidas de servicio.
- Casos de Aplicacion: Banca digital, pasarelas de pago, comercio electronico y LeoFit.
- Mecanismos Clave: Redundancia activa, clúster de nodos, balanceo de carga y failover automatico ante contingencias.
- Meta LeoFit: Uptime proyectado del 99.9% anual.

### HPC: Computacion de Alto Rendimiento

- Enfoque: Maxima velocidad de procesamiento y calculo intensivo.
- Casos de Aplicacion: Entrenamiento de modelos IA (LLMs), bioinformatica, simulaciones sismicas.
- Arquitectura: Miles de GPUs/CPUs trabajando en paralelo sobre grandes volumenes (Petabytes).
- Diferencia: HPC prioriza calculo; HA prioriza tiempo activo 24/7.

### Tolerancia a Fallos en LeoFit

- PWA con Modo Offline: Service Workers almacenan cache estatico y catalogo textil para consultas sin conexion en Gamarra.
- Circuit Breakers y Reintentos: En colas de notificaciones WhatsApp y SUNAT ante indisponibilidad externa.
- Degradacion Elegante: Mensajes claros al usuario sin bloqueos de pantalla ni caidas fatales.

### Respaldo y Recuperacion (PITR)

- Respaldo Continuo en Neon PostgreSQL: Registro ininterrumpido de Write-Ahead Logs (WAL) en almacenamiento duradero.
- Point-in-Time Restore (PITR): Restauracion exacta a cualquier segundo previo ante corrupcion o incidente humano.
- Metricas de Continuidad: RPO (Recovery Point Objective) < 5 min; RTO (Recovery Time Objective) < 15 min.

> **Notas del Orador:**  
> NOTAS DEL ORADOR (SLIDE 19 - CONFIABILIDAD SEMANA 16):  
> Proyectando hacia la Semana 16, abordamos la calidad de confiabilidad segun ISO 25010. El docente nos planteo una distincion clave: servidores HPC frente a servidores HA. Mientras que HPC resuelve calculo intensivo masivo para modelos de IA con GPUs, sistemas de comercio y pedidos como LeoFit requieren arquitectura HA de Alta Disponibilidad 24/7, garantizando que el servicio nunca se detenga. En LeoFit aplicamos tolerancia a fallos mediante la PWA con Service Workers que permite operar offline en las galerias de Gamarra, y garantizamos recuperacion ante desastres con copias continuas Point-in-Time Restore en PostgreSQL, con un objetivo de punto de recuperacion menor a 5 minutos.  

---

## Diapositiva 20
### 11. TESTING Y CALIDAD (QA)

### Aseguramiento de Calidad: 194 Pruebas Automatizadas (100% OK)

### LeoFit Solutions - Grupo 01 | UTP Curso Integrador II

### Sustentacion Semana 18

### 194

### TOTAL PRUEBAS APROBADAS (0 FALLOS)

### 125

### PRUEBAS BACKEND (JEST + SUPERTEST)

### 69

### PRUEBAS FRONTEND (VITEST + RTL)

### Distribucion de Suites de Prueba Automatizadas

- Seguridad y OWASP Top 10 (security.test.ts): Inyeccion SQL, XSS, headers Helmet y validacion Zod.
- Autenticacion y Matriz RBAC (auth.test.ts): Control estricto de roles admin y operador (401/403).
- Integracion e Interoperabilidad (integration_external.test.ts): Contrato OpenAPI y webhooks HMAC.
- Transaccionalidad de Pedidos (orders.test.ts): Bloqueo FOR UPDATE y decremento atomico de stock.
- Usabilidad y Accesibilidad (usability_iso25010.test.ts): Navegacion por teclado y renderizado WCAG.
- Generacion de Documentos (pdfGenerator.test.ts): Creacion de rotulos de envio y comprobantes PDF.

> **Notas del Orador:**  
> NOTAS DEL ORADOR (SLIDE 20 - TESTING QA):  
> La confiabilidad de LeoFit no es declarativa; esta demostrada con 194 pruebas automatizadas con 100% de exito. En el backend corremos 125 pruebas con Jest que validan seguridad OWASP, inyeccion SQL, tokens manipulados y concurrencia. En el frontend ejecutamos 69 pruebas con Vitest y Testing Library que certifican el renderizado de formularios, generacion de PDFs de despacho y guardas de autenticacion en la interfaz.  

---

## Diapositiva 21
### 11. TESTING Y CALIDAD (QA)

### Marco Integral ISO/IEC 25010:2023 y Capacidad de Interaccion (SUS)

### LeoFit Solutions - Grupo 01 | UTP Curso Integrador II

### Sustentacion Semana 18

### Las 9 Caracteristicas de ISO/IEC 25010:2023

- 1. Functional Suitability: 100% completitud (10 RF verificados).
- 2. Performance Efficiency: p95 = 480 ms y sat. < 25% (SLA < 700 ms).
- 3. Compatibility: Coexistencia Docker certificada sin degradacion.
- 4. Interaction Capability: Evaluacion SUS 88.5/100 y WCAG 2.1 AA.
- 5. Reliability: Tolerancia a fallos PWA y DRP con RTO de 3.2s.
- 6. Security: Autenticacion JWT HS256, Bcrypt y HMAC-SHA256.
- 7. Maintainability: Clean Architecture, complejidad 1-3 y TDD.
- 8. Flexibility: Adaptabilidad multi-entorno y escalabilidad.
- 9. Safety: Ausencia de dano financiero (cero sobreventas ACID).

### Capacidad de Interaccion y Accesibilidad WCAG

- System Usability Scale (SUS): Puntaje obtenido de 88.5 / 100 (Grado A - Excelente, Percentil 96%).
- Estudio Empirico en Gamarra: Evaluacion con 5 participantes reales en el stand comercial de LeoFit.
- Agilidad Operativa: Reduccion del tiempo de pedido de 310s a 38.2s (mejora del 87.6%).
- Accesibilidad WCAG 2.1 AA/AAA: Contrastes de color certificados desde 5.42:1 hasta 17.8:1.
- Navegacion Accesible: 100% de acciones operables exclusivamente mediante teclado (Tab/Enter).
- Diseno Responsivo: Adaptabilidad probada en moviles Android, iOS y pantallas desktop.

> **Notas del Orador:**  
> NOTAS DEL ORADOR (SLIDE 21 - ISO 25010:2023):  
> Cerramos el modulo de calidad respaldando la totalidad del software bajo las 9 caracteristicas de la ISO/IEC 25010:2023. Destacamos la incorporacion de Safety, que garantiza la ausencia de danos economicos para la empresa mediante consistencia ACID estricta. En Interaction Capability, nuestro estudio con la metodologia estandar SUS alcanzo 88.5 sobre 100 con usuarios reales de Gamarra, reduciendo el tiempo de atencion en 87.6%. Cumplimos ademas con accesibilidad web WCAG 2.1 con contrastes de hasta 17.8 a 1, optimizados para operar en condiciones de alta luminosidad en el stand comercial.  

---

## Diapositiva 22
### 12. DESPLIEGUE Y OPERACION

### Validacion y Despliegue en Vivo en la Nube (Cloud Staging)

### LeoFit Solutions - Grupo 01 | UTP Curso Integrador II

### Sustentacion Semana 18

### FRONTEND PWA

- URL Publica: Enlace en GitHub Pages con certificado SSL global.
- Edge CDN: Distribucion geografica rapida de activos.
- Soporte PWA: Instalable en dispositivos Android, iOS y Windows.
- Cache Estrategico: Service Workers almacenan catalogo base para consulta sin conexion.

### BACKEND API

- Hosting: Render Cloud Platform con Dockerfile de produccion.
- Endpoint Health: /api/health retorna HTTP 200 con estado de BD.
- Documentacion Viva: OpenAPI y Swagger integrados en /api/docs.
- Variables Cifradas: Inyeccion segura sin filtracion de secretos en Git.

### BASE DE DATOS

- Motor: Neon Serverless PostgreSQL 16.
- SSL Enforcement: Conexiones forzadas con cifrado TLS en transito.
- Timezone Configurado: Sesiones fijadas en America/Lima.
- Backups Continuos: Point-in-Time Restore activo para recuperacion ante incidentes.

> **Notas del Orador:**  
> NOTAS DEL ORADOR (SLIDE 22 - CLOUD EN VIVO):  
> El sistema no es una maqueta local; esta desplegado y operativo en la nube. El frontend se sirve a traves de la CDN de GitHub Pages con soporte PWA instalable en celulares. La API REST corre en un contenedor Docker sobre Render con un health check activo en /api/health, y la base de datos PostgreSQL 16 en Neon opera con conexiones SSL forzadas y respaldos continuos.  

---

## Diapositiva 23
### 13. DEFENSA ANTE EL JURADO

### Matriz de Trazabilidad: Respuestas a las 5 Preguntas del Jurado

### LeoFit Solutions - Grupo 01 | UTP Curso Integrador II

### Sustentacion Semana 18

### Trazabilidad Directa entre Preguntas, Anexos y Codigo Fuente

PREGUNTA DEL JURADO              | DOCUMENTO TECNICO | EVIDENCIA EN CODIGO (`ruta:linea`)    | ESTADO  
--------------------------------------------------------------------------------------------------------------------
1. ¿Por que Render+Neon vs AWS?  | Anexo ADR-001     | render.yaml:1-70 / database.ts:16-55  | LISTO  
2. Maquetacion 100% AWS?         | Anexo ADR-002     | culqi.ts:57 / nubefact.service.ts:1   | LISTO  
3. Cumplimiento Normativo SUNAT? | Anexo DOC-SUNAT   | nubefact.service.ts:171 / 008_inv.ts  | LISTO  
4. Pagos reales o simulados?     | Anexo DOC-PAY     | culqi.ts:85 / paymentWebhook.ts:61    | LISTO  
5. Arquitectura del Repositorio? | Anexo DOC-ARCH    | backend/src/ / 190 tests unitarios    | LISTO  
  
SINTESIS DEFENSIBLE:  
- Cada afirmacion técnica del equipo está respaldada por una linea verificable en el repositorio.
- Toda la documentacion cuenta con referencias normativas y fuentes oficiales citadas.
- Cero suposiciones: lo implementado esta probado y lo planificado tiene hoja de ruta cuantitativa.

> **Notas del Orador:**  
> NOTAS DEL ORADOR (SLIDE 23 - TRAZABILIDAD JURADO):  
> Esta lamina resume la preparacion del equipo ante la evaluacion del tribunal. Las cinco preguntas tipicas sobre eleccion de infraestructura, maquetacion AWS, SUNAT, pasarelas de pago y arquitectura de software estan formalmente documentadas en seis anexos tecnicos y cuentan con evidencia verificable linea a linea en el repositorio GitHub. No hay respuestas ambiguas: todo lo afirmado se sustenta en el codigo fuente.  

---

## Diapositiva 24
### 14. CONCLUSIONES Y APORTES

### Conclusiones del Proyecto y Aportes a la Empresa LeoFit

### LeoFit Solutions - Grupo 01 | UTP Curso Integrador II

### Sustentacion Semana 18

### Impacto Comercial y Operativo en LeoFit

- Eliminacion Total de Sobreventa: Bloqueo pesado en base de datos garantiza stock 100% certero.
- Reduccion de Tiempo de Registro: De mas de 5 minutos por llamada/WhatsApp a 38.2 segundos en la PWA.
- Cero Errores en Despacho: Automatizacion de guias locales y rotulos oficiales de agencia de transporte.
- Facturacion Inmediata: Emision de boletas en menos de 3 segundos integrada al proceso de cobro.
- Autonomia Operativa: Personal del stand capacitado y operando fluidamente en moviles.

### Aportes Formativos de Ingenieria de Software

- Aplicacion Rigurosa de Estandares: Clean Architecture, ISO/IEC 25010, C4 Model y MADR para ADRs.
- Cultura DevSecOps: 190 pruebas automatizadas en CI/CD, sanitizacion PII y escaneo de vulnerabilidades.
- Enfoque Financiero Real: Demostracion de eficiencia de costos antes de sobre-arquitecturar en la nube.
- Documentacion Defendible: Manuales tecnicos, diagramas compilados y matrices de trazabilidad auditables.

> **Notas del Orador:**  
> NOTAS DEL ORADOR (SLIDE 24 - CONCLUSIONES):  
> Como conclusiones finales, el proyecto LeoFit Solutions demostro viabilidad tecnica y valor comercial tangible. Para la empresa, redujo el tiempo de procesamiento de pedidos en un 87% y elimino las discrepancias de inventario. Para nuestro equipo de ingenieria, el proyecto represento la integracion integral de todas las competencias del curso: desde el modelado relacional BCNF hasta la seguridad criptografica, el testing automatizado y la gestion de infraestructura cloud.  

---

## Diapositiva 25
### PROYECTO FINAL COMPLETADO SATISFACTORIAMENTE

### Muchas Gracias por su Atencion

### LeoFit Solutions - Grupo 01 | Seccion 35374 (Ciclo 2026-I)

PANEL DE PREGUNTAS Y DEFENSA TECNICA ABIERTO:  
  
- Repositorio Oficial: github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema
- Documentacion de Anexos: _PROYECTO_FINAL_LOCAL/01_ANEXOS_TECNICOS/
- Sistema en Vivo: leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/

> **Notas del Orador:**  
> NOTAS DEL ORADOR (SLIDE 25 - CIERRE):  
> Con esto concluimos la exposicion formal de la arquitectura y resultados de LeoFit Solutions. Agradecemos profundamente al docente asesor Ing. Enrique Lee Huamani por el acompanamiento y exigencia academica a lo largo del ciclo. Quedamos a disposicion del jurado evaluador para absolver cualquier pregunta tecnica sobre el codigo, los diagramas, la base de datos o las decisiones de arquitectura presentadas. Muchas gracias.  

---
