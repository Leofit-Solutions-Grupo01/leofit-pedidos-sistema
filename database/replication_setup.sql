-- =============================================================================
-- POSTGRESQL 16 — STREAMING REPLICATION FÍSICA CON HIGH AVAILABILITY
-- SISTEMA DE GESTIÓN DE PEDIDOS LEOFIT SOLUTIONS
-- Slot: standby_slot_leofit_replica1
-- =============================================================================
-- VERSION : 2.0.0
-- MOTOR   : PostgreSQL 16+
-- =============================================================================
-- NOTA: Los bloques de configuración de archivos externos (.conf, shell)
--       están documentados con comentarios de línea (--) para evitar el
--       error de comentarios /* */ anidados en psql.
-- =============================================================================

-- =============================================================================
-- PASO 1: Crear usuario dedicado de replicación
-- =============================================================================
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_catalog.pg_roles WHERE rolname = 'replicator_leofit'
    ) THEN
        CREATE ROLE replicator_leofit
            WITH REPLICATION LOGIN
            ENCRYPTED PASSWORD 'Leofit_Repl_2026!SecurePass';
        RAISE NOTICE '✅ Role replicator_leofit creado exitosamente.';
    ELSE
        RAISE NOTICE 'ℹ️  Role replicator_leofit ya existe — omitido.';
    END IF;
END;
$$;

-- =============================================================================
-- PASO 2: Crear Replication Slot físico
--         Garantiza que el Primary conserve WAL hasta que el Standby
--         los consuma (evita pérdida de datos ante lag temporal).
-- =============================================================================
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_replication_slots
         WHERE slot_name = 'standby_slot_leofit_replica1'
    ) THEN
        PERFORM pg_create_physical_replication_slot('standby_slot_leofit_replica1');
        RAISE NOTICE '✅ Slot standby_slot_leofit_replica1 creado.';
    ELSE
        RAISE NOTICE 'ℹ️  Slot standby_slot_leofit_replica1 ya existe.';
    END IF;
END;
$$;

-- =============================================================================
-- PASO 3: Verificar estado del slot
-- =============================================================================
SELECT
    slot_name,
    slot_type,
    active         AS "activo",
    restart_lsn    AS "WAL_desde",
    wal_status     AS "estado_wal",
    safe_wal_size  AS "wal_safe_bytes"
FROM pg_replication_slots
WHERE slot_name = 'standby_slot_leofit_replica1';

-- =============================================================================
-- PASO 4: Configuración requerida en postgresql.conf del NODO PRIMARIO
--         (Ya aplicada vía docker-compose command: -c wal_level=replica ...)
--
-- wal_level             = replica
-- max_wal_senders       = 5
-- max_replication_slots = 5
-- wal_keep_size         = 512MB
-- hot_standby           = on
-- hot_standby_feedback  = on
-- wal_sender_timeout    = 60s
-- archive_mode          = on
-- archive_command       = 'cp %p /var/lib/postgresql/wal_archive/%f'
-- archive_timeout       = 300
-- =============================================================================

-- =============================================================================
-- PASO 5: Configuración requerida en pg_hba.conf del NODO PRIMARIO
--         (Ajustar la IP de red según entorno)
--
-- host  replication  replicator_leofit  10.0.0.0/24  scram-sha-256
-- host  leofit_db    all                10.0.0.0/24  scram-sha-256
-- =============================================================================

-- =============================================================================
-- PASO 6: Inicialización del NODO STANDBY (ejecutar en la máquina Standby)
--
-- systemctl stop postgresql@16-main
-- rm -rf /var/lib/postgresql/16/main/*
--
-- pg_basebackup \
--     -h 10.0.0.10 \
--     -D /var/lib/postgresql/16/main \
--     -U replicator_leofit \
--     -P -v -R \
--     --slot=standby_slot_leofit_replica1 \
--     --wal-method=stream
--
-- El flag -R genera automáticamente:
--   standby.signal    (marca este nodo como Standby en PG16)
--   primary_conninfo  (cadena de conexión al Primary)
--
-- systemctl start postgresql@16-main
-- =============================================================================

-- =============================================================================
-- PASO 7: Configuración postgresql.conf del NODO STANDBY
--
-- primary_conninfo      = 'host=10.0.0.10 port=5432 user=replicator_leofit
--                          password=Leofit_Repl_2026!SecurePass sslmode=require'
-- primary_slot_name     = 'standby_slot_leofit_replica1'
-- hot_standby           = on
-- hot_standby_feedback  = on
-- recovery_target_timeline = 'latest'
-- =============================================================================

-- =============================================================================
-- PASO 8: Monitoreo de la replicación (ejecutar en el PRIMARY)
-- =============================================================================

-- Estado de senders activos
SELECT
    application_name,
    client_addr,
    state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn,
    write_lag,
    flush_lag,
    replay_lag,
    sync_state
FROM pg_stat_replication;

-- Lag de replicación en bytes
SELECT
    slot_name,
    pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn) AS lag_bytes,
    active
FROM pg_replication_slots
WHERE slot_name = 'standby_slot_leofit_replica1';

-- En el STANDBY verificar que la réplica está activa:
-- SELECT pg_is_in_recovery();   -- debe retornar TRUE

-- =============================================================================
-- PASO 9: Failover manual (en caso de caída del Primary)
--
-- En el servidor STANDBY:
--   pg_ctl promote -D /var/lib/postgresql/16/main
--   O via SQL (PG16+): SELECT pg_promote();
--
-- Después del failover actualizar la cadena de conexión de PgBouncer
-- y del backend para apuntar al nuevo Primary.
-- =============================================================================

-- Fin del script de replicación