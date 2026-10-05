---
name: leofit-expert
description: Guía operativa y técnica del proyecto LeoFit para que el asistente de IA comprenda rápidamente el contexto, comandos y estructura del proyecto.
---

# 🧠 Base de Conocimiento del Proyecto LeoFit (Cheat Sheet)

Bienvenido. Como asistente de IA, tu objetivo es ayudar a mantener y desarrollar el proyecto "Sistema Web PWA de Gestión de Pedidos Multicanal para LeoFit". Esta guía te proporciona atajos y contexto para que operes con máxima eficiencia.

## 📁 1. Estructura del Proyecto (Single Source of Truth)
- `docs/DOCUMENTO_MAESTRO_INTEGRAL_LEOFIT.md`: **¡El archivo más importante!** Es el documento entregable unificado. Contiene desde el APF1 hasta el Trabajo Final. Si el usuario pide actualizar documentación, este es el archivo a modificar.
- `scripts/`: Contiene los scripts de automatización en Python.
- `database/`: Scripts DDL de PostgreSQL (`schema.sql`), BCNF y respaldos.
- `backend/`: API RESTful Node.js bajo arquitectura limpia (Clean Architecture: Repositorios, Casos de Uso, Controladores).
- `frontend/`: Aplicación React PWA construida con Vite.

## 🛠️ 2. Comandos Esenciales (¡Memoriza esto!)
Cuando el usuario te pida compilar, probar o generar, utiliza estos comandos desde la raíz (`c:\Users\Loayza\Downloads\leofit-pedidos-sistema`):

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

## 🔒 3. Reglas Críticas de Seguridad
- **Cero Credenciales:** JAMÁS subas o expongas archivos `.env`. Si necesitas probar variables de entorno, asegúrate de que están en el `.gitignore`.
- OWASP: El backend ya cuenta con protección (Helmet, Zod, bcrypt, JWT). Si agregas un endpoint, DEBE pasar por el middleware de autenticación (`requireRole`).

## 🚀 4. Flujo de Trabajo Recomendado
1. Entiende el requerimiento del usuario (ej. "Prepara el APF3").
2. Modifica el código o el `DOCUMENTO_MAESTRO_INTEGRAL_LEOFIT.md`.
3. Ejecuta `python scripts/rebuild_all_formal_reports.py`.
4. Haz `git commit` y `git push`.
