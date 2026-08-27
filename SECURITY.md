# Directrices de Seguridad y Buenas Prácticas - Leofit Solutions

Este documento establece los estándares de seguridad obligatorios para el desarrollo y despliegue del proyecto.

---

## 1. Reglas Críticas para GitHub Pages y Frontend

1. **Nunca incluir credenciales o secretos en el Frontend:**
   * El código publicado en GitHub Pages es **100% público** y accesible desde el navegador del cliente (HTML, CSS, JS, bundle).
   * **NUNCA** coloques contraseñas de bases de datos, claves privadas (`JWT_SECRET`), tokens maestros ni llaves de API sensibles en archivos del frontend ni en variables `VITE_*`.
   * Las variables `VITE_*` se embeben públicamente en el bundle compilado.

2. **Manejo de Rutas y Enlaces Relativos:**
   * Configuración de base path relativa (`base: './'`) en `vite.config.js` para evitar fallos de carga de recursos y errores MIME.
   * Manejador de redirección SPA `404.html` en `frontend/public/` para evitar caídas de navegación al recargar subrutas.

3. **Protección contra Cross-Site Scripting (XSS):**
   * Usar React / Vanilla DOM con `textContent` en lugar de `innerHTML` o `dangerouslySetInnerHTML`.
   * Sanitizar cualquier entrada de texto proveniente de usuarios o APIs antes de renderizarla.

4. **Políticas de Seguridad en Cabeceras (CSP):**
   * Configurar meta-etiquetas de Content Security Policy (CSP) en `index.html` para permitir únicamente conexiones seguras hacia el backend.

---

## 2. Reglas de Seguridad en Backend y Base de Datos

1. **Autenticación y Hashing de Contraseñas:**
   * Utilizar siempre `bcrypt` con un factor de salting (cost) de al menos 10 para todas las contraseñas de usuarios.
   * Firmar los tokens JWT con un secreto robusto y definir expiración máxima de 7 días.

2. **Control de Acceso y CORS Estricto:**
   * Limitar el middleware `cors()` únicamente a los orígenes autorizados (ej. `http://localhost:5173` en desarrollo y el dominio exacto de GitHub Pages en producción).

3. **Prevención de Inyecciones SQL:**
   * Utilizar siempre ORM (Prisma / Sequelize) o sentencias preparadas (*Prepared Statements* / consultas parametrizadas).

4. **Rate Limiting:**
   * Implementar `express-rate-limit` en los endpoints de `/api/auth/login` para prevenir ataques de fuerza bruta.

---

## 3. Lista de Verificación de Archivos Ignorados (`.gitignore`)

Asegurarse de que los siguientes archivos nunca sean comiteados:
* `.env`, `.env.local`, `.env.production`
* `node_modules/`
* Archivos `.pem`, `.key`, `.cert`
* Carpetas de build local (`dist/`, `build/`)
