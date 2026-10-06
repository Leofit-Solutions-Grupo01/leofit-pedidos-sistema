# Política de Seguridad y Directrices Técnicas - Leofit Solutions

Este documento establece las políticas de divulgación responsable de vulnerabilidades y los estándares de seguridad obligatorios para el desarrollo y despliegue del proyecto.

---

## 1. Versiones con Soporte Activo

Actualmente se proporciona soporte y parches de seguridad para las siguientes versiones activas:

| Versión | Estado de Soporte |
|:--- |:---: |
| `1.0.x-beta` | Soportada (Activa) |
| `< 1.0.0` | No compatible |

---

## 2. Procedimiento de Reporte Responsable de Vulnerabilidades

Si se identifica una vulnerabilidad de seguridad en este proyecto, se solicita no divulgarla públicamente a través de incidencias abiertas o foros públicos. En su lugar, se debe proceder según el siguiente protocolo:

1. **Contacto Confidencial:** Enviar un correo electrónico formal al equipo de seguridad a `seguridad@leofit.com` o comunicarse directamente con los mantenedores principales del repositorio.
2. **Información Requerida:**
  - Descripción técnica detallada del hallazgo.
  - Pasos estructurados o prueba de concepto (*PoC*) para su reproducción.
  - Componente afectado (Frontend, Backend, Base de Datos, CI/CD).
  - Estimación del nivel de severidad e impacto potencial.
3. **Compromiso de Respuesta:**
  - Acuse de recibo formal en un plazo máximo de 48 horas.
  - Plan de evaluación y mitigación en un lapso no mayor a 7 días hábiles.
  - Notificación de cierre una vez desplegado el parche correctivo.

---

## 3. Directrices de Seguridad para Frontend y GitHub Pages

1. **Ausencia Estricta de Secretos en el Cliente:**
  - El código fuente publicado en GitHub Pages es de dominio público y accesible desde el navegador web (código HTML, CSS, JavaScript y bundles).
  - Queda terminantemente prohibido almacenar credenciales de base de datos, claves privadas (`JWT_SECRET`), tokens maestros o llaves de API sensibles en archivos del frontend o en variables de entorno expuestas (`VITE_*`).
2. **Enrutamiento Seguro y Resiliencia SPA:**
  - Empleo de rutas relativas (`base: './'`) en `vite.config.ts` para evitar fallos de resolución de recursos estáticos.
  - Implementación del manejador de respaldo `404.html` en `frontend/public/` para garantizar la persistencia de navegación en recargas de página.
3. **Mitigación de Ataques Cross-Site Scripting (XSS):**
  - Utilización de React DOM con asignación mediante `textContent` en sustitución de `innerHTML` o `dangerouslySetInnerHTML`.
  - Sanitización rigurosa de toda entrada suministrada por el usuario o retornada por servicios externos.
4. **Política de Seguridad de Contenidos (CSP):**
  - Inclusión de directivas Content Security Policy (CSP) en las cabeceras HTML para restringir las conexiones salientes exclusivamente a endpoints autorizados.

---

## 4. Directrices de Seguridad en Backend y Persistencia

1. **Autenticación y Cifrado de Contraseñas:**
  - Uso obligatorio de la librería `bcrypt` con un factor de salting (cost) no menor a 10 para el almacenamiento de contraseñas.
  - Firma criptográfica de tokens JWT con algoritmos HMAC-SHA256 y vigencia máxima de 7 días.
2. **Control de Acceso y Política CORS:**
  - Restricción estricta del middleware `cors()` únicamente a los orígenes autorizados de desarrollo y al dominio oficial de producción en GitHub Pages.
3. **Prevención de Inyecciones SQL:**
  - Utilización exclusiva de ORM (Prisma / Sequelize) y sentencias parametrizadas (*Prepared Statements*) para cualquier interacción con la base de datos relacional.
4. **Protección contra Fuerza Bruta (Rate Limiting):**
  - Implementación de límites de tasa de peticiones (`express-rate-limit`) en los endpoints críticos de autenticación (`/api/auth/login`).

---

## 5. Control de Exclusiones y Archivos Sensibles (.gitignore)

Se debe garantizar que los siguientes artefactos permanezcan permanentemente fuera del control de versiones:
* `.env`, `.env.local`, `.env.production`
* `node_modules/`
* Certificados y claves privadas (`.pem`, `.key`, `.cert`)
* Directorios de compilación local (`dist/`, `build/`)

---

## 6. Estado de la Auditoría y Manejo de Secretos (APF3)

El sistema opera bajo una estricta política de **Fail-Fast** en producción. Es mandatorio configurar adecuadamente las siguientes variables de entorno:

- `JWT_SECRET`: Clave criptográfica para firma de tokens. **Falla si falta.**
- `WEBHOOK_SECRET`: Clave HMAC compartida con la pasarela de pagos. **Falla si falta.**
- `CORS_ORIGIN`: Orígenes autorizados. **En producción, falla si falta.**

### Incidentes Activos y Deuda Técnica
La última auditoría forense (APF3) cerró exitosamente múltiples vulnerabilidades críticas. Sin embargo, los siguientes incidentes y deudas permanecen activos y formalmente declarados:

1. **[SEC-00] Credenciales Hardcodeadas en Historial (ESTADO: ABIERTO - P0)**
   La contraseña original de BD fue expuesta en commits previos. 
   - **Acción:** Requiere rotación de credenciales inmediata en producción y purga del historial con `git filter-repo`. (Responsable: DevOps/DBA).
   
2. **[SEC-08] Contraseñas Débiles en Seeds (ESTADO: ABIERTO - P1)**
   - **Acción:** Los scripts de seeding deben ser refactorizados para obtener las contraseñas administrativas iniciales desde variables de entorno.

3. **Migración a Cookies httpOnly (Deuda Técnica P0)**
   - **Acción:** Migrar almacenamiento del JWT (`sessionStorage`) a cookies de sesión `httpOnly` con flags `Secure` y `SameSite=Strict`, implementando protección CSRF en los endpoints.
   - **Fecha Objetivo / Owner:** Sprint 3 (Q1 2027) / Frontend Lead & Security Architecture Team.

4. **[SEC-09] Credenciales y PII en documentaci�n compilada (ESTADO: ABIERTO - P0)**
   - **Vector:** PDFs y DOCXs compilados y trackeados en git (DOCUMENTO_MAESTRO, 13_Evidencia) con PasswordSeguro2026! y victor@leofit.com.
   - **Distribuci�n:** PDFs circulan fuera del control del repo (email, Drive, descargas) e historial Git.
   - **Acci�n requerida:**
     1. Rotaci�n de credencial (SEC-00, DevOps/DBA).
     2. Regeneraci�n de binarios desde .md sanitizados (Fase 3) y purga de historial (git filter-repo).
     3. Notificaci�n a destinatarios conocidos.
     4. Evaluar obligaci�n de reporte bajo Ley 29733.
   - **Owner:** DevOps / Security
