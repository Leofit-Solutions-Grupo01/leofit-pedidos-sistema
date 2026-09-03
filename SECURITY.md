# Política de Seguridad y Directrices Técnicas - Leofit Solutions

Este documento establece las políticas de divulgación responsable de vulnerabilidades y los estándares de seguridad obligatorios para el desarrollo y despliegue del proyecto.

---

## 1. Versiones con Soporte Activo

Actualmente se proporciona soporte y parches de seguridad para las siguientes versiones activas:

| Versión | Estado de Soporte |
| :--- | :---: |
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
