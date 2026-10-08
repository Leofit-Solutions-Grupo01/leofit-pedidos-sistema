---
name: leofit-expert
description: Guía operativa y técnica del proyecto LeoFit para que el asistente de IA comprenda rápidamente el contexto, comandos y estructura del proyecto.
---

# 🧠 Base de Conocimiento del Proyecto LeoFit (Cheat Sheet)

Bienvenido. Como asistente de IA, tu objetivo es ayudar a mantener y desarrollar el proyecto "Sistema Web PWA de Gestión de Pedidos Multicanal para LeoFit". Esta guía te proporciona atajos y contexto para que operes con máxima eficiencia.

## 📁 1. Estructura del Proyecto (Contexto)
- `docs/documento_maestro/DOCUMENTO_MAESTRO_INTEGRAL_LEOFIT.md`: Documento entregable unificado.
- `docs/diagramas/`: Contiene los 7 diagramas arquitectónicos (D1 a D7) en formato Mermaid (`.mmd`), SVG y su `README.md` explicativo. TODO cambio de arquitectura debe actualizar estos diagramas.
- `scripts/`: Scripts de automatización en Python (ej. `rebuild_all_formal_reports.py`).
- `database/`: Scripts DDL de PostgreSQL (`schema.sql`), BCNF y semillas.
- `backend/`: API RESTful Node.js (Express, TypeScript) desplegado en Render (`render.yaml`). Usa ESM compilado a CommonJS con resolución `node16`.
- `frontend/`: Aplicación React PWA construida con Vite, desplegada en GitHub Pages.

## 🛠️ 2. Comandos Esenciales (¡Memoriza esto!)
Cuando el usuario te pida compilar, probar o generar, utiliza estos comandos desde la raíz del proyecto (workspace root):

*   **Regenerar y Exportar Documentos (DOCX y PDF):**
    ```bash
    python scripts/rebuild_all_formal_reports.py
    ```
    *Uso:* Siempre que modifiques el `DOCUMENTO_MAESTRO_INTEGRAL_LEOFIT.md` o cualquier otro archivo en `docs/`, DEBES ejecutar este comando para que se generen los PDFs y Words actualizados.

*   **Verificar Estado y Git:**
    ```bash
    git status
    git add docs/
    git commit -m "docs: actualizacion de contenido"
    git push origin main
    ```

*   **Despliegue a Producción:**
    El proyecto utiliza *zero-config GitHub Pages* mediante GitHub Actions. Todo push a la rama `main` despliega automáticamente el frontend.

## 🔒 3. Reglas Críticas de Seguridad (APF3 & SEC-10)
- **Cero Credenciales y Política Fail-Fast:** JAMÁS subas o expongas archivos `.env`. NUNCA incluyas strings de fallback en `docker-compose.yml` (ej. usa `${JWT_SECRET}` en vez de `${JWT_SECRET:-secreto}`). Si falta un secreto, la aplicación DEBE fallar inmediatamente (Fail-Fast).
- **Prohibido revelar secretos:** JAMÁS imprimas contraseñas, tokens JWT (`JWT_SECRET`) o `WEBHOOK_SECRET` reales en el chat o en commits. Utiliza siempre placeholders descriptivos como `<TU_SECRETO_SEGURO>`.
- **Configuración Cloud (`render.yaml`):** El backend se despliega en Render. Los secretos inyectables internamente (como `JWT_SECRET`) usan `generateValue: true`. Secretos compartidos con terceros (como `WEBHOOK_SECRET`) usan `sync: false` para inyección manual desde el dashboard.
- OWASP: El backend usa Helmet, Zod, bcrypt y JWT. Todo nuevo endpoint requiere middleware de autenticación (`requireRole`).

## 🚀 4. Flujo de Trabajo Recomendado
1. Entiende el requerimiento del usuario (ej. "Prepara el APF3").
2. Modifica el código o el `DOCUMENTO_MAESTRO_INTEGRAL_LEOFIT.md`.
3. Ejecuta `python scripts/rebuild_all_formal_reports.py`.
4. Haz `git commit` y `git push`.
