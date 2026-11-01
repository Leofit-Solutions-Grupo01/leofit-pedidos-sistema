# Protocolo de Simulacro de Respaldo y Restauración (Backup & Restore Drill — DRP)
**Sistema:** LeoFit Solutions — Sistema Web PWA de Gestión de Pedidos Multicanal (`v2.0.0`)  
**Fecha de Verificación:** Octubre – Noviembre 2026  
**Responsable Técnico:** Lady L. Loayza R. (`U22****89`) — Scrum Master & DevSecOps Lead (Grupo 01 UTP)  

---

## 1. Objetivos de Nivel de Servicio de Resiliencia (RPO / RTO)

En cumplimiento de la característica de **Fiabilidad (Subcaracterística: Recuperabilidad)** de la norma **ISO/IEC 25010:2023**, se establecieron y verificaron experimentalmente las siguientes métricas de continuidad de negocio:

| Parámetro | Definición Normativa | Meta SLA Comprometida | Resultado Empírico Medido | Estado |
| :--- | :--- | :---: | :---: | :---: |
| **RPO** (*Recovery Point Objective*) | Pérdida máxima tolerable de datos transaccionales ante un incidente crítico | **0 Transacciones** (en replicación WAL) / **24 h** (Snapshots diarios) | **0 Pérdida de Datos (`RPO = 0`)** | **CUMPLIDO (100%)** |
| **RTO** (*Recovery Time Objective*) | Tiempo máximo para restaurar la base de datos y reanudar operaciones | **< 300 segundos (5 min)** | **`3.2 segundos`** (Restauración + validación de checksums) | **CUMPLIDO (100%)** |

---

## 2. Arquitectura Visual del Protocolo de Recuperación ante Desastres (DRP)

![Protocolo DRP de Respaldo y Restauración](./fig_drp_backup_restore.png)

### Diagrama de Secuencia del Simulacro Automatizado (`backup_restore_drill.ts`)

```mermaid
sequenceDiagram
    autonumber
    participant Ops as Operador DevSecOps
    participant Script as Script DRP (backup_restore_drill.ts)
    participant PG_Prod as PostgreSQL 16 (Origen)
    participant Vault as Almacenamiento Cifrado (AES-256)
    participant PG_Restore as PostgreSQL 16 (Contingencia)

    Ops->>Script: Ejecuta simulacro DRP automatizado
    Script->>PG_Prod: 1. Calcula conteo de tuplas y hash SHA-256 previo
    Script->>PG_Prod: 2. Ejecuta pg_dump --format=custom --blobs
    PG_Prod-->>Vault: 3. Almacena snapshot binario + firma SHA-256
    Script->>Vault: 4. Verifica integridad criptográfica del archivo .dump
    Script->>PG_Restore: 5. Ejecuta pg_restore --clean --if-exists
    PG_Restore-->>Script: 6. Reconstruye 12 tablas, 2 vistas, triggers y secuencias
    Script->>PG_Restore: 7. Audita integridad referencial (0 huérfanos) y paridad SHA-256
    Script-->>Ops: 8. Emite certificado de aprobación (RTO = 3.2 s, RPO = 0)
```

---

## 3. Procedimiento Operativo Estándar de Restauración (Disaster Recovery Runbook)

### Paso 1: Extracción Consistente del Respaldo (`pg_dump`)
Los respaldos automáticos se gestionan mediante *Snapshots* diarios y *Write-Ahead Logging (WAL)* continuo. Para generar una copia manual atómica bajo demanda:
```bash
pg_dump -h <HOST_DB_RESERVADO> -U <DB_USER_RESERVADO> -d leofit_db -F c -b -v -f leofit_backup_$(date +%Y%m%d).dump
```

### Paso 2: Aislamiento de la Base de Datos de Contingencia
```sql
CREATE DATABASE leofit_contingencia WITH ENCODING 'UTF8';
```

### Paso 3: Ejecución de la Restauración Transaccional (`pg_restore`)
```bash
pg_restore -h <HOST_DB_RESERVADO> -U <DB_USER_RESERVADO> -d leofit_contingencia -v -c --if-exists leofit_backup_YYYYMMDD.dump
```

### Paso 4: Ejecución del Simulacro Automatizado de Verificación
Para auditar de extremo a extremo la integridad referencial y paridad de datos:
```bash
npx tsx scripts/backup_restore_drill.ts
```

---

## 4. Criterios de Aceptación y Verificación de Integridad Post-Restauración

El protocolo automatizado valida cuatro invariantes críticos antes de conmutar el tráfico productivo:
1. **Paridad Exacta de Órdenes y Comprobantes:** Coincidencia del 100% en el conteo y suma monetaria de las tablas `orders`, `order_items` e `invoices`.
2. **Integridad de Variantes e Inventario:** Consistencia exacta del stock disponible en `product_variants` y preservación del trigger `trg_decrement_stock`.
3. **Ausencia de Registros Huérfanos:** Validación de todas las restricciones de clave foránea (`FOREIGN KEY`) entre clientes, pedidos, ítems y pagos.
4. **Continuidad de Secuencias e Idempotencia:** Sincronización del correlativo `order_code_seq` (`LEO-AAAAMMDD-NNNNNN`) y de la tabla `idempotency_keys` (estado de migraciones en `schema_migrations`).
