# Política de Seguridad y Directrices Técnicas - Leofit Solutions

Este documento establece las políticas de divulgación responsable de vulnerabilidades y los estándares de seguridad obligatorios para el desarrollo y despliegue del proyecto.

---

## 🔒 1. Versiones Soportadas

Actualmente se proporciona soporte y parches de seguridad para las siguientes versiones activas:

| Versión | ¿Soportada? |
| :--- | :---: |
| `1.0.x-beta` | ✅ Sí |
| `< 1.0.0` | ❌ No |

---

## 🛡️ 2. Reporte Responsable de Vulnerabilidades

Si descubres una vulnerabilidad de seguridad en este proyecto, te solicitamos **no divulgarla públicamente** a través de *Issues* abiertos o foros públicos. En su lugar, sigue el siguiente procedimiento:

1. **Contacto Privado:** Envía un correo electrónico detallado al equipo de seguridad a `seguridad@leofit.com` o contacta a los mantenedores principales del repositorio de manera confidencial.
2. **Información requerida:**
   - Descripción detallada de la vulnerabilidad.
   - Pasos exactos o prueba de concepto (*PoC*) para reproducirla.
   - Componente afectado (Frontend, Backend, Base de Datos, CI/CD).
   - Impacto potencial estimado.
3. **Compromiso de Respuesta:**
   - Acuse de recibo inicial en un plazo máximo de **48 horas**.
   - Evaluación y plan de mitigación en un plazo no mayor a **7 días laborables**.
   - Notificación una vez que el parche de seguridad sea desplegado.

---

## 🌐 3. Reglas Críticas para GitHub Pages y Frontend

1. **Nunca incluir credenciales o secretos en el Frontend:**
   * El código publicado en GitHub Pages es **100% público** y accesible desde el navegador del cliente (HTML, CSS, JS, bundle).
   * **NUNCA** coloques contraseñas de bases de datos, claves privadas (`JWT_SECRET`), tokens maestros ni llaves de API sensibles en archivos del frontend ni en variables `VITE_*`.
   * Las variables `VITE_*` se embeben públicamente en el bundle compilado.

2. **Manejo de Rutas y Enlaces Relativos:**
   * Configuración de base path relativa (`base: './'`) en `vite.config.ts` para evitar fallos de carga de recursos y errores MIME.
   * Manejador de redirección SPA `404.html` en `frontend/public/` para evitar caídas de navegación al recargar subrutas.

3. **Protección contra Cross-Site Scripting (XSS):**
   * Usar React / Vanilla DOM con `textContent` en lugar de `innerHTML` o `dangerouslySetInnerHTML`.
   * Sanitizar cualquier entrada de texto proveniente de usuarios o APIs antes de renderizarla.

4. **Políticas de Seguridad en Cabeceras (CSP):**
   * Configurar meta-etiquetas de Content Security Policy (CSP) en `index.html` para permitir únicamente conexiones seguras hacia el backend.

---

## 🗄️ 4. Reglas de Seguridad en Backend y Base de Datos

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

## 📋 5. Lista de Verificación de Archivos Ignorados (`.gitignore`)

Asegurarse de que los siguientes archivos nunca sean comiteados:
* `.env`, `.env.local`, `.env.production`
* `node_modules/`
* Archivos `.pem`, `.key`, `.cert`
* Carpetas de build local (`dist/`, `build/`)
