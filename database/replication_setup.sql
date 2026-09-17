-- =============================================================================
-- POSTGRESQL STREAMING REPLICATION & HIGH AVAILABILITY CONFIGURATION
-- SISTEMA DE GESTIÓN DE PEDIDOS LEOFIT SOLUTIONS
-- =============================================================================

-- 1. Crear usuario dedicado para replicación física (Streaming Replication)
DO $$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'replicator_user') THEN
      CREATE ROLE replicator_user WITH REPLICATION LOGIN ENCRYPTED PASSWORD 'ReplicationSecretKey2026!';
   END IF;
END
$$;

-- 2. Creación de Slot de Replicación Físico (Evita pérdida de segmentos WAL en el Primary)
SELECT pg_create_physical_replication_slot('standby_slot_leofit_replica1') 
WHERE NOT EXISTS (
    SELECT 1 FROM pg_replication_slots WHERE slot_name = 'standby_slot_leofit_replica1'
);

-- 3. Parámetros recomendados para postgresql.conf (Primary Node):
/*
wal_level = replica
max_wal_senders = 10
max_replication_slots = 10
wal_keep_size = 1024MB
hot_standby = on
archive_mode = on
archive_command = 'test ! -f /var/lib/postgresql/wal_archive/%f && cp %p /var/lib/postgresql/wal_archive/%f'
*/

-- 4. Parámetros de pg_hba.conf para permitir acceso a la réplica Standby:
/*
host replication replicator_user 10.0.0.0/16 scram-sha-256
*/

-- 5. Comando de inicialización en el nodo réplica (Standby Node):
/*
pg_basebackup -h primary_db_host -D /var/lib/postgresql/data -U replicator_user -P -v -R --slot=standby_slot_leofit_replica1
*/
