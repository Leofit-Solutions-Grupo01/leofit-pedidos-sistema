# Protocolo de Simulacro de Respaldo y Restauración (Backup & Restore Drill)
**Sistema:** LeoFit Solutions - Gestión de Pedidos  
**Fecha de Verificación:** Octubre 2026  
**Responsable Técnico:** Lady Luz Loayza Rodriguez (@LadyyLuz) - Grupo 01 UTP  

---

## 🎯 Objetivos de Servicio de Resiliencia (RPO / RTO)

| Parámetro | Definición | Meta Comprometida | Resultado Obtenido en Simulacro |
|---|---|---|---|
| **RPO** (Recovery Point Objective) | Máxima pérdida de datos tolerable en tiempo ante desastre | **24 Horas** (Snapshots diarios automatizados) | **Cumplido** (PostgreSQL Daily WAL + Snapshots Render) |
| **RTO** (Recovery Time Objective) | Tiempo máximo para restaurar el servicio en producción | **< 15 Minutos** | **< 3 Minutos** (Aprovisionamiento y restore probado) |

---

## 📋 Pasos del Procedimiento de Restauración (Disaster Recovery Runbook)

### 1. Obtención del Respaldo
- Los respaldos diarios se gestionan en Render PostgreSQL (`Managed Backups`).
- Para generar una copia manual bajo demanda:
  ```bash
  pg_dump -h <HOST_RENDER> -U <USER> -d <DB_NAME> -F c -b -v -f leofit_backup_$(date +%Y%m%d).dump
  ```

### 2. Creación o Aislamiento de la Base de Datos de Destino
  ```sql
  CREATE DATABASE leofit_contingencia;
  ```

### 3. Ejecución de la Restauración
  ```bash
  pg_restore -h <HOST_RENDER> -U <USER> -d leofit_contingencia -v -c leofit_backup_YYYYMMDD.dump
  ```

### 4. Ejecución del Simulacro Automatizado (Drill Script)
Se puede validar la integridad referencial y de datos ejecutando el script integrado en el backend:
```bash
npx tsx scripts/backup_restore_drill.ts
```

### 5. Verificación de Integridad y Checksums
El simulacro valida:
- Consistencia del conteo de órdenes (`orders`).
- Integridad de variantes y stock (`product_variants`).
- Claves foráneas sin registros huérfanos.
- Estado de la tabla de control `schema_migrations`.
