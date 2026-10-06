# PolÃ­tica de Seguridad y Directrices TÃ©cnicas - Leofit Solutions

Este documento establece las polÃ­ticas de divulgaciÃ³n responsable de vulnerabilidades y los estÃ¡ndares de seguridad obligatorios para el desarrollo y despliegue del proyecto.

---

## 1. Versiones con Soporte Activo

Actualmente se proporciona soporte y parches de seguridad para las siguientes versiones activas:

| VersiÃ³n | Estado de Soporte |
|:--- |:---: |
| `1.0.x-beta` | Soportada (Activa) |
| `< 1.0.0` | No compatible |

---

## 2. Procedimiento de Reporte Responsable de Vulnerabilidades

Si se identifica una vulnerabilidad de seguridad en este proyecto, se solicita no divulgarla pÃºblicamente a travÃ©s de incidencias abiertas o foros pÃºblicos. En su lugar, se debe proceder segÃºn el siguiente protocolo:

1. **Contacto Confidencial:** Enviar un correo electrÃ³nico formal al equipo de seguridad a `seguridad@leofit.com` o comunicarse directamente con los mantenedores principales del repositorio.
2. **InformaciÃ³n Requerida:**
  - DescripciÃ³n tÃ©cnica detallada del hallazgo.
  - Pasos estructurados o prueba de concepto (*PoC*) para su reproducciÃ³n.
  - Componente afectado (Frontend, Backend, Base de Datos, CI/CD).
  - EstimaciÃ³n del nivel de severidad e impacto potencial.
3. **Compromiso de Respuesta:**
  - Acuse de recibo formal en un plazo mÃ¡ximo de 48 horas.
  - Plan de evaluaciÃ³n y mitigaciÃ³n en un lapso no mayor a 7 dÃ­as hÃ¡biles.
  - NotificaciÃ³n de cierre una vez desplegado el parche correctivo.

---

## 3. Directrices de Seguridad para Frontend y GitHub Pages

1. **Ausencia Estricta de Secretos en el Cliente:**
  - El cÃ³digo fuente publicado en GitHub Pages es de dominio pÃºblico y accesible desde el navegador web (cÃ³digo HTML, CSS, JavaScript y bundles).
  - Queda terminantemente prohibido almacenar credenciales de base de datos, claves privadas (`JWT_SECRET`), tokens maestros o llaves de API sensibles en archivos del frontend o en variables de entorno expuestas (`VITE_*`).
2. **Enrutamiento Seguro y Resiliencia SPA:**
  - Empleo de rutas relativas (`base: './'`) en `vite.config.ts` para evitar fallos de resoluciÃ³n de recursos estÃ¡ticos.
  - ImplementaciÃ³n del manejador de respaldo `404.html` en `frontend/public/` para garantizar la persistencia de navegaciÃ³n en recargas de pÃ¡gina.
3. **MitigaciÃ³n de Ataques Cross-Site Scripting (XSS):**
  - UtilizaciÃ³n de React DOM con asignaciÃ³n mediante `textContent` en sustituciÃ³n de `innerHTML` o `dangerouslySetInnerHTML`.
  - SanitizaciÃ³n rigurosa de toda entrada suministrada por el usuario o retornada por servicios externos.
4. **PolÃ­tica de Seguridad de Contenidos (CSP):**
  - InclusiÃ³n de directivas Content Security Policy (CSP) en las cabeceras HTML para restringir las conexiones salientes exclusivamente a endpoints autorizados.

---

## 4. Directrices de Seguridad en Backend y Persistencia

1. **AutenticaciÃ³n y Cifrado de ContraseÃ±as:**
  - Uso obligatorio de la librerÃ­a `bcrypt` con un factor de salting (cost) no menor a 10 para el almacenamiento de contraseÃ±as.
  - Firma criptogrÃ¡fica de tokens JWT con algoritmos HMAC-SHA256 y vigencia mÃ¡xima de 7 dÃ­as.
2. **Control de Acceso y PolÃ­tica CORS:**
  - RestricciÃ³n estricta del middleware `cors()` Ãºnicamente a los orÃ­genes autorizados de desarrollo y al dominio oficial de producciÃ³n en GitHub Pages.
