# Historial de Cambios (Changelog)

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y este proyecto se adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [No publicado / Unreleased]

### Añadido
- Suite de pruebas unitarias con Vitest para validación de datos y modelos del frontend.
- Guías de contribución (`CONTRIBUTING.md`), código de conducta (`CODE_OF_CONDUCT.md`)
  y política de divulgación responsable en `SECURITY.md`.
- Paso de ejecución de pruebas automatizadas en el flujo de CI de GitHub Actions.

---

## [2.0.0] — 2026-09-24

### Añadido — Base de Datos

- **`database/schema.sql` v2 — BCNF completo:**
  - Extraídas 4 tablas de dominio independiente para eliminar dependencias
    transitivas: `sizes`, `colors`, `districts`, `payment_methods`.
  - Tipos ENUM nativos de PG16: `user_role_enum`, `order_status_enum`.
  - Función `fn_set_updated_at()` y 5 triggers de actualización automática
    de `updated_at` en todas las entidades principales.
  - Trigger `fn_decrement_stock()` / `trg_decrement_stock_on_order`:
    descuenta stock automáticamente al insertar en `order_items` con
    validación de stock negativo.
  - Restricción declarativa `chk_total`: `total_amount = subtotal + shipping_cost`.
  - 14 índices de optimización incluyendo índice parcial de stock bajo.
  - Vista `vw_low_stock_alert`: variantes con stock ≤ umbral de alerta.
  - Vista `vw_orders_summary`: listado desnormalizado para dashboard.

- **`database/seeds.sql` v2 — Catálogo deportivo completo:**
  - 6 tallas (S, M, L, XL, XXL, UNICA).
  - 10 colores con códigos HEX (Negro Lavado, Blanco Crudo, Gris Jaspe…).
  - 10 distritos de Lima para reparto.
  - 5 métodos de pago (Yape, Plin, Transferencia, Contraentrega, Efectivo).
  - 8 productos deportivos y 23 variantes con SKU único.
  - 7 clientes y 6 pedidos con historial completo de estados.
  - Verificación automática al final con `RAISE NOTICE` de conteos.

- **`database/replication_setup.sql` v2 — Streaming Replication:**
  - Creación idempotente del role `replicator_leofit` con `REPLICATION LOGIN`.
  - Creación idempotente del slot físico `standby_slot_leofit_replica1`.
  - Documentación completa de parámetros `postgresql.conf`, `pg_hba.conf`,
    comando `pg_basebackup`, configuración del Standby y procedimiento de
    failover con `pg_promote()`.
  - Corrección: todos los bloques de documentación usan comentarios `--`
    (eliminados bloques `/* */` anidados que causaban error en psql).

- **`database/backup_strategy.sh` v2 — Respaldo con SHA-256:**
  - 6 comandos: `full`, `incremental`, `verify`, `restore`, `purge`, `status`.
  - Firma SHA-256 generada automáticamente para cada archivo de backup.
  - Verificación obligatoria de integridad antes de ejecutar `pg_restore`.
  - Confirmación explícita (`si`) requerida para restauraciones.
  - Alertas por correo ante fallos de conexión o corrupción detectada.
  - Política de retención configurable (default: 30 días).
  - Exportación separada del schema SQL legible con su propia firma SHA-256.

- **`database/pgbouncer/` — Connection Pooling Transaccional (nuevo):**
  - `pgbouncer.ini`: pool transaccional, 200 clientes / 25 conexiones reales,
    autenticación SCRAM-SHA-256, `max_prepared_statements=100` para PG16,
    pool de solo lectura apuntando al Standby (`leofit_db_ro`).
  - `userlist.txt`: plantilla de usuarios con hashes SCRAM-SHA-256.
  - `setup_pgbouncer.sh`: instalación completa — instala PgBouncer, crea
    roles en PostgreSQL con mínimos privilegios, genera `userlist.txt` real
    desde `pg_shadow`, levanta y verifica el servicio.

- **`docker-compose.yml` v2:**
  - Servicio `pgbouncer` usando imagen `edoburu/pgbouncer:latest`.
  - Backend configurado para conectar a través de PgBouncer (`:6432`).
  - Parámetros de replicación pasados via `command: postgres -c wal_level=replica ...`
    para garantizar que estén activos antes de los scripts de init.
  - `start_period: 30s` en healthcheck para dar tiempo a los scripts de init.
  - Eliminado `POSTGRES_INITDB_ARGS` con locale no disponible en Alpine.

- **`database/README.md` v2:**
  - ERD actualizado con las 12 tablas incluyendo las 4 tablas de dominio.
  - Diccionario de datos completo para todas las tablas.
  - Documentación de triggers, índices, vistas y datos de seeds.
  - Sección de quickstart con Docker.

- **`database/ADMINISTRATION_AND_REPLICATION.md` v2:**
  - Diagrama de arquitectura actualizado con PgBouncer.
  - Tabla de parámetros de replicación aplicados.
  - Documentación completa de PgBouncer: parámetros, consola de admin,
    instalación en bare-metal.
  - Tabla de políticas de backup con RPO/RTO.
  - Comandos de monitoreo proactivo del sistema.

### Corregido

- Error `unterminated /* comment` en `replication_setup.sql` al ejecutarse
  como script de init de Docker — eliminados comentarios de bloque anidados.
- Error `locale es_PE.UTF-8 not found` en imagen `postgres:16-alpine`
  (Alpine no tiene locales instalados) — eliminado `POSTGRES_INITDB_ARGS`.
- Imagen `bitnami/pgbouncer:1.22.1` inexistente en Docker Hub —
  reemplazada por `edoburu/pgbouncer:latest`.
- Contenedor `leofit_postgres` marcado como `unhealthy` por ausencia de
  `wal_level=replica` durante la inicialización — resuelto con `command`.

---

## [1.0.0-beta] — 2026-08-30

### Añadido
- Aplicación Web Progresiva (PWA) con módulo de autenticación por roles.
- Dashboard interactivo con indicadores clave de ventas y stock.
- Módulo de gestión de pedidos con filtrado por estado y canal.
- Catálogo de productos deportivos con alerta de stock crítico.
- Soporte offline y manifest PWA para instalación móvil.
- Documentación técnica completa en `/docs` (12 módulos).
- Pipeline CI/CD: despliegue a GitHub Pages y escaneo de seguridad.
- Schema inicial de base de datos con normalización hasta BCNF.