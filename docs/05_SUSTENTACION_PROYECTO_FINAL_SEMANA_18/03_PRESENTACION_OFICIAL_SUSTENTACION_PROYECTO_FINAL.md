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

### Calidad de Rendimiento (ISO/IEC 25010): Latencia p50/p95/p99 y SRE

### LeoFit Solutions - Grupo 01 | UTP Curso Integrador II

### Sustentacion Semana 18

### 280 ms / 480 ms

### PERCENTIL 95 (P95) EN 1 Y 10 VU (META SLO < 700 ms)

### 0.0% ERRORES

### TASA DE FALLOS EN CARGA

### 45 req / seg

### CAPACIDAD MAXIMA TIER BASE

### Evaluacion de Latencia y Senales Doradas SRE

- Operacion Critica: POST /api/orders (verificacion y reserva atomica de stock).
- Mediana p50: 120 ms (1 VU) y 240 ms (10 VU) - Experiencia tipica excelente.
- Percentil 95: 480 ms en carga nominal (SLA < 700 ms superado con holgura).
- Cola Larga (p99 = 720 ms): Causada por contencion en pool y RTT hacia Neon.
- Optimizacion: Indices B-Tree redujeron costo de consulta en 64.2%.
- Soak Test 60 min: Cero fugas de memoria (RAM estable < 185 MB).

> **Notas del Orador:**  
> NOTAS DEL ORADOR (SLIDE 15 - RENDIMIENTO SEMANA 14):  
> En la Semana 14 evaluamos cuantitativamente el rendimiento del software bajo la norma ISO/IEC 25010:2023. A la derecha pueden observar el grafico cientifico de barras horizontales de percentiles. Superando el promedio simple, medimos p50, p90, p95 y p99. La experiencia tipica de la mediana p50 es de solo 120 a 240 ms. En carga nominal de 10 usuarios virtuales, el percentil 95 responde en 480 ms, muy por debajo de la linea roja de corte del SLO de 700 ms. La cola larga de p99 refleja la contencion del pool de conexiones hacia Neon, la cual mitigamos en un 64% creando indices B-Tree compuestos.  

---

## Diapositiva 16
### 8. CALIDAD DE RENDIMIENTO (SEMANA 14)

### Curva de Carga k6: Capacidad Maxima y Punto de Saturacion

### LeoFit Solutions - Grupo 01 | UTP Curso Integrador II

### Sustentacion Semana 18

### Analisis de Capacidad, Limites y Auto-Scaling

- Zona de Crecimiento Lineal (1 a 25 VU):
  * Throughput (TPS) escala proporcionalmente hasta 45.6 TPS.  
  * CPU permanece por debajo del 50% y latencia contenida (< 600 ms).  
  
- Punto de Inflexion y Saturacion (~33 a 35 VU):
  * Throughput se ameseta en ~47 TPS por contencion del pool PostgreSQL.  
  * Utilizacion de CPU cruza el umbral critico del 70% sostenido.  
  * Latencia p95 entra en regimen exponencial no lineal (> 2,000 ms).  
  
- Parametros de Disparo de Auto-Scaling (AWS ECS):
  * Trigger: CPU > 70% sostenido durante 60 segundos.  
  * Aprovisionamiento: 42 segundos en nuevo contenedor Fargate.  
  * Cooldown: 300 segundos para evitar oscilaciones destructivas (flapping).  
  
- Respaldo Normativo: ISO/IEC 25010:2023 - Flexibility - Scalability.

> **Notas del Orador:**  
> NOTAS DEL ORADOR (SLIDE 16 - SATURACION Y CAPACIDAD):  
> En esta diapositiva presentamos el grafico combinado de saturacion y capacidad, el cual responde con rigor cientifico donde esta el limite del sistema. A la derecha vemos que hasta los 25 usuarios virtuales el throughput crece de forma lineal y la CPU se mantiene en rangos seguros. Entre los 33 y 35 usuarios virtuales identificamos con precision el punto de saturacion: el throughput se ameseta en 47 transacciones por segundo, la CPU supera el 70% del limite seguro de Google SRE, y la latencia entra en regimen no lineal. Este grafico justifica empiricamente el parametro de disparo del autoescalado en ECS Fargate para aprovisionar nuevas instancias antes de degradar la experiencia de compra.  

