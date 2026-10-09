# BACKLOG Y DEUDA TÉCNICA (MEDIANO PLAZO)

Este documento centraliza las oportunidades de mejora continua y refactorización técnica que no son bloqueantes para los pases a producción actuales, pero que elevarán la madurez, seguridad y mantenibilidad del proyecto LeoFit.

---

## 1. Migración del Framework de Testing Backend (Jest → Vitest)
* **Prioridad:** Media
* **Esfuerzo Estimado:** Medio día de trabajo.
* **Motivación:** 
  Actualmente el backend utiliza Jest junto con `ts-jest`. Esta cadena de dependencias arrastra vulnerabilidades indirectas de severidad moderada (reportadas en `npm audit`). 
  Migrar a Vitest eliminará esta cadena de vulnerabilidades, unificará el stack de testing (el frontend ya utiliza el ecosistema de Vite/Vitest) y mejorará los tiempos de ejecución por ser nativo para TypeScript.

## 2. CI Dedicado para Documentación (Docs Pipeline)
* **Prioridad:** Baja
* **Esfuerzo Estimado:** 2 horas.
* **Motivación:** 
  Para evitar regresiones en la calidad documental (como reintroducir emojis no formales, aspas decorativas o enlaces rotos entre Markdowns). 
* **Acción sugerida:** 
  Crear un workflow de GitHub Actions (`docs-ci.yml`) que se dispare en *pushes* al directorio `docs/`. Este workflow ejecutará:
  1. Un linter de Markdown o un script personalizado de `Select-String` / `grep` para buscar caracteres Unicode prohibidos (📐, 📊, ✔️).
  2. Un validador de enlaces rotos (ej. `markdown-link-check`).

## 3. Pruebas End-to-End (E2E) Automatizadas en Producción
* **Prioridad:** Alta
* **Esfuerzo Estimado:** 1 a 2 días.
* **Motivación:** 
  Actualmente, un cambio en la configuración de Vite (ej. un bug de AST) puede romper la integración con el backend sin que las pruebas unitarias fallen.
* **Acción sugerida:** 
  Implementar Playwright o Cypress. Configurar un workflow que se ejecute post-despliegue (tras publicar en GitHub Pages) para levantar un navegador *headless*, navegar a la URL de producción, rellenar el formulario de login y verificar aserciones (que se navegue al dashboard o aparezca el mensaje de credenciales inválidas). Esta es la red de seguridad definitiva.
