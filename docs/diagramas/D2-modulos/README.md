# D2 — Flujo entre áreas/módulos del sistema

## Pregunta que responde
¿Qué componente llama a cuál? ¿Cómo se comunican internamente?

## Decisiones de diseño
El sistema sigue una arquitectura Monolítica por Capas estricta. El diagrama `flowchart` refleja esta separación estructural.
Se han dibujado los límites claros entre el **Frontend**, el **Backend** y la **Base de Datos**.

Debido al hallazgo de desconexión en operaciones de negocio (documentado en D1), se representa el flujo interno del frontend de forma aislada recayendo en `mockData.ts`, mostrando explícitamente que la única comunicación inter-sistemas (`HTTP Fetch`) se da a nivel de autenticación. Internamente, el backend respeta la inyección de dependencias mediante interfaces (`domain/repositories/interfaces.ts`), lo que desacopla los Controladores de los Repositorios de infraestructura.

## Fuentes
| Nodo | Descripción | Fuente |
| --- | --- | --- |
| `Pages` | Componentes de UI | `frontend/src/pages/*.tsx` |
| `Context` | Estado Global de React | `frontend/src/context/AppContext.tsx` |
| `MockData` | Persistencia simulada en UI | `frontend/src/data/mockData.ts` |
| `Routes` | Definición de endpoints | `backend/src/routes/*.ts` |
| `Mids` | Seguridad y validación cruzada | `backend/src/middlewares/*.ts` |
| `Controllers` | Lógica de controladores y validación Zod | `backend/src/controllers/*.ts` |
| `Interfaces` | Contratos abstractos | `backend/src/domain/repositories/interfaces.ts` |
| `Repos` | Implementación PostgreSQL | `backend/src/infrastructure/repositories/pg.repositories.ts` |

## Límites explícitos
- El diagrama no baja a nivel de funciones ni tipos específicos de datos DTOs (eso corresponde a D3 - Contratos).
- Las dependencias de Node.js (Express, Cors, Helmet) se engloban dentro del comportamiento general de `Routes` y `Mids`.

## Cómo regenerar
```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i diagram.mmd -o diagram.svg
```

## Versión
- Fecha: 2026-10-07