---

## Diapositiva 17
### 9. CALIDAD DE MANTENIBILIDAD (SEMANA 15)

### Calidad de Mantenibilidad (ISO/IEC 25010): Modularidad y Reusabilidad

### LeoFit Solutions - Grupo 01 | UTP Curso Integrador II

### Sustentacion Semana 18

### El Anti-Patron Monolitico

- Archivo gigante (tipo app.py / server.js) que mezcla todo:
  * Rutas HTTP y endpoints  
  * Renderizado de pantallas  
  * Reglas de negocio hardcodeadas  
  * Consultas SQL directas  
  * Validaciones de entrada  
  
- Consecuencias Graves:
  * Alto acoplamiento  
  * Un cambio rompe modulos no relacionados  
  * Imposible hacer pruebas unitarias aisladas  
  * Deuda tecnica exponencial y dificil incorporacion de nuevos desarrolladores.  

### Modularidad en LeoFit (Clean)

- Separacion Estricta de Responsabilidades:
  * src/routes/ : Definicion de rutas HTTP y contratos REST.  
  * src/controllers/ : Mapeo de requests, codigos de estado y DTOs.  
  * src/services/ : Logica de negocio pura (descuentos, stock, estados).  
  * src/repositories/ : Consultas SQL parametrizadas.  
  * src/tests/ : Suites de pruebas automatizadas aisladas.  
  
- Beneficio Concreto:
  Modificar la logica de pedidos no toca la base de datos ni los endpoints HTTP.  

### Reusabilidad Comprobada

- Cero Codigo Duplicado:
  
- Middleware RBAC (requireRole):
  Reutilizado en 14 endpoints administrativos y de venta.  
  
- Middleware Idempotencia (RFC 8785):
  Reutilizado en creacion de pedidos, cobros y anulaciones.  
  
- Motor PDF (pdfGenerator):
  Consumido para rotulos de agencia y boletas de venta.  
  
- Componentes UI PWA:
  Botones accesibles, modales y tablas paginadas compartidas en 12 vistas.  

> **Notas del Orador:**  
> NOTAS DEL ORADOR (SLIDE 17 - MANTENIBILIDAD SEMANA 15):  
> En la Semana 15 analizamos la mantenibilidad segun ISO/IEC 25010, evaluando modularidad y reusabilidad. Evitamos a toda costa el anti-patron del archivo monolitico donde se mezclan rutas, SQL y logica. En LeoFit estructuramos el backend siguiendo Clean Architecture: las rutas estan en src/routes, los controladores validan con schemas Zod, los servicios encapsulan las reglas comerciales y los repositorios ejecutan SQL parametrizado. En reusabilidad, demostramos componentes transversales consumidos en multiples puntos sin una sola linea duplicada: el middleware de roles protege 14 endpoints, el generador de PDF emite tanto rotulos de envio como comprobantes, y el validador de idempotencia asegura consistencia en todas las operaciones transaccionales.  

---

## Diapositiva 18
### 9. CALIDAD DE MANTENIBILIDAD (SEMANA 15)

### Calidad de Mantenibilidad: Modificabilidad y Complejidad McCabe

### LeoFit Solutions - Grupo 01 | UTP Curso Integrador II

### Sustentacion Semana 18

### Modificabilidad y Radio de Impacto (Blast Radius)

- Definicion ISO/IEC 25010:2023: Eficacia y eficiencia con que el software se modifica sin introducir defectos ni degradar la calidad.
  
- Caso Practico Aplicado en LeoFit (CHG-01):
  * Requerimiento Comercial: Aplicar 10% de descuento en compras textiles >= 6 unidades.  
  * Archivo Afectado: Exclusivamente src/services/order.service.ts (calculateOrderTotal).  
  * Blast Radius Minimo: Solo 2 archivos modificados (servicio y test unitario).  
  * Impacto en Controladores y Rutas: 0 lineas de cambio en Express.  
  * Impacto en Base de Datos: 0 alteraciones en esquemas relacionales.  
  
- Auditoria de Complejidad Ciclomatica (McCabe):
  * 100% de los modulos en la zona optima de 1 a 3 (estandar <= 4).  
  * Modulo order.service.ts: Complejidad promedio de 2.8 en 380 LOC.  
  * Garantiza bajo costo cognitivo y ausencia de regresiones.  

