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

### [SEC-10] Fallback hardcodeado de JWT_SECRET en docker-compose.yml

- **Estado:** MITIGADO
- **Severidad:** ALTA
- **Vector:** Sintaxis `${VAR:-fallback}` en `docker-compose.yml` deja
  un string literal como clave de firma por defecto si la variable
  de entorno no está definida. Fallback efectivo:
  `leofit_super_secret_jwt_key_academic_2026_production_ready`.
- **Commits afectados:**
  - Introducción: `28d043b` (repo público).
  - Mitigación: `57f5a79` (merge de `fix/secret-exposure-v2`).
- **Acciones tomadas:**
  1. Eliminado el fallback de `docker-compose.yml` → ahora es
     `${JWT_SECRET}` sin default. Fail-fast si falta.
  2. `WEBHOOK_SECRET` cambiado a `sync: false` en `render.yaml`
     (valor configurado manualmente, no generado por Render).
  3. `JWT_SECRET` y `WEBHOOK_SECRET` rotados en el dashboard de
     Render con valores nuevos.
- **Deuda residual:** el string sigue en la historia de git en el
  commit `28d043b`. La mitigación completa requeriría `filter-repo`.
  No se ejecutó por bajo impacto (el secreto ya está rotado y es
  inutilizable).
- **Owner:** DevOps / Security
- **Fecha de detección:** 2026-10-08
- **Fecha de mitigación:** 2026-10-08

1. **[SEC-00] Credenciales activas expuestas (ABIERTO - P0)**
   - **Vectores:**
     1. HEAD actual: `docker-compose.yml` (postgrespassword2026!), `scripts/generate_master_markdown.py` (PasswordSeguro2026!).
     2. Historia git: commits 900c375, 5653086, 1e42944, 6bfe2e1, 1f9531d, 827cd62... (lista completa).
     3. Binarios históricos: cubierto por SEC-09.
   - **Mitigación en curso:**
     - [inmediato] Sanitizar los 2 archivos en HEAD vía variables de entorno con fail-fast. Commit normal (no filter-repo).
     - [corto plazo] Rotación de ambas credenciales en el entorno real.
     - [corto plazo] git filter-repo para purgar historia.
     - **Impacto operativo:** 52 commits reescritos. Todos los clones existentes quedan inválidos. Coordinación obligatoria con contributors. Apertura de ticket a GitHub Support para purga de objetos en caché.
     - **Ventana de coordinación:** 2026-10-07 a 2026-10-15
     - [corto plazo] Coordinación de clones + soporte GitHub.
   - **Fecha Objetivo / Owner:** Sprint 3 (Q1 2027) / DevOps & DBA Team.

2. **[SEC-08] Contraseñas Débiles en Seeds (ESTADO: ABIERTO - P1)**
   - **Acción:** Los scripts de seeding deben ser refactorizados para obtener las contraseñas administrativas iniciales desde variables de entorno.
   - **Owner:** Product Owner / Back-End Lead
   - **Fecha Límite:** 2026-10-15

3. **Migración a Cookies httpOnly (Deuda Técnica P0)**
   - **Acción:** Migrar almacenamiento del JWT (`sessionStorage`) a cookies de sesión `httpOnly` con flags `Secure` y `SameSite=Strict`, implementando protección CSRF en los endpoints.
   - **Fecha Objetivo / Owner:** Sprint 3 (Q1 2027) / Frontend Lead & Security Architecture Team.

4. **[SEC-09] Credenciales y PII en documentaciÃ³n compilada (ESTADO: ABIERTO - P0)**
   - **Vector:** PDFs y DOCXs compilados y trackeados en git (DOCUMENTO_MAESTRO, 13_Evidencia) con la contraseña hardcodeada y correo del administrador.
   - **DistribuciÃ³n:** PDFs circulan fuera del control del repo (email, Drive, descargas) e historial Git.
   - **AcciÃ³n requerida:**
     1. RotaciÃ³n de credencial (SEC-00, DevOps/DBA).
     2. RegeneraciÃ³n de binarios desde .md sanitizados (Fase 3) y purga de historial (git filter-repo).
     3. NotificaciÃ³n a destinatarios conocidos.
     4. Evaluar obligaciÃ³n de reporte bajo Ley 29733.
   - **Owner:** VÃ­ctor CÃ¡rdenas (Product Owner / Back-End Lead).
   - **Fecha LÃ­mite RotaciÃ³n Credencial:** 2026-10-15
   - **Fecha LÃ­mite Purga Git (filter-repo):** 2026-10-15


> <TODO: decisi�n del Product Owner>
> Pol�tica sobre PII en documentos acad�micos (Ficha, Actas). 
> Opci�n A: Mantener como datos institucionales p�blicos. 
> Opci�n B: Sanitizar a <autor 1> en el repo p�blico.
> Archivos afectados:
> - docs/DOCUMENTO_MAESTRO_INTEGRAL_LEOFIT.md:301,670
> - docs/modulos_tecnicos/03_Acta_Reunion_1.md:60
> - docs/modulos_tecnicos/09_Guion_Video_Demo_Remotion.md:33
> - docs/modulos_tecnicos/13_Evidencia_Cumplimiento_Requerimientos_Software.md:96
> - docs/modulos_tecnicos/15_Profundizacion_Seguridad_Formal_y_Objetiva.md:24
