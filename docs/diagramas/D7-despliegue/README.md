# D7 — Topología de despliegue

## Pregunta que responde
¿Dónde está desplegado cada componente y cómo se comunican en el entorno actual vs. el propuesto?

## Decisiones de diseño
Se estructuró el diagrama dividiendo el ecosistema en dos zonas (Estado Actual vs Target Propuesto) para evidenciar claramente que la aplicación frontend ya está en la nube (GitHub Pages), pero el backend sigue corriendo de forma local. El target muestra la arquitectura nativa de nube que el proyecto persigue.

## Límites explícitos
- El diagrama no detalla la configuración interna de DNS, balanceadores de carga o VPCs, centrándose exclusivamente en los proveedores de nube propuestos (Vercel, Render, Supabase).
- No se detallan los triggers específicos de GitHub Actions, solo el concepto de CI/CD continuo vs manual.

## GAPs a marcar explícitamente
- El **Backend no está desplegado** en producción (solo corre en `localhost:3000`).
- El `Dockerfile` existe pero no es el deploy activo (el deploy se realiza usando Node nativo según render.yaml).
- No hay manifiestos de Kubernetes (K8s) ni Infraestructura como Código (Terraform/Pulumi).
- No hay dominios custom configurados (frontend y backend dependen de URLs asignadas por plataformas como GitHub o Render).

## Fuentes

| Componente | Fuente (archivo:línea) |
| --- | --- |
| Deploy del Frontend | `.github/workflows/deploy.yml:1` |
| Conexión PostgreSQL (Supabase) | `backend/src/config/database.ts:12` |
| Variables BD en entorno | `backend/.env.example:14` |
| URL base Frontend | `frontend/.env.example:4` |
| Dev Environment | `docker-compose.yml:1` |

## Nota sobre el tamaño
El archivo SVG renderizado incrusta la tipografía, pesando alrededor de 200 KB. Puede ser optimizado utilizando el flag `--no-svg-fonts` en el CLI de Mermaid (verificando visualmente antes de commitear).

## Cómo regenerar
```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i diagram.mmd -o diagram.svg
```

## Versión
- Fecha: 2026-10-07