> **Notas del Orador:**  
> NOTAS DEL ORADOR (SLIDE 18 - MODIFICABILIDAD Y COMPLEJIDAD):  
> En esta diapositiva demostramos la mantenibilidad mediante metricas de complejidad ciclomatica y analisis de radio de impacto. A la derecha se visualiza la auditoria estatica de McCabe: todos los modulos del backend se situan entre 1 y 3, dentro de la franja verde optima. Esto se traduce en que realizar un cambio de negocio real, como la regla de descuento por volumen textil CHG-01, solo toco 2 archivos: el servicio de pedidos y su prueba unitaria, con cero impacto en controladores o base de datos.  

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

### Aseguramiento de Calidad: 194 Pruebas Automatizadas y Piramide

### LeoFit Solutions - Grupo 01 | UTP Curso Integrador II

### Sustentacion Semana 18

### 194 TESTS APROBADOS (100% OK)

### 125 BACKEND (JEST) + 69 FRONTEND (VITEST) - CERO FALLOS

### Distribucion de Suites y Cobertura por Capa

- Capa Dominio (98.4% Cobertura): Entidades puras, validacion Zod, reglas de stock y calculo monetario con Decimal.js.
- Capa Aplicacion (94.2% Cobertura): Servicios de pedidos, autenticacion JWT, RBAC y logica de negocio.
- Capa Infraestructura (86.5% Cobertura): Repositorios SQL, pooling de conexiones y clientes externos.
- Capa Frontend PWA (91.5% Cobertura): Componentes React 19, navegacion accesible WCAG y Service Workers offline.
- Inversion de Dependencias: Dependencias apuntan estrictamente hacia el dominio (0 violaciones de acoplamiento).

> **Notas del Orador:**  
> NOTAS DEL ORADOR (SLIDE 20 - TESTING QA):  
> La confiabilidad de LeoFit esta respaldada por 194 pruebas automatizadas con 100% de exito. A la derecha pueden observar el grafico de cobertura por capas bajo Clean Architecture: la cobertura supera el 98% en el dominio y 94% en aplicacion, demostrando que el esfuerzo de pruebas se enfoca donde reside el valor comercial. Todas las dependencias apuntan hacia el interior del sistema sin violaciones de acoplamiento.  

---

## Diapositiva 21
### 11. TESTING Y CALIDAD (QA)

### Evaluacion Integral de Calidad ISO/IEC 25010:2023 y Usabilidad

### LeoFit Solutions - Grupo 01 | UTP Curso Integrador II

### Sustentacion Semana 18

### Perfil de Calidad Global y Accesibilidad

- Modelo ISO/IEC 25010:2023 (9 Caracteristicas):
  * Adecuacion Funcional: 98.0% (10 de 10 RF verificados).  
  * Eficiencia de Desempeno: 94.0% (p95 = 480 ms en carga nominal).  
  * Seguridad de la Informacion: 97.0% (Bcrypt, JWT, HMAC).  
  * Mantenibilidad: 95.5% (McCabe 1-3, 194 pruebas automatizadas).  
  * Confiabilidad: 96.5% (PWA offline, PITR RPO < 5 min).  
  * Seguridad Funcional (Safety): 91.0% (Cero sobreventas ACID).  
  
- Puntaje Sintetico Global: 94.6 / 100 (Nivel Sobresaliente).
  
- Estudio de Usabilidad (System Usability Scale):
  * Puntaje SUS: 88.5 / 100 (Grado A, Percentil 96% de excelencia).  
  * Tiempo de registro reducido de 310s a 38.2s (-87.6%).  
  
- Accesibilidad WCAG 2.1 AA/AAA: Contrastes de hasta 17.8:1.

> **Notas del Orador:**  
> NOTAS DEL ORADOR (SLIDE 21 - ISO 25010):  
> Para cerrar la evaluacion de calidad, a la derecha presentamos el grafico radial de las 9 caracteristicas de la norma ISO/IEC 25010:2023. El poligono demuestra un sistema altamente equilibrado, superando en todas las dimensiones el 90% y alcanzando un puntaje sintetico global de 94.6 sobre 100. En la parte humana, certificamos una usabilidad de 88.5 puntos SUS en el percentil 96 y accesibilidad web de contraste AAA.  

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
