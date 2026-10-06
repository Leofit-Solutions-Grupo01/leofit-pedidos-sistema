# PolÃƒÂ­tica de Seguridad y Directrices TÃƒÂ©cnicas - Leofit Solutions

Este documento establece las polÃƒÂ­ticas de divulgaciÃƒÂ³n responsable de vulnerabilidades y los estÃƒÂ¡ndares de seguridad obligatorios para el desarrollo y despliegue del proyecto.

---

## 1. Versiones con Soporte Activo

Actualmente se proporciona soporte y parches de seguridad para las siguientes versiones activas:

| VersiÃƒÂ³n | Estado de Soporte |
|:--- |:---: |
| `1.0.x-beta` | Soportada (Activa) |
| `< 1.0.0` | No compatible |

---

## 2. Procedimiento de Reporte Responsable de Vulnerabilidades

Si se identifica una vulnerabilidad de seguridad en este proyecto, se solicita no divulgarla pÃƒÂºblicamente a travÃƒÂ©s de incidencias abiertas o foros pÃƒÂºblicos. En su lugar, se debe proceder segÃƒÂºn el siguiente protocolo:

1. **Contacto Confidencial:** Enviar un correo electrÃƒÂ³nico formal al equipo de seguridad a `seguridad@leofit.com` o comunicarse directamente con los mantenedores principales del repositorio.
2. **InformaciÃƒÂ³n Requerida:**
  - DescripciÃƒÂ³n tÃƒÂ©cnica detallada del hallazgo.
  - Pasos estructurados o prueba de concepto (*PoC*) para su reproducciÃƒÂ³n.
  - Componente afectado (Frontend, Backend, Base de Datos, CI/CD).
  - EstimaciÃƒÂ³n del nivel de severidad e impacto potencial.
3. **Compromiso de Respuesta:**
  - Acuse de recibo formal en un plazo mÃƒÂ¡ximo de 48 horas.
  - Plan de evaluaciÃƒÂ³n y mitigaciÃƒÂ³n en un lapso no mayor a 7 dÃƒÂ­as hÃƒÂ¡biles.
  - NotificaciÃƒÂ³n de cierre una vez desplegado el parche correctivo.

---

## 3. Directrices de Seguridad para Frontend y GitHub Pages

1. **Ausencia Estricta de Secretos en el Cliente:**
  - El cÃƒÂ³digo fuente publicado en GitHub Pages es de dominio pÃƒÂºblico y accesible desde el navegador web (cÃƒÂ³digo HTML, CSS, JavaScript y bundles).
  - Queda terminantemente prohibido almacenar credenciales de base de datos, claves privadas (`JWT_SECRET`), tokens maestros o llaves de API sensibles en archivos del frontend o en variables de entorno expuestas (`VITE_*`).
2. **Enrutamiento Seguro y Resiliencia SPA:**
  - Empleo de rutas relativas (`base: './'`) en `vite.config.ts` para evitar fallos de resoluciÃƒÂ³n de recursos estÃƒÂ¡ticos.
  - ImplementaciÃƒÂ³n del manejador de respaldo `404.html` en `frontend/public/` para garantizar la persistencia de navegaciÃƒÂ³n en recargas de pÃƒÂ¡gina.
3. **MitigaciÃƒÂ³n de Ataques Cross-Site Scripting (XSS):**
  - UtilizaciÃƒÂ³n de React DOM con asignaciÃƒÂ³n mediante `textContent` en sustituciÃƒÂ³n de `innerHTML` o `dangerouslySetInnerHTML`.
  - SanitizaciÃƒÂ³n rigurosa de toda entrada suministrada por el usuario o retornada por servicios externos.
4. **PolÃƒÂ­tica de Seguridad de Contenidos (CSP):**
  - InclusiÃƒÂ³n de directivas Content Security Policy (CSP) en las cabeceras HTML para restringir las conexiones salientes exclusivamente a endpoints autorizados.

---

## 4. Directrices de Seguridad en Backend y Persistencia

1. **AutenticaciÃƒÂ³n y Cifrado de ContraseÃƒÂ±as:**
  - Uso obligatorio de la librerÃƒÂ­a `bcrypt` con un factor de salting (cost) no menor a 10 para el almacenamiento de contraseÃƒÂ±as.
  - Firma criptogrÃƒÂ¡fica de tokens JWT con algoritmos HMAC-SHA256 y vigencia mÃƒÂ¡xima de 7 dÃƒÂ­as.
2. **Control de Acceso y PolÃƒÂ­tica CORS:**
  - RestricciÃƒÂ³n estricta del middleware `cors()` ÃƒÂºnicamente a los orÃƒÂ­genes autorizados de desarrollo y al dominio oficial de producciÃƒÂ³n en GitHub Pages.
3. **PrevenciÃƒÂ³n de Inyecciones SQL:**
  - UtilizaciÃƒÂ³n exclusiva de ORM (Prisma / Sequelize) y sentencias parametrizadas (*Prepared Statements*) para cualquier interacciÃƒÂ³n con la base de datos relacional.
4. **ProtecciÃƒÂ³n contra Fuerza Bruta (Rate Limiting):**
  - ImplementaciÃƒÂ³n de lÃƒÂ­mites de tasa de peticiones (`express-rate-limit`) en los endpoints crÃƒÂ­ticos de autenticaciÃƒÂ³n (`/api/auth/login`).

---

## 5. Control de Exclusiones y Archivos Sensibles (.gitignore)

Se debe garantizar que los siguientes artefactos permanezcan permanentemente fuera del control de versiones:
* `.env`, `.env.local`, `.env.production`
* `node_modules/`
* Certificados y claves privadas (`.pem`, `.key`, `.cert`)
* Directorios de compilaciÃƒÂ³n local (`dist/`, `build/`)

---

## 6. Estado de la AuditorÃƒÂ­a y Manejo de Secretos (APF3)

El sistema opera bajo una estricta polÃƒÂ­tica de **Fail-Fast** en producciÃƒÂ³n. Es mandatorio configurar adecuadamente las siguientes variables de entorno:

- `JWT_SECRET`: Clave criptogrÃƒÂ¡fica para firma de tokens. **Falla si falta.**
- `WEBHOOK_SECRET`: Clave HMAC compartida con la pasarela de pagos. **Falla si falta.**
- `CORS_ORIGIN`: OrÃƒÂ­genes autorizados. **En producciÃƒÂ³n, falla si falta.**

### Incidentes Activos y Deuda TÃƒÂ©cnica
La ÃƒÂºltima auditorÃƒÂ­a forense (APF3) cerrÃƒÂ³ exitosamente mÃƒÂºltiples vulnerabilidades crÃƒÂ­ticas. Sin embargo, los siguientes incidentes y deudas permanecen activos y formalmente declarados:

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

2. **[SEC-08] ContraseÃƒÂ±as DÃƒÂ©biles en Seeds (ESTADO: ABIERTO - P1)**
   - **AcciÃƒÂ³n:** Los scripts de seeding deben ser refactorizados para obtener las contraseÃƒÂ±as administrativas iniciales desde variables de entorno.
   - **Owner:** Product Owner / Back-End Lead
   - **Fecha Límite:** 2026-10-15

3. **MigraciÃƒÂ³n a Cookies httpOnly (Deuda TÃƒÂ©cnica P0)**
   - **AcciÃƒÂ³n:** Migrar almacenamiento del JWT (`sessionStorage`) a cookies de sesiÃƒÂ³n `httpOnly` con flags `Secure` y `SameSite=Strict`, implementando protecciÃƒÂ³n CSRF en los endpoints.
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