3. **PrevenciÃ³n de Inyecciones SQL:**
  - UtilizaciÃ³n exclusiva de ORM (Prisma / Sequelize) y sentencias parametrizadas (*Prepared Statements*) para cualquier interacciÃ³n con la base de datos relacional.
4. **ProtecciÃ³n contra Fuerza Bruta (Rate Limiting):**
  - ImplementaciÃ³n de lÃ­mites de tasa de peticiones (`express-rate-limit`) en los endpoints crÃ­ticos de autenticaciÃ³n (`/api/auth/login`).

---

## 5. Control de Exclusiones y Archivos Sensibles (.gitignore)

Se debe garantizar que los siguientes artefactos permanezcan permanentemente fuera del control de versiones:
* `.env`, `.env.local`, `.env.production`
* `node_modules/`
* Certificados y claves privadas (`.pem`, `.key`, `.cert`)
* Directorios de compilaciÃ³n local (`dist/`, `build/`)

---

## 6. Estado de la AuditorÃ­a y Manejo de Secretos (APF3)

El sistema opera bajo una estricta polÃ­tica de **Fail-Fast** en producciÃ³n. Es mandatorio configurar adecuadamente las siguientes variables de entorno:

- `JWT_SECRET`: Clave criptogrÃ¡fica para firma de tokens. **Falla si falta.**
- `WEBHOOK_SECRET`: Clave HMAC compartida con la pasarela de pagos. **Falla si falta.**
- `CORS_ORIGIN`: OrÃ­genes autorizados. **En producciÃ³n, falla si falta.**

### Incidentes Activos y Deuda TÃ©cnica
La Ãºltima auditorÃ­a forense (APF3) cerrÃ³ exitosamente mÃºltiples vulnerabilidades crÃ­ticas. Sin embargo, los siguientes incidentes y deudas permanecen activos y formalmente declarados:

1. **[SEC-00] Credenciales Hardcodeadas en Historial (ESTADO: ABIERTO - P0)**
   La contraseÃ±a original de BD fue expuesta en commits previos. 
   - **AcciÃ³n:** Requiere rotaciÃ³n de credenciales inmediata en producciÃ³n y purga del historial con `git filter-repo`.
   - **Owner:** V�ctor C�rdenas (Product Owner / Back-End Lead).
   - **Fecha L�mite:** 2026-10-15
   
2. **[SEC-08] ContraseÃ±as DÃ©biles en Seeds (ESTADO: ABIERTO - P1)**
   - **AcciÃ³n:** Los scripts de seeding deben ser refactorizados para obtener las contraseÃ±as administrativas iniciales desde variables de entorno.
   - **Owner:** V�ctor C�rdenas (Product Owner / Back-End Lead).
   - **Fecha L�mite:** 2026-10-15

3. **MigraciÃ³n a Cookies httpOnly (Deuda TÃ©cnica P0)**
   - **AcciÃ³n:** Migrar almacenamiento del JWT (`sessionStorage`) a cookies de sesiÃ³n `httpOnly` con flags `Secure` y `SameSite=Strict`, implementando protecciÃ³n CSRF en los endpoints.
   - **Fecha Objetivo / Owner:** Sprint 3 (Q1 2027) / Frontend Lead & Security Architecture Team.

4. **[SEC-09] Credenciales y PII en documentación compilada (ESTADO: ABIERTO - P0)**
   - **Vector:** PDFs y DOCXs compilados y trackeados en git (DOCUMENTO_MAESTRO, 13_Evidencia) con PasswordSeguro2026! y victor@leofit.com.
   - **Distribución:** PDFs circulan fuera del control del repo (email, Drive, descargas) e historial Git.
   - **Acción requerida:**
     1. Rotación de credencial (SEC-00, DevOps/DBA).
     2. Regeneración de binarios desde .md sanitizados (Fase 3) y purga de historial (git filter-repo).
     3. Notificación a destinatarios conocidos.
     4. Evaluar obligación de reporte bajo Ley 29733.
   - **Owner:** Víctor Cárdenas (Product Owner / Back-End Lead).
   - **Fecha Límite Rotación Credencial:** 2026-10-15
   - **Fecha Límite Purga Git (filter-repo):** 2026-10-15

